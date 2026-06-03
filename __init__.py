"""Data Viz Dashboard — Slash Command."""

import os
import socket
import subprocess
import sys
from pathlib import Path

# --- Auto-start backend server -------------------------------------------------

def _is_port_in_use(port: int) -> bool:
    """Check if a TCP port is already bound on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(("127.0.0.1", port))
        return result == 0

def _resolve_python_executable() -> str:
    """Resolve the venv Python binary (Linux-first, Windows fallback)."""
    base_dir = Path(__file__).resolve().parent
    # Linux / POSIX venv layout (primary – Docker container)
    for candidate in [
        base_dir / "backend" / "venv" / "bin" / "python3",
        base_dir / "backend" / "venv" / "bin" / "python",
        # Windows venv layout (fallback)
        base_dir / "backend" / "venv" / "Scripts" / "python.exe",
    ]:
        if candidate.is_file():
            return str(candidate)
    # Last resort: whatever Python is running the gateway
    return sys.executable

def auto_install_requirements() -> None:
    """Install Python dependencies from backend/requirements.txt using the venv pip.
    Falls back to system pip if the venv pip binary is missing.
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    req_path = os.path.join(base_dir, "backend", "requirements.txt")
    # Try venv pip first (Linux layout)
    for pip_candidate in [
        os.path.join(base_dir, "backend", "venv", "bin", "pip"),
        os.path.join(base_dir, "backend", "venv", "Scripts", "pip.exe"),
    ]:
        if os.path.isfile(pip_candidate):
            pip_path = pip_candidate
            break
    else:
        pip_path = "pip"
    try:
        subprocess.run(
            [pip_path, "install", "-r", req_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except Exception as e:
        print(f"[data-viz-dashboard] Dependency install failed: {e}")

def _start_backend():
    """Start the Flask backend if it is not already running."""
    if _is_port_in_use(5000):
        return

    # Ensure dependencies are installed before launching the server.
    auto_install_requirements()

    python_exe = _resolve_python_executable()
    server_script = Path(__file__).resolve().parent / "backend" / "server.py"

    if not server_script.is_file():
        print(f"[data-viz-dashboard] server.py not found at {server_script}")
        return

    backend_dir = Path(__file__).resolve().parent / "backend"
    
    print(f"[data-viz-dashboard] Starting backend with Gunicorn via: {python_exe}")
    try:
        subprocess.Popen(
            [python_exe, "-m", "gunicorn", "-b", "0.0.0.0:5000", "--threads", "4", "server:app"],
            cwd=str(backend_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as e:
        print(f"[data-viz-dashboard] Failed to start backend: {e}")

# Trigger auto‑start as soon as the module is imported.
_start_backend()

# ------------------------------------------------------------------------------

def _handle_dashboard(raw_args: str) -> str:
    url = "http://localhost:5000/"
    return f"🚀 **System Intelligence Dashboard**\n\nClick here to open the UI in a new tab:\n{url}"

def register(ctx):
    # Not to 'callback'. comes to 'handler'
    ctx.register_command(
        "dashboard",
        handler=_handle_dashboard,
        description="Open the System Intelligence Dashboard"
    )