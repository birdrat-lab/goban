from dataclasses import dataclass
from typing import Optional, Tuple, Literal

Color = Literal["B", "W"]
Point = Tuple[int, int]  # (row, col), 0-indexed

@dataclass(frozen=True)
class Move:
    color: Color
    point: Optional[Point]  # None means pass
    is_resign: bool = False
