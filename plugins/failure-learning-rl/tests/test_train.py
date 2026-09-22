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
    env = GridWorld()
    result = train(env, FailureLearningAgent(seed=0), verbose=False)
    assert result.failures >= 1
    assert result.solved
    assert result.path[0] == env.start and result.path[-1] == env.goal


def test_route_is_a_valid_walk():
    env = GridWorld()
    result = train(env, FailureLearningAgent(seed=0), verbose=False)
    assert result.solved
    for (r0, c0), (r1, c1) in zip(result.path, result.path[1:]):
        assert abs(r0 - r1) + abs(c0 - c1) == 1, "route must move one cell at a time"
        assert 0 <= r1 < env.rows and 0 <= c1 < env.cols
        assert (r1, c1) not in env.walls and (r1, c1) not in env.traps


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
