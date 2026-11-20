"""Tests for bench.units. Written by a colleague who liked copy and paste."""

import pytest

from bench.units import convert, to_bar


def test_to_bar_from_bar():
    assert to_bar(7.5, "bar") == 7.5


def test_to_bar_from_psi():
    assert to_bar(14.5038, "psi") == pytest.approx(1.0)


def test_to_bar_from_kpa():
    assert to_bar(760, "kPa") == pytest.approx(7.6)


def test_to_bar_default_unit_is_bar():
    assert to_bar(7.5) == 7.5


def test_convert_bar_to_psi():
    assert convert(7.5, "bar", "psi") == pytest.approx(108.7785)


def test_convert_unknown_unit():
    with pytest.raises(ValueError):
        convert(7.5, "bar", "atm")
