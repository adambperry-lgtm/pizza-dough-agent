"""SQLite Database storage for base recipes, dough plans, and user preferences."""

import sqlite3
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from .models import Recipe

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "dough.db"

SEED_RECIPES = [
    Recipe(
        id="ny_style",
        name="Classic New York Style",
        description="Authentic NYC pizzeria slice: crispy bottom, chewy foldable rim, golden leopard blisters.",
        flour_type="High-Gluten or Bread Flour (12.7% - 14% protein, e.g. King Arthur Bread or All Trumps)",
        hydration_pct=65.0,
        salt_pct=2.3,
        oil_pct=2.0,
        sugar_pct=1.5,
        default_ball_weight=265.0,  # 12-14 inch pie
        default_balls=4,
        oven_type="Home Oven (500-550°F on Pizza Steel / Stone)",
        bake_temp_f=550,
        bake_time_min="6-8 minutes",
        recommended_ferment="CF",
        notes="Sugar aids browning in home ovens below 700°F. Oil gives tenderness and stretch to the crumb.",
        is_custom=False
    ),
    Recipe(
        id="neapolitan",
        name="Neapolitan Vera Pizza (AVPN)",
        description="Traditional wood-fired style: pillowy cloud-like cornicione, tender melt-in-the-mouth texture.",
        flour_type="Tipo 00 Italian Flour (e.g. Caputo Pizzeria or Caputo Chef)",
        hydration_pct=62.0,
        salt_pct=2.8,
        oil_pct=0.0,
        sugar_pct=0.0,
        default_ball_weight=250.0,  # 11-12 inch pie
        default_balls=4,
        oven_type="High-Heat Outdoor Pizza Oven (Ooni / Gozney / Roccbox at 850-950°F)",
        bake_temp_f=900,
        bake_time_min="60-90 seconds",
        recommended_ferment="RT",
        notes="Zero oil or sugar required. The intense 900°F heat creates rapid oven spring and dark leopard spots without sugar.",
        is_custom=False
    ),
    Recipe(
        id="detroit",
        name="Detroit Style Pan Pizza",
        description="Airy focaccia-like crumb with caramelized cheesy frico crust around blue steel pan edges.",
        flour_type="Bread Flour (e.g. King Arthur Bread Flour)",
        hydration_pct=73.0,
        salt_pct=2.2,
        oil_pct=2.5,
        sugar_pct=1.0,
        default_ball_weight=420.0,  # 10x14 LloydPan
        default_balls=2,
        oven_type="Home Oven (450-500°F in 10x14 LloydPans blue steel)",
        bake_temp_f=475,
        bake_time_min="13-16 minutes",
        recommended_ferment="CF",
        notes="Spread Wisconsin brick cheese or low-moisture mozzarella all the way to the pan edges for iconic crunchy caramelized corners.",
        is_custom=False
    ),
    Recipe(
        id="same_day_quick",
        name="Same-Day Express Dough (3-5 Hours)",
        description="Fast turnaround dough when you decide to make pizza for dinner tonight.",
        flour_type="Bread Flour or All-Purpose Flour",
        hydration_pct=64.0,
        salt_pct=2.2,
        oil_pct=2.0,
        sugar_pct=1.5,
        default_ball_weight=260.0,
        default_balls=3,
        oven_type="Home Oven (500-550°F on Steel)",
        bake_temp_f=550,
        bake_time_min="6-8 minutes",
        recommended_ferment="RT",
        notes="Uses higher yeast inoculation and slightly warm water (~85°F) for rapid 3-4 hour turnaround.",
        is_custom=False
    ),
    Recipe(
        id="roman_pinsa",
        name="Roman Pizza al Taglio / Pinsa",
        description="Ultra-high hydration, cloud-like airy crumb with an ultra-crisp shattered glass bottom.",
        flour_type="Strong High-Protein Bread Flour + 10% Rice Flour / Semolina",
        hydration_pct=78.0,
        salt_pct=2.5,
        oil_pct=3.0,
        sugar_pct=0.0,
        default_ball_weight=500.0,  # Baking sheet / tray
        default_balls=2,
        oven_type="Home Oven (500°F on Baking Sheet or Steel)",
        bake_temp_f=500,
        bake_time_min="10-14 minutes",
        recommended_ferment="CF",
        notes="High hydration requires coil folds and at least 48h cold fermentation for honeycomb open crumb.",
        is_custom=False
    ),
    Recipe(
        id="sourdough_artisan",
        name="Artisan Naturally Leavened Sourdough",
        description="Pure wild yeast sourdough crust: complex lactic tang, blistered charred bubbles, supreme digestibility.",
        flour_type="Bread Flour + 10% Whole Wheat or Spelt",
        hydration_pct=66.0,
        salt_pct=2.4,
        oil_pct=1.5,
        sugar_pct=0.0,
        default_ball_weight=265.0,
        default_balls=4,
        oven_type="Home Oven (550°F) or Outdoor High Heat",
        bake_temp_f=550,
        bake_time_min="6-8 minutes",
        recommended_ferment="CF",
        notes="Inoculated with active mature 100% hydration levain. 24-48h cold retard creates exquisite aroma.",
        is_custom=False
    ),
    Recipe(
        id="adams_outdoor_base",
        name="Adam's High-Heat Outdoor Dough",
        description="Base recipe: 200g 00 flour, 3g salt, ~62% hydration for high-heat outdoor oven.",
        flour_type="Tipo 00 Italian Flour",
        hydration_pct=62.0,
        salt_pct=1.5,
        oil_pct=0.0,
        sugar_pct=0.0,
        default_ball_weight=325.0,
        default_balls=1,
        oven_type="High-Heat Outdoor Pizza Oven (Ooni / Roccbox / Gozney at 850-950°F)",
        bake_temp_f=900,
        bake_time_min="60-90 seconds",
        recommended_ferment="CF",
        notes="00 flour with 62% hydration, 1.5% salt, 0% oil, 0% sugar. Designed for intense 850-950°F stone temperatures.",
        is_custom=True
    ),
    Recipe(
        id="adams_detroit",
        name="Adam's Detroit Style Pan Pizza",
        description="Authentic Detroit pan pizza: 74.3% hydration, 2.86% salt, 5.71% EVOO. 2-3 day in-pan cold ferment for 13x9, 14x10, or 8x10 pans.",
        flour_type="Bread Flour (e.g. King Arthur Bread Flour)",
        hydration_pct=74.3,
        salt_pct=2.86,
        oil_pct=5.71,
        sugar_pct=0.0,
        default_ball_weight=643.0,
        default_balls=1,
        oven_type="Home Oven (475-500°F in Detroit Blue Steel or LloydPan)",
        bake_temp_f=485,
        bake_time_min="14-16 minutes",
        recommended_ferment="CF",
        notes="Calibrated for Detroit pans: 13x9 (643g dough / 350g flour), 14x10 (770g dough / 420g flour), and 8x10 (440g dough / 240g flour). Cold ferment 48-72h (2-3 days) directly in the well-oiled pan. Bring to room temp 3-4 hours before baking, dimpling to corners, top cheese edge-to-edge for crispy frico crust.",
        is_custom=True
    )
]


