---
description: Train the fail-learn-retry RL agent until it solves the gridworld
argument-hint: "[--seed N] [--map path/to/map.txt] [--max-episodes N] [--max-steps N] [--quiet]"
allowed-tools: Bash(python:*), Bash(python3:*)
---

Run the failure-learning RL agent and report what happened.

1. Run: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/train.py" $ARGUMENTS`. If `python3` is not found on
   this system, retry with `python` instead (Windows commonly only has `python`; Linux/macOS
   commonly only have `python3`). No dependencies are needed beyond the standard library, and
   Python 3.8+ is required.
2. Report concisely:
   - whether it solved the task, and after how many episodes and failures
   - the failure reasons it hit first (trap vs timeout) and how epsilon changed
   - the final route
3. If the run exits non-zero: exit code 1 means it hit the episode cap without solving (check that
   the map is solvable: goal reachable from `S` without crossing `#` or `T`, and that `--max-steps`
   is large enough for the map's size); exit code 2 means the arguments or map file were invalid, so
   show the error message.

Map files are plain text, one row per line: `S` start, `G` goal, `#` wall, `T` trap, `.` floor.
An example lives at `${CLAUDE_PLUGIN_ROOT}/skills/failure-learning-rl/references/example-map.txt`.
`--max-steps` (default 60) is the per-episode step budget before a `timeout` failure; raise it for
larger custom maps.
