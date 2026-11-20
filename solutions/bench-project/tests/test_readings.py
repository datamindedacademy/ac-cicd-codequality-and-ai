"""Tests for bench.readings (exercise pytest/01)."""

import pytest

from bench.readings import classify, parse_reading, summarize


# Task 2: parse_reading, as its docstring describes it.
def test_parse_reading():
    assert parse_reading("7.5 bar") == (7.5, "bar")


def test_parse_reading_extra_spaces():
    assert parse_reading("  108.8   psi ") == (108.8, "psi")


def test_parse_reading_decimal_comma():
    assert parse_reading("7,5 bar") == (7.5, "bar")


# Task 2: classify, with both boundaries tested from both sides.
def test_classify_ok():
    assert classify(7.2) == "OK"


def test_classify_warning_boundary():
    assert classify(7.99) == "OK"
    assert classify(8.0) == "WARNING"


def test_classify_alarm_boundary():
    # This test found the bug: classify used > instead of >= for the alarm limit.
    assert classify(8.49) == "WARNING"
    assert classify(8.5) == "ALARM"


def test_classify_custom_limits():
    assert classify(7.2, warning_bar=7.0) == "WARNING"
    assert classify(8.2, alarm_bar=8.0) == "ALARM"


def test_summarize():
    # Arrange
    values = [7.4, 7.1, 7.2]
    # Act
    result = summarize(values)
    # Assert
    assert result == {"count": 3, "min": 7.1, "max": 7.4, "mean": 7.23}


def test_summarize_empty():
    assert summarize([]) == {"count": 0}


# Task 3: bad input raises ValueError, with a message that names the problem.
def test_parse_reading_unknown_unit():
    with pytest.raises(ValueError, match="Unknown pressure unit: atm"):
        parse_reading("7.5 atm")


def test_parse_reading_not_a_number():
    with pytest.raises(ValueError):
        parse_reading("seven bar")


def test_parse_reading_missing_unit():
    with pytest.raises(ValueError):
        parse_reading("7.5")
