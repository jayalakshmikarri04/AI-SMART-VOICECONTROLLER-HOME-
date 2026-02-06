"""Simple intent parser for voice commands.
Detects appliance and action (on/off) from text.
"""
from typing import Dict


APPLIANCES = {
    "light": ["light", "lights"],
    "fan": ["fan", "fans"],
    "tv": ["tv", "television", "tube"],
    "ac": ["ac", "air conditioner", "aircon"],
}


def find_appliance(text: str):
    text = text.lower()
    for key, aliases in APPLIANCES.items():
        for a in aliases:
            if a in text:
                return key
    return None


def find_action(text: str):
    t = text.lower()
    # check for explicit off
    off_words = ["off", "switch off", "turn off", "stop"]
    on_words = ["on", "switch on", "turn on", "start"]

    for w in off_words:
        if w in t:
            return "off"
    for w in on_words:
        if w in t:
            return "on"

    # fallback: look for words 'enable'/'disable'
    if "enable" in t:
        return "on"
    if "disable" in t:
        return "off"

    return None


def parse_intent(text: str) -> Dict[str, str]:
    """Return dict with 'appliance' and 'action' keys (or None values)."""
    if not text:
        return {"appliance": None, "action": None}

    appliance = find_appliance(text)
    action = find_action(text)

    return {"appliance": appliance, "action": action}
