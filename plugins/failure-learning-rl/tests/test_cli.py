from train import main

EXAMPLE_MAP = "S.....\n.###T.\n...#..\nT..#.#\n......\n.#T.TG\n"


def test_cli_solves_map_file_and_exits_zero(tmp_path, capsys):
    map_file = tmp_path / "map.txt"
    map_file.write_text(EXAMPLE_MAP)
    assert main(["--map", str(map_file), "--quiet"]) == 0
    assert "SOLVED" in capsys.readouterr().out


def test_cli_unsolvable_exits_one(tmp_path):
    map_file = tmp_path / "map.txt"
    map_file.write_text("S.#.G\n")
    assert main(["--map", str(map_file), "--max-episodes", "20", "--quiet"]) == 1


def test_cli_bad_map_exits_two(tmp_path, capsys):
    map_file = tmp_path / "map.txt"
    map_file.write_text("S..\n")  # no goal
    assert main(["--map", str(map_file)]) == 2
    assert "error" in capsys.readouterr().err


def test_cli_missing_map_file_exits_two(tmp_path):
    assert main(["--map", str(tmp_path / "nope.txt")]) == 2


def test_cli_ignores_leading_and_trailing_blank_lines(tmp_path, capsys):
    map_file = tmp_path / "map.txt"
    map_file.write_text("\n\n" + EXAMPLE_MAP + "\n\n")
    assert main(["--map", str(map_file), "--quiet"]) == 0
    assert "SOLVED" in capsys.readouterr().out


def test_cli_interior_blank_line_is_a_clear_error(tmp_path, capsys):
    map_file = tmp_path / "map.txt"
    map_file.write_text("S.G\n\n...\n")
    assert main(["--map", str(map_file)]) == 2
    assert "error" in capsys.readouterr().err


def test_cli_handles_crlf_line_endings(tmp_path, capsys):
    map_file = tmp_path / "map.txt"
    map_file.write_bytes(EXAMPLE_MAP.replace("\n", "\r\n").encode())
    assert main(["--map", str(map_file), "--quiet"]) == 0
    assert "SOLVED" in capsys.readouterr().out


def test_cli_max_steps_is_configurable(tmp_path):
    map_file = tmp_path / "map.txt"
    map_file.write_text("S.....G\n")  # 6 steps needed, well under the default cap
    # Too tight a budget: can never reach the goal, so it stays NOT SOLVED at the cap.
    assert main(["--map", str(map_file), "--max-steps", "3", "--max-episodes", "20", "--quiet"]) == 1
    # Enough budget: solvable, given enough episodes to learn the corridor.
    assert main(["--map", str(map_file), "--max-steps", "10", "--max-episodes", "200", "--quiet"]) == 0


def test_cli_rejects_non_positive_limits():
    assert main(["--max-episodes", "0"]) == 2
    assert main(["--max-steps", "0"]) == 2
