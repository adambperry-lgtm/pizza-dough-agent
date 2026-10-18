/**
 * Pizza Dough Artisan Agent - Front-end Application
 * Supports both HTTP Server API mode and 100% Offline Standalone file:// bookmark mode!
 */

// Default Built-in Master Recipes
const DEFAULT_RECIPES = [
  {
    id: "adams_detroit",
    name: "Adam's Detroit Style Pan Pizza",
    description: "Authentic Detroit pan pizza: 74.3% hydration, 2.86% salt, 5.71% EVOO. 2-3 day in-pan cold ferment for 13x9, 14x10, or 8x10 pans.",
    flour_type: "Bread Flour (e.g. King Arthur Bread Flour)",
    hydration_pct: 74.3,
    salt_pct: 2.86,
    oil_pct: 5.71,
    sugar_pct: 0.0,
    default_ball_weight: 643.0,
    default_balls: 1,
    oven_type: "Home Oven (475-500°F in Detroit Blue Steel or LloydPan)",
    bake_temp_f: 485,
    bake_time_min: "14-16 minutes",
    recommended_ferment: "CF",
    is_custom: true
  },
  {
    id: "adams_outdoor_base",
    name: "Adam's High-Heat Outdoor Dough",
    description: "00 flour with 62% hydration, 1.5% salt, 0% oil, 0% sugar. Designed for intense 850-950°F stone temperatures.",
    flour_type: "Tipo 00 Italian Flour",
    hydration_pct: 62.0,
    salt_pct: 1.5,
    oil_pct: 0.0,
    sugar_pct: 0.0,
    default_ball_weight: 325.0,
    default_balls: 1,
    oven_type: "High-Heat Outdoor Pizza Oven (Ooni / Roccbox / Gozney at 850-950°F)",
    bake_temp_f: 900,
    bake_time_min: "60-90 seconds",
    recommended_ferment: "RT",
    is_custom: true
  },
  {
    id: "adams_freezable",
    name: "Adam's Freezable Home Oven Dough",
    description: "Freeze-ahead dough for regular oven: 200g flour, 124g water (62%), 6g olive oil (3%), 4g sugar (2%), 4g salt (2%), 2.5g yeast (1.25%). Flash-freeze after balling; store up to 3 months.",
    flour_type: "Bread Flour or All-Purpose Flour",
    hydration_pct: 62.0,
    salt_pct: 2.0,
    oil_pct: 3.0,
    sugar_pct: 2.0,
    default_ball_weight: 340.5,
    default_balls: 4,
    oven_type: "Regular Home Oven (475-525°F on Pizza Stone / Steel / Baking Sheet)",
    bake_temp_f: 500,
    bake_time_min: "7-10 minutes",
    recommended_ferment: "FREEZE",
    is_custom: true
  },
  {
    id: "ny_style",
    name: "Classic New York Style",
    description: "Authentic NYC pizzeria slice: crispy bottom, chewy foldable rim, golden leopard blisters.",
    flour_type: "High-Gluten or Bread Flour (12.7% - 14% protein)",
    hydration_pct: 65.0,
    salt_pct: 2.3,
    oil_pct: 2.0,
    sugar_pct: 1.5,
    default_ball_weight: 265.0,
    default_balls: 4,
    oven_type: "Home Oven (500-550°F on Pizza Steel / Stone)",
    bake_temp_f: 550,
    bake_time_min: "6-8 minutes",
    recommended_ferment: "CF",
    is_custom: false
  },
  {
    id: "neapolitan",
    name: "Neapolitan Vera Pizza (AVPN)",
    description: "Traditional wood-fired style: pillowy cloud-like cornicione, tender melt-in-the-mouth texture.",
    flour_type: "Tipo 00 Italian Flour (e.g. Caputo Pizzeria)",
    hydration_pct: 62.0,
    salt_pct: 2.8,
    oil_pct: 0.0,
    sugar_pct: 0.0,
    default_ball_weight: 250.0,
    default_balls: 4,
    oven_type: "High-Heat Outdoor Pizza Oven (850-950°F)",
    bake_temp_f: 900,
    bake_time_min: "60-90 seconds",
    recommended_ferment: "RT",
    is_custom: false
  },
  {
    id: "detroit",
    name: "Detroit Style Pan Pizza",
    description: "Airy focaccia-like crumb with caramelized cheesy frico crust around blue steel pan edges.",
    flour_type: "Bread Flour (e.g. King Arthur Bread Flour)",
    hydration_pct: 73.0,
    salt_pct: 2.2,
    oil_pct: 2.5,
    sugar_pct: 1.0,
    default_ball_weight: 420.0,
    default_balls: 2,
    oven_type: "Home Oven (450-500°F in 10x14 LloydPans blue steel)",
    bake_temp_f: 475,
    bake_time_min: "13-16 minutes",
    recommended_ferment: "CF",
    is_custom: false
  },
  {
    id: "same_day_quick",
    name: "Same-Day Express Dough (3-5 Hours)",
    description: "Fast turnaround dough when you decide to make pizza for dinner tonight.",
    flour_type: "Bread Flour or All-Purpose Flour",
    hydration_pct: 64.0,
    salt_pct: 2.2,
    oil_pct: 2.0,
    sugar_pct: 1.5,
    default_ball_weight: 260.0,
    default_balls: 3,
    oven_type: "Home Oven (500-550°F on Steel)",
    bake_temp_f: 550,
    bake_time_min: "6-8 minutes",
    recommended_ferment: "RT",
    is_custom: false
  },
  {
    id: "roman_pinsa",
    name: "Roman Pizza al Taglio / Pinsa",
    description: "Ultra-high hydration, cloud-like airy crumb with an ultra-crisp shattered glass bottom.",
    flour_type: "Strong High-Protein Bread Flour",
    hydration_pct: 78.0,
    salt_pct: 2.5,
    oil_pct: 3.0,
    sugar_pct: 0.0,
    default_ball_weight: 500.0,
    default_balls: 2,
    oven_type: "Home Oven (500°F on Baking Sheet or Steel)",
    bake_temp_f: 500,
    bake_time_min: "10-14 minutes",
    recommended_ferment: "CF",
    is_custom: false
  },
  {
    id: "sourdough_artisan",
    name: "Artisan Naturally Leavened Sourdough",
    description: "Pure wild yeast sourdough crust: complex lactic tang, blistered charred bubbles, supreme digestibility.",
    flour_type: "Bread Flour + 10% Whole Wheat or Spelt",
    hydration_pct: 66.0,
    salt_pct: 2.4,
    oil_pct: 1.5,
    sugar_pct: 0.0,
    default_ball_weight: 265.0,
    default_balls: 4,
    oven_type: "Home Oven (550°F) or Outdoor High Heat",
    bake_temp_f: 550,
    bake_time_min: "6-8 minutes",
    recommended_ferment: "CF",
    is_custom: false
  }
];

let recipesState = [];
let currentPlan = null;
let currentFermentMode = "AUTO";
const isStaticHost = window.location.hostname.endsWith("github.io") || window.location.protocol === "file:";

const PAN_SIZES = {
  "13x9": { name: '13" × 9" Pan (Standard)', dough_weight_g: 643.0, flour_g: 350.0 },
  "14x10": { name: '14" × 10" Pan (Large)', dough_weight_g: 770.0, flour_g: 419.0 },
  "8x10": { name: '8" × 10" Pan (Small / Half)', dough_weight_g: 440.0, flour_g: 239.0 }
};
let selectedPanSize = "13x9";

