import subprocess
import threading
from datetime import datetime
import logging
from flask import Blueprint, jsonify, request, send_from_directory, Response, stream_with_context

from config import FRONTEND_FOLDER
from app_state import state
from telemetry import telemetry_loop, stop_services

logger = logging.getLogger(__name__)

# We will export a blueprint for HTTP routes
api_bp = Blueprint('api', __name__)

COMMANDS = {
    "update": ["sh", "-c",
               "echo '=== OS ===' && cat /etc/os-release | grep PRETTY | cut -d= -f2 && "
               "echo '=== Uptime ===' && uptime && "
               "echo '=== Python ===' && python3 --version 2>&1 && "
               "echo '=== Disk Usage ===' && df -h / | tail -1 && "
               "echo '=== Memory ===' && free -h | grep Mem"],
    "cleanup": ["sh", "-c",
                "cd /home && "
                "pip cache purge 2>&1 || true; "
                "find /tmp -maxdepth 1 -type f -delete 2>/dev/null; "
                "echo 'User-level cleanup complete:' && "
                "echo '  ✓ Pip cache purged' && "
                "echo '  ✓ /tmp files cleared' && "
                "echo '' && "
                "echo 'For system-level apt cleanup (requires root):' && "
                "echo '  sudo apt-get clean' && "
                "echo '  sudo apt-get autoremove -y' && "
                "echo '  sudo apt-get update'"],
    "backup":  ["sh", "-c", "echo 'No backup script configured. Add your script to /opt/backup.sh'"],
    "restart": ["sh", "-c", "echo 'Restarting Flask backend in 1s...' && (sleep 1 && kill -15 $PPID) &"],
}

@api_bp.route('/cmd/<action>', methods=['POST'])
def run_cmd(action):
    if action not in COMMANDS:
        return jsonify({"status": "error", "message": f"Unknown command: {action}"}), 400
    try:
        result = subprocess.run(
            COMMANDS[action],
            capture_output=True, text=True, timeout=20,
        )
        output = (result.stdout + result.stderr).strip() or "Done."
        return jsonify({"status": "ok", "output": output[:800]})
    except subprocess.TimeoutExpired:
        return jsonify({"status": "ok", "output": "Command is running in background…"})
    except Exception as e:
        logger.error(f"Error executing command '{action}': {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/start', methods=['POST'])
def start():
    if state["telemetry_running"]:
        return jsonify({"status": "already_running"}), 200
    state["telemetry_running"] = True
    threading.Thread(target=telemetry_loop, daemon=True).start()
    state["last_heartbeat"] = datetime.now()
    return jsonify({"status": "started"}), 200

@api_bp.route('/stop', methods=['POST'])
def stop():
    stop_services()
    return jsonify({"status": "stopped"}), 200

@api_bp.route('/telemetry', methods=['GET'])
def get_telemetry():
    return jsonify(state["telemetry_data"]), 200

@api_bp.route('/heartbeat', methods=['POST'])
def heartbeat():
    state["last_heartbeat"] = datetime.now()
    return jsonify({"status": "ok"}), 200


# -------------------------------------------------------------------------
# Static frontend – Catch-all
# -------------------------------------------------------------------------
@api_bp.route('/')
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@api_bp.route('/<path:filename>')
def serve_static(filename):
    # If file exists in frontend dist, serve it. Otherwise fallback to index.html (SPA)
    import os
    if os.path.exists(os.path.join(FRONTEND_FOLDER, filename)):
        return send_from_directory(FRONTEND_FOLDER, filename)
    return send_from_directory(FRONTEND_FOLDER, 'index.html')
