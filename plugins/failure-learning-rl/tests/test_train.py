from collections import deque

from agent import FailureLearningAgent
from env import GridWorld
from train import train


def reachable(env):
    seen, queue = {env.start}, deque([env.start])
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nxt = (r + dr, c + dc)
            if (0 <= nxt[0] < env.rows and 0 <= nxt[1] < env.cols
                    and nxt not in env.walls and nxt not in env.traps and nxt not in seen):
                seen.add(nxt)
                queue.append(nxt)
    return env.goal in seen


def test_default_map_is_solvable():
    assert reachable(GridWorld())


def test_agent_fails_then_succeeds():
    result = train(GridWorld(), FailureLearningAgent(seed=0), verbose=False)
    assert result.failures >= 1
    assert result.solved
    assert result.path[0] == (0, 0) and result.path[-1] == (5, 5)


def test_route_avoids_traps():
    env = GridWorld()
    result = train(env, FailureLearningAgent(seed=0), verbose=False)
    assert not set(result.path) & env.traps


def test_same_seed_is_reproducible():
    a = train(GridWorld(), FailureLearningAgent(seed=7), verbose=False)
    b = train(GridWorld(), FailureLearningAgent(seed=7), verbose=False)
    assert (a.episodes, a.failures, a.path) == (b.episodes, b.failures, b.path)


def test_solves_across_seeds():
    for seed in range(5):
        assert train(GridWorld(), FailureLearningAgent(seed=seed), verbose=False).solved


def test_unsolvable_map_stops_at_cap():
    env = GridWorld(["S..#..", "...#..", "...#..", "...#..", "...#..", "...#.G"])
    assert not reachable(env)
    result = train(env, FailureLearningAgent(seed=0), max_episodes=50, verbose=False)
    assert not result.solved and result.episodes == 50
