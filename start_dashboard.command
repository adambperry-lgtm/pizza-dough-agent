#!/bin/zsh
# Double-clickable macOS launcher for Pizza Dough Artisan Agent
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🍕 Starting Pizza Dough Artisan Dashboard..."
open "http://localhost:8001"
python3 "$DIR/dough" serve --port 8001
