"""Deterministic gridworld: reach the goal without falling in a trap or running out of steps."""

ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
ACTION_NAMES = ["up", "down", "left", "right"]

STEP_REWARD = -1
TRAP_REWARD = -50
GOAL_REWARD = 100

DEFAULT_MAP = [
    "S.....",
    ".###T.",
    "...#..",
    "T..#.#",
    "......",
    ".#T.TG",
]


class GridWorld:
    def __init__(self, layout=None, max_steps=60):
        layout = DEFAULT_MAP if layout is None else layout
        self.max_steps = max_steps
        self._parse(layout)
        self.reset()

    def _parse(self, layout):
        if not layout or len({len(row) for row in layout}) != 1:
            raise ValueError("layout must be non-empty with equal-length rows")
        self.rows, self.cols = len(layout), len(layout[0])
        self.walls, self.traps = set(), set()
        starts, goals = [], []
        for r, row in enumerate(layout):
            for c, ch in enumerate(row):
                if ch == "#":
                    self.walls.add((r, c))
                elif ch == "T":
                    self.traps.add((r, c))
                elif ch == "S":
                    starts.append((r, c))
                elif ch == "G":
                    goals.append((r, c))
                elif ch != ".":
                    raise ValueError(f"unknown map character {ch!r}")
        if len(starts) != 1 or len(goals) != 1:
            raise ValueError("layout needs exactly one 'S' and one 'G'")
        self.start, self.goal = starts[0], goals[0]

    def reset(self):
        self.pos = self.start
        self.steps = 0
        return self.pos

    def step(self, action):
        """Return (state, reward, done, outcome); outcome is 'goal', 'trap', 'timeout' or None."""
        dr, dc = ACTIONS[action]
        r, c = self.pos[0] + dr, self.pos[1] + dc
        if 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.walls:
            self.pos = (r, c)
        self.steps += 1

        if self.pos == self.goal:
            return self.pos, GOAL_REWARD, True, "goal"
        if self.pos in self.traps:
            return self.pos, TRAP_REWARD, True, "trap"
        if self.steps >= self.max_steps:
            return self.pos, STEP_REWARD, True, "timeout"
        return self.pos, STEP_REWARD, False, None