const actionIcons = {
  mix: "🥣",
  knead: "🌀",
  bulk: "⏳",
  ball: "⚪",
  cold_retard: "❄️",
  temper: "🌡️",
  preheat: "🔥",
  bake: "🍕",
};

// DOM Elements
const recipeSelect = document.getElementById("recipe-select");
const recipeDesc = document.getElementById("recipe-desc");
const ballsSlider = document.getElementById("balls-slider");
const ballsVal = document.getElementById("balls-val");
const weightSlider = document.getElementById("weight-slider");
const weightVal = document.getElementById("weight-val");
const hoursInput = document.getElementById("hours-input");
const yeastSelect = document.getElementById("yeast-select");
const roomTempSlider = document.getElementById("room-temp-slider");
const roomTempVal = document.getElementById("room-temp-val");
const fridgeTempSlider = document.getElementById("fridge-temp-slider");
const fridgeTempVal = document.getElementById("fridge-temp-val");

const formulaMeta = document.getElementById("formula-meta");
const totalWeightDisplay = document.getElementById("total-weight-display");
const ingredientsTbody = document.getElementById("ingredients-tbody");
const ddtTemp = document.getElementById("ddt-temp");
const ddtDesc = document.getElementById("ddt-desc");
const kineticDesc = document.getElementById("kinetic-desc");
const timelineSteps = document.getElementById("timeline-steps");
const scheduleSubtitle = document.getElementById("schedule-subtitle");

// Modal Elements
const recipeModal = document.getElementById("recipe-modal");
const recipeForm = document.getElementById("recipe-form");
const modalTitle = document.getElementById("modal-title");
const btnNewRecipe = document.getElementById("btn-new-recipe");
const btnEditRecipe = document.getElementById("btn-edit-recipe");
const btnDeleteRecipe = document.getElementById("btn-delete-recipe");
const modalClose = document.getElementById("modal-close");
const btnCancelModal = document.getElementById("btn-cancel-modal");
const btnPrint = document.getElementById("btn-print");

// Initialize
document.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  await loadRecipes();
  triggerRecalculate();
});

function setupEventListeners() {
  ballsSlider.addEventListener("input", (e) => {
    ballsVal.textContent = e.target.value;
    debounceRecalculate();
  });

  weightSlider.addEventListener("input", (e) => {
    weightVal.textContent = `${e.target.value} g`;
    debounceRecalculate();
  });

  // Pan Size Preset Buttons
  document.querySelectorAll(".pan-size-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".pan-size-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      selectedPanSize = btn.dataset.pan;
      const weight = parseFloat(btn.dataset.weight);
      weightSlider.value = weight;
      weightVal.textContent = `${weight} g`;
      const spec = PAN_SIZES[selectedPanSize];
      const badge = document.getElementById("pan-spec-badge");
      if (badge && spec) {
        badge.textContent = `${spec.name.split(' (')[0]} (${spec.dough_weight_g}g dough)`;
      }
      triggerRecalculate();
    });
  });

  hoursInput.addEventListener("input", () => {
    updateActivePreset();
    debounceRecalculate();
  });

  recipeSelect.addEventListener("change", (e) => {
    const selected = recipesState.find(r => r.id === e.target.value);
    const panGroup = document.getElementById("pan-size-group");
    const ballsLabel = document.getElementById("balls-label");
    const weightLabel = document.getElementById("weight-label");

    if (selected) {
      recipeDesc.textContent = `${selected.description} • Flour: ${selected.flour_type}`;
      const isPan = (selected.id === "adams_detroit" || selected.id === "detroit" || selected.name.toLowerCase().includes("detroit") || selected.name.toLowerCase().includes("pan"));

      if (isPan) {
        if (panGroup) panGroup.style.display = "block";
        if (ballsLabel) ballsLabel.textContent = "Detroit Pans (Count)";
        if (weightLabel) weightLabel.textContent = "Weight per Pan";
        ballsSlider.value = selected.default_balls || 1;
        ballsVal.textContent = ballsSlider.value;
        weightSlider.value = selected.default_ball_weight || 643;
        weightVal.textContent = `${weightSlider.value} g`;

        // Default to 48 hours cold ferment preset for Detroit style
        hoursInput.value = 48;
        document.querySelectorAll(".preset-btn").forEach(b => {
          b.classList.toggle("active", b.dataset.hours === "48");
        });
        document.querySelectorAll(".segment-btn").forEach(b => {
          b.classList.toggle("active", b.dataset.mode === "CF");
        });
        currentFermentMode = "CF";
      } else {
        if (panGroup) panGroup.style.display = "none";
        if (ballsLabel) ballsLabel.textContent = "Dough Balls";
        if (weightLabel) weightLabel.textContent = "Ball Weight";
        ballsSlider.value = selected.default_balls || 4;
        ballsVal.textContent = ballsSlider.value;
        weightSlider.value = selected.default_ball_weight || 260;
        weightVal.textContent = `${weightSlider.value} g`;
      }
    }
    triggerRecalculate();
  });

  yeastSelect.addEventListener("change", triggerRecalculate);

  roomTempSlider.addEventListener("input", (e) => {
    roomTempVal.textContent = `${e.target.value}°F`;
    debounceRecalculate();
  });

  fridgeTempSlider.addEventListener("input", (e) => {
    fridgeTempVal.textContent = `${e.target.value}°F`;
    debounceRecalculate();
  });

  // Fermentation Mode Segments
  document.querySelectorAll(".segment-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".segment-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentFermentMode = btn.dataset.mode;
      triggerRecalculate();
    });
  });

  // Preset Buttons
  document.querySelectorAll(".preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".preset-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      hoursInput.value = btn.dataset.hours;
      const targetFerment = btn.dataset.ferment;

      document.querySelectorAll(".segment-btn").forEach(b => {
        b.classList.toggle("active", b.dataset.mode === targetFerment);
      });
      currentFermentMode = targetFerment;

      triggerRecalculate();
    });
  });

  // Print
  btnPrint.addEventListener("click", () => window.print());

  // Modal actions
  btnNewRecipe.addEventListener("click", () => openRecipeModal(null));
  btnEditRecipe.addEventListener("click", () => {
    const selected = recipesState.find(r => r.id === recipeSelect.value);
    openRecipeModal(selected);
  });
  modalClose.addEventListener("click", closeRecipeModal);
  btnCancelModal.addEventListener("click", closeRecipeModal);
  btnDeleteRecipe.addEventListener("click", handleDeleteRecipe);
  recipeForm.addEventListener("submit", handleSaveRecipe);
}

function updateActivePreset() {
  const currentHours = parseFloat(hoursInput.value);
  document.querySelectorAll(".preset-btn").forEach(btn => {
    btn.classList.toggle("active", parseFloat(btn.dataset.hours) === currentHours);
  });
}

let debounceTimer = null;
function debounceRecalculate() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(triggerRecalculate, 180);
}