class Database:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Recipes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    flour_type TEXT,
                    hydration_pct REAL NOT NULL,
                    salt_pct REAL NOT NULL,
                    oil_pct REAL DEFAULT 0.0,
                    sugar_pct REAL DEFAULT 0.0,
                    default_ball_weight REAL DEFAULT 260.0,
                    default_balls INTEGER DEFAULT 4,
                    oven_type TEXT,
                    bake_temp_f INTEGER DEFAULT 550,
                    bake_time_min TEXT,
                    recommended_ferment TEXT DEFAULT 'CF',
                    notes TEXT,
                    is_custom INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Dough logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dough_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id TEXT,
                    recipe_name TEXT,
                    balls INTEGER,
                    ball_weight_g REAL,
                    flour_g REAL,
                    water_g REAL,
                    salt_g REAL,
                    yeast_g REAL,
                    yeast_type TEXT,
                    yeast_pct REAL,
                    oil_g REAL,
                    sugar_g REAL,
                    total_hours REAL,
                    ferment_type TEXT,
                    mix_time TEXT,
                    ready_time TEXT,
                    room_temp_f REAL,
                    fridge_temp_f REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # User preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.commit()

        # Seed initial recipes if empty
        self._seed_recipes_if_needed()

    def _seed_recipes_if_needed(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for r in SEED_RECIPES:
                cursor.execute("SELECT id FROM recipes WHERE id = ?", (r.id,))
                if not cursor.fetchone():
                    self.save_recipe(r, overwrite=False)

    def list_recipes(self) -> List[Recipe]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes ORDER BY is_custom ASC, name ASC")
            rows = cursor.fetchall()
            return [Recipe.from_dict(dict(row)) for row in rows]

    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes WHERE id = ? COLLATE NOCASE OR name = ? COLLATE NOCASE", (recipe_id, recipe_id))
            row = cursor.fetchone()
            if row:
                return Recipe.from_dict(dict(row))
            # Fallback prefix / fuzzy match
            cursor.execute("SELECT * FROM recipes WHERE id LIKE ? OR name LIKE ? LIMIT 1", (f"%{recipe_id}%", f"%{recipe_id}%"))
            row = cursor.fetchone()
            if row:
                return Recipe.from_dict(dict(row))
            return None

    def save_recipe(self, recipe: Recipe, overwrite: bool = True) -> Recipe:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO recipes (
                    id, name, description, flour_type, hydration_pct, salt_pct,
                    oil_pct, sugar_pct, default_ball_weight, default_balls,
                    oven_type, bake_temp_f, bake_time_min, recommended_ferment,
                    notes, is_custom, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    description=excluded.description,
                    flour_type=excluded.flour_type,
                    hydration_pct=excluded.hydration_pct,
                    salt_pct=excluded.salt_pct,
                    oil_pct=excluded.oil_pct,
                    sugar_pct=excluded.sugar_pct,
                    default_ball_weight=excluded.default_ball_weight,
                    default_balls=excluded.default_balls,
                    oven_type=excluded.oven_type,
                    bake_temp_f=excluded.bake_temp_f,
                    bake_time_min=excluded.bake_time_min,
                    recommended_ferment=excluded.recommended_ferment,
                    notes=excluded.notes,
                    is_custom=excluded.is_custom,
                    updated_at=CURRENT_TIMESTAMP
            """, (
                recipe.id, recipe.name, recipe.description, recipe.flour_type,
                recipe.hydration_pct, recipe.salt_pct, recipe.oil_pct, recipe.sugar_pct,
                recipe.default_ball_weight, recipe.default_balls, recipe.oven_type,
                recipe.bake_temp_f, recipe.bake_time_min, recipe.recommended_ferment,
                recipe.notes, 1 if recipe.is_custom else 0
            ))
            conn.commit()
            return recipe

    def delete_recipe(self, recipe_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipes WHERE id = ? AND is_custom = 1", (recipe_id,))
            conn.commit()
            return cursor.rowcount > 0

    def log_plan(self, plan_data: Dict[str, Any]) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            ing = plan_data.get("ingredients", {})
            cursor.execute("""
                INSERT INTO dough_plans (
                    recipe_id, recipe_name, balls, ball_weight_g, flour_g,
                    water_g, salt_g, yeast_g, yeast_type, yeast_pct,
                    oil_g, sugar_g, total_hours, ferment_type, mix_time,
                    ready_time, room_temp_f, fridge_temp_f, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan_data.get("recipe", {}).get("id"),
                plan_data.get("recipe", {}).get("name"),
                ing.get("balls"),
                ing.get("ball_weight_g"),
                ing.get("flour_g"),
                ing.get("water_g"),
                ing.get("salt_g"),
                ing.get("yeast_g"),
                plan_data.get("yeast_type"),
                ing.get("yeast_pct"),
                ing.get("oil_g"),
                ing.get("sugar_g"),
                plan_data.get("total_hours"),
                plan_data.get("ferment_type"),
                plan_data.get("mix_time_iso"),
                plan_data.get("ready_time_iso"),
                plan_data.get("room_temp_f"),
                plan_data.get("fridge_temp_f"),
                plan_data.get("notes", "")
            ))
            conn.commit()
            return cursor.lastrowid

    def list_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dough_plans ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]
