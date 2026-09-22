"""Q-learning agent that turns each failed episode into a lesson and explores differently next time."""

import random
from collections import defaultdict

TRAP_PENALTY = 20
TIMEOUT_PENALTY = 5


class FailureLearningAgent:
    def __init__(self, n_actions=4, alpha=0.5, gamma=0.95, epsilon=0.3,
                 eps_min=0.05, eps_max=0.6, lookback=3, seed=0):
        self.n_actions = n_actions
        self.alpha, self.gamma = alpha, gamma
        self.epsilon, self.eps_min, self.eps_max = epsilon, eps_min, eps_max
        self.lookback = lookback
        self.rng = random.Random(seed)
        self.q = defaultdict(float)
        self.failure_memory = defaultdict(int)  # (state, action) -> times it preceded a failure

    def _failures(self, state, action):
        return self.failure_memory[(state, action)]

    def greedy_action(self, state):
        best = max(self.q[(state, a)] for a in range(self.n_actions))
        ties = [a for a in range(self.n_actions) if self.q[(state, a)] == best]
        return self._least_failed(state, ties)

    def _least_failed(self, state, actions):
        fewest = min(self._failures(state, a) for a in actions)
        return self.rng.choice([a for a in actions if self._failures(state, a) == fewest])

    def choose_action(self, state, explore=True):
        if explore and self.rng.random() < self.epsilon:
            # a different approach: only try the actions that have failed least from here
            return self._least_failed(state, list(range(self.n_actions)))
        return self.greedy_action(state)

    def update(self, state, action, reward, next_state, done):
        future = 0.0 if done else max(self.q[(next_state, a)] for a in range(self.n_actions))
        target = reward + self.gamma * future
        self.q[(state, action)] += self.alpha * (target - self.q[(state, action)])

    def learn_from_failure(self, trajectory, reason):
        """trajectory: list of (state, action). Penalize the decisions that led to the failure."""
        penalty = TRAP_PENALTY if reason == "trap" else TIMEOUT_PENALTY
        culprits = trajectory[-self.lookback:]
        for state, action in culprits:
            self.q[(state, action)] -= penalty
            self.failure_memory[(state, action)] += 1
        self.epsilon = min(self.eps_max, self.epsilon * 1.5)
        return f"penalized last {len(culprits)} moves ({reason}); epsilon -> {self.epsilon:.2f}"

    def learn_from_success(self):
        self.epsilon = max(self.eps_min, self.epsilon * 0.9)
