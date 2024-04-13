from snid.game_of_life import GameOfLife
from snid.tetris import Tetris
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="Snid's Grid & Sid", description='Choose a game to play')
    parser.add_argument(
        '-g', '--game', choices=['gol', 'tetris'], required=True)
    args = parser.parse_args()
    if args.game == 'gol':
        GameOfLife().tick()
    if args.game == 'tetris':
        Tetris().tick()
