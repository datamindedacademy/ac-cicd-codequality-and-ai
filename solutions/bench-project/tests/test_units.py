"""Tests for bench.units (exercise pytest/02)."""

from itertools import permutations

import pytest

from bench.units import UNITS, convert, to_bar


# Task 1: four copy-pasted tests become one parametrized test.
@pytest.mark.parametrize(
    ("value", "unit", "expected"),
    [
        (7.5, "bar", 7.5),
        (14.5038, "psi", 1.0),
        (760, "kPa", 7.6),
    ],
    ids=["bar", "psi", "kPa"],
)
def test_to_bar(value, unit, expected):
    assert to_bar(value, unit) == pytest.approx(expected)


def test_to_bar_default_unit_is_bar():
    assert to_bar(7.5) == 7.5


# Task 2: a table of values you can check in a handbook.
@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (7.5, "bar", "psi", 108.7785),
        (7.5, "bar", "kPa", 750.0),
        (100, "degC", "degF", 212.0),
        (212, "degF", "degC", 100.0),  # found the bug in the degF offset
        (32, "degF", "degC", 0.0),
        (-40, "degC", "degF", -40.0),
        (0, "K", "degC", -273.15),
    ],
)
def test_convert_known_values(value, from_unit, to_unit, expected):
    assert convert(value, from_unit, to_unit) == pytest.approx(expected, abs=1e-6)


def test_convert_unknown_unit():
    with pytest.raises(ValueError):
        convert(7.5, "bar", "atm")


# Task 3: every pair of units of the same family survives a round trip.
SAME_FAMILY = [(a, b) for a, b in permutations(UNITS, 2) if UNITS[a][0] == UNITS[b][0]]
OTHER_FAMILY = [(a, b) for a, b in permutations(UNITS, 2) if UNITS[a][0] != UNITS[b][0]]


@pytest.mark.parametrize(("from_unit", "to_unit"), SAME_FAMILY)
@pytest.mark.parametrize("value", [-40.0, 0.0, 7.5, 300.0])
def test_convert_round_trip(value, from_unit, to_unit):
    there = convert(value, from_unit, to_unit)
    assert convert(there, to_unit, from_unit) == pytest.approx(value)


@pytest.mark.parametrize(("from_unit", "to_unit"), OTHER_FAMILY)
def test_convert_between_families_fails(from_unit, to_unit):
    with pytest.raises(ValueError, match="Cannot convert"):
        convert(1.0, from_unit, to_unit)
