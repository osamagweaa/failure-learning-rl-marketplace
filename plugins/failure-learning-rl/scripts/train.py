"""Retry loop: keep training until the agent reliably completes the task."""

import argparse
import sys
from dataclasses import dataclass, field

from agent import FailureLearningAgent
from env import ACTION_NAMES, GridWorld


@dataclass
class Result:
    solved: bool
    episodes: int
    failures: int
    path: list = field(default_factory=list)


def run_episode(env, agent, learn=True):
    """Play one episode. Returns (outcome, trajectory of (state, action), visited states)."""
    state = env.reset()
    trajectory, path, outcome, done = [], [state], None, False
    while not done:
        action = agent.choose_action(state, explore=learn)
        next_state, reward, done, outcome = env.step(action)
        if learn:
            agent.update(state, action, reward, next_state, done)
        trajectory.append((state, action))
        path.append(next_state)
        state = next_state
    return outcome, trajectory, path


def train(env, agent, max_episodes=5000, solved_streak=3, verbose=True):
    failures, streak, path = 0, 0, []
    for episode in range(1, max_episodes + 1):
        outcome, trajectory, _ = run_episode(env, agent, learn=True)
        if outcome == "goal":
            agent.learn_from_success()
        else:
            failures += 1
            lesson = agent.learn_from_failure(trajectory, outcome)
            if verbose and (failures <= 10 or failures % 100 == 0):
                state, action = trajectory[-1]
                print(f"episode {episode}: FAILED ({outcome}) at {state} after "
                      f"'{ACTION_NAMES[action]}' -> {lesson}")

        greedy_outcome, _, path = run_episode(env, agent, learn=False)
        streak = streak + 1 if greedy_outcome == "goal" else 0
        if streak >= solved_streak:
            return Result(True, episode, failures, path)
    return Result(False, max_episodes, failures, path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Train an RL agent that learns from its failures.")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--map", help="text file, one grid row per line (S start, G goal, # wall, T trap, . floor)")
    parser.add_argument("--max-episodes", type=int, default=5000)
    parser.add_argument("--quiet", action="store_true", help="hide per-failure lessons")
    args = parser.parse_args(argv)

    try:
        layout = None
        if args.map:
            with open(args.map, encoding="utf-8") as f:
                layout = [line.strip() for line in f if line.strip()]
        env = GridWorld(layout)
    except (OSError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 2

    result = train(env, FailureLearningAgent(seed=args.seed),
                   max_episodes=args.max_episodes, verbose=not args.quiet)
    status = "SOLVED" if result.solved else "NOT SOLVED"
    print(f"\n{status} after {result.episodes} episodes ({result.failures} failures)")
    if result.solved:
        print("route:", " -> ".join(map(str, result.path)))
    return 0 if result.solved else 1


if __name__ == "__main__":
    sys.exit(main())