async function loadRecipes() {
  let fetched = null;
  if (!isStaticHost && window.location.protocol.startsWith("http")) {
    try {
      const res = await fetch("/api/recipes");
      if (res.ok) fetched = await res.json();
    } catch (e) {
      console.warn("Could not reach API, using offline recipes:", e);
    }
  }

  if (fetched && fetched.length > 0) {
    recipesState = fetched;
  } else {
    // Load offline recipes + any saved in localStorage
    let stored = null;
    let customList = [];
    try {
      stored = localStorage.getItem("pizza_custom_recipes");
      if (stored) {
        customList = JSON.parse(stored);
      }
    } catch (e) {
      console.warn("localStorage not available:", e);
    }
    recipesState = [...customList, ...DEFAULT_RECIPES];
    // Deduplicate by ID
    const seen = new Set();
    recipesState = recipesState.filter(r => {
      if (seen.has(r.id)) return false;
      seen.add(r.id);
      return true;
    });
  }

  recipeSelect.innerHTML = "";
  recipesState.forEach(r => {
    const opt = document.createElement("option");
    opt.value = r.id;
    opt.textContent = `${r.name} ${r.is_custom ? '⭐ [Custom]' : ''}`;
    recipeSelect.appendChild(opt);
  });

  if (recipesState.length > 0) {
    // Default to adams_outdoor_base if present
    const adamsRecipe = recipesState.find(r => r.id === "adams_outdoor_base");
    const active = adamsRecipe || recipesState[0];
    recipeSelect.value = active.id;
    recipeDesc.textContent = `${active.description} • Flour: ${active.flour_type}`;
    ballsSlider.value = active.default_balls || 1;
    ballsVal.textContent = ballsSlider.value;
    weightSlider.value = active.default_ball_weight || 325;
    weightVal.textContent = `${weightSlider.value} g`;
  }
}

async function triggerRecalculate() {
  const recipe = recipesState.find(r => r.id === recipeSelect.value) || recipesState[0];
  const payload = {
    recipe_id: recipe.id,
    pan: selectedPanSize,
    balls: parseInt(ballsSlider.value, 10),
    ball_weight_g: parseFloat(weightSlider.value),
    hours: parseFloat(hoursInput.value),
    ferment_type: currentFermentMode,
    yeast_type: yeastSelect.value,
    room_temp_f: parseFloat(roomTempSlider.value),
    fridge_temp_f: parseFloat(fridgeTempSlider.value),
  };

  // Try API first if on HTTP and not on static host (e.g. GitHub Pages)
  if (!isStaticHost && window.location.protocol.startsWith("http")) {
    try {
      const res = await fetch("/api/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        currentPlan = await res.json();
        renderPlan(currentPlan);
        return;
      }
    } catch (err) {
      // Fallback to local JS calculation
    }
  }

  // Standalone Client-Side Calculation Engine (Works 100% Offline with zero server!)
  currentPlan = clientSideCalculate(recipe, payload);
  renderPlan(currentPlan);
}

