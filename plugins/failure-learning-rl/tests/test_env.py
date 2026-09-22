import pytest

from env import GOAL_REWARD, STEP_REWARD, TRAP_REWARD, GridWorld

UP, DOWN, LEFT, RIGHT = range(4)


def test_step_reward_and_move():
    env = GridWorld(["S.G"])
    assert env.step(RIGHT) == ((0, 1), STEP_REWARD, False, None)


def test_wall_bump_keeps_position():
    env = GridWorld(["S#G", "..."])
    state, reward, done, _ = env.step(RIGHT)
    assert (state, reward, done) == ((0, 0), STEP_REWARD, False)


def test_edge_bump_keeps_position():
    env = GridWorld(["S.G"])
    assert env.step(UP)[0] == (0, 0)


def test_goal_and_trap_terminate():
    assert GridWorld(["SG"]).step(RIGHT) == ((0, 1), GOAL_REWARD, True, "goal")
    assert GridWorld(["ST.G"]).step(RIGHT) == ((0, 1), TRAP_REWARD, True, "trap")


def test_timeout_after_max_steps():
    env = GridWorld(["S.G"], max_steps=2)
    env.step(RIGHT)
    assert env.step(LEFT) == ((0, 0), STEP_REWARD, True, "timeout")


def test_goal_on_final_step_beats_timeout():
    assert GridWorld(["SG"], max_steps=1).step(RIGHT) == ((0, 1), GOAL_REWARD, True, "goal")


def test_reset_restores_start():
    env = GridWorld(["S.G"])
    env.step(RIGHT)
    assert env.reset() == (0, 0) and env.steps == 0


@pytest.mark.parametrize("layout", [[], ["S.", "G"], ["..G"], ["S.GG"], ["SxG"]])
def test_invalid_layouts_raise(layout):
    with pytest.raises(ValueError):
        GridWorld(layout)
