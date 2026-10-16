# 🍕 Pizza Dough Artisan Agent & Fermentation Assistant

An intelligent, master-pizzaiolo-grade agent and pizza dough management platform. Works off your personal base recipes, dynamically adjusts yeast percentages based on fermentation time and temperature, and generates precise, timestamped proofing and baking schedules.

---

## 🌟 Key Capabilities

1. **Dynamic Yeast Kinetics Engine**:
   - Calibrated using **Craig's Fermentation Curve** and **Arrhenius / Q10 metabolic rate scaling**.
   - Accurately adjusts yeast whether you are baking **today in 4 hours** or cold-fermenting for **72 hours in the refrigerator**.
   - Supports:
     - **Instant Dry Yeast (IDY)**
     - **Active Dry Yeast (ADY)**
     - **Fresh / Cake Yeast (CY)**
     - **Sourdough Starter / Levain**
   - Automatically provides kitchen-friendly fractional teaspoon measurements (e.g. `1/4 tsp`, `1/2 tsp`, `tiny pinch`) alongside precision scale grams.

2. **Base Recipe Management (Custom & Classic)**:
   - Store and customize your personal base recipes with baker's percentages:
     - **Hydration %** (Water)
     - **Salt %**
     - **Olive Oil %**
     - **Sugar / Diastatic Malt %**
     - **Target Ball Weight & Count**
     - **Flour Recommendations & Oven Targets**
   - Pre-loaded with master styles and Adam's signature formulas:
     - 🧀 `Adam's Detroit Style Pan Pizza` (74.3% hydration, 2.86% salt, 5.71% olive oil, 2-3 day in-pan cold ferment)
     - 🔥 `Adam's High-Heat Outdoor Dough` (62.0% hydration, 1.5% salt, 0% oil, 0% sugar for 900°F ovens)
     - 🗽 `Classic New York Style` (65% hydration, 2.3% salt, 2.0% oil, 1.5% sugar)
     - 🇮🇹 `Neapolitan Vera Pizza (AVPN)` (62% hydration, 2.8% salt, 0% oil, 0% sugar)
     - ⚡ `Same-Day Express (3-5 Hours)` (64% hydration, 2.2% salt, 2.0% oil, 1.5% sugar)
     - 🌾 `Artisan Naturally Leavened Sourdough` (66% hydration, 2.4% salt, 1.5% oil)
     - 🍕 `Roman Pizza al Taglio / Pinsa` (78% hydration, 2.5% salt, 3.0% oil)
   - **Detroit & Sicilian Pan Sizing Support**:
     - Automatic area-scaled calculations for **13" × 9"** (643g dough / 350g flour), **14" × 10"** (770g dough / 419g flour), and **8" × 10"** (440g dough / 239g flour) pans.
     - Pan-specific proofing roadmap: in-pan cold fermentation (48–72h), room temp 4-corner dimpling proof (3–4h), lowest rack oven preheat, and caramelized frico cheese crown baking instructions.

3. **Desired Dough Temperature (DDT) Water Calibration**:
   - Calculates exact water temperature needed:
     $$\text{Water Temp} = (3 \times \text{DDT}) - \text{Room Temp} - \text{Flour Temp} - \text{Friction Factor}$$
   - Ensures finished mixed dough hits the optimal fermentation sweet spot (**75°F – 78°F**).

4. **Chronological Proofing Roadmap**:
   - Generates backwards- and forward-scheduled milestones with exact timestamps:
     - 🥣 **Step 1: Mise en Place & Water Temp Calibration**
     - 🌀 **Step 2: Autolyse Rest & Gluten Development (Kneading)**
     - ⏳ **Step 3: Bulk Fermentation (Initial Rise)**
     - ⚪ **Step 4: Dividing & Balling**
     - ❄️ **Step 5: Cold Retardation (Refrigerator Maturation)**
     - 🌡️ **Step 6: Room Temperature Tempering (Final Proof & Poke Test)**
     - 🔥 **Step 7: Oven & Steel Preheat**
     - 🍕 **Step 8: Stretch, Top, Launch & Bake!**
   - Includes **Visual Cues** (what to look for before moving to next step) and **Pro Tips**.

5. **Interactive Web Dashboard**:
   - Visual sliders for dough balls (1–12) and ball weights (180g–520g).
   - Real-time recalculation of baker's percentages and scale grams.
   - Interactive timeline cards.
   - **One-click "Print Kitchen Sheet"** formatting for clean kitchen prep.
   - Built-in Recipe Creator and Editor modal.

6. **Antigravity Custom Skill**:
   - Fully integrated skill in `.agents/skills/pizza-dough-artisan/SKILL.md` so Antigravity can calculate dough formulas directly in chat.

---

## 🚀 Quick Start

### 1. View Available Base Recipes
```bash
cd /Users/adamperry/.gemini/antigravity/scratch/pizza_dough_agent
./dough recipe list
```

