---
name: failure-learning-rl
description: This skill should be used when the user asks to "build a reinforcement learning agent that learns from failure", "retry until success with RL", "make an agent learn from its mistakes", "train a Q-learning agent", or wants to adapt, tune, or extend the bundled fail-learn-retry gridworld agent.
version: 1.0.0
---

# Failure-learning RL agent

A tabular Q-learning agent that treats each failed episode as a lesson: it penalizes the moves that
led to the failure, remembers them, explores differently, and loops until it reliably succeeds.

## Run it

To train on the built-in map:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/train.py"
```

Options: `--seed N`, `--map FILE`, `--max-episodes N`, `--quiet`. Exit code 0 means solved, 1 means the
episode cap was reached, 2 means an invalid map. The `/rl-demo` command wraps this.

To run the tests: `python -m pytest "${CLAUDE_PLUGIN_ROOT}/tests" -q`.

## How the loop works

Each training episode ends in `goal` (success), `trap` or `timeout` (failure).

- **On failure** (`FailureLearningAgent.learn_from_failure`): subtract an extra penalty from the last
  `lookback` (state, action) pairs (trap 20, timeout 5), increment their counts in `failure_memory`,
  and raise epsilon by 1.5x up to `eps_max`.
- **On success** (`learn_from_success`): decay epsilon by 0.9x down to `eps_min`.
- **Exploration** picks only among actions with the fewest recorded failures from that state, so a
  retry differs from the last attempt instead of repeating it.
- **Stopping**: after every episode a greedy rollout runs with no exploration; training ends when it
  reaches the goal `solved_streak` (default 3) times in a row, or at `max_episodes`.

## Adapting it

- **New task**: edit or replace the map. Any grid with one `S` and one `G` works; `env.py` raises
  `ValueError` otherwise. Check solvability with the BFS helper in `tests/test_train.py`.
- **Different environment**: keep the `reset()` / `step(action) -> (state, reward, done, outcome)`
  contract from `scripts/env.py`, with `outcome` in `goal`, `trap`, `timeout`, or `None`. Any new
  failure outcome gets its penalty in `agent.py` (`TRAP_PENALTY`, `TIMEOUT_PENALTY`).
- **Tuning**: slow or unstable learning usually means `eps_max` is too high (agent stays random) or
  `lookback` is too small (penalty misses the real mistake). Raise `lookback` for long failure chains.
- **Limits**: tabular Q-learning needs small, hashable, discrete states. For large or continuous
  state spaces, replace the Q-table with a function approximator (e.g. DQN); keep the
  failure-memory and adaptive-epsilon logic.

## Additional resources

- **`references/design.md`**: design rationale and test plan.
- **`references/example-map.txt`**: default map, usable with `--map`.
