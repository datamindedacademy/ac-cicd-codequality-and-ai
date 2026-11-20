"""Read test bench logs: CSV files with a pressure_bar column."""

import os
from pathlib import Path
import csv

from bench.readings import summarize


def read_pressures(path: Path) -> tuple[list[float], int]:
    """Read the pressure_bar column of one CSV log.

    Returns the pressures that are valid numbers, and how many rows were skipped
    because the pressure was missing or not a number.
    """
    pressures = []
    skipped = 0
    with open(path, newline="") as file:
        for row in csv.DictReader(file):
            try:
                pressures.append(float(row["pressure_bar"]))
            except ValueError:
                skipped += 1
    return pressures, skipped


def summarize_folder(folder: Path) -> dict[str, dict]:
    """Summarize every CSV log in a folder.

    Only files ending in .csv count. The result maps the file name without
    extension to the summary of its pressures, plus the number of skipped rows:
    {"run_01": {"count": 3, "min": ..., "max": ..., "mean": ..., "skipped": 1}}
    """
    result = {}
    for path in sorted(folder.iterdir()):
        pressures, skipped = read_pressures(path)
        result[path.stem] = summarize(pressures) | {"skipped": skipped}
    return result
