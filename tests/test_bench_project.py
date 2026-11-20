"""Check the bench project: the starting point, the solution, and the bugs between them."""

import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
EXERCISE = ROOT / "exercises" / "bench-project"
SOLUTION = ROOT / "solutions" / "bench-project"

# The bugs planted in the exercise, and the solution tests that must find them.
BUG_FINDERS = {
    "test_readings.test_classify_alarm_boundary",  # > instead of >=
    "test_readings.test_parse_reading_unknown_unit",  # unit not checked
    "test_logs.test_summarize_folder",  # .txt counted as a log
    # degF offset 255.37 instead of 255.3722...
    "test_units.test_convert_known_values[100-degC-degF-212.0]",
    "test_units.test_convert_known_values[212-degF-degC-100.0]",
    "test_units.test_convert_known_values[32-degF-degC-0.0]",
    "test_units.test_convert_known_values[-40-degC-degF--40.0]",
}


def run_pytest(project: Path, source: Path, report: Path) -> dict[str, bool]:
    """Run the tests of a project against the code in source. Return {test: passed}."""
    env = os.environ | {"PYTHONPATH": str(source / "src")}
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={report}"],
        cwd=project,
        env=env,
        capture_output=True,
        timeout=120,
    )
    results = {}
    for case in ET.parse(report).iter("testcase"):
        name = f"{case.get('classname').split('.')[-1]}.{case.get('name')}"
        results[name] = case.find("failure") is None and case.find("error") is None
    return results


def test_exercise_starts_green(tmp_path):
    results = run_pytest(EXERCISE, EXERCISE, tmp_path / "report.xml")
    assert len(results) == 6
    assert all(results.values())


def test_solution_is_green(tmp_path):
    results = run_pytest(SOLUTION, SOLUTION, tmp_path / "report.xml")
    assert len(results) > 50
    assert all(results.values()), [name for name, ok in results.items() if not ok]


def test_solution_tests_find_exactly_the_planted_bugs(tmp_path):
    results = run_pytest(SOLUTION, EXERCISE, tmp_path / "report.xml")
    failed = {name for name, ok in results.items() if not ok}
    assert failed == BUG_FINDERS


def test_projects_differ_only_where_expected():
    for relative in ["uv.lock", ".python-version", ".gitignore", "README.md"]:
        assert (EXERCISE / relative).read_text() == (SOLUTION / relative).read_text(), relative
    assert (EXERCISE / "src/bench/__init__.py").read_text() == (
        SOLUTION / "src/bench/__init__.py"
    ).read_text()
    # Choosing the ruff rules is task 2 of the ruff exercise.
    assert "[tool.ruff" not in (EXERCISE / "pyproject.toml").read_text()
    assert "[tool.ruff" in (SOLUTION / "pyproject.toml").read_text()


def ruff(project: Path, tmp_path: Path, *args: str) -> subprocess.CompletedProcess:
    """Run ruff on a copy of the project outside this repository, as a participant would."""
    copy = tmp_path / project.name
    shutil.copytree(project, copy, ignore=shutil.ignore_patterns(".venv", "*_cache"))
    return subprocess.run(
        [sys.executable, "-m", "ruff", *args, "--no-cache", "."],
        cwd=copy,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_exercise_has_lint_and_format_findings(tmp_path):
    check = ruff(EXERCISE, tmp_path, "check", "--output-format", "concise")
    assert check.returncode == 1
    assert "F401" in check.stdout
    form = ruff(EXERCISE, tmp_path / "f", "format", "--check")
    assert "units.py" in form.stdout


def test_solution_is_ruff_clean(tmp_path):
    assert ruff(SOLUTION, tmp_path, "check").returncode == 0
    assert ruff(SOLUTION, tmp_path / "f", "format", "--check").returncode == 0


def test_solution_pre_commit_config():
    config = yaml.safe_load((SOLUTION / ".pre-commit-config.yaml").read_text())
    hooks = {hook["id"]: hook for repo in config["repos"] for hook in repo["hooks"]}
    assert hooks["ruff-check"]["entry"] == "uv run ruff check --fix"
    assert hooks["ruff-format"]["entry"] == "uv run ruff format"
    assert hooks["pytest"]["stages"] == ["pre-push"]
    assert config["default_stages"] == ["pre-commit"]


def test_lockfile_uses_public_pypi_only():
    lock = (EXERCISE / "uv.lock").read_text()
    assert "https://pypi.org/simple" in lock
    assert "pkgs.dev.azure.com" not in lock


def test_solution_pipeline():
    pipeline = yaml.safe_load((SOLUTION / "azure-pipelines.yml").read_text())
    assert pipeline["trigger"]["branches"]["include"] == ["main"]
    assert "pr" not in pipeline
    jobs = {job["job"]: job for job in pipeline["jobs"]}
    assert set(jobs) == {"lint", "test"}
    lint = [step.get("script", "") for step in jobs["lint"]["steps"]]
    assert "uv sync --locked" in lint
    assert "uv run ruff check ." in lint
    assert "uv run ruff format --check ." in lint
    test = [step.get("script", "") for step in jobs["test"]["steps"]]
    assert any(script.startswith("uv run pytest") for script in test)


def test_exercise_pipeline_matches_solution_lint_job():
    """The YAML given in pipelines exercise 01 is the lint job of the solution."""
    readme = (ROOT / "exercises/pipelines/01-format-check-and-policies/README.md").read_text()
    given = yaml.safe_load(readme.split("```yaml\n", 1)[1].split("```", 1)[0])
    solution = yaml.safe_load((SOLUTION / "azure-pipelines.yml").read_text())
    assert given["jobs"][0] == solution["jobs"][0]


def test_exercise_folders_exist():
    counts = {"code-quality": 2, "pytest": 3, "pipelines": 2}
    for folder, count in counts.items():
        readmes = sorted((ROOT / "exercises" / folder).glob("0*/README.md"))
        assert len(readmes) == count, folder
        for readme in readmes:
            assert readme.read_text().startswith("# 0"), readme
