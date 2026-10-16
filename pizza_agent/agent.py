"""Core Pizza Dough Artisan Agent.

Coordinates recipe retrieval, yeast kinetics calculations, Desired Dough
Temperature calibration, proofing milestones, and natural language requests.
"""

from datetime import datetime, timedelta
import re
from typing import Optional, Dict, Any, Tuple
from .models import Recipe, DoughPlan, IngredientBreakdown, PAN_SIZES
from .database import Database
from .yeast_engine import (
    calculate_yeast_percentage,
    calculate_ingredients_breakdown,
    calculate_desired_dough_water_temp,
    format_tsp_fraction,
)
from .proofing import generate_proofing_schedule


class PizzaDoughAgent:
    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()

    def parse_time_target(
        self,
        ready_time_str: Optional[str] = None,
        duration_hours: Optional[float] = None,
        mix_time: Optional[datetime] = None,
    ) -> Tuple[datetime, datetime, float]:
        """Resolves mix_time, ready_time, and total_hours from strings or numbers."""
        now = mix_time or datetime.now().replace(second=0, microsecond=0)

        if duration_hours is not None and duration_hours > 0:
            total_hours = float(duration_hours)
            ready_time = now + timedelta(hours=total_hours)
            return now, ready_time, total_hours

        if not ready_time_str:
            # Default to 24 hours cold ferment
            total_hours = 24.0
            ready_time = now + timedelta(hours=24)
            return now, ready_time, total_hours

        s = ready_time_str.strip().lower()

        # Match phrases like "+24h", "24h", "48 hours", "in 6 hours"
        hour_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:h|hr|hrs|hour|hours)", s)
        if hour_match:
            total_hours = float(hour_match.group(1))
            ready_time = now + timedelta(hours=total_hours)
            return now, ready_time, total_hours

        # Match "tonight at 6pm", "tonight 7:00 pm", "tonight"
        time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", s)
        target_hour = 18  # default 6pm
        target_minute = 0
        is_pm = True

        if time_match:
            hr = int(time_match.group(1))
            target_minute = int(time_match.group(2)) if time_match.group(2) else 0
            meridiem = time_match.group(3)
            if meridiem:
                is_pm = (meridiem == "pm")
                if is_pm and hr < 12:
                    target_hour = hr + 12
                elif not is_pm and hr == 12:
                    target_hour = 0
                else:
                    target_hour = hr
            else:
                # If no am/pm given, assume PM if hr between 1 and 11
                target_hour = hr + 12 if hr < 12 else hr

        if "tomorrow" in s:
            target_date = (now + timedelta(days=1)).date()
            ready_time = datetime.combine(target_date, datetime.min.time()).replace(
                hour=target_hour, minute=target_minute
            )
        elif "tonight" in s or "today" in s:
            target_date = now.date()
            ready_time = datetime.combine(target_date, datetime.min.time()).replace(
                hour=target_hour, minute=target_minute
            )
            # If target time is earlier today, assume next day
            if ready_time <= now:
                ready_time += timedelta(days=1)
        elif any(day in s for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
            # Find next target day of week
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            target_day_idx = next(i for i, day in enumerate(days) if day in s)
            current_day_idx = now.weekday()
            days_ahead = (target_day_idx - current_day_idx) % 7
            if days_ahead == 0 and (target_hour < now.hour or (target_hour == now.hour and target_minute <= now.minute)):
                days_ahead = 7
            target_date = (now + timedelta(days=days_ahead)).date()
            ready_time = datetime.combine(target_date, datetime.min.time()).replace(
                hour=target_hour, minute=target_minute
            )
        else:
            # Try ISO parse
            try:
                ready_time = datetime.fromisoformat(ready_time_str)
            except Exception:
                # Fallback to tomorrow 6pm
                target_date = (now + timedelta(days=1)).date()
                ready_time = datetime.combine(target_date, datetime.min.time()).replace(hour=18, minute=0)

        total_hours = max(1.0, (ready_time - now).total_seconds() / 3600.0)
        return now, ready_time, total_hours

    def create_plan(
        self,
        recipe_id_or_name: str = "ny_style",
        balls: Optional[int] = None,
        ball_weight_g: Optional[float] = None,
        pan_size: Optional[str] = None,
        ready_time_str: Optional[str] = None,
        duration_hours: Optional[float] = None,
        mix_time: Optional[datetime] = None,
        ferment_type: Optional[str] = None,   # 'CF', 'RT', 'AUTO'
        yeast_type: str = "IDY",              # 'IDY', 'ADY', 'CY', 'SOURDOUGH'
        room_temp_f: float = 70.0,
        fridge_temp_f: float = 38.0,
        custom_rt_hours: Optional[float] = None,
        custom_cf_hours: Optional[float] = None,
        knead_type: str = "hand",
    ) -> DoughPlan:
        """Calculates a complete custom dough plan with scaled yeast and step-by-step schedule."""
        # 0. Handle Pan Sizing (13x9, 14x10, 8x10)
        resolved_recipe_id = recipe_id_or_name
        if pan_size:
            pan_clean = pan_size.lower().replace(" ", "").replace("*", "x").replace("by", "x")
            if pan_clean in PAN_SIZES:
                pan_info = PAN_SIZES[pan_clean]
                if ball_weight_g is None:
                    ball_weight_g = pan_info["dough_weight_g"]
                if balls is None:
                    balls = 1
                if resolved_recipe_id == "ny_style":
                    resolved_recipe_id = "adams_detroit"

        # 1. Resolve Recipe
        recipe = self.db.get_recipe(resolved_recipe_id)
        if not recipe:
            # Fallback
            recipe = self.db.get_recipe("adams_detroit") or self.db.get_recipe("ny_style")
            if not recipe:
                recipe = Recipe(
                    id="custom",
                    name="Default Pizza Dough",
                    description="Standard home pizza dough",
                    flour_type="Bread Flour",
                    hydration_pct=65.0,
                    salt_pct=2.4,
                    oil_pct=2.0,
                    sugar_pct=1.0,
                    default_ball_weight=260.0,
                    default_balls=4,
                )

        # 2. Scale Dough Balls
        target_balls = balls if balls and balls > 0 else recipe.default_balls
        target_ball_weight = ball_weight_g if ball_weight_g and ball_weight_g > 0 else recipe.default_ball_weight

        # Default Detroit pan pizza to 48-hour cold ferment if unspecified
        if recipe.id == "adams_detroit" and duration_hours is None and not ready_time_str:
            duration_hours = 48.0

        # 3. Resolve Timings
        mix_dt, ready_dt, total_hours = self.parse_time_target(
            ready_time_str=ready_time_str,
            duration_hours=duration_hours,
            mix_time=mix_time,
        )

        # 4. Resolve Fermentation Mode
        if ferment_type is None or ferment_type.upper() == "AUTO":
            if total_hours > 12.0:
                resolved_ferment = "CF"
            else:
                resolved_ferment = "RT"
        else:
            resolved_ferment = ferment_type.upper()

        # 5. Scientific Yeast Kinetics Calculation
        yeast_pct, equiv_rt_hours, rt_hours, cf_hours = calculate_yeast_percentage(
            total_hours=total_hours,
            ferment_type=resolved_ferment,
            room_temp_f=room_temp_f,
            fridge_temp_f=fridge_temp_f,
            yeast_type=yeast_type,
            custom_rt_hours=custom_rt_hours,
            custom_cf_hours=custom_cf_hours,
        )

        # 6. Desired Dough Temperature (DDT) Water Calculation
        water_temp_f, water_temp_desc = calculate_desired_dough_water_temp(
            desired_dough_temp_f=76.0,
            room_temp_f=room_temp_f,
            flour_temp_f=room_temp_f,
            knead_type=knead_type,
        )

        # 7. Baker's Percentages & Gram Breakdown
        ingredients = calculate_ingredients_breakdown(
            recipe=recipe,
            balls=target_balls,
            ball_weight_g=target_ball_weight,
            yeast_pct=yeast_pct,
            yeast_type=yeast_type,
            water_temp_f=water_temp_f,
        )

        # 8. Proofing Milestone Roadmap
        schedule = generate_proofing_schedule(
            recipe=recipe,
            ingredients=ingredients,
            mix_time=mix_dt,
            ready_time=ready_dt,
            ferment_type=resolved_ferment,
            rt_hours=rt_hours,
            cf_hours=cf_hours,
            room_temp_f=room_temp_f,
            fridge_temp_f=fridge_temp_f,
            water_temp_f=water_temp_f,
            water_temp_desc=water_temp_desc,
            yeast_type=yeast_type,
        )

        # 9. Summary Text
        summary = (
            f"Plan for {target_balls}x {target_ball_weight}g pizzas ({recipe.name}). "
            f"Fermentation window: {round(total_hours, 1)}h total "
            f"({resolved_ferment} profile: {round(rt_hours, 1)}h room temp, {round(cf_hours, 1)}h cold retard). "
            f"Calculated yeast: {ingredients.yeast_g}g ({ingredients.yeast_pct}% {yeast_type}, ~{format_tsp_fraction(ingredients.yeast_tsp)})."
        )

        plan = DoughPlan(
            recipe=recipe,
            ingredients=ingredients,
            yeast_type=yeast_type,
            mix_time_iso=mix_dt.isoformat(),
            ready_time_iso=ready_dt.isoformat(),
            total_hours=total_hours,
            ferment_type=resolved_ferment,
            room_temp_f=room_temp_f,
            fridge_temp_f=fridge_temp_f,
            rt_hours=rt_hours,
            cf_hours=cf_hours,
            schedule=schedule,
            desired_dough_temp_f=76.0,
            water_temp_recommendation=water_temp_desc,
            summary_text=summary,
        )

        # Log to database
        self.db.log_plan(plan.to_dict())

        return plan

    def parse_natural_language_request(self, text: str) -> DoughPlan:
        """Parses conversational user prompt and creates plan."""
        s = text.lower()

        # Detect pan size (13x9, 14x10, 8x10)
        pan_size = None
        if re.search(r"13\s*(?:x|by|\*)\s*9", s):
            pan_size = "13x9"
        elif re.search(r"14\s*(?:x|by|\*)\s*10", s):
            pan_size = "14x10"
        elif re.search(r"8\s*(?:x|by|\*)\s*10", s):
            pan_size = "8x10"

        # Detect recipe
        recipes = self.db.list_recipes()
        selected_recipe_id = "ny_style"
        if pan_size or "detroit" in s or "frico" in s or "in the pan" in s or "pan pizza" in s:
            selected_recipe_id = "adams_detroit"
        elif "neapolitan" in s or "napoli" in s:
            selected_recipe_id = "neapolitan"
        elif "outdoor" in s or "ooni" in s or "roccbox" in s:
            selected_recipe_id = "adams_outdoor_base"
        elif "quick" in s or "express" in s or "fast" in s or "today" in s or "tonight" in s:
            if "hours" in s and any(h in s for h in ["2 hour", "3 hour", "4 hour", "5 hour"]):
                selected_recipe_id = "same_day_quick"
        elif "sourdough" in s or "levain" in s or "starter" in s:
            selected_recipe_id = "sourdough_artisan"
        elif "pinsa" in s or "taglio" in s or "roman" in s:
            selected_recipe_id = "roman_pinsa"
        else:
            for r in recipes:
                if r.id in s or r.name.lower() in s:
                    selected_recipe_id = r.id
                    break

        # Detect dough ball / pan count (ignoring pan dimensions like 13x9 or 14x10)
        s_clean = re.sub(r"\b\d+\s*(?:x|by|\*)\s*\d+\b", "", s)
        balls = None
        ball_match = re.search(r"(\d+)\s+(?:[\w-]+\s+){0,3}(?:dough\s+)?(?:balls?|pizzas?|pies?|portions?|pans?)", s_clean)
        if ball_match:
            balls = int(ball_match.group(1))
        elif pan_size or selected_recipe_id == "adams_detroit":
            balls = 1

        # Detect ball weight or pan weight
        ball_weight = None
        if pan_size and pan_size in PAN_SIZES:
            ball_weight = PAN_SIZES[pan_size]["dough_weight_g"]
        else:
            weight_match = re.search(r"(\d+)\s*(?:g|grams?|gram)\b", s)
            if weight_match:
                val = float(weight_match.group(1))
                if 150 <= val <= 900:
                    ball_weight = val

        # Detect yeast type
        yeast_type = "IDY"
        if "active dry" in s or "ady" in s:
            yeast_type = "ADY"
        elif "fresh" in s or "cake" in s or "cy" in s:
            yeast_type = "CY"
        elif "sourdough" in s or "levain" in s:
            yeast_type = "SOURDOUGH"

        # Detect time phrase
        # E.g. "tomorrow at 6pm", "in 5 hours", "friday 7pm", "tonight", "2 day", "3 day"
        time_phrase = None
        if "3 day" in s or "3-day" in s or "72 hour" in s or "72h" in s:
            time_phrase = "72 hours"
        elif "2 day" in s or "2-day" in s or "48 hour" in s or "48h" in s:
            time_phrase = "48 hours"
        elif "tomorrow" in s:
            time_phrase = "tomorrow"
            tm = re.search(r"tomorrow\s*(?:at\s*)?(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)?", s)
            if tm and tm.group(1):
                time_phrase = f"tomorrow at {tm.group(1)}"
        elif "tonight" in s:
            time_phrase = "tonight"
            tm = re.search(r"tonight\s*(?:at\s*)?(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)?", s)
            if tm and tm.group(1):
                time_phrase = f"tonight at {tm.group(1)}"
        elif "in " in s:
            im = re.search(r"in\s+(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|h)\b", s)
            if im:
                time_phrase = f"{im.group(1)} hours"

        return self.create_plan(
            recipe_id_or_name=selected_recipe_id,
            balls=balls,
            ball_weight_g=ball_weight,
            pan_size=pan_size,
            ready_time_str=time_phrase,
            yeast_type=yeast_type,
        )
