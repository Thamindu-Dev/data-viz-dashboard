import time
import psutil
from datetime import datetime, timedelta
from config import TTL_MINUTES
from app_state import state
import logging

logger = logging.getLogger(__name__)

def telemetry_loop():
    while state["telemetry_running"]:
        try:
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            state["telemetry_data"] = {
                "cpu": {
                    "per_core": cpu_per_core,
                    "overall": round(sum(cpu_per_core) / len(cpu_per_core), 1)
                },
                "ram": {
                    "total": ram.total,
                    "available": ram.available,
                    "percent": round(ram.percent, 1)
                },
                "disk": {
                    "total": round(disk.total / (1024 ** 3), 2),
                    "used": round(disk.used / (1024 ** 3), 2),
                    "free": round(disk.free / (1024 ** 3), 2),
                    "percent": disk.percent
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Telemetry error: {e}", exc_info=True)
        time.sleep(2)

def stop_services():
    state["telemetry_running"] = False
    logger.info("Services stopped.")

def watchdog_loop():
    while True:
        if state["telemetry_running"]:
            if datetime.now() - state["last_heartbeat"] > timedelta(minutes=TTL_MINUTES):
                logger.info("Watchdog: TTL expired. Stopping services.")
                stop_services()
        time.sleep(30)
