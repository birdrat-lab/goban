from .board import Board, BLACK, WHITE, opponent
from .move import Move

class Game:
    def __init__(self, size=19, komi=7.5, superko=True):
        self.board = Board(size)
        self.komi = komi
        self.superko = superko

        self.to_play = BLACK  # BLACK starts
        self.moves: List[Move] = []
        self.passes_in_a_row = 0
        self.position_history = set()
        self.position_history.add(self._hash_position())

        self.is_over = False

    def _hash_position(self):
        # Simple hash; later use Zobrist for speed
        return tuple(tuple(row) for row in self.board.grid)

    def play(self, move: Move) -> bool:
        if self.is_over:
            return False

        color_int = BLACK if move.color == "B" else WHITE
        if color_int != self.to_play:
            return False

        if move.is_resign:
            self.is_over = True
            self.moves.append(move)
            return True

        if move.point is None:  # pass
            self.moves.append(move)
            self.passes_in_a_row += 1
            self.to_play = opponent(self.to_play)
            if self.passes_in_a_row >= 2:
                self.is_over = True
            return True

        # normal move
        self.passes_in_a_row = 0
        snapshot = self.board.copy()

        if not self.board.place_and_resolve(color_int, move.point):
            return False

        # ko / superko check
        pos_hash = self._hash_position()
        if self.superko and pos_hash in self.position_history:
            # illegal: repeats a previous position
            self.board = snapshot
            return False

        self.position_history.add(pos_hash)
        self.moves.append(move)
        self.to_play = opponent(self.to_play)
        return True