// -------------------------------------------------------------
// STANDALONE OFFLINE ENGINE (Craig Kinetics + Baker's Formula)
// -------------------------------------------------------------
function clientSideCalculate(recipe, params) {
  const balls = params.balls || 1;
  const ballWeight = params.ball_weight_g || 325;
  const totalHours = params.hours || 24;
  const yeastType = params.yeast_type || "IDY";
  const roomTemp = params.room_temp_f || 70;
  const fridgeTemp = params.fridge_temp_f || 38;

  let ferment = params.ferment_type;
  if (ferment === "AUTO") {
    ferment = totalHours > 12 ? "CF" : "RT";
  }

  let rtHours = totalHours;
  let cfHours = 0;
  if (ferment === "CF") {
    rtHours = totalHours > 24 ? 4.5 : Math.min(6, Math.max(2.5, totalHours * 0.15));
    cfHours = Math.max(0, totalHours - rtHours);
  }

  // Temperature multipliers
  function getMultiplier(temp) {
    if (temp < 33) return 0.03;
    if (temp < 50) {
      const base50 = Math.pow(2.15, (50 - 68) / 18);
      const dormancy = Math.pow(Math.max(0.05, (temp - 32) / 18), 1.2);
      return Math.max(0.04, base50 * dormancy);
    }
    return Math.pow(2.15, (temp - 68) / 18);
  }

  const rtMult = getMultiplier(roomTemp);
  const cfMult = getMultiplier(fridgeTemp);
  const equivHours = Math.max(0.5, (rtHours * rtMult) + (cfHours * cfMult));

  // Craig's Regression
  const ratios = { IDY: 1.0, ADY: 1.33, CY: 3.0, SOURDOUGH: 20.0 };
  let yeastPct = 0.035;
  if (recipe.id === "adams_freezable" || (recipe.name && recipe.name.toLowerCase().includes("freez"))) {
    yeastPct = 1.25;
  } else if (yeastType === "SOURDOUGH") {
    yeastPct = Math.max(4, Math.min(25, 25 * Math.pow(equivHours, -0.45)));
  } else {
    const baseIDY = Math.max(0.015, Math.min(1.4, 2.42 * Math.pow(equivHours, -1.35)));
    yeastPct = baseIDY * (ratios[yeastType] || 1.0);
  }

  // Desired Dough Temp
  const friction = 2.0;
  const targetDDT = 76.0;
  const waterTemp = Math.round((3 * targetDDT) - roomTemp - roomTemp - friction);
  let waterDesc = "Warm / tepid water (~" + waterTemp + "°F) to wake up yeast.";
  if (waterTemp < 50) waterDesc = "Very cold tap / ice water (~" + waterTemp + "°F).";
  else if (waterTemp < 68) waterDesc = "Cool tap water (~" + waterTemp + "°F).";
  else if (waterTemp <= 82) waterDesc = "Room-temperature water (~" + waterTemp + "°F).";

  // Baker's Ingredients
  const totalWeight = balls * ballWeight;
  const sumPct = 1.0 + (recipe.hydration_pct / 100) + (recipe.salt_pct / 100) +
                 (recipe.oil_pct / 100) + (recipe.sugar_pct / 100) + (yeastPct / 100);

  const flourG = totalWeight / sumPct;
  const waterG = flourG * (recipe.hydration_pct / 100);
  const saltG = flourG * (recipe.salt_pct / 100);
  const yeastG = flourG * (yeastPct / 100);
  const oilG = flourG * (recipe.oil_pct / 100);
  const sugarG = flourG * (recipe.sugar_pct / 100);
  const yeastTsp = yeastG / (yeastType === "ADY" ? 2.85 : 3.15);

  // Timestamps
  const now = new Date();
  const ready = new Date(now.getTime() + totalHours * 3600 * 1000);

  function formatDate(d) {
    return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  }

  // Milestones Timeline
  const tStart = now;
  const tAutolyse = new Date(now.getTime() + 15 * 60 * 1000);
  const tKneadDone = new Date(now.getTime() + 35 * 60 * 1000);
  const availHours = Math.max(0.5, (ready.getTime() - tKneadDone.getTime()) / (3600 * 1000));

  const schedule = [];
  let step = 1;

  const isPanStyle = (recipe.id === "adams_detroit" || recipe.id === "detroit" || (recipe.name && recipe.name.toLowerCase().includes("detroit")) || (recipe.name && recipe.name.toLowerCase().includes("pan")));
  const isFreezable = (recipe.id === "adams_freezable" || (recipe.name && recipe.name.toLowerCase().includes("freez")));

  // Yeast Preparation Note for Step 1
  let yeastPrep = "";
  if (isFreezable) {
    yeastPrep = `Calibrate water to ~80-85°F. Whisk ${sugarG.toFixed(1)}g sugar and ${yeastG.toFixed(2)}g ${yeastType} yeast directly into warm water until dissolved to activate and jumpstart hydration.`;
  } else if (yeastType === "ADY") {
    yeastPrep = `Calibrate water to ${waterTemp}°F using the DDT formula. Bloom yeast: Take ~50g of calibrated warm water into a small cup, stir in ${yeastG.toFixed(2)}g Active Dry Yeast (ADY)` + (sugarG > 0 ? " with a pinch of sugar" : "") + `, and let sit 7-10 minutes until vigorously foamy before mixing.`;
  } else if (yeastType === "CY") {
    yeastPrep = `Calibrate water to ${waterTemp}°F using the DDT formula. Dissolve yeast: Crumble ${yeastG.toFixed(2)}g fresh cake yeast (CY) directly into calibrated water and stir until milky and completely dissolved.`;
  } else if (yeastType === "SOURDOUGH") {
    yeastPrep = `Calibrate water to ${waterTemp}°F using the DDT formula. Dissolve starter: Whisk ${yeastG.toFixed(1)}g active sourdough starter directly into calibrated water until aerated and milky.`;
  } else {
    yeastPrep = `Calibrate water to ${waterTemp}°F using the DDT formula. Dissolve yeast: Whisk ${yeastG.toFixed(2)}g Instant Dry Yeast (IDY) directly into calibrated water until fully dissolved and dispersed (or whisk thoroughly into dry flour).`;
  }

  // Step 1: Mise en Place
  schedule.push({
    step_num: step++,
    title: isFreezable ? "Mise en Place & Water Prep (Lukewarm ~85°F)" : (isPanStyle ? "Mise en Place, Water Prep & Detroit Pan Setup" : "Mise en Place & Water Temp Calibration"),
    action_category: "mix",
    display_time: formatDate(tStart),
    duration_str: "10-15 mins",
    temp_desc: `Target Water: ${waterTemp}°F`,
    instruction: `1. Weigh ${flourG.toFixed(1)}g flour (${recipe.flour_type}), ${waterG.toFixed(1)}g water, ${saltG.toFixed(1)}g fine sea salt, and ${yeastG.toFixed(2)}g ${yeastType} (${formatTeaspoon(yeastTsp)})`
      + (oilG > 0 ? `, plus ${oilG.toFixed(1)}g extra virgin olive oil.` : ".")
      + (sugarG > 0 ? ` Also weigh ${sugarG.toFixed(1)}g sugar.` : "")
      + `\n2. ${yeastPrep}`
      + (isPanStyle ? "\n3. Coat your Detroit style pan(s) (13x9, 14x10, or 8x10) generously with 1-2 tbsp olive oil across bottom and sides." : ""),
    visual_cue: isFreezable ? "Yeast and sugar dissolved in warm water; ingredients scaled." : (isPanStyle ? "Ingredients scaled; Detroit pan thoroughly coated in olive oil." : "Ingredients accurately weighed on a gram scale; yeast completely dissolved or bloomed in water."),
    pro_tip: isFreezable
      ? "Olive oil protects gluten cell walls against freezing damage; sugar promotes golden browning in 500°F home ovens!"
      : (isPanStyle
        ? "Olive oil in the blue steel pan is what fries the bottom crust to golden crispness! Never pour salt directly onto dry yeast—salt exerts osmotic shock."
        : "Always use a gram scale! Never pour salt directly onto dry yeast—salt draws moisture out of yeast cells via osmotic shock. Always dissolve yeast into calibrated water or flour before introducing salt.")
  });

  // Step 2: Autolyse & Knead
  let step2Phase1 = "";
  if (isFreezable) {
    step2Phase1 = `1. ADD YEAST-WATER TO FLOUR (Autolyse): Pour warm water with dissolved yeast and sugar into mixing bowl. Add all ${flourG.toFixed(1)}g flour. Mix 1-2 mins until a rough shaggy mass forms. Cover and rest 15-20 mins (Autolyse) to hydrate flour proteins.`;
  } else if (yeastType === "ADY") {
    step2Phase1 = `1. ADD YEAST & WATER TO FLOUR (Fermentolyse/Autolyse): Pour foamy bloomed ADY yeast mixture and remaining calibrated water into mixing bowl. Add all ${flourG.toFixed(1)}g flour. Mix 1-2 mins until rough shaggy mass forms. Cover and rest 15-20 mins to allow flour proteins to fully hydrate.`;
  } else {
    step2Phase1 = `1. ADD YEAST & WATER TO FLOUR (Fermentolyse/Autolyse): Pour calibrated water with dissolved ${yeastType} yeast into mixing bowl (or pour calibrated water over flour if yeast was pre-whisked into dry flour). Add all ${flourG.toFixed(1)}g flour. Mix 1-2 mins until rough shaggy mass forms. Cover and rest 15-20 mins to allow flour proteins to fully hydrate.`;
  }

  let step2Phase2 = `2. ADD SALT` + (sugarG > 0 && !isFreezable ? ` & SUGAR: Sprinkle ${saltG.toFixed(1)}g fine sea salt and ${sugarG.toFixed(1)}g sugar` : `: Sprinkle ${saltG.toFixed(1)}g fine sea salt`) + ` across rested dough. (Never add salt directly to dry yeast—salt exerts extreme osmotic pressure that damages yeast cells. Adding salt after the hydration rest protects yeast vitality and strengthens gluten formation).`;

  let step2Phase3 = (oilG > 0)
    ? `3. KNEAD & ADD OIL: Knead by hand or mixer on medium-low for 3-4 mins until dough begins pulling together. Drizzle in ${oilG.toFixed(1)}g olive oil in two small increments, continuing to knead until fully absorbed. Knead another 4-5 mins (total 7-9 mins hand / 5-6 mins mixer) until dough is silky smooth, elastic, and passes the windowpane test.`
    : `3. KNEAD: Knead by hand on clean counter or mixer on medium-low for 7-9 mins (5-6 mins mixer) until dough transitions from shaggy to silky smooth, elastic, and passes the windowpane test.`;

  schedule.push({
    step_num: step++,
    title: "Autolyse Rest & Gluten Development (Kneading)",
    action_category: "knead",
    display_time: formatDate(tAutolyse),
    duration_str: "20 mins",
    temp_desc: `Room Temp ~${roomTemp}°F`,
    instruction: `${step2Phase1}\n${step2Phase2}\n${step2Phase3}`,
    visual_cue: "The dough transitions from shaggy and sticky to smooth, supple, and satiny. Passes the 'windowpane test' (stretches thin enough to see light through without tearing).",
    pro_tip: isFreezable
      ? "Developing a full windowpane before freezing is critical so thawed dough has high elasticity and won't tear."
      : (oilG > 0
        ? "Adding yeast with water at the initial mix jumpstarts enzymatic starch breakdown (fermentolyse), while holding back salt and oil gives gluten chains uninterrupted time to bond. Adding oil at the end prevents fat from coating flour proteins prematurely!"
        : "Adding yeast with water at the initial mix jumpstarts enzymatic activity (fermentolyse), while delaying salt until after hydration ensures maximum yeast vitality and a lighter, airier crust structure.")
  });

  let tPreheat = null;
  let preheatMins = 45;

  if (isFreezable) {
    // FREEZING & THAWING PROCESS
    const tRest = tKneadDone;
    const tRestDone = new Date(tRest.getTime() + 15 * 60 * 1000);
    schedule.push({
      step_num: step++,
      title: `Bench Rest & Divide into ${balls} Portion${balls > 1 ? 's' : ''} (${ballWeight}g each)`,
      action_category: "ball",
      display_time: formatDate(tRest),
      duration_str: "15 mins",
      temp_desc: `Room Temp ~${roomTemp}°F`,
      instruction: `1. Cover dough mass with a damp towel or inverted bowl and rest 10-15 minutes on counter.\n2. Cut into ${balls} equal pieces using a bench scraper, each weighing ${ballWeight}g.`,
      visual_cue: "Relaxed dough cuts cleanly with bench scraper.",
      pro_tip: "A brief bench rest relaxes gluten for effortless portioning and rounding."
    });

    const tBall = tRestDone;
    const tBallDone = new Date(tBall.getTime() + 15 * 60 * 1000);
    schedule.push({
      step_num: step++,
      title: `Shape into ${balls} Taut, Smooth Dough Ball${balls > 1 ? 's' : ''}`,
      action_category: "ball",
      display_time: formatDate(tBall),
      duration_str: "15 mins",
      temp_desc: "Room Temp Bench",
      instruction: `1. Cup hand over each portion and rotate firmly against counter to form taut, smooth spherical balls.\n2. Pinch bottom seam shut.\n3. Rub each ball with a light film of olive oil on all sides.`,
      visual_cue: "Smooth, tight spheres with glossy surface and sealed bottom seams.",
      pro_tip: "Surface tension holds shape and prevents dough from flattening out in the freezer."
    });

    const tFreezeStart = tBallDone;
    const tFreezeDone = new Date(tFreezeStart.getTime() + 2.5 * 3600 * 1000);
    schedule.push({
      step_num: step++,
      title: "Flash Freeze on Baking Sheet (2-3 Hours @ 0°F)",
      action_category: "freeze",
      display_time: formatDate(tFreezeStart),
      duration_str: "2-3 hours",
      temp_desc: "Freezer ~0°F (Parchment Tray)",
      instruction: `1. Line a rimmed baking sheet with parchment paper.\n2. Arrange oiled dough balls spaced 2-3 inches apart.\n3. Place sheet uncovered in freezer at ~0°F for 2 to 3 hours until dough balls freeze solid to the core.`,
      visual_cue: "Dough balls are rock solid to the touch and hold shape completely when lifted.",
      pro_tip: "Flash freezing individually ensures balls will NEVER stick together when bagged together!"
    });

    const tBag = tFreezeDone;
    schedule.push({
      step_num: step++,
      title: "Airtight Storage in Freezer Bags (Up to 3 Months @ 0°F)",
      action_category: "freeze",
      display_time: formatDate(tBag),
      duration_str: "Up to 3 months",
      temp_desc: "Deep Freezer 0°F (Airtight Bags)",
      instruction: `1. Transfer frozen balls into heavy-duty Ziploc freezer bags or individual vacuum-seal bags.\n2. Squeeze out all residual air before sealing.\n3. Label bag with date and dough weight (${ballWeight}g). Store at 0°F for up to 3 months.`,
      visual_cue: "Sealed tight with zero air pockets. No ice crystals or frost inside.",
      pro_tip: "Removing all air prevents freezer burn and protects yeast viability."
    });

    const tThaw = new Date(ready.getTime() - 22.5 * 3600 * 1000);
    schedule.push({
      step_num: step++,
      title: "Overnight Refrigerator Thaw (18-24 Hours @ 38°F)",
      action_category: "cold_retard",
      display_time: formatDate(tThaw),
      duration_str: "18-24 hours",
      temp_desc: `Refrigerator ~${fridgeTemp}°F (Covered Container)`,
      instruction: `1. Night before pizza night: transfer frozen ball(s) from freezer into lightly oiled covered container in refrigerator.\n2. Dough thaws slowly with zero thermal shock, and yeast gently awakens.`,
      visual_cue: "Dough ball is fully thawed, cold, soft, and slightly relaxed.",
      pro_tip: "Slow overnight refrigerator thawing produces dramatically better texture and flavor than rapid counter thawing."
    });

    const tTemper = new Date(ready.getTime() - 2.5 * 3600 * 1000);
    schedule.push({
      step_num: step++,
      title: "Room Temperature Temper & Final Proof (2-3 Hours @ 70°F)",
      action_category: "temper",
      display_time: formatDate(tTemper),
      duration_str: "2-3 hours",
      temp_desc: `Room Temp ~${roomTemp}°F (Airtight)`,
      instruction: `1. Remove container from fridge 2-3 hours before bake time.\n2. Keep covered at room temp (~70°F). Dough will warm to 60-65°F and expand until pillowy and passes poke test.`,
      visual_cue: "Dough ball is warm, puffy, and pillowy. Poked gently, it springs back slowly.",
      pro_tip: "NEVER stretch cold dough! Room temp tempering allows gluten to relax for effortless stretching."
    });

    tPreheat = new Date(ready.getTime() - 45 * 60 * 1000);
  } else if (cfHours > 0 && availHours >= 6.0) {
    // COLD FERMENTATION SCHEDULE
    const bulkHours = Math.min(2.0, Math.max(0.75, rtHours * 0.35));
    const tBulkStart = tKneadDone;
    const tBulkEnd = new Date(tBulkStart.getTime() + bulkHours * 3600 * 1000);

    // Step 3: Bulk Ferment
    schedule.push({
      step_num: step++,
      title: "Bulk Fermentation (Initial Rise)",
      action_category: "bulk",
      display_time: formatDate(tBulkStart),
      duration_str: `${bulkHours.toFixed(1)} hours`,
      temp_desc: `Room Temp ~${roomTemp}°F (Covered)`,
      instruction: `Form into a smooth ball. Cover airtight and rest at room temperature for ${bulkHours.toFixed(1)} hours.`,
      visual_cue: "Volume increases by ~25-35% with delicate surface doming.",
      pro_tip: "Do not let dough double during bulk if you plan to cold ferment!"
    });

    // Step 4: Divide and Ball / Pan Placement
    const tBall = tBulkEnd;
    const tBallDone = new Date(tBall.getTime() + 15 * 60 * 1000);
    schedule.push({
      step_num: step++,
      title: isPanStyle ? `Portion Directly into ${balls} Oiled Detroit Pan${balls > 1 ? 's' : ''} (${ballWeight}g each)` : `Divide & Shape into ${balls} Ball${balls > 1 ? 's' : ''} (${ballWeight}g each)`,
      action_category: "ball",
      display_time: formatDate(tBall),
      duration_str: "15 mins",
      temp_desc: isPanStyle ? "Room Temp Pan Setup" : "Room Temp Bench",
      instruction: isPanStyle
        ? `1. Cut dough into ${balls} portion${balls > 1 ? 's' : ''} (${ballWeight}g each).\n2. Place dough mass directly into center of oiled Detroit pan; turn once to oil both sides.\n3. Gently dimple and spread outward toward corners with flat fingertips (it will shrink back—do not force it).`
        : `Portion into ${balls} pieces of ${ballWeight}g. Cup hand and roll tightly on counter to create taut surface tension. Pinch bottom seam shut.`,
      visual_cue: isPanStyle ? "Dough rests in oiled pan, lightly coated in olive oil." : "Taut, smooth spheres with tightly sealed bases.",
      pro_tip: isPanStyle ? "Never force cold/unrelaxed dough to corners; time and cold fermentation will relax it naturally." : "Surface tension traps CO₂ inside the dough for high, puffy cornicione rims!"
    });

    // Step 5: Cold Retardation
    let temperHours = isPanStyle ? Math.min(4.0, Math.max(2.5, rtHours * 0.70)) : Math.min(3.5, Math.max(1.5, rtHours * 0.65));
    let tTemperStart = new Date(ready.getTime() - temperHours * 3600 * 1000);
    if (tTemperStart.getTime() < tBallDone.getTime() + 3600 * 1000) {
      tTemperStart = new Date(tBallDone.getTime() + Math.max(0.5, (availHours - bulkHours - 0.25) * 0.5) * 3600 * 1000);
      temperHours = (ready.getTime() - tTemperStart.getTime()) / (3600 * 1000);
    }

    const tCfStart = tBallDone;
    const actualCfHours = Math.max(0.5, (tTemperStart.getTime() - tCfStart.getTime()) / (3600 * 1000));

    schedule.push({
      step_num: step++,
      title: isPanStyle ? `In-Pan Cold Fermentation (${actualCfHours.toFixed(1)}h / 2-3 Days)` : `Cold Retardation / Refrigerator Maturation (${actualCfHours.toFixed(1)}h)`,
      action_category: "cold_retard",
      display_time: formatDate(tCfStart),
      duration_str: `${actualCfHours.toFixed(1)} hours`,
      temp_desc: `Fridge ~${fridgeTemp}°F (Covered Pan)`,
      instruction: isPanStyle
        ? `Cover Detroit pan tightly with plastic wrap or LloydPan lid. Chill in refrigerator at ~${fridgeTemp}°F for ${actualCfHours.toFixed(1)}h (2-3 days). Flavor and extensible gluten develop in the pan.`
        : `Transfer sealed dough containers to refrigerator for ${actualCfHours.toFixed(1)} hours. Slow enzyme action develops deep complex flavor and micro-blisters.`,
      visual_cue: isPanStyle ? "Dough relaxes and creeps outward across pan bottom with micro-bubbles." : "Dough relaxes outward; delicate micro-blistering appears on the skin.",
      pro_tip: isPanStyle ? "2-3 days cold ferment in the pan creates incredible sourdough-like flavor and airy focaccia crumb." : "Cold fermentation builds the authentic airy crumb and charred leopard spotting!"
    });

    // Step 6: Tempering
    schedule.push({
      step_num: step++,
      title: isPanStyle ? `Room Temperature Temper & Final Pan Proof (${temperHours.toFixed(1)}h)` : "Room Temperature Tempering & Poke Test",
      action_category: "temper",
      display_time: formatDate(tTemperStart),
      duration_str: `${temperHours.toFixed(1)} hours`,
      temp_desc: `Room Temp ~${roomTemp}°F (Airtight)`,
      instruction: isPanStyle
        ? `1. Remove covered pan from fridge ${temperHours.toFixed(1)}h before bake.\n2. After 1 hour, use oiled fingertips to gently dimple dough into all 4 corners.\n3. Let rise covered until puffy and halfway up the sides (~1 to 1.5" deep).`
        : `Remove from fridge ${temperHours.toFixed(1)} hours before bake. Keep airtight! Internal temp must reach 60-65°F before stretching.`,
      visual_cue: isPanStyle ? "Dough completely fills pan to all 4 corners, jiggly and buoyant with air pockets." : "Dough feels soft and pillowy; fingertip poke springs back slowly.",
      pro_tip: isPanStyle ? "Handle gently during final proof to protect the delicate honeycomb air bubbles!" : "NEVER stretch cold dough! Cold gluten resists, snaps back, and produces dense gum-lines."
    });

    tPreheat = new Date(ready.getTime() - 45 * 60 * 1000);
    if (tPreheat.getTime() < tTemperStart.getTime()) {
      tPreheat = tTemperStart;
    }
  } else {
    // ROOM TEMPERATURE SCHEDULE
    const fermentAvailHours = Math.max(0.5, availHours - 0.25);
    const bulkHours = parseFloat((fermentAvailHours * 0.42).toFixed(2));
    const ballProofHours = parseFloat((fermentAvailHours - bulkHours).toFixed(2));

    const tBulkStart = tKneadDone;
    const tBulkEnd = new Date(tBulkStart.getTime() + bulkHours * 3600 * 1000);

    // Step 3: Bulk Ferment
    schedule.push({
      step_num: step++,
      title: "Bulk Fermentation (Initial Rise)",
      action_category: "bulk",
      display_time: formatDate(tBulkStart),
      duration_str: `${bulkHours.toFixed(1)} hours`,
      temp_desc: `Room Temp ~${roomTemp}°F (Covered)`,
      instruction: `Form dough into a tidy ball. Cover tightly and bulk ferment at room temperature (~${roomTemp}°F) for ${bulkHours.toFixed(1)} hours.`,
      visual_cue: "Dough expands noticeably in volume with soft, pillowy texture.",
      pro_tip: "Room temperature bulk starts flavor development and gives yeast an active start."
    });

    // Step 4: Divide and Ball
    const tBall = tBulkEnd;
    const tBallDone = new Date(tBall.getTime() + 15 * 60 * 1000);
    schedule.push({
      step_num: step++,
      title: isPanStyle ? `Portion Directly into ${balls} Oiled Detroit Pan${balls > 1 ? 's' : ''} (${ballWeight}g each)` : `Divide & Shape into ${balls} Ball${balls > 1 ? 's' : ''} (${ballWeight}g each)`,
      action_category: "ball",
      display_time: formatDate(tBall),
      duration_str: "15 mins",
      temp_desc: isPanStyle ? "Room Temp Pan Setup" : "Room Temp Bench",
      instruction: isPanStyle
        ? `Portion into ${balls} pans of ${ballWeight}g. Lightly coat in olive oil and dimple outward.`
        : `Portion into ${balls} pieces of ${ballWeight}g. Cup hand and roll tightly on counter to create taut surface tension. Pinch bottom seam shut.`,
      visual_cue: isPanStyle ? "Dough portioned in pan with olive oil." : "Taut, smooth spheres with tightly sealed bases.",
      pro_tip: "Surface tension traps CO₂ inside the dough for high, puffy cornicione rims!"
    });

    // Step 5: Ball Proof
    const tBallProofStart = tBallDone;
    schedule.push({
      step_num: step++,
      title: isPanStyle ? `Room Temperature Pan Proof (${ballProofHours.toFixed(1)} hours)` : `Room Temperature Ball Proof (${ballProofHours.toFixed(1)} hours)`,
      action_category: "temper",
      display_time: formatDate(tBallProofStart),
      duration_str: `${ballProofHours.toFixed(1)} hours`,
      temp_desc: `Room Temp ~${roomTemp}°F (Airtight)`,
      instruction: `Keep dough containers sealed at room temperature (~${roomTemp}°F) for ${ballProofHours.toFixed(1)} hours until fully expanded and relaxed.`,
      visual_cue: "Balls double in volume, spreading gently. Very soft, delicate, and pillowy to touch.",
      pro_tip: "Handle proofed balls with extreme gentleness using a flat bench scraper so you don't degas the rim."
    });

    preheatMins = Math.min(45, Math.max(15, Math.round(ballProofHours * 30)));
    tPreheat = new Date(ready.getTime() - preheatMins * 60 * 1000);
    if (tPreheat.getTime() < tBallProofStart.getTime()) {
      tPreheat = tBallProofStart;
    }
  }

  // Preheat
  schedule.push({
    step_num: step++,
    title: isPanStyle ? `Preheat Oven to ${recipe.bake_temp_f}°F (Lowest Rack Setup)` : `Preheat ${recipe.oven_type} to ${recipe.bake_temp_f}°F`,
    action_category: "preheat",
    display_time: formatDate(tPreheat),
    duration_str: `${preheatMins} mins`,
    temp_desc: `${recipe.bake_temp_f}°F Bottom Heat`,
    instruction: isPanStyle
      ? `Preheat oven to ${recipe.bake_temp_f}°F with pizza stone/steel on the LOWEST rack. Setting Detroit pan directly on steel fries the bottom crust in olive oil.`
      : `Preheat oven. Ensure stone floor reaches 800-850°F (outdoor) or saturate baking steel at 550°F for at least ${preheatMins} minutes.`,
    visual_cue: "Baking surface is screaming hot and fully heat-saturated.",
    pro_tip: isPanStyle ? "Bottom rack placement ensures crispy bottom without burning cheese." : "Verify floor temp with an infrared laser thermometer before launching."
  });

  // Bake
  schedule.push({
    step_num: step++,
    title: isPanStyle ? `Edge-to-Edge Cheese & Pan Bake (${recipe.bake_time_min})` : `Stretch, Top & Bake (${recipe.bake_time_min})`,
    action_category: "bake",
    display_time: formatDate(ready),
    duration_str: recipe.bake_time_min,
    temp_desc: `${recipe.bake_temp_f}°F`,
    instruction: isPanStyle
      ? `1. Top generously with Wisconsin brick cheese or whole milk mozzarella edge-to-edge, pressing cheese against pan sides.\n2. Bake ${recipe.bake_time_min} until caramelized frico cheese crown forms.\n3. Ladle warm sauce in 2 racing stripes, release with spatula, and slice!`
      : `1. Invert container gently onto a bed of semola rimacinata.\n2. Push air outward with fingertips into the rim.\n3. Stretch on knuckles to 12-14", top lightly, launch, and bake ${recipe.bake_time_min}!`,
    visual_cue: isPanStyle ? "Crisp mahogany frico cheese crown along all 4 edges; airy crumb." : "Puffy, charred leopard spots and melted bubbly cheese.",
    pro_tip: isPanStyle ? "Cheese against metal edge melts down side to form the iconic caramelized frico crust!" : "Less is more on toppings! Heavy toppings cause soggy centers."
  });

  return {
    recipe: recipe,
    ingredients: {
      flour_g: flourG,
      water_g: waterG,
      salt_g: saltG,
      yeast_g: yeastG,
      yeast_tsp: yeastTsp,
      yeast_pct: yeastPct,
      oil_g: oilG,
      sugar_g: sugarG,
      total_weight_g: totalWeight,
      balls: balls,
      ball_weight_g: ballWeight,
      water_temp_f: waterTemp
    },
    yeast_type: yeastType,
    total_hours: totalHours,
    ferment_type: ferment,
    room_temp_f: roomTemp,
    fridge_temp_f: fridgeTemp,
    rt_hours: rtHours,
    cf_hours: cfHours,
    desired_dough_temp_f: targetDDT,
    water_temp_recommendation: waterDesc,
    schedule: schedule
  };
}

