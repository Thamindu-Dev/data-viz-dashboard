import os
import subprocess
import threading
import time
import psutil
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='../dashboard/dist', static_url_path='/')
CORS(app)

# Frontend folder configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = os.path.join(BASE_DIR, '../dashboard/dist')

# Ensure the static folder exists
if not os.path.exists(FRONTEND_FOLDER):
    print(f"WARNING: Frontend folder not found at {FRONTEND_FOLDER}")

# Configuration
TTYD_PORT = 7681
TTYD_BIND = "0.0.0.0"
TTYD_PATH = os.path.join(BASE_DIR, "ttyd")
TTL_MINUTES = 15

# State
state = {
    "ttyd_process": None,
    "telemetry_running": False,
    "last_heartbeat": datetime.now(),
    "telemetry_data": {}
}

def telemetry_loop():
    while state["telemetry_running"]:
        try:
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            state["telemetry_data"] = {
                "cpu": {
                    "per_core": cpu_per_core,
                    "overall": sum(cpu_per_core) / len(cpu_per_core)
                },
                "ram": {
                    "total": ram.total,
                    "available": ram.available,
                    "percent": ram.percent
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": disk.percent
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Telemetry error: {e}")
        time.sleep(2)

def watchdog_loop():
    while True:
        if state["ttyd_process"] or state["telemetry_running"]:
            if datetime.now() - state["last_heartbeat"] > timedelta(minutes=TTL_MINUTES):
                print("Watchdog: TTL expired. Stopping services.")
                stop_services()
        time.sleep(30)

def stop_services():
    global state
    if state["ttyd_process"]:
        state["ttyd_process"].terminate()
        state["ttyd_process"] = None
        print("TTYD process terminated.")
    
    state["telemetry_running"] = False
    print("Telemetry thread stopped.")

# --- STATIC FRONTEND SERVING ---
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)

@app.route('/start', methods=['POST'])
def start():
    global state
    if state["ttyd_process"] or state["telemetry_running"]:
        return jsonify({"status": "already_running"}), 200

    # Start ttyd
    try:
        # Check if ttyd exists
        if not os.path.exists(TTYD_PATH):
            # Try to find it in system path
            ttyd_bin = subprocess.check_output(["which", "ttyd"], text=True).strip()
        else:
            ttyd_bin = TTYD_PATH

        state["ttyd_process"] = subprocess.Popen(
            [ttyd_bin, "-p", str(TTYD_PORT), "-b", TTYD_BIND, "bash"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to start ttyd: {str(e)}"}), 500

    # Start telemetry
    state["telemetry_running"] = True
    telemetry_thread = threading.Thread(target=telemetry_loop, daemon=True)
    telemetry_thread.start()
    
    state["last_heartbeat"] = datetime.now()
    
    return jsonify({"status": "started", "ttyd_port": TTYD_PORT}), 200

@app.route('/stop', methods=['POST'])
def stop():
    stop_services()
    return jsonify({"status": "stopped"}), 200

@app.route('/telemetry', methods=['GET'])
def get_telemetry():
    return jsonify(state["telemetry_data"]), 200

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    state["last_heartbeat"] = datetime.now()
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # Start watchdog thread
    watchdog_thread = threading.Thread(target=watchdog_loop, daemon=True)
    watchdog_thread.start()
    
    app.run(host='0.0.0.0', port=5000)
