# Design notes

## Components
- `scripts/env.py`: `GridWorld`, deterministic. Rewards: -1 per step, -50 trap, +100 goal.
  Episode ends on goal, trap, or `max_steps` (default 60, outcome `timeout`).
- `scripts/agent.py`: `FailureLearningAgent`, Q-table with alpha 0.5, gamma 0.95, epsilon-greedy,
  plus `failure_memory[(state, action)] -> count`.
- `scripts/train.py`: `train(env, agent, max_episodes=5000, solved_streak=3) -> Result(solved,
  episodes, failures, path)` and a CLI.

## Why these choices
- Zero-initialized Q with negative step rewards is optimistic, which drives early exploration.
- Failure memory makes "try a different approach" explicit: exploration is restricted to the least
  failed actions from each state, rather than uniformly random.
- Evaluating with a greedy rollout after each episode separates "the agent got lucky while exploring"
  from "the learned policy works".
- The episode cap guarantees termination on unsolvable maps; the result reports `solved=False`.

## Tests (`tests/`)
1. Env: rewards, wall/edge bump, trap/goal/timeout termination, invalid layouts raise.
2. Agent: penalty on last K pairs, epsilon raise/cap/decay, exploration avoids failed actions.
3. Train: at least one failure then success, route avoids traps, same seed reproduces, solves across
   seeds 0-4, unsolvable map stops at the cap.
