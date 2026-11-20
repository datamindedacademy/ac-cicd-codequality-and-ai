"""Tests for bench.logs (exercise pytest/03)."""

from bench.logs import read_pressures, summarize_folder


# Task 1: a test that writes its own small file in tmp_path.
def test_read_pressures_tmp_path(tmp_path):
    path = tmp_path / "run.csv"
    path.write_text("timestamp,pressure_bar\n09:00,7.1\n09:01,7.3\n")

    pressures, skipped = read_pressures(path)

    assert pressures == [7.1, 7.3]
    assert skipped == 0


# Task 2: the same idea with the sample_log fixture from conftest.py.
def test_read_pressures_skips_bad_rows(sample_log):
    pressures, skipped = read_pressures(sample_log)
    assert pressures == [7.31, 7.35, 7.42]
    assert skipped == 2


def test_read_pressures_only_bad_rows(tmp_path):
    path = tmp_path / "run.csv"
    path.write_text("timestamp,pressure_bar\n09:00,ERR\n09:01,\n")
    assert read_pressures(path) == ([], 2)


# Task 3: a whole folder, with a file that is not a log.
def test_summarize_folder(sample_log):
    folder = sample_log.parent
    (folder / "run_02.csv").write_text("timestamp,pressure_bar\n09:00,8.0\n")
    (folder / "notes.txt").write_text("Bench was recalibrated on Monday.\n")

    result = summarize_folder(folder)

    # This test found the bug: notes.txt showed up as a log called "notes".
    assert list(result) == ["run_01", "run_02"]
    assert result["run_01"] == {
        "count": 3,
        "min": 7.31,
        "max": 7.42,
        "mean": 7.36,
        "skipped": 2,
    }
    assert result["run_02"]["skipped"] == 0


def test_summarize_folder_empty(tmp_path):
    assert summarize_folder(tmp_path) == {}
