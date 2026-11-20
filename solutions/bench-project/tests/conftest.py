"""Fixtures that every test file in this folder can use (exercise pytest/03, task 2)."""

import pytest

SAMPLE_LOG = """timestamp,pressure_bar,temperature_c
2026-01-16 09:00:00,7.31,81.2
2026-01-16 09:01:00,ERR,81.5
2026-01-16 09:02:00,7.35,81.9
2026-01-16 09:03:00,,82.0
2026-01-16 09:04:00,7.42,82.4
"""


@pytest.fixture
def sample_log(tmp_path):
    """A CSV log with three good rows and two bad ones, in a temporary folder."""
    path = tmp_path / "run_01.csv"
    path.write_text(SAMPLE_LOG)
    return path
