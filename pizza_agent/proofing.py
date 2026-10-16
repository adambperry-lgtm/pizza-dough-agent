"""Proofing schedule generator and step-by-step master pizzaiolo instructions."""

from datetime import datetime, timedelta
from typing import List
from .models import Recipe, IngredientBreakdown, ProofingMilestone, DoughPlan
from .yeast_engine import format_tsp_fraction


def generate_proofing_schedule(
    recipe: Recipe,
    ingredients: IngredientBreakdown,
    mix_time: datetime,
    ready_time: datetime,
    ferment_type: str,
    rt_hours: float,
    cf_hours: float,
    room_temp_f: float,
    fridge_temp_f: float,
    water_temp_f: float,
    water_temp_desc: str,
    yeast_type: str = "IDY",
) -> List[ProofingMilestone]:
    """Generates a complete chronologically timestamped proofing roadmap with exact times."""
    milestones: List[ProofingMilestone] = []
    step = 1
    is_pan_style = ("detroit" in recipe.id.lower() or "detroit" in recipe.name.lower() or "pan" in recipe.name.lower())

    # Format helper
    def dt_str(dt: datetime) -> str:
        return dt.strftime("%A, %b %-d at %-I:%M %p")

    # Step 1: Mise en Place & Water Prep
    t_start = mix_time
    pan_setup_note = (
        f"\n3. Prepare your Detroit pizza pan(s) (13x9, 14x10, or 8x10 LloydPan or dark blue steel). "
        f"Pour 1-2 tbsp (15-25g) extra virgin olive oil into the pan and rub over the entire bottom, sides, and corners."
        if is_pan_style else ""
    )
    milestones.append(ProofingMilestone(
        step_num=step,
        title="Mise en Place & Water Temperature Calibration" if not is_pan_style else "Mise en Place, Water Prep & Detroit Pan Setup",
        action_category="mix",
        timestamp_iso=t_start.isoformat(),
        display_time=dt_str(t_start),
        duration_str="10-15 mins",
        temp_desc=f"Target Water: {water_temp_f}°F ({water_temp_desc})",
        instruction=(
            f"1. Weigh out {ingredients.flour_g}g flour ({recipe.flour_type}), "
            f"{ingredients.water_g}g water, {ingredients.salt_g}g fine sea salt, "
            f"and {ingredients.yeast_g}g {yeast_type} "
            f"({format_tsp_fraction(ingredients.yeast_tsp)})."
            + (f" Also weigh {ingredients.oil_g}g extra virgin olive oil." if ingredients.oil_g > 0 else "")
            + (f" Also weigh {ingredients.sugar_g}g sugar/malt." if ingredients.sugar_g > 0 else "")
            + f"\n2. Calibrate water to {water_temp_f}°F using the Desired Dough Temperature formula. "
            + ("If using Active Dry Yeast (ADY), bloom in 50g of warm water for 7 minutes first." if yeast_type == "ADY" else "If using Instant Dry Yeast (IDY), whisk directly into flour or dissolve in the water.")
            + pan_setup_note
        ),
        visual_cue="Ingredients accurately weighed on a gram scale; yeast completely dissolved or dispersed." + (" Pan thoroughly coated in olive oil." if is_pan_style else ""),
        pro_tip="Always use a gram scale. Volumetric cup measurements introduce up to 25% error in flour density!"
    ))
    step += 1

    # Step 2: Autolyse / Rest & Knead
    t_autolyse = t_start + timedelta(minutes=15)
    t_knead_end = t_autolyse + timedelta(minutes=20)
    milestones.append(ProofingMilestone(
        step_num=step,
        title="Autolyse Rest & Gluten Development (Kneading)",
        action_category="knead",
        timestamp_iso=t_autolyse.isoformat(),
        display_time=dt_str(t_autolyse),
        duration_str="20 mins",
        temp_desc=f"Room Temp ~{room_temp_f}°F",
        instruction=(
            "1. Combine flour and water into a rough, shaggy mass. Let rest covered for 15-20 minutes (Autolyse). "
            "This lets the flour fully hydrate before gluten formation.\n"
            f"2. Add {ingredients.salt_g}g salt"
            + (f", {ingredients.sugar_g}g sugar" if ingredients.sugar_g > 0 else "")
            + (f", and {ingredients.oil_g}g olive oil towards the end of mixing." if ingredients.oil_g > 0 else ".")
            + "\n3. Knead for 6-8 minutes by hand (or 4-5 mins in stand mixer on low speed) until smooth and elastic."
        ),
        visual_cue="The dough transitions from shaggy and sticky to smooth, supple, and satiny. Passes the 'windowpane test' (stretches thin enough to see light through without tearing).",
        pro_tip="Adding oil at the very end of kneading allows gluten bonds to form first, preventing fat from coating flour proteins prematurely."
    ))
    step += 1

    # Available time between end of kneading and ready_time
    t_knead_done = t_knead_end  # t_start + 35 min
    avail_seconds = max(1800.0, (ready_time - t_knead_done).total_seconds())
    avail_hours = avail_seconds / 3600.0

    if cf_hours > 0 and avail_hours >= 6.0:
        # COLD FERMENTATION SCHEDULE
        # 1. Bulk ferment at room temp
        bulk_hours = min(2.0, max(0.75, rt_hours * 0.35))
        t_bulk_start = t_knead_done
        t_bulk_end = t_bulk_start + timedelta(hours=bulk_hours)

        milestones.append(ProofingMilestone(
            step_num=step,
            title="Bulk Fermentation (Initial Rise)",
            action_category="bulk",
            timestamp_iso=t_bulk_start.isoformat(),
            display_time=dt_str(t_bulk_start),
            duration_str=f"{round(bulk_hours, 1)} hours",
            temp_desc=f"Room Temp ~{room_temp_f}°F (Covered)",
            instruction=(
                f"1. Form dough into a tidy ball and place in a lightly oiled bowl or container.\n"
                f"2. Cover tightly with plastic wrap or a fitted lid to prevent the skin from drying out.\n"
                f"3. Allow to bulk ferment at room temperature (~{room_temp_f}°F) for {round(bulk_hours, 1)} hours."
                + (" Optional: perform 1 gentle stretch-and-fold at the 45-minute mark to build dough strength." if recipe.hydration_pct >= 67 else "")
            ),
            visual_cue=(
                "Dough expands by ~25-35% in volume. "
                "Surface looks domed, lively, and soft to the touch with small internal fermentation bubbles."
            ),
            pro_tip="Don't wait for dough to double during bulk if cold fermenting! Cold ferment requires residual yeast energy to work in the fridge."
        ))
        step += 1

        # 2. Divide and Ball / Pan Placement
        t_ball = t_bulk_end
        t_ball_done = t_ball + timedelta(minutes=15)
        if is_pan_style:
            milestones.append(ProofingMilestone(
                step_num=step,
                title=f"Portion Directly into {ingredients.balls} Oiled Detroit Pan{'s' if ingredients.balls > 1 else ''} ({ingredients.ball_weight_g}g each)",
                action_category="ball",
                timestamp_iso=t_ball.isoformat(),
                display_time=dt_str(t_ball),
                duration_str="15 mins",
                temp_desc="Room Temp Pan Setup",
                instruction=(
                    f"1. Cut dough into {ingredients.balls} portion{'s' if ingredients.balls > 1 else ''} ({ingredients.ball_weight_g}g each) using a bench scraper.\n"
                    "2. Place each portion directly into the center of a well-oiled Detroit pizza pan (13x9, 14x10, or 8x10).\n"
                    "3. Turn dough once so both top and bottom are lightly coated with olive oil.\n"
                    "4. Using flat, oiled fingertips, gently press and dimple the dough outward towards the edges and corners. "
                    "(It will resist and shrink back toward the center—do NOT force it! Gluten relaxes naturally during the cold ferment)."
                ),
                visual_cue="Dough rests in an oiled oval/rectangle in the pan, lightly coated in oil with gentle dimpling.",
                pro_tip="Never force cold or unrelaxed dough to fill the corners. Gentle dimpling and time do all the work!"
            ))
        else:
            milestones.append(ProofingMilestone(
                step_num=step,
                title=f"Divide & Shape into {ingredients.balls} Dough Balls ({ingredients.ball_weight_g}g each)",
                action_category="ball",
                timestamp_iso=t_ball.isoformat(),
                display_time=dt_str(t_ball),
                duration_str="15 mins",
                temp_desc="Room Temp Bench",
                instruction=(
                    f"1. Turn dough onto clean, un-floured or lightly oiled counter.\n"
                    f"2. Cut into {ingredients.balls} equal pieces using a bench scraper, each weighing exactly {ingredients.ball_weight_g}g.\n"
                    "3. Cup your hand over each portion and drag in a circular motion against the counter to create taut surface tension. "
                    "Pinch the bottom seam shut tightly.\n"
                    "4. Place into lightly oiled individual proofing containers (round plastic deli tubs or a proofing box), spaced 2-3 inches apart."
                ),
                visual_cue="Smooth, tight, spherical dough balls with zero surface tears and a sealed bottom belly.",
                pro_tip="Surface tension during balling is what traps carbon dioxide and gives you high, puffy cornicione crust borders!"
            ))
        step += 1

        # 3. Cold Retardation & Tempering
        temper_hours = min(4.0, max(2.5, rt_hours * 0.70)) if is_pan_style else min(3.5, max(1.5, rt_hours * 0.65))
        t_temper_start = ready_time - timedelta(hours=temper_hours)
        if t_temper_start < t_ball_done + timedelta(hours=1.0):
            t_temper_start = t_ball_done + timedelta(hours=max(0.5, (avail_hours - bulk_hours - 0.25) * 0.5))
            temper_hours = (ready_time - t_temper_start).total_seconds() / 3600.0

        t_cf_start = t_ball_done
        actual_cf_hours = max(0.5, (t_temper_start - t_cf_start).total_seconds() / 3600.0)

        if is_pan_style:
            milestones.append(ProofingMilestone(
                step_num=step,
                title=f"In-Pan Cold Fermentation ({round(actual_cf_hours, 1)} hours / 2-3 Days)",
                action_category="cold_retard",
                timestamp_iso=t_cf_start.isoformat(),
                display_time=dt_str(t_cf_start),
                duration_str=f"{round(actual_cf_hours, 1)} hours",
                temp_desc=f"Refrigerator ~{fridge_temp_f}°F (Covered Pan)",
                instruction=(
                    f"1. Cover the Detroit pan tightly with plastic wrap, heavy-duty foil, or a fitted LloydPan lid.\n"
                    f"2. Place directly into the refrigerator at ~{fridge_temp_f}°F for {round(actual_cf_hours, 1)} hours (2-3 days).\n"
                    "3. In the cold, enzyme activity breaks starches into sugars while the dough slowly absorbs the olive oil, "
                    "building an airy, tender focaccia-like crumb and unmatched flavor."
                ),
                visual_cue="Dough slowly relaxes and creeps outward across the pan bottom; small fermentation micro-bubbles appear under the skin.",
                pro_tip="A 2-3 day (48-72h) in-pan cold ferment produces the deep, complex sourdough-like flavor profile iconic to Detroit pizza."
            ))
        else:
            milestones.append(ProofingMilestone(
                step_num=step,
                title=f"Cold Retardation / Refrigerator Maturation ({round(actual_cf_hours, 1)} hours)",
                action_category="cold_retard",
                timestamp_iso=t_cf_start.isoformat(),
                display_time=dt_str(t_cf_start),
                duration_str=f"{round(actual_cf_hours, 1)} hours",
                temp_desc=f"Refrigerator ~{fridge_temp_f}°F (Covered)",
                instruction=(
                    f"1. Seal containers tightly and place in the refrigerator at ~{fridge_temp_f}°F.\n"
                    f"2. Leave undisturbed for {round(actual_cf_hours, 1)} hours.\n"
                    "3. In the cold, yeast gas production slows down while natural enzymes (amylases & proteases) "
                    "break starches into sweet sugars and soften gluten strands for incredible tender chew."
                ),
                visual_cue="Dough balls slowly relax outward into flat pucks; subtle micro-blisters form under the surface skin.",
                pro_tip="Cold fermentation is where pizzeria-grade flavor is born! 24-72 hours produces deep, complex, nutty flavors."
            ))
        step += 1

        if is_pan_style:
            milestones.append(ProofingMilestone(
                step_num=step,
                title=f"Room Temperature Temper & Final Pan Proof ({round(temper_hours, 1)} hours)",
                action_category="temper",
                timestamp_iso=t_temper_start.isoformat(),
                display_time=dt_str(t_temper_start),
                duration_str=f"{round(temper_hours, 1)} hours",
                temp_desc=f"Room Temp ~{room_temp_f}°F (Covered Pan)",
                instruction=(
                    f"1. Remove covered pan from the refrigerator {round(temper_hours, 1)} hours before your target bake time.\n"
                    "2. Keep covered at room temperature (~70°F). After 1 hour of warming, use oiled fingertips to gently dimple and ease the relaxed dough all the way into the four corners of the pan.\n"
                    "3. Re-cover and let rise undisturbed until the dough proofs halfway up the sides of the pan (~1 to 1.5 inches deep)."
                ),
                visual_cue="Dough completely covers pan floor to all 4 corners, pillowy, aerated, and jiggly with large surface bubbles.",
                pro_tip="Handle gently during the final pan proof so you preserve all the pockets of air that create Detroit's airy honeycomb crumb!"
            ))
        else:
            milestones.append(ProofingMilestone(
                step_num=step,
                title="Room Temperature Tempering & Final Proof",
                action_category="temper",
                timestamp_iso=t_temper_start.isoformat(),
                display_time=dt_str(t_temper_start),
                duration_str=f"{round(temper_hours, 1)} hours",
                temp_desc=f"Room Temp ~{room_temp_f}°F (Airtight)",
                instruction=(
                    f"1. Remove dough containers from the refrigerator {round(temper_hours, 1)} hours before your target bake time.\n"
                    "2. KEEP CONTAINERS AIRTIGHT to avoid condensation drying out the delicate dough surface.\n"
                    f"3. Allow internal dough temperature to rise from 38°F to 60-65°F at room temperature (~{room_temp_f}°F)."
                ),
                visual_cue=(
                    "Dough balls feel warm and pillowy. When poked gently with a floured finger, the indent springs back slowly, "
                    "leaving a slight indentation (the classic 'poke test')."
                ),
                pro_tip="NEVER stretch cold dough straight from the fridge! Cold gluten resists, snaps back, tears easily, and creates dense gum-lines."
            ))
        step += 1

        preheat_mins = 45
        t_preheat = ready_time - timedelta(minutes=preheat_mins)
        if t_preheat < t_temper_start:
            t_preheat = t_temper_start
    else:
        # ROOM TEMPERATURE SCHEDULE (Direct same-day or short proof)
        ferment_avail_hours = max(0.5, avail_hours - 0.25)
        bulk_hours = round(ferment_avail_hours * 0.42, 2)
        ball_proof_hours = round(ferment_avail_hours - bulk_hours, 2)

        t_bulk_start = t_knead_done
        t_bulk_end = t_bulk_start + timedelta(hours=bulk_hours)

        milestones.append(ProofingMilestone(
            step_num=step,
            title="Bulk Fermentation (Initial Rise)",
            action_category="bulk",
            timestamp_iso=t_bulk_start.isoformat(),
            display_time=dt_str(t_bulk_start),
            duration_str=f"{round(bulk_hours, 1)} hours",
            temp_desc=f"Room Temp ~{room_temp_f}°F (Covered)",
            instruction=(
                f"1. Form dough into a tidy ball and place in a lightly oiled bowl or container.\n"
                f"2. Cover tightly with plastic wrap or a fitted lid to prevent the skin from drying out.\n"
                f"3. Allow to bulk ferment at room temperature (~{room_temp_f}°F) for {round(bulk_hours, 1)} hours."
            ),
            visual_cue="Dough expands noticeably in volume with soft, pillowy texture.",
            pro_tip="Room temperature bulk starts the flavor development and gives yeast an active start."
        ))
        step += 1

        t_ball = t_bulk_end
        t_ball_done = t_ball + timedelta(minutes=15)
        milestones.append(ProofingMilestone(
            step_num=step,
            title=f"Divide & Shape into {ingredients.balls} Dough Balls ({ingredients.ball_weight_g}g each)",
            action_category="ball",
            timestamp_iso=t_ball.isoformat(),
            display_time=dt_str(t_ball),
            duration_str="15 mins",
            temp_desc="Room Temp Bench",
            instruction=(
                f"1. Turn dough onto clean, un-floured or lightly oiled counter.\n"
                f"2. Cut into {ingredients.balls} equal pieces using a bench scraper, each weighing exactly {ingredients.ball_weight_g}g.\n"
                "3. Cup your hand over each portion and drag in a circular motion against the counter to create taut surface tension. "
                "Pinch the bottom seam shut tightly.\n"
                "4. Place into lightly oiled individual proofing containers, spaced 2-3 inches apart."
            ),
            visual_cue="Smooth, tight, spherical dough balls with zero surface tears and a sealed bottom belly.",
            pro_tip="Surface tension during balling is what traps carbon dioxide and gives you high, puffy cornicione crust borders!"
        ))
        step += 1

        t_ball_proof_start = t_ball_done
        milestones.append(ProofingMilestone(
            step_num=step,
            title=f"Room Temperature Ball Proof ({round(ball_proof_hours, 1)} hours)",
            action_category="temper",
            timestamp_iso=t_ball_proof_start.isoformat(),
            display_time=dt_str(t_ball_proof_start),
            duration_str=f"{round(ball_proof_hours, 1)} hours",
            temp_desc=f"Room Temp ~{room_temp_f}°F (Airtight)",
            instruction=(
                f"1. Keep dough containers sealed at room temperature (~{room_temp_f}°F).\n"
                f"2. Let balls proof for {round(ball_proof_hours, 1)} hours until fully expanded, soft, and relaxed."
            ),
            visual_cue="Balls double in volume, spreading gently. Very soft, delicate, and pillowy to touch.",
            pro_tip="Handle proofed balls with extreme gentleness using a flat bench scraper so you don't degas the rim."
        ))
        step += 1

        preheat_mins = min(45, max(15, int(ball_proof_hours * 30)))
        t_preheat = ready_time - timedelta(minutes=preheat_mins)
        if t_preheat < t_ball_proof_start:
            t_preheat = t_ball_proof_start

    # Oven Preheat & Setup
    if is_pan_style:
        milestones.append(ProofingMilestone(
            step_num=step,
            title=f"Preheat Oven to {recipe.bake_temp_f}°F (Lowest Rack Setup)",
            action_category="preheat",
            timestamp_iso=t_preheat.isoformat(),
            display_time=dt_str(t_preheat),
            duration_str=f"{preheat_mins} mins",
            temp_desc=f"{recipe.bake_temp_f}°F Bottom Heat",
            instruction=(
                f"1. Preheat oven to {recipe.bake_temp_f}°F with baking steel or pizza stone placed on the LOWEST rack.\n"
                f"2. Setting the heavy Detroit pan directly on top of a preheated steel/stone ensures the bottom crust "
                "immediately begins frying in the olive oil for maximum bottom crunch.\n"
                f"3. Allow oven and stone to heat-saturate for at least {preheat_mins} minutes."
            ),
            visual_cue="Baking stone/steel is thoroughly preheated and oven has stabilized at target temperature.",
            pro_tip="Bottom rack placement is crucial for Detroit pizza to cook the dense dough and fry the bottom crust without burning the top cheese prematurely."
        ))
    else:
        milestones.append(ProofingMilestone(
            step_num=step,
            title=f"Preheat {recipe.oven_type} to {recipe.bake_temp_f}°F",
            action_category="preheat",
            timestamp_iso=t_preheat.isoformat(),
            display_time=dt_str(t_preheat),
            duration_str=f"{preheat_mins} mins",
            temp_desc=f"{recipe.bake_temp_f}°F Intense Heat",
            instruction=(
                f"1. Preheat oven to {recipe.bake_temp_f}°F with baking steel or pizza stone placed on the second rack from the top.\n"
                f"2. Let the steel/stone thoroughly saturate with thermal energy for at least {preheat_mins} minutes.\n"
                + ("If using home oven: switch to BROIL high 5 minutes before launching pizza for maximum blistered top heat." if recipe.bake_temp_f <= 550 else "If using outdoor oven: ensure stone floor reads 800-850°F on infrared thermometer.")
            ),
            visual_cue="Baking surface is screaming hot and fully heat-soaked.",
            pro_tip="A preheated baking steel transfers heat 18x faster than ceramic pizza stone, guaranteeing a crispy bottom crust!"
        ))
    step += 1

    # Step: Stretch / Top & Bake!
    t_bake = ready_time
    if is_pan_style:
        milestones.append(ProofingMilestone(
            step_num=step,
            title=f"Edge-to-Edge Cheese & Pan Bake ({recipe.bake_time_min})",
            action_category="bake",
            timestamp_iso=t_bake.isoformat(),
            display_time=dt_str(t_bake),
            duration_str=recipe.bake_time_min,
            temp_desc=f"{recipe.bake_temp_f}°F",
            instruction=(
                "1. Spread cubed or shredded Wisconsin brick cheese, low-moisture whole milk mozzarella, or Monterey Jack "
                "generously across the dough, packing cheese all the way against the dark steel edges and corners of the pan.\n"
                f"2. Bake in the pan for {recipe.bake_time_min} at {recipe.bake_temp_f}°F (placed on bottom steel) "
                "until cheese is sizzling, deeply browned, and a dark mahogany caramelized cheese crown (frico) forms around the perimeter.\n"
                "3. Warm your pizza sauce separately. Ladle two thick 'racing stripes' of sauce over the hot baked cheese.\n"
                "4. Run a thin metal offset spatula around the edges to release the crispy frico rim, lift the pizza out onto a cutting board, and slice into squares with a rocker blade!"
            ),
            visual_cue="Crisp, mahogany frico cheese crown along all 4 edges; airy focaccia crumb with fried crispy olive oil bottom.",
            pro_tip="Pressing the cheese directly against the metal pan edge is the secret to Detroit pizza! It melts down the side to create the crunchy caramelized frico."
        ))
    else:
        milestones.append(ProofingMilestone(
            step_num=step,
            title=f"Stretch, Top & Bake ({recipe.bake_time_min})",
            action_category="bake",
            timestamp_iso=t_bake.isoformat(),
            display_time=dt_str(t_bake),
            duration_str=recipe.bake_time_min,
            temp_desc=f"{recipe.bake_temp_f}°F",
            instruction=(
                "1. Dust work surface generously with a 50/50 mix of semolina flour (semola rimacinata) and 00 flour.\n"
                "2. Gently invert container; let dough ball drop onto flour without pulling.\n"
                "3. Starting 1/2 inch from edge, use fingertips to press outward, pushing gas into the outer rim (cornicione).\n"
                "4. Lift dough onto backs of floured knuckles and rotate gently to stretch to 12-14 inches diameter.\n"
                "5. Transfer to lightly dusted peel. Shake peel to verify dough slides freely!\n"
                "6. Top sparingly (crushed San Marzano tomatoes, whole milk mozzarella, basil, drizzle of EVOO).\n"
                f"7. Launch onto hot steel/stone and bake for {recipe.bake_time_min} until charred, bubbly, and crisp."
            ),
            visual_cue="Cornicione rises with deep airy bubbles, golden leopard spotting, and melted cheese with slight browning.",
            pro_tip="Less is more on toppings! Heavy wet toppings make the center soggy. Shake the peel before launching every time."
        ))

    return milestones
