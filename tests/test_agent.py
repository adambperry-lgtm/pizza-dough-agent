"""Unit tests for Pizza Dough Artisan Agent."""

import unittest
from datetime import datetime, timedelta
import tempfile
from pathlib import Path
from pizza_agent.models import Recipe
from pizza_agent.database import Database
from pizza_agent.yeast_engine import (
    calculate_yeast_percentage,
    calculate_ingredients_breakdown,
    calculate_desired_dough_water_temp,
    calculate_temperature_rate_multiplier,
)
from pizza_agent.proofing import generate_proofing_schedule
from pizza_agent.agent import PizzaDoughAgent


class TestPizzaDoughAgent(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_dough.db"
        self.db = Database(self.db_path)
        self.agent = PizzaDoughAgent(self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_temperature_multiplier(self):
        # 68°F is baseline -> multiplier = 1.0
        m_base = calculate_temperature_rate_multiplier(68.0)
        self.assertAlmostEqual(m_base, 1.0, places=2)

        # 77°F should be faster (> 1.0)
        m_warm = calculate_temperature_rate_multiplier(77.0)
        self.assertGreater(m_warm, 1.3)

        # 38°F (refrigerator) should be much slower (~0.12)
        m_cold = calculate_temperature_rate_multiplier(38.0)
        self.assertLess(m_cold, 0.25)
        self.assertGreater(m_cold, 0.05)

    def test_yeast_scaling_with_time(self):
        # RT scaling: 4h room temp requires significantly more yeast than 24h room temp
        y_4h_rt, _, _, _ = calculate_yeast_percentage(total_hours=4.0, ferment_type="RT", yeast_type="IDY")
        y_24h_rt, _, _, _ = calculate_yeast_percentage(total_hours=24.0, ferment_type="RT", yeast_type="IDY")
        self.assertGreater(y_4h_rt, y_24h_rt)
        self.assertGreater(y_4h_rt, 0.25)
        self.assertLess(y_24h_rt, 0.05)

        # CF scaling: 24h cold ferment requires more yeast than 48h or 72h cold ferment
        y_24h_cf, _, _, _ = calculate_yeast_percentage(total_hours=24.0, ferment_type="CF", yeast_type="IDY")
        y_48h_cf, _, _, _ = calculate_yeast_percentage(total_hours=48.0, ferment_type="CF", yeast_type="IDY")
        y_72h_cf, _, _, _ = calculate_yeast_percentage(total_hours=72.0, ferment_type="CF", yeast_type="IDY")
        self.assertGreater(y_24h_cf, y_48h_cf)
        self.assertGreater(y_48h_cf, y_72h_cf)
        self.assertLess(y_72h_cf, 0.10)

    def test_ddt_water_temp(self):
        # Desired Dough Temp = 76°F, Room = 70°F, Flour = 70°F, Hand knead (1°F)
        # Water = (3 * 76) - 70 - 70 - 1 = 228 - 141 = 87°F
        w_temp, desc = calculate_desired_dough_water_temp(
            desired_dough_temp_f=76.0, room_temp_f=70.0, flour_temp_f=70.0, knead_type="hand"
        )
        self.assertEqual(w_temp, 87.0)
        self.assertIn("Warm", desc)

    def test_bakers_percentages_calculation(self):
        recipe = self.db.get_recipe("ny_style")
        ing = calculate_ingredients_breakdown(
            recipe=recipe,
            balls=4,
            ball_weight_g=250.0,  # 1000g total
            yeast_pct=0.1,
            yeast_type="IDY",
        )
        # Sum of ingredients should equal exactly total_dough_g (1000g)
        calc_total = ing.flour_g + ing.water_g + ing.salt_g + ing.yeast_g + ing.oil_g + ing.sugar_g
        self.assertAlmostEqual(calc_total, 1000.0, places=0)
        # Check hydration ratio
        self.assertAlmostEqual(ing.water_g / ing.flour_g, 0.65, places=2)

    def test_recipe_database_crud(self):
        # Add custom recipe
        custom = Recipe(
            id="adams_thin_crust",
            name="Adam's Thin & Crispy",
            description="Crispy tavern style crust",
            flour_type="All-Purpose",
            hydration_pct=58.0,
            salt_pct=2.5,
            oil_pct=3.0,
            sugar_pct=0.0,
            default_ball_weight=220.0,
            default_balls=4,
            is_custom=True,
        )
        self.db.save_recipe(custom)

        # Retrieve
        fetched = self.db.get_recipe("adams_thin_crust")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Adam's Thin & Crispy")
        self.assertEqual(fetched.hydration_pct, 58.0)

        # Delete
        deleted = self.db.delete_recipe("adams_thin_crust")
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get_recipe("adams_thin_crust"))

    def test_natural_language_parser(self):
        plan = self.agent.parse_natural_language_request(
            "I want 3 Neapolitan dough balls of 250g each for tomorrow night"
        )
        self.assertEqual(plan.recipe.id, "neapolitan")
        self.assertEqual(plan.ingredients.balls, 3)
        self.assertEqual(plan.ingredients.ball_weight_g, 250.0)
        self.assertGreater(len(plan.schedule), 5)


if __name__ == "__main__":
    unittest.main()
