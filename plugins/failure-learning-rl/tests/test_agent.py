from agent import TIMEOUT_PENALTY, TRAP_PENALTY, FailureLearningAgent


def test_update_moves_q_toward_target():
    agent = FailureLearningAgent(alpha=0.5, gamma=0.9)
    agent.update((0, 0), 3, 10, (0, 1), True)
    assert agent.q[((0, 0), 3)] == 5.0


def test_failure_penalizes_last_k_and_raises_epsilon():
    agent = FailureLearningAgent(epsilon=0.2, lookback=2)
    trajectory = [((0, 0), 0), ((0, 1), 3), ((0, 2), 3)]
    agent.learn_from_failure(trajectory, "trap")
    assert agent.q[((0, 0), 0)] == 0
    assert agent.q[((0, 1), 3)] == -TRAP_PENALTY
    assert agent.q[((0, 2), 3)] == -TRAP_PENALTY
    assert agent.failure_memory[((0, 2), 3)] == 1
    assert agent.epsilon > 0.2


def test_timeout_penalty_is_milder_than_trap():
    agent = FailureLearningAgent()
    agent.learn_from_failure([((0, 0), 0)], "timeout")
    assert agent.q[((0, 0), 0)] == -TIMEOUT_PENALTY > -TRAP_PENALTY


def test_epsilon_is_capped_and_decays_on_success():
    agent = FailureLearningAgent(epsilon=0.5, eps_max=0.6, eps_min=0.05)
    agent.learn_from_failure([((0, 0), 0)], "trap")
    assert agent.epsilon == 0.6
    agent.learn_from_success()
    assert agent.epsilon < 0.6


def test_exploration_avoids_actions_that_failed_before():
    agent = FailureLearningAgent(epsilon=1.0, seed=1)
    for action in (0, 1, 2):
        agent.failure_memory[((0, 0), action)] = 3
    assert {agent.choose_action((0, 0)) for _ in range(20)} == {3}


def test_greedy_picks_highest_q():
    agent = FailureLearningAgent()
    agent.q[((0, 0), 2)] = 5
    assert agent.choose_action((0, 0), explore=False) == 2
