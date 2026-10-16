"""Scientific yeast fermentation kinetics and baker's percentage engine.

Based on Craig's Fermentation Prediction Curve (pizzamaking.com standard)
and Arrhenius / Q10 metabolic rate scaling for cold retard vs room temperature.
"""

import math
from typing import Tuple, Dict, Any
from .models import Recipe, IngredientBreakdown

# Standard conversions
GRAMS_PER_TSP_IDY = 3.15
GRAMS_PER_TSP_ADY = 2.85
GRAMS_PER_TSP_CY = 3.80

# Yeast type multipliers relative to Instant Dry Yeast (IDY = 1.0)
YEAST_TYPE_RATIOS = {
    "IDY": 1.0,         # Instant Dry Yeast
    "ADY": 1.33,        # Active Dry Yeast
    "CY": 3.0,          # Cake / Fresh Yeast
    "SOURDOUGH": 20.0,  # Levain starter inoculant (typically ~10-20% of flour)
}


def calculate_temperature_rate_multiplier(temp_f: float, baseline_f: float = 68.0) -> float:
    """Calculates biological metabolic reaction rate multiplier relative to 68°F (20°C).
    
    Uses Q10 biological temperature coefficient ~2.15 per 10°C (18°F), with cellular
    membrane dormancy attenuation in cold refrigeration below 50°F (10°C).
    At 68°F -> 1.0
    At 77°F -> ~1.46 (faster fermentation)
    At 50°F -> ~0.46
    At 38°F (fridge) -> ~0.12 (approx 8x slower than room temp)
    At 34°F -> ~0.05
    """
    if temp_f < 33.0:
        return 0.03
    if temp_f > 115.0:
        return 0.0

    if temp_f < 50.0:
        # Cold dormancy attenuation below 10°C
        base_50 = math.pow(2.15, (50.0 - baseline_f) / 18.0)  # ~0.465
        cold_ratio = max(0.05, (temp_f - 32.0) / 18.0)
        dormancy_multiplier = math.pow(cold_ratio, 1.2)
        return max(0.04, round(base_50 * dormancy_multiplier, 4))

    delta_f = temp_f - baseline_f
    exponent = delta_f / 18.0
    multiplier = math.pow(2.15, exponent)
    return max(0.05, min(round(multiplier, 4), 3.5))


def calculate_equivalent_rt_hours(
    total_hours: float,
    rt_hours: float,
    cf_hours: float,
    room_temp_f: float = 70.0,
    fridge_temp_f: float = 38.0
) -> float:
    """Computes total Equivalent Fermentation Hours at baseline 68°F (20°C).
    
    Converts cold refrigeration time into equivalent room temp metabolic hours.
    """
    rt_multiplier = calculate_temperature_rate_multiplier(room_temp_f, baseline_f=68.0)
    cf_multiplier = calculate_temperature_rate_multiplier(fridge_temp_f, baseline_f=68.0)

    # Ensure hours sum up
    if rt_hours + cf_hours < 0.01:
        rt_hours = total_hours
        cf_hours = 0.0

    equiv_hours = (rt_hours * rt_multiplier) + (cf_hours * cf_multiplier)
    return max(0.5, equiv_hours)


def calculate_yeast_percentage(
    total_hours: float,
    ferment_type: str = "CF",       # 'CF' (Cold Ferment), 'RT' (Room Temp), 'AUTO'
    room_temp_f: float = 70.0,
    fridge_temp_f: float = 38.0,
    yeast_type: str = "IDY",
    custom_rt_hours: float = None,
    custom_cf_hours: float = None,
) -> Tuple[float, float, float, float]:
    """Calculates optimal yeast percentage based on Craig's Fermentation Prediction Curve.
    
    Returns:
        (yeast_pct, equiv_rt_hours, actual_rt_hours, actual_cf_hours)
    """
    # Auto-determine split if not specified
    if custom_rt_hours is not None and custom_cf_hours is not None:
        rt_hours = custom_rt_hours
        cf_hours = custom_cf_hours
    elif ferment_type == "RT" or total_hours <= 12.0:
        # All room temperature
        rt_hours = total_hours
        cf_hours = 0.0
    else:
        # Cold ferment workflow:
        # 1.5h - 2h initial bulk + (3h - 4h) warm-up ball proof before bake
        # Rest is in refrigerator
        rt_hours = min(6.0, max(2.5, total_hours * 0.15))
        if total_hours > 24:
            rt_hours = 4.5  # standard 1.5h bulk + 3.0h ball warm up
        cf_hours = max(0.0, total_hours - rt_hours)

    equiv_rt_hours = calculate_equivalent_rt_hours(
        total_hours, rt_hours, cf_hours, room_temp_f, fridge_temp_f
    )

    # Craig's model regression formula for IDY at 68°F:
    # Y_IDY % = 2.42 * (equiv_hours)^(-1.35)
    # Clamped to safe artisan ranges:
    # e.g., 2h -> ~0.95%, 4h -> ~0.37%, 8h -> ~0.15%, 24h RT -> ~0.033%
    # For cold ferments with equiv ~8-12h -> ~0.08% - 0.14% IDY
    if yeast_type == "SOURDOUGH":
        # Sourdough starter scaling: typically 8% to 20% of flour weight
        # Inverse logarithmic relationship with equivalent hours
        sourdough_pct = 25.0 * math.pow(equiv_rt_hours, -0.45)
        yeast_pct = max(4.0, min(sourdough_pct, 25.0))
    else:
        base_idy_pct = 2.42 * math.pow(equiv_rt_hours, -1.35)
        # Apply bounds: min 0.015% (for ultra long cold ferment), max 1.5% (for extreme 1h rush)
        clamped_idy = max(0.015, min(base_idy_pct, 1.4))

        # Convert to requested yeast type
        ratio = YEAST_TYPE_RATIOS.get(yeast_type.upper(), 1.0)
        yeast_pct = clamped_idy * ratio

    return round(yeast_pct, 4), round(equiv_rt_hours, 2), round(rt_hours, 2), round(cf_hours, 2)


