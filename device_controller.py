"""Simulated device controller keeping in-memory states."""
from typing import Dict

EMOJI = {
    "light": "💡",
    "fan": "🌀",
    "tv": "📺",
    "ac": "❄️",
}


class DeviceController:
    def __init__(self):
        # default states: OFF
        self.states = {k: "OFF" for k in EMOJI.keys()}

    def get_states(self) -> Dict[str, str]:
        return dict(self.states)

    def perform(self, appliance: str, action: str) -> Dict[str, str]:
        if appliance not in self.states:
            return {"message": f"Unknown appliance: {appliance}"}

        action = action.lower()
        if action == "on":
            self.states[appliance] = "ON"
            msg = f"{EMOJI.get(appliance,'')} {appliance.capitalize()} turned ON"
            return {"message": msg}
        elif action == "off":
            self.states[appliance] = "OFF"
            msg = f"{EMOJI.get(appliance,'')} {appliance.capitalize()} turned OFF"
            return {"message": msg}
        else:
            return {"message": f"Unknown action: {action}"}
