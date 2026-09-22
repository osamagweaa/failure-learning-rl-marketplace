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
