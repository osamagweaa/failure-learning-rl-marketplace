# failure-learning-rl

A Claude Code plugin with a reinforcement-learning agent that fails, learns from the failure, changes
its approach, and retries until it succeeds.

- **Command** `/rl-demo [--seed N] [--map FILE] [--max-episodes N] [--quiet]`: trains the agent and
  reports failures, lessons, and the final route.
- **Skill** `failure-learning-rl`: guidance for adapting the agent to new maps or environments.
- **Code** in `scripts/` (Python 3.9+, standard library only); tests in `tests/` (pytest).

## Try it locally

```
claude --plugin-dir path/to/failure-learning-rl
```

Then run `/rl-demo`, or directly:

```
python scripts/train.py --seed 0
python -m pytest tests -q
```