function renderPlan(plan) {
  const ing = plan.ingredients;
  const r = plan.recipe;

  formulaMeta.textContent = `${ing.balls} dough ball${ing.balls > 1 ? 's' : ''} @ ${ing.ball_weight_g}g each (${r.name})`;
  totalWeightDisplay.textContent = `${Math.round(ing.total_weight_g).toLocaleString()} g`;

  ingredientsTbody.innerHTML = `
    <tr>
      <td><strong>Flour</strong> <div style="font-size:0.8rem;color:var(--text-dim);">${r.flour_type}</div></td>
      <td class="pct-cell">100.0%</td>
      <td class="text-right gram-cell">${ing.flour_g.toFixed(1)} g</td>
      <td class="text-right kitchen-cell">Base (100%)</td>
    </tr>
    <tr>
      <td><strong>Water</strong></td>
      <td class="pct-cell">${r.hydration_pct.toFixed(1)}%</td>
      <td class="text-right gram-cell">${ing.water_g.toFixed(1)} g</td>
      <td class="text-right kitchen-cell">${(ing.water_g / 236.6).toFixed(1)} cups</td>
    </tr>
    <tr>
      <td><strong>Fine Sea Salt</strong></td>
      <td class="pct-cell">${r.salt_pct.toFixed(1)}%</td>
      <td class="text-right gram-cell">${ing.salt_g.toFixed(1)} g</td>
      <td class="text-right kitchen-cell">${(ing.salt_g / 5.7).toFixed(1)} tsp</td>
    </tr>
    <tr style="background: rgba(231, 111, 81, 0.08);">
      <td><strong>Yeast (${plan.yeast_type})</strong></td>
      <td class="pct-cell" style="color:var(--accent-pizza); font-weight:700;">${ing.yeast_pct.toFixed(3)}%</td>
      <td class="text-right gram-cell" style="color:var(--accent-pizza); font-weight:700;">${ing.yeast_g.toFixed(2)} g</td>
      <td class="text-right kitchen-cell" style="color:var(--accent-pizza); font-weight:700;">${formatTeaspoon(ing.yeast_tsp)}</td>
    </tr>
    ${ing.oil_g > 0 ? `
    <tr>
      <td><strong>Extra Virgin Olive Oil</strong></td>
      <td class="pct-cell">${r.oil_pct.toFixed(1)}%</td>
      <td class="text-right gram-cell">${ing.oil_g.toFixed(1)} g</td>
      <td class="text-right kitchen-cell">${(ing.oil_g / 13.5).toFixed(1)} tbsp</td>
    </tr>` : ''}
    ${ing.sugar_g > 0 ? `
    <tr>
      <td><strong>Sugar / Diastatic Malt</strong></td>
      <td class="pct-cell">${r.sugar_pct.toFixed(1)}%</td>
      <td class="text-right gram-cell">${ing.sugar_g.toFixed(1)} g</td>
      <td class="text-right kitchen-cell">${(ing.sugar_g / 4.2).toFixed(1)} tsp</td>
    </tr>` : ''}
  `;

  ddtTemp.textContent = `${ing.water_temp_f}°F`;
  ddtDesc.textContent = `${plan.water_temp_recommendation} Target finished dough temp is ${plan.desired_dough_temp_f}°F.`;

  let kineticText = "";
  if (plan.cf_hours > 0) {
    kineticText = `Total time: ${plan.total_hours}h (${plan.rt_hours.toFixed(1)}h room temp @ ${plan.room_temp_f}°F + ${plan.cf_hours.toFixed(1)}h cold retard @ ${plan.fridge_temp_f}°F). Yeast is dynamically dialed to ${ing.yeast_g.toFixed(2)}g (${ing.yeast_pct.toFixed(3)}%) to allow enzymatic flavor development without over-proofing.`;
  } else {
    kineticText = `Direct Room Temperature ferment: ${plan.total_hours}h at ${plan.room_temp_f}°F. Yeast scaled to ${ing.yeast_g.toFixed(2)}g (${ing.yeast_pct.toFixed(3)}%) for optimal volume expansion and gluten relaxation.`;
  }
  kineticDesc.textContent = kineticText;

  scheduleSubtitle.textContent = `Chronological timeline for ${r.name} (${ing.balls} pizza${ing.balls > 1 ? 's' : ''}) • Total: ${plan.total_hours}h`;

  timelineSteps.innerHTML = "";
  plan.schedule.forEach(m => {
    const icon = actionIcons[m.action_category] || "📌";
    const card = document.createElement("div");
    card.className = "milestone-card";
    card.innerHTML = `
      <div class="milestone-header">
        <div class="milestone-title-row">
          <span class="milestone-icon">${icon}</span>
          <span class="milestone-title">Step ${m.step_num}: ${m.title}</span>
        </div>
        <div class="milestone-badges">
          <span class="badge-time">${m.display_time} (${m.duration_str})</span>
          <span class="badge-temp">${m.temp_desc}</span>
        </div>
      </div>
      <div class="milestone-instructions">${m.instruction}</div>
      <div class="milestone-callouts">
        <div class="cue-box">
          <strong>👁️ Visual Cue:</strong> ${m.visual_cue}
        </div>
        <div class="tip-box">
          <strong>💡 Pro Tip:</strong> ${m.pro_tip}
        </div>
      </div>
    `;
    timelineSteps.appendChild(card);
  });
}

