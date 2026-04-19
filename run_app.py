"""
run_app.py — Single script to start the full GreenThumb AI stack.
Run from the project root: python run_app.py
"""

import subprocess
import sys
import time
import os
import webbrowser
from pathlib import Path

BASE = Path(__file__).resolve().parent

def run():
    print("\n" + "═"*55)
    print("  🌿  GreenThumb AI — Starting up")
    print("═"*55)

    # 1. Start Ollama (non-blocking, will be managed by FastAPI too)
    print("\n[1/3] Checking Ollama...")
    try:
        import requests
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        print("      ✅ Ollama already running")
    except Exception:
        print("      Starting Ollama server...")
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        time.sleep(15)
        print("      ✅ Ollama started")

    # 2. Start FastAPI backend
    print("\n[2/3] Starting FastAPI backend on http://127.0.0.1:8000 ...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app",
         "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=str(BASE),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    time.sleep(15)
    print("      ✅ FastAPI running")

    # 3. Start Streamlit frontend
    print("\n[3/3] Starting Streamlit frontend on http://localhost:8501 ...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run",
         str(BASE / "frontend" / "app.py"),
         "--server.port", "8501",
         "--server.headless", "true",
         "--theme.base", "light"],
        cwd=str(BASE),
    )
    time.sleep(15)

    print("\n" + "═"*55)
    print("  ✅  GreenThumb AI is running!")
    print("  🌐  Open: http://localhost:8501")
    print("  📡  API:  http://127.0.0.1:8000/docs")
    print("  Press Ctrl+C to stop all services")
    print("═"*55 + "\n")

    webbrowser.open("http://localhost:8501")

    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        backend.terminate()
        frontend.terminate()
        print("   Goodbye! 🌿")

if __name__ == "__main__":
    run()
