"""Data models for Pizza Dough Artisan Agent."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any


# Standard Pan Sizing for Detroit / Sicilian Pan Styles
PAN_SIZES = {
    "13x9": {
        "id": "13x9",
        "name": '13" × 9" Pan (Standard Detroit)',
        "length_in": 13.0,
        "width_in": 9.0,
        "area_sq_in": 117.0,
        "dough_weight_g": 643.0,  # 350g flour, 260g water, 10g salt, 20g oil, 3g yeast
        "flour_g": 350.0,
        "water_g": 260.0,
        "salt_g": 10.0,
        "oil_g": 20.0,
        "yeast_g": 3.0,
        "yeast_pct": 0.857,
    },
    "14x10": {
        "id": "14x10",
        "name": '14" × 10" Pan (Large Detroit)',
        "length_in": 14.0,
        "width_in": 10.0,
        "area_sq_in": 140.0,
        "dough_weight_g": 770.0,  # 140/117 * 643 = ~769.4g
        "flour_g": 419.0,
        "water_g": 311.0,
        "salt_g": 12.0,
        "oil_g": 24.0,
        "yeast_g": 3.6,
        "yeast_pct": 0.857,
    },
    "8x10": {
        "id": "8x10",
        "name": '8" × 10" Pan (Small / Half Detroit)',
        "length_in": 10.0,
        "width_in": 8.0,
        "area_sq_in": 80.0,
        "dough_weight_g": 440.0,  # 80/117 * 643 = ~439.7g
        "flour_g": 239.0,
        "water_g": 178.0,
        "salt_g": 6.8,
        "oil_g": 13.7,
        "yeast_g": 2.1,
        "yeast_pct": 0.857,
    },
}


@dataclass
class Recipe:
    id: str
    name: str
    description: str
    flour_type: str
    hydration_pct: float          # e.g. 65.0 for 65%
    salt_pct: float               # e.g. 2.5 for 2.5%
    oil_pct: float = 0.0          # e.g. 2.0 for 2.0%
    sugar_pct: float = 0.0        # e.g. 1.5 for 1.5%
    default_ball_weight: float = 260.0  # grams per ball
    default_balls: int = 4
    oven_type: str = "Home Oven (500-550°F / Pizza Steel)"
    bake_temp_f: int = 550
    bake_time_min: str = "5-7 minutes"
    recommended_ferment: str = "CF"  # 'CF' (Cold Ferment) or 'RT' (Room Temp)
    notes: str = ""
    is_custom: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Recipe":
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "Custom Recipe")),
            description=str(data.get("description", "")),
            flour_type=str(data.get("flour_type", "Bread Flour or Tipo 00")),
            hydration_pct=float(data.get("hydration_pct", 65.0)),
            salt_pct=float(data.get("salt_pct", 2.5)),
            oil_pct=float(data.get("oil_pct", 0.0)),
            sugar_pct=float(data.get("sugar_pct", 0.0)),
            default_ball_weight=float(data.get("default_ball_weight", 260.0)),
            default_balls=int(data.get("default_balls", 4)),
            oven_type=str(data.get("oven_type", "Home Oven")),
            bake_temp_f=int(data.get("bake_temp_f", 550)),
            bake_time_min=str(data.get("bake_time_min", "5-7 minutes")),
            recommended_ferment=str(data.get("recommended_ferment", "CF")),
            notes=str(data.get("notes", "")),
            is_custom=bool(data.get("is_custom", False)),
        )


@dataclass
class IngredientBreakdown:
    flour_g: float
    water_g: float
    salt_g: float
    yeast_g: float
    yeast_tsp: float
    yeast_pct: float
    oil_g: float
    sugar_g: float
    total_weight_g: float
    balls: int
    ball_weight_g: float
    water_temp_f: float
    yeast_type: str = "Instant Dry Yeast (IDY)"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProofingMilestone:
    step_num: int
    title: str
    action_category: str          # 'mix', 'knead', 'bulk', 'ball', 'cold_retard', 'temper', 'preheat', 'bake'
    timestamp_iso: str
    display_time: str
    duration_str: str
    temp_desc: str
    instruction: str
    visual_cue: str
    pro_tip: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DoughPlan:
    recipe: Recipe
    ingredients: IngredientBreakdown
    yeast_type: str               # 'IDY', 'ADY', 'CY', 'SOURDOUGH'
    mix_time_iso: str
    ready_time_iso: str
    total_hours: float
    ferment_type: str             # 'CF', 'RT', 'HYBRID'
    room_temp_f: float
    fridge_temp_f: float
    rt_hours: float
    cf_hours: float
    schedule: List[ProofingMilestone]
    desired_dough_temp_f: float = 76.0
    water_temp_recommendation: str = ""
    summary_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recipe": self.recipe.to_dict(),
            "ingredients": self.ingredients.to_dict(),
            "yeast_type": self.yeast_type,
            "mix_time_iso": self.mix_time_iso,
            "ready_time_iso": self.ready_time_iso,
            "total_hours": round(self.total_hours, 1),
            "ferment_type": self.ferment_type,
            "room_temp_f": self.room_temp_f,
            "fridge_temp_f": self.fridge_temp_f,
            "rt_hours": round(self.rt_hours, 1),
            "cf_hours": round(self.cf_hours, 1),
            "desired_dough_temp_f": self.desired_dough_temp_f,
            "water_temp_recommendation": self.water_temp_recommendation,
            "summary_text": self.summary_text,
            "schedule": [m.to_dict() for m in self.schedule],
        }
