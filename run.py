"""
run.py -- Convenience startup script for CreatorLens
Usage:  python run.py
"""

import sys
import os

# ── Python 3.13+ check ──────────────────────────────────────────────────────
if sys.version_info < (3, 13):
    sys.stdout.buffer.write(
        f"[WARNING] Python 3.13+ required. You are running {sys.version}\n".encode("utf-8")
    )
    sys.exit(1)

# ── Banner (ASCII-safe for Windows CP1252 consoles) ──────────────────────────
BANNER = (
    "\n"
    "  ================================================\n"
    "  |   CreatorLens  --  YouTube Creator Analyzer  |\n"
    "  |       AI-Powered Sentiment Analysis          |\n"
    "  ================================================\n"
    "\n"
    "  Backend : Flask 3.x  (Python {ver})\n"
    "  Frontend: Vanilla JS SPA + Chart.js\n"
    "  API     : YouTube Data API v3 + VADER NLP\n"
    "\n"
    "  Open in browser -->  http://localhost:5000\n"
    "  Press Ctrl+C to stop.\n"
)

sys.stdout.buffer.write(BANNER.format(ver=sys.version.split()[0]).encode("utf-8"))

# ── Import & run ─────────────────────────────────────────────────────────────
try:
    from app import app
except ValueError as exc:
    # config.py raises ValueError if YOUTUBE_API_KEY is missing
    print(f"\n❌  Configuration error: {exc}")
    print("   Add your key to the .env file:  YOUTUBE_API_KEY=your_key_here\n")
    sys.exit(1)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