def calculate_desired_dough_water_temp(
    desired_dough_temp_f: float = 76.0,
    room_temp_f: float = 70.0,
    flour_temp_f: float = 70.0,
    knead_type: str = "hand",  # 'hand', 'stand_mixer', 'spiral'
) -> Tuple[float, str]:
    """Calculates water temperature needed using the Desired Dough Temperature (DDT) rule:
    Water Temp = (3 * DDT) - Room Temp - Flour Temp - Friction Factor
    """
    friction_factors = {
        "hand": 1.0,
        "stand_mixer": 6.0,
        "spiral": 9.0,
    }
    friction = friction_factors.get(knead_type, 2.0)
    water_temp = (3.0 * desired_dough_temp_f) - room_temp_f - flour_temp_f - friction

    # Guardrails
    water_temp = max(38.0, min(water_temp, 110.0))

    if water_temp < 50.0:
        desc = f"Very cold tap or iced water (~{round(water_temp)}°F) to prevent dough overheating."
    elif water_temp < 68.0:
        desc = f"Cool tap water (~{round(water_temp)}°F)."
    elif water_temp <= 82.0:
        desc = f"Room-temperature / cellar water (~{round(water_temp)}°F)."
    else:
        desc = f"Warm / tepid water (~{round(water_temp)}°F) to wake up yeast."

    return round(water_temp, 1), desc


def format_tsp_fraction(tsp: float) -> str:
    """Formats decimal teaspoons into kitchen friendly fractions (e.g. 1/4 tsp, 1/2 tsp)."""
    if tsp < 0.08:
        return "< 1/8 tsp (a tiny pinch)"
    elif tsp <= 0.18:
        return "1/8 tsp"
    elif tsp <= 0.35:
        return "1/4 tsp"
    elif tsp <= 0.60:
        return "1/2 tsp"
    elif tsp <= 0.85:
        return "3/4 tsp"
    elif tsp <= 1.15:
        return "1 tsp"
    elif tsp <= 1.4:
        return "1 1/4 tsp"
    elif tsp <= 1.65:
        return "1 1/2 tsp"
    elif tsp <= 1.9:
        return "1 3/4 tsp"
    elif tsp <= 2.2:
        return "2 tsp"
    else:
        whole = int(tsp)
        rem = tsp - whole
        if rem > 0.6:
            return f"{whole + 1} tsp"
        elif rem > 0.3:
            return f"{whole} 1/2 tsp"
        return f"{whole} tsp"


def calculate_ingredients_breakdown(
    recipe: Recipe,
    balls: int,
    ball_weight_g: float,
    yeast_pct: float,
    yeast_type: str = "IDY",
    water_temp_f: float = 75.0,
) -> IngredientBreakdown:
    """Calculates exact gram weights using Baker's Percentages.
    
    Total Dough Weight = Flour + Water + Salt + Yeast + Oil + Sugar
    Total Pct = 100% + Hydration% + Salt% + Yeast% + Oil% + Sugar%
    Flour = Total Weight / (Total Pct / 100)
    """
    total_dough_g = float(balls * ball_weight_g)

    # Baker's percentages as decimals
    hydration_dec = recipe.hydration_pct / 100.0
    salt_dec = recipe.salt_pct / 100.0
    oil_dec = recipe.oil_pct / 100.0
    sugar_dec = recipe.sugar_pct / 100.0
    yeast_dec = yeast_pct / 100.0

    total_pct_dec = 1.0 + hydration_dec + salt_dec + oil_dec + sugar_dec + yeast_dec

    flour_g = total_dough_g / total_pct_dec
    water_g = flour_g * hydration_dec
    salt_g = flour_g * salt_dec
    yeast_g = flour_g * yeast_dec
    oil_g = flour_g * oil_dec
    sugar_g = flour_g * sugar_dec

    # Teaspoon equivalent for yeast
    if yeast_type == "ADY":
        tsp = yeast_g / GRAMS_PER_TSP_ADY
    elif yeast_type == "CY":
        tsp = yeast_g / GRAMS_PER_TSP_CY
    else:
        tsp = yeast_g / GRAMS_PER_TSP_IDY

    return IngredientBreakdown(
        flour_g=round(flour_g, 1),
        water_g=round(water_g, 1),
        salt_g=round(salt_g, 1),
        yeast_g=round(yeast_g, 2),
        yeast_tsp=round(tsp, 2),
        yeast_pct=round(yeast_pct, 4),
        oil_g=round(oil_g, 1),
        sugar_g=round(sugar_g, 1),
        total_weight_g=round(total_dough_g, 1),
        balls=balls,
        ball_weight_g=round(ball_weight_g, 1),
        water_temp_f=water_temp_f,
        yeast_type=yeast_type,
    )
