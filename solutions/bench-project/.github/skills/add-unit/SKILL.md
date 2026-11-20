---
name: add-unit
description: Add a new pressure or temperature unit to the bench project, with tests from known values. Use when asked to support a new unit such as MPa, mbar, inHg or degR in bench.units or bench.readings.
---

# Add a unit to the bench project

Follow these steps in order. Stop and ask when a step is unclear; do not guess a conversion factor.

## 1. Find the conversion

- Ask the user for the source of the conversion factor (a datasheet, a standard, a handbook) if they did not give one.
- Write the unit as `value_in_base = value * factor + offset`, where the base unit is bar for pressure and K for temperature.
- Keep factors exact where possible: write `1 / 14.5038`, not `0.068948`.

## 2. Tests first

- Add at least two rows for the new unit to `test_convert_known_values` in `tests/test_units.py`, with expected values taken from the source in step 1, not from running the code.
- For a pressure unit, add a test that `parse_reading` accepts a reading in that unit.
- Run `uv run pytest` and show the failures to the user before changing any code.

## 3. Change the code

- Add the unit to `UNITS` in `src/bench/units.py`.
- For a pressure unit, also add it to `PRESSURE_UNITS` in `src/bench/readings.py`.
- Do not change existing tests. If an existing test fails, stop and report it.

## 4. Check

- Run `uv run pytest`, `uv run ruff check .` and `uv run ruff format --check .`. All three must pass.
- Summarize for the user: the factor and its source, the tests you added, and the files you changed.
