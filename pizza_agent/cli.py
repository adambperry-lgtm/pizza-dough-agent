"""Command-line interface for Pizza Dough Artisan Agent."""

import argparse
import sys
import json
from datetime import datetime
from typing import Optional
from .agent import PizzaDoughAgent
from .database import Database
from .models import Recipe
from .yeast_engine import format_tsp_fraction


def format_plan_terminal(plan) -> str:
    """Formats a DoughPlan into an aesthetically pleasing terminal layout with ASCII tables."""
    lines = []
    r = plan.recipe
    ing = plan.ingredients

    lines.append("=" * 78)
    lines.append(f"  🍕 PIZZA DOUGH ARTISAN AGENT: {r.name.upper()}")
    lines.append("=" * 78)
    lines.append(f"  Description : {r.description}")
    lines.append(f"  Flour Rec   : {r.flour_type}")
    lines.append(f"  Oven Setup  : {r.oven_type} ({r.bake_temp_f}°F, {r.bake_time_min})")
    lines.append("-" * 78)

    # Overview box
    lines.append("  🕒 TIMING & FERMENTATION PROFILE:")
    lines.append(f"    • Mixing Started     : {plan.mix_time_iso.replace('T', ' ')}")
    lines.append(f"    • Target Ready/Bake  : {plan.ready_time_iso.replace('T', ' ')}")
    lines.append(f"    • Total Duration     : {round(plan.total_hours, 1)} hours ({plan.ferment_type} profile)")
    if plan.cf_hours > 0:
        lines.append(f"      - Room Temp Phases : {round(plan.rt_hours, 1)} hours at {plan.room_temp_f}°F")
        lines.append(f"      - Refrigerator Retard: {round(plan.cf_hours, 1)} hours at {plan.fridge_temp_f}°F")
    else:
        lines.append(f"      - Direct Room Temp : {round(plan.rt_hours, 1)} hours at {plan.room_temp_f}°F")
    lines.append("-" * 78)

    # Ingredients Table
    lines.append(f"  ⚖️ BAKER'S INGREDIENT FORMULA ({ing.balls} balls @ {ing.ball_weight_g}g = {ing.total_weight_g}g total):")
    lines.append("  ┌────────────────────────────────────┬──────────────┬───────────────┐")
    lines.append("  │ Ingredient                         │ Baker's %    │ Grams (Scale) │")
    lines.append("  ├────────────────────────────────────┼──────────────┼───────────────┤")
    lines.append(f"  │ Flour ({r.flour_type[:24]:<24}) │ 100.0%       │ {ing.flour_g:>8.1f} g  │")
    lines.append(f"  │ Water                              │ {r.hydration_pct:>5.1f}%       │ {ing.water_g:>8.1f} g  │")
    lines.append(f"  │ Fine Sea Salt                      │ {r.salt_pct:>5.1f}%       │ {ing.salt_g:>8.1f} g  │")

    yeast_name = f"{plan.yeast_type} ({format_tsp_fraction(ing.yeast_tsp)})"
    lines.append(f"  │ Yeast: {yeast_name[:27]:<27} │ {ing.yeast_pct:>5.3f}%      │ {ing.yeast_g:>8.2f} g  │")

    if ing.oil_g > 0:
        lines.append(f"  │ Extra Virgin Olive Oil             │ {r.oil_pct:>5.1f}%       │ {ing.oil_g:>8.1f} g  │")
    if ing.sugar_g > 0:
        lines.append(f"  │ Sugar / Diastatic Malt             │ {r.sugar_pct:>5.1f}%       │ {ing.sugar_g:>8.1f} g  │")

    lines.append("  ├────────────────────────────────────┼──────────────┼───────────────┤")
    lines.append(f"  │ TOTAL DOUGH WEIGHT                 │              │ {ing.total_weight_g:>8.1f} g  │")
    lines.append("  └────────────────────────────────────┴──────────────┴───────────────┘")
    lines.append(f"  💧 Water Temperature (DDT): {ing.water_temp_f}°F — {plan.water_temp_recommendation}")
    lines.append("=" * 78)

    # Step-by-Step Proofing Roadmap
    lines.append("  📋 CHRONOLOGICAL PROOFING & BAKING SCHEDULE:")
    lines.append("=" * 78)

    action_icons = {
        "mix": "🥣",
        "knead": "🌀",
        "bulk": "⏳",
        "ball": "⚪",
        "cold_retard": "❄️",
        "temper": "🌡️",
        "preheat": "🔥",
        "bake": "🍕",
    }

    for m in plan.schedule:
        icon = action_icons.get(m.action_category, "📌")
        lines.append(f"  {icon} STEP {m.step_num}: {m.title.upper()}")
        lines.append(f"     Time     : {m.display_time} ({m.duration_str})")
        lines.append(f"     Ambient  : {m.temp_desc}")
        lines.append("     Actions  :")
        for subline in m.instruction.split("\n"):
            lines.append(f"       {subline}")
        lines.append(f"     👁️  Visual Cue : {m.visual_cue}")
        lines.append(f"     💡 Pro Tip    : {m.pro_tip}")
        lines.append("  " + "-" * 76)

    lines.append("=" * 78)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="🍕 Pizza Dough Artisan Agent: Base recipes, dynamic yeast kinetics, and proofing schedules."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Command: plan
    p_plan = subparsers.add_parser("plan", help="Calculate dough and generate full proofing schedule")
    p_plan.add_argument("-r", "--recipe", default="ny_style", help="Recipe ID or name (e.g. ny_style, neapolitan, detroit)")
    p_plan.add_argument("-b", "--balls", type=int, default=None, help="Number of dough balls (default from recipe)")
    p_plan.add_argument("-w", "--weight", type=float, default=None, help="Weight per ball in grams (default from recipe)")
    p_plan.add_argument("-t", "--ready", default=None, help="Ready/bake time (e.g. 'tomorrow 6pm', 'tonight 7pm', '+24h')")
    p_plan.add_argument("--hours", type=float, default=None, help="Fermentation duration in hours (e.g. 6, 24, 48)")
    p_plan.add_argument("-y", "--yeast", default="IDY", choices=["IDY", "ADY", "CY", "SOURDOUGH"], help="Yeast type")
    p_plan.add_argument("--room-temp", type=float, default=70.0, help="Room temperature in °F (default 70°F)")
    p_plan.add_argument("--fridge-temp", type=float, default=38.0, help="Fridge temperature in °F (default 38°F)")
    p_plan.add_argument("--pan", choices=["13x9", "14x10", "8x10"], default=None, help="Detroit pizza pan size (13x9, 14x10, or 8x10)")
    p_plan.add_argument("--ferment", default="AUTO", choices=["AUTO", "CF", "RT"], help="Fermentation profile")
    p_plan.add_argument("--json", action="store_true", help="Output result as JSON")

    # Command: quick
    p_quick = subparsers.add_parser("quick", help="Quick dough plan for today (e.g. 4-6 hours)")
    p_quick.add_argument("-b", "--balls", type=int, default=3, help="Number of dough balls")
    p_quick.add_argument("--hours", type=float, default=5.0, help="Hours from now until dinner (default 5)")
    p_quick.add_argument("-r", "--recipe", default="same_day_quick", help="Recipe ID")
    p_quick.add_argument("--json", action="store_true", help="Output result as JSON")

    # Command: ask (natural language)
    p_ask = subparsers.add_parser("ask", help="Ask the agent using natural conversational English")
    p_ask.add_argument("query", help="E.g. 'I want to make 4 NY style pizzas for tomorrow night at 6pm'")
    p_ask.add_argument("--json", action="store_true", help="Output result as JSON")

    # Command: recipe
    p_recipe = subparsers.add_parser("recipe", help="Manage base recipes")
    recipe_sub = p_recipe.add_subparsers(dest="recipe_command")

    # recipe list
    p_rlist = recipe_sub.add_parser("list", help="List all available base recipes")

    # recipe show
    p_rshow = recipe_sub.add_parser("show", help="Show full details for a recipe")
    p_rshow.add_argument("id", help="Recipe ID or name")

    # recipe add
    p_radd = recipe_sub.add_parser("add", help="Add or customize a base recipe")
    p_radd.add_argument("--id", required=True, help="Unique recipe ID (e.g. my_crust)")
    p_radd.add_argument("--name", required=True, help="Recipe display name")
    p_radd.add_argument("--hydration", type=float, required=True, help="Hydration percentage (e.g. 66.0)")
    p_radd.add_argument("--salt", type=float, default=2.5, help="Salt percentage (default 2.5)")
    p_radd.add_argument("--oil", type=float, default=0.0, help="Oil percentage (default 0.0)")
    p_radd.add_argument("--sugar", type=float, default=0.0, help="Sugar percentage (default 0.0)")
    p_radd.add_argument("--weight", type=float, default=260.0, help="Default ball weight in grams")
    p_radd.add_argument("--balls", type=int, default=4, help="Default dough ball count")
    p_radd.add_argument("--flour", default="Bread Flour or Tipo 00", help="Flour type")
    p_radd.add_argument("--oven", default="Home Oven (550°F / Steel)", help="Oven setup")
    p_radd.add_argument("--temp", type=int, default=550, help="Bake temp in °F")
    p_radd.add_argument("--time", default="6-8 minutes", help="Bake duration")
    p_radd.add_argument("--notes", default="", help="Recipe notes or secret tips")

    # recipe delete
    p_rdel = recipe_sub.add_parser("delete", help="Delete a custom recipe")
    p_rdel.add_argument("id", help="Custom Recipe ID to delete")

    # Command: serve (Web UI)
    p_serve = subparsers.add_parser("serve", help="Launch interactive web dashboard")
    p_serve.add_argument("-p", "--port", type=int, default=8001, help="Port to run web server on (default 8001)")

    args = parser.parse_args()
    agent = PizzaDoughAgent()

    if not args.command:
        # Default: print quick help and list recipes
        parser.print_help()
        print("\nAvailable Base Recipes:")
        for r in agent.db.list_recipes():
            custom_tag = " [CUSTOM]" if r.is_custom else ""
            print(f"  • {r.id:<18} : {r.name}{custom_tag} ({r.hydration_pct}% hyd, {r.salt_pct}% salt)")
        sys.exit(0)

    if args.command == "plan":
        plan = agent.create_plan(
            recipe_id_or_name=args.recipe,
            balls=args.balls,
            ball_weight_g=args.weight,
            pan_size=args.pan,
            ready_time_str=args.ready,
            duration_hours=args.hours,
            ferment_type=args.ferment,
            yeast_type=args.yeast,
            room_temp_f=args.room_temp,
            fridge_temp_f=args.fridge_temp,
        )
        if args.json:
            print(json.dumps(plan.to_dict(), indent=2))
        else:
            print(format_plan_terminal(plan))

    elif args.command == "quick":
        plan = agent.create_plan(
            recipe_id_or_name=args.recipe,
            balls=args.balls,
            duration_hours=args.hours,
            ferment_type="RT",
            yeast_type="IDY",
        )
        if args.json:
            print(json.dumps(plan.to_dict(), indent=2))
        else:
            print(format_plan_terminal(plan))

    elif args.command == "ask":
        plan = agent.parse_natural_language_request(args.query)
        if args.json:
            print(json.dumps(plan.to_dict(), indent=2))
        else:
            print(format_plan_terminal(plan))

    elif args.command == "recipe":
        if args.recipe_command == "list" or not args.recipe_command:
            recipes = agent.db.list_recipes()
            print("=" * 80)
            print("  🍕 MASTER BASE PIZZA RECIPES")
            print("=" * 80)
            print(f"  {'ID':<18} {'NAME':<28} {'HYD%':<6} {'SALT%':<6} {'OIL%':<6} {'TYPE'}")
            print("  " + "-" * 76)
            for r in recipes:
                tag = "Custom" if r.is_custom else "Classic"
                print(f"  {r.id:<18} {r.name[:27]:<28} {r.hydration_pct:<6.1f} {r.salt_pct:<6.1f} {r.oil_pct:<6.1f} {tag}")
            print("=" * 80)
            print("  Use `./dough recipe show <id>` for full recipe details.")
            print("  Use `./dough recipe add ...` to register your own custom base recipe.")

        elif args.recipe_command == "show":
            r = agent.db.get_recipe(args.id)
            if not r:
                print(f"❌ Recipe '{args.id}' not found.")
                sys.exit(1)
            print("=" * 70)
            print(f"  🍕 RECIPE: {r.name.upper()} (ID: {r.id})")
            print("=" * 70)
            print(f"  Description    : {r.description}")
            print(f"  Flour Type     : {r.flour_type}")
            print(f"  Hydration      : {r.hydration_pct}%")
            print(f"  Salt           : {r.salt_pct}%")
            print(f"  Oil            : {r.oil_pct}%")
            print(f"  Sugar/Malt     : {r.sugar_pct}%")
            print(f"  Default Ball   : {r.default_balls} balls @ {r.default_ball_weight}g")
            print(f"  Oven Setup     : {r.oven_type}")
            print(f"  Bake Temp      : {r.bake_temp_f}°F ({r.bake_time_min})")
            print(f"  Ferment Style  : {r.recommended_ferment}")
            if r.notes:
                print(f"  Notes          : {r.notes}")
            print("=" * 70)

        elif args.recipe_command == "add":
            r = Recipe(
                id=args.id,
                name=args.name,
                description=f"Custom recipe for {args.name}",
                flour_type=args.flour,
                hydration_pct=args.hydration,
                salt_pct=args.salt,
                oil_pct=args.oil,
                sugar_pct=args.sugar,
                default_ball_weight=args.weight,
                default_balls=args.balls,
                oven_type=args.oven,
                bake_temp_f=args.temp,
                bake_time_min=args.time,
                notes=args.notes,
                is_custom=True,
            )
            agent.db.save_recipe(r)
            print(f"✅ Successfully saved custom base recipe '{r.name}' (ID: {r.id})!")
            print(f"   Hydration: {r.hydration_pct}%, Salt: {r.salt_pct}%, Oil: {r.oil_pct}%, Sugar: {r.sugar_pct}%")

        elif args.recipe_command == "delete":
            deleted = agent.db.delete_recipe(args.id)
            if deleted:
                print(f"✅ Successfully deleted custom recipe '{args.id}'.")
            else:
                print(f"❌ Could not delete '{args.id}' (either not found or is a protected classic recipe).")

    elif args.command == "serve":
        from .server import start_server
        start_server(port=args.port)


if __name__ == "__main__":
    main()
