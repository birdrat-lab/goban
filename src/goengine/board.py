from typing import List, Set, Iterable, Optional
import copy

from .move import Point

EMPTY = 0
BLACK = 1
WHITE = 2

def opponent(color_int: int) -> int:
    return BLACK if color_int == WHITE else WHITE

class Board:
    def __init__(self, size: int = 19):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]

    def copy(self) -> "Board":
        b = Board(self.size)
        b.grid = copy.deepcopy(self.grid)
        return b

    def in_bounds(self, p: Point) -> bool:
        r, c = p
        return 0 <= r < self.size and 0 <= c < self.size

    def get(self, p: Point) -> int:
        r, c = p
        return self.grid[r][c]

    def set(self, p: Point, val: int):
        r, c = p
        self.grid[r][c] = val

    def neighbors(self, p: Point) -> Iterable[Point]:
        r, c = p
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            q = (r+dr, c+dc)
            if self.in_bounds(q):
                yield q

    # --- group as a derived concept ---
    def collect_group(self, start: Point) -> Set[Point]:
        color = self.get(start)
        assert color != EMPTY
        stack = [start]
        group = set([start])
        while stack:
            p = stack.pop()
            for q in self.neighbors(p):
                if q not in group and self.get(q) == color:
                    group.add(q)
                    stack.append(q)
        return group

    def liberties(self, group: Set[Point]) -> Set[Point]:
        libs = set()
        for p in group:
            for q in self.neighbors(p):
                if self.get(q) == EMPTY:
                    libs.add(q)
        return libs

    def remove_group(self, group: Set[Point]):
        for p in group:
            self.set(p, EMPTY)

    def place_and_resolve(self, color_int: int, p: Point) -> bool:
        """
        Attempt to play at p. If legal, mutate board and return True.
        If illegal, leave board unchanged and return False.
        """
        if self.get(p) != EMPTY:
            return False

        snapshot = self.copy()
        self.set(p, color_int)

        # 1. capture adjacent enemy groups with no liberties
        captured_any = False
        for q in self.neighbors(p):
            if self.get(q) == opponent(color_int):
                enemy_group = self.collect_group(q)
                if len(self.liberties(enemy_group)) == 0:
                    self.remove_group(enemy_group)
                    captured_any = True

        # 2. check suicide: your new group must have liberties unless captured
        my_group = self.collect_group(p)
        if len(self.liberties(my_group)) == 0 and not captured_any:
            # illegal suicide: revert
            self.grid = snapshot.grid
            return False

        return True