### 2. Plan Dough for Tomorrow Night (e.g. 4 pizzas at 6 PM)
```bash
./dough plan --recipe ny_style --balls 4 --ready "tomorrow 6pm"
```

### 3. Plan for an Exact Duration (e.g. 48-Hour Cold Ferment)
```bash
./dough plan --recipe ny_style --hours 48 --balls 4
```

### 4. Plan Adam's Detroit Style Pan Pizza (13x9, 14x10, or 8x10)
```bash
# Standard 13" x 9" Detroit Pan (643g dough / 350g flour)
./dough plan --recipe adams_detroit --pan 13x9

# Large 14" x 10" Detroit Pan (770g dough / 419g flour)
./dough plan --recipe adams_detroit --pan 14x10 --hours 72

# Two Small 8" x 10" Detroit Pans (440g dough / 239g flour each)
./dough plan --recipe adams_detroit --pan 8x10 --balls 2
```

### 5. Fast Same-Day Express Dough (Dinner in 4 Hours)
```bash
./dough quick --hours 4 --balls 3
```

### 6. Add Your Own Base Recipe
```bash
./dough recipe add \
  --id my_crust \
  --name "Adam's Go-To NY Style" \
  --hydration 66.0 \
  --salt 2.4 \
  --oil 2.0 \
  --sugar 1.5 \
  --weight 265 \
  --balls 4 \
  --flour "King Arthur Bread Flour" \
  --oven "Home Oven (550°F on Pizza Steel)" \
  --temp 550 \
  --time "6-7 minutes" \
  --notes "Cold ferment 48 hours. Let warm up 3 hours before stretching."
```

### 7. Ask the Agent in Natural Conversational English
```bash
./dough ask "For a 13 x 9 detroit style pizza pan: 350g bread flour, 260g water, 3g yeast, 10g salt, 20g olive oil"
./dough ask "I want two 8x10 detroit pan pizzas for 3 days from now"
./dough ask "I want 4 Neapolitan dough balls of 250g each for tomorrow night at 7pm"
./dough ask "I have 5 hours until dinner, make 3 pizzas with instant dry yeast"
```

### 8. Launch the Interactive Web Dashboard
```bash
./dough serve --port 8001
```
*Or double-click `start_dashboard.command` in Finder!*
Then open [http://localhost:8001](http://localhost:8001) in your browser.

---

## 📊 Yeast Scaling Reference Table

Approximate Instant Dry Yeast (IDY) percentages for optimal fermentation:

| Total Fermentation Time | Fermentation Profile | Calculated IDY % | Grams per 1kg Flour | Kitchen Measurement |
| :--- | :--- | :--- | :--- | :--- |
| **3 Hours** | Direct Room Temp (70°F) | ~0.45% | ~4.5 g | ~1 1/2 tsp |
| **5 Hours** | Direct Room Temp (70°F) | ~0.26% | ~2.6 g | ~3/4 tsp |
| **8 Hours** | Direct Room Temp (70°F) | ~0.15% | ~1.5 g | ~1/2 tsp |
| **12 Hours** | Direct Room Temp (70°F) | ~0.09% | ~0.9 g | ~1/4 tsp |
| **24 Hours** | Direct Room Temp (70°F) | ~0.035% | ~0.35 g | ~1/8 tsp |
| **24 Hours** | Cold Ferment (Fridge 38°F + RT warm) | ~0.16% | ~1.6 g | ~1/2 tsp |
| **48 Hours** | Cold Ferment (Fridge 38°F + RT warm) | ~0.11% | ~1.1 g | ~1/4 tsp |
| **72 Hours** | Cold Ferment (Fridge 38°F + RT warm) | ~0.07% | ~0.7 g | ~1/4 tsp (scant) |

*Active Dry Yeast (ADY) = 1.33x IDY | Fresh Cake Yeast (CY) = 3.0x IDY*

---

## 🧪 Unit Tests

Run test suite to verify yeast kinetics, baker's percentages, and scheduling:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 🚂 Deploy to Railway

This repository is pre-configured for instant zero-configuration deployment on [Railway](https://railway.app):
- **`railway.json`**: Configures Nixpacks builder, healthchecks (`/api/status`), and restart policy.
- **`Procfile`**: Declares the web worker (`web: python3 -m pizza_agent.server`).
- **`Dockerfile`**: Container definition ready if you prefer the Docker engine.
- **Dynamic Port Binding**: Automatically binds to `$PORT` assigned by Railway or default `8001`.

### Instant Deployment Steps:
1. Navigate to your [Railway Dashboard](https://railway.app/dashboard).
2. Click **"+ New Project"** → **"Deploy from GitHub repo"**.
3. Select **`adambperry-lgtm/pizza-dough-agent`**.
4. Click **Deploy Now**. Railway builds and provisions the app automatically.
5. In your Railway project service view:
   - Go to **Settings** → **Networking** → Click **"Generate Domain"** (e.g. `pizza-dough-agent-production.up.railway.app`).
   - Open your generated domain to access your live Pizza Dough Artisan dashboard from anywhere on phone, tablet, or desktop!