function formatTeaspoon(tsp) {
  if (tsp < 0.08) return "< 1/8 tsp (tiny pinch)";
  if (tsp <= 0.18) return "1/8 tsp";
  if (tsp <= 0.35) return "1/4 tsp";
  if (tsp <= 0.60) return "1/2 tsp";
  if (tsp <= 0.85) return "3/4 tsp";
  if (tsp <= 1.15) return "1 tsp";
  if (tsp <= 1.4) return "1 1/4 tsp";
  if (tsp <= 1.65) return "1 1/2 tsp";
  if (tsp <= 2.2) return "2 tsp";
  return `${tsp.toFixed(1)} tsp`;
}

// Modal handling
function openRecipeModal(recipe) {
  recipeModal.classList.remove("hidden");
  if (recipe) {
    modalTitle.textContent = `Edit Base Recipe: ${recipe.name}`;
    document.getElementById("rec-id").value = recipe.id;
    document.getElementById("rec-id").readOnly = !recipe.is_custom;
    document.getElementById("rec-name").value = recipe.name;
    document.getElementById("rec-flour").value = recipe.flour_type || "";
    document.getElementById("rec-hyd").value = recipe.hydration_pct;
    document.getElementById("rec-salt").value = recipe.salt_pct;
    document.getElementById("rec-oil").value = recipe.oil_pct;
    document.getElementById("rec-sugar").value = recipe.sugar_pct;
    document.getElementById("rec-weight").value = recipe.default_ball_weight;
    document.getElementById("rec-balls").value = recipe.default_balls;
    document.getElementById("rec-oven").value = recipe.oven_type || "";
    document.getElementById("rec-temp").value = recipe.bake_temp_f || 550;
    document.getElementById("rec-notes").value = recipe.notes || "";

    btnDeleteRecipe.classList.toggle("hidden", !recipe.is_custom);
  } else {
    modalTitle.textContent = "Create Custom Base Recipe";
    document.getElementById("rec-id").value = "";
    document.getElementById("rec-id").readOnly = false;
    document.getElementById("rec-name").value = "";
    document.getElementById("rec-flour").value = "King Arthur Bread Flour or Tipo 00";
    document.getElementById("rec-hyd").value = "66.0";
    document.getElementById("rec-salt").value = "2.4";
    document.getElementById("rec-oil").value = "1.5";
    document.getElementById("rec-sugar").value = "1.0";
    document.getElementById("rec-weight").value = "260";
    document.getElementById("rec-balls").value = "4";
    document.getElementById("rec-oven").value = "Home Oven (550°F / Pizza Steel)";
    document.getElementById("rec-temp").value = "550";
    document.getElementById("rec-notes").value = "";
    btnDeleteRecipe.classList.add("hidden");
  }
}

