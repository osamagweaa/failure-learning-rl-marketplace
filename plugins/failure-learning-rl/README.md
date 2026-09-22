# failure-learning-rl

A Claude Code plugin with a reinforcement-learning agent that fails, learns from the failure, changes
its approach, and retries until it succeeds.

- **Command** `/rl-demo [--seed N] [--map FILE] [--max-episodes N] [--max-steps N] [--quiet]`: trains
  the agent and reports failures, lessons, and the final route.
- **Skill** `failure-learning-rl`: guidance for adapting the agent to new maps or environments.
- **Code** in `scripts/` (Python 3.8+, standard library only, no pip install needed); tests in
  `tests/` (pytest — `pip install pytest` to run them).

## Try it locally

```
claude --plugin-dir path/to/failure-learning-rl
```

Then run `/rl-demo`, or directly (use `python3` instead of `python` on Linux/macOS if needed):

```
python scripts/train.py --seed 0
python -m pytest tests -q
```
