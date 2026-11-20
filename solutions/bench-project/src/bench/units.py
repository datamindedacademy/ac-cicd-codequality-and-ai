"""Convert pressures and temperatures between units."""

# Every unit converts to a base unit of its family: bar for pressure, K for temperature.
# value_in_base = value * factor + offset
UNITS = {
    "bar": ("pressure", 1.0, 0.0),
    "psi": ("pressure", 1 / 14.5038, 0.0),
    "kPa": ("pressure", 0.01, 0.0),
    "K": ("temperature", 1.0, 0.0),
    "degC": ("temperature", 1.0, 273.15),
    "degF": ("temperature", 5 / 9, 273.15 - 32 * 5 / 9),
}


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a value from one unit to another unit of the same family.

    Raises ValueError for an unknown unit, or for units of different families,
    such as bar and degC.
    """
    if from_unit not in UNITS or to_unit not in UNITS:
        raise ValueError(f"Unknown unit: {from_unit} or {to_unit}")
    from_family, from_factor, from_offset = UNITS[from_unit]
    to_family, to_factor, to_offset = UNITS[to_unit]
    if from_family != to_family:
        raise ValueError(f"Cannot convert {from_family} to {to_family}")
    value_in_base = value * from_factor + from_offset
    return (value_in_base - to_offset) / to_factor


def to_bar(value: float, unit: str = "bar") -> float:
    """Convert a pressure in bar, psi or kPa to bar."""
    return convert(value, unit, "bar")