function closeRecipeModal() {
  recipeModal.classList.add("hidden");
}

async function handleSaveRecipe(e) {
  e.preventDefault();
  const id = document.getElementById("rec-id").value.trim().toLowerCase().replace(/\s+/g, "_");
  const payload = {
    id: id,
    name: document.getElementById("rec-name").value.trim(),
    flour_type: document.getElementById("rec-flour").value.trim(),
    hydration_pct: parseFloat(document.getElementById("rec-hyd").value),
    salt_pct: parseFloat(document.getElementById("rec-salt").value),
    oil_pct: parseFloat(document.getElementById("rec-oil").value) || 0,
    sugar_pct: parseFloat(document.getElementById("rec-sugar").value) || 0,
    default_ball_weight: parseFloat(document.getElementById("rec-weight").value) || 260,
    default_balls: parseInt(document.getElementById("rec-balls").value, 10) || 4,
    oven_type: document.getElementById("rec-oven").value.trim(),
    bake_temp_f: parseInt(document.getElementById("rec-temp").value, 10) || 550,
    notes: document.getElementById("rec-notes").value.trim(),
    is_custom: true
  };

  // Try API first
  if (!isStaticHost && window.location.protocol.startsWith("http")) {
    try {
      const res = await fetch("/api/recipes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        closeRecipeModal();
        await loadRecipes();
        recipeSelect.value = id;
        triggerRecalculate();
        return;
      }
    } catch (e) {}
  }

  // Save to localStorage for standalone offline mode
  try {
    let stored = JSON.parse(localStorage.getItem("pizza_custom_recipes") || "[]");
    const idx = stored.findIndex(r => r.id === id);
    if (idx >= 0) stored[idx] = payload;
    else stored.unshift(payload);
    localStorage.setItem("pizza_custom_recipes", JSON.stringify(stored));
  } catch (e) {
    console.warn("Could not save to localStorage:", e);
  }

  closeRecipeModal();
  await loadRecipes();
  recipeSelect.value = id;
  triggerRecalculate();
}

async function handleDeleteRecipe() {
  const id = document.getElementById("rec-id").value;
  if (!confirm(`Are you sure you want to delete custom recipe '${id}'?`)) return;

  if (!isStaticHost && window.location.protocol.startsWith("http")) {
    try {
      const res = await fetch(`/api/recipes/${id}`, { method: "DELETE" });
      if (res.ok) {
        closeRecipeModal();
        await loadRecipes();
        triggerRecalculate();
        return;
      }
    } catch (e) {}
  }

  // Remove from localStorage
  try {
    let stored = JSON.parse(localStorage.getItem("pizza_custom_recipes") || "[]");
    stored = stored.filter(r => r.id !== id);
    localStorage.setItem("pizza_custom_recipes", JSON.stringify(stored));
  } catch (e) {
    console.warn("Could not remove from localStorage:", e);
  }

  closeRecipeModal();
  await loadRecipes();
  triggerRecalculate();
}
