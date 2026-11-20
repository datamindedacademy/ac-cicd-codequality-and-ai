# bench

Helpers for the readings and logs of a (fictional) compressor test bench.

| Module | What it does |
| --- | --- |
| `src/bench/units.py` | Convert pressures and temperatures between units |
| `src/bench/readings.py` | Parse, summarize and classify single readings |
| `src/bench/logs.py` | Read CSV logs and summarize a folder of them |

## Run the checks

```powershell
uv sync
uv run pytest
uv run ruff check .
```
