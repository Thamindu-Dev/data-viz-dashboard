"""
Shared mutable runtime state – one dict imported by every module.
Never reassign this name; mutate the dict in-place.
"""
from datetime import datetime

state: dict = {
    "telemetry_running": False,
    "last_heartbeat": datetime.now(),
    "telemetry_data": {},
}
