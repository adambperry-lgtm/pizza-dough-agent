"""Lightweight HTTP server for Pizza Dough Artisan web dashboard and API."""

import http.server
import socketserver
import json
import urllib.parse
import os
from pathlib import Path
from typing import Optional
from .agent import PizzaDoughAgent
from .models import Recipe

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


class PizzaRequestHandler(http.server.SimpleHTTPRequestHandler):
    agent: PizzaDoughAgent = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/recipes":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            recipes = [r.to_dict() for r in self.agent.db.list_recipes()]
            self.wfile.write(json.dumps(recipes).encode("utf-8"))
            return

        elif path.startswith("/api/recipes/"):
            recipe_id = path.split("/api/recipes/")[1]
            recipe = self.agent.db.get_recipe(recipe_id)
            if recipe:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(recipe.to_dict()).encode("utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Recipe not found"}).encode("utf-8"))
            return

        elif path == "/api/logs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            logs = self.agent.db.list_logs(limit=25)
            self.wfile.write(json.dumps(logs).encode("utf-8"))
            return

        elif path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "app": "Pizza Dough Artisan Agent"}).encode("utf-8"))
            return

        # Serve static web files
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            payload = {}

        if path == "/api/calculate":
            try:
                recipe_id = payload.get("recipe_id", "ny_style")
                balls = int(payload.get("balls", 4))
                ball_weight = float(payload.get("ball_weight_g", 260.0))
                hours = float(payload.get("hours")) if payload.get("hours") is not None else None
                ready_str = payload.get("ready_time_str")
                ferment_type = payload.get("ferment_type", "AUTO")
                yeast_type = payload.get("yeast_type", "IDY")
                room_temp = float(payload.get("room_temp_f", 70.0))
                fridge_temp = float(payload.get("fridge_temp_f", 38.0))

                plan = self.agent.create_plan(
                    recipe_id_or_name=recipe_id,
                    balls=balls,
                    ball_weight_g=ball_weight,
                    ready_time_str=ready_str,
                    duration_hours=hours,
                    ferment_type=ferment_type,
                    yeast_type=yeast_type,
                    room_temp_f=room_temp,
                    fridge_temp_f=fridge_temp,
                )

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(plan.to_dict()).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        elif path == "/api/recipes":
            try:
                recipe = Recipe.from_dict(payload)
                recipe.is_custom = True
                self.agent.db.save_recipe(recipe)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(recipe.to_dict()).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/recipes/"):
            recipe_id = path.split("/api/recipes/")[1]
            success = self.agent.db.delete_recipe(recipe_id)
            self.send_response(200 if success else 400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": success}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def start_server(port: Optional[int] = None):
    # Support Railway and container runtime dynamic PORT env var
    env_port = os.environ.get("PORT")
    if env_port and env_port.strip().isdigit():
        active_port = int(env_port.strip())
    elif port is not None:
        active_port = port
    else:
        active_port = 8001

    agent = PizzaDoughAgent()
    PizzaRequestHandler.agent = agent

    class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    with ThreadedHTTPServer(("", active_port), PizzaRequestHandler) as httpd:
        print(f"🍕 Pizza Dough Artisan Server running at http://localhost:{active_port}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


if __name__ == "__main__":
    start_server()

