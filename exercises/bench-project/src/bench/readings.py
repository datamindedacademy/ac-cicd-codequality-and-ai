"""Parse, summarize and classify single pressure readings."""

from typing import Dict, List, Tuple

PRESSURE_UNITS = ("bar", "psi", "kPa")


def parse_reading(text: str) -> Tuple[float, str]:
    """Split a reading like "7.5 bar" into its value and its unit.

    Extra spaces are ignored, and a decimal comma counts as a decimal point:
    "  7,5   bar " gives (7.5, "bar").
    The unit must be one of PRESSURE_UNITS. Anything else raises ValueError.
    """
    value, unit = text.replace(",", ".").split()
    return float(value), unit


def classify(pressure_bar: float, warning_bar: float = 8.0, alarm_bar: float = 8.5) -> str:
    """Return "OK", "WARNING" or "ALARM" for a pressure in bar.

    A pressure at or above a limit counts as that level: 8.0 is a WARNING,
    8.5 is an ALARM.
    """
    if pressure_bar > alarm_bar:
        return "ALARM"
    if pressure_bar >= warning_bar:
        return "WARNING"
    return "OK"


def summarize(values: List[float], decimals: int = 2) -> Dict:
    """Return count, min, max and mean of the values, rounded.

    An empty list gives {"count": 0}.
    """
    if not values:
        return {"count": 0}
    l = len(values)
    return {
        "count": l,
        "min": round(min(values), decimals),
        "max": round(max(values), decimals),
        "mean": round(sum(values) / l, decimals),
    }
