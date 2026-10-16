---
name: pizza-dough-artisan
description: Master Pizzaiolo & Pizza Dough Fermentation Agent. Works off base recipes (custom or classic NY, Neapolitan, Detroit, Roman, Sourdough), dynamically adjusts yeast percentages based on fermentation time and temperature, calculates Desired Dough Temperature (DDT) water calibration, and provides timestamped step-by-step proofing and baking instructions.
---

# 🍕 Pizza Dough Artisan & Fermentation Skill

When the user asks to make pizza dough, plan a pizza night, adjust yeast for a specific timeline, or manage their dough recipes:

## 1. Quick Capabilities
- **Dynamic Yeast Kinetics**: Accurately scales Instant Dry Yeast (IDY), Active Dry Yeast (ADY), Fresh Cake Yeast (CY), or Sourdough starter for any timeline (from a 3-hour same-day emergency dough to a 72-hour cold retard).
- **Base Recipe Engine**: Works from pre-loaded classic base recipes or user-defined custom recipes (baker's percentages for hydration, salt, oil, sugar, and flour type).
- **Water Temperature (DDT) Calibration**: Computes target water temperature based on room temperature and kneading method so the dough finishes at 75–78°F.
- **Timestamped Proofing Roadmap**: Generates step-by-step milestones (Mix & autolyse, Knead, Bulk ferment, Balling, Cold retard, Tempering & warm-up, Preheat, and Bake) with visual cues and pizzaiolo tips.
- **Interactive Web Dashboard**: Visual sliders, real-time recalculations, and printable kitchen sheets.

## 2. Using the Dough CLI
The dough engine and CLI are located at:
`/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough`

Common commands:
```bash
# Calculate plan for 4 NY Style pizzas ready tomorrow at 6pm
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough plan --recipe ny_style --balls 4 --ready "tomorrow 6pm"

# Calculate for an exact fermentation duration (e.g. 48-hour cold ferment)
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough plan --recipe ny_style --hours 48 --balls 4

# Calculate for Adam's Detroit Style Pan Pizza (13x9, 14x10, or 8x10 pan)
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough plan --recipe adams_detroit --pan 13x9

# Calculate for two 8x10 Detroit pans with 72-hour cold retard
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough plan --recipe adams_detroit --pan 8x10 --balls 2 --hours 72

# Calculate for Adam's Freezable Home Oven Dough (batch of 4 to freeze)
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough plan --recipe adams_freezable --balls 4

# Quick 4-hour same-day dough for dinner tonight
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough quick --hours 4 --balls 3

# Ask the agent in conversational English
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough ask "For a 13 x 9 detroit style pizza pan: 350g bread flour, 260g water, 3g yeast, 10g salt, 20g olive oil"

# List all available base recipes
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough recipe list

# View full details of a recipe
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough recipe show ny_style

# Add or update a user's custom base recipe
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough recipe add \
  --id my_crust \
  --name "Adam's Secret Crust" \
  --hydration 66.5 \
  --salt 2.4 \
  --oil 2.0 \
  --sugar 1.5 \
  --weight 265 \
  --balls 4 \
  --flour "King Arthur Bread Flour" \
  --oven "Home Oven (550°F / Pizza Steel)" \
  --notes "Cold ferment 48-72h for optimal blistering"

# Launch the interactive visual web dashboard
/Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent/dough serve --port 8080
```

## 3. Fermentation Heuristics & Craig's Kinetic Model
- **Yeast Scaling Curve**:
  - 3–4 Hours (Room Temp): ~0.35% – 0.50% IDY (quick rise)
  - 8–12 Hours (Room Temp): ~0.10% – 0.16% IDY
  - 24 Hours (Room Temp): ~0.033% – 0.040% IDY
  - 24 Hours (Cold Ferment in Refrigerator @ 38°F): ~0.16% – 0.20% IDY
  - 48 Hours (Cold Ferment): ~0.10% – 0.13% IDY
  - 72 Hours (Cold Ferment): ~0.06% – 0.08% IDY
- **Yeast Type Conversions**:
  - IDY (Instant Dry Yeast) = 1.0x (baseline)
  - ADY (Active Dry Yeast) = 1.33x IDY (dissolve in warm 100°F water first)
  - CY (Fresh Cake Yeast) = 3.0x IDY
  - Sourdough Starter = 8% – 20% of flour weight depending on fermentation hours
- **Refrigeration Dormancy**:
  - Yeast activity at 38°F drops by ~8x compared to 68°F. Cold retard allows amylase and protease enzymes to break down starches and gluten bonds into flavor compounds without over-gassing.
- **Crucial Rule**: Never stretch cold dough straight from the fridge! Dough balls must temper at room temperature for 2 to 3.5 hours until internal temperature reaches 60–65°F.
