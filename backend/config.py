"""
Configuration constants – single source of truth for the whole backend.
"""
import os

# Absolute path of the backend/ directory
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

# Absolute path of the compiled frontend (dashboard/dist/)
FRONTEND_FOLDER: str = os.getenv(
    "FRONTEND_FOLDER", 
    os.path.join(BASE_DIR, "..", "dashboard", "dist")
)

# Minutes of inactivity before the watchdog stops telemetry
try:
    TTL_MINUTES: int = int(os.getenv("TTL_MINUTES", "15"))
except ValueError:
    TTL_MINUTES = 15
