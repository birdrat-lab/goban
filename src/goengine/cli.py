# src/goengine/cli.py
from .game import Game
from .move import Move

def parse_coord(s: str):
    # simple "row col" parser
    row, col = map(int, s.split())
    return row, col

def main():
    game = Game(size=9)
    while not game.is_over:
        # print board + prompt etc.
        # build Move and call game.play(...)
        ...

if __name__ == "__main__":
    main()
