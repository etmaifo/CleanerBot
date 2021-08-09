from rich.traceback import install
install()

from gamelib import logicfactory
import pygame
from gamelib.constants import GAME

from rich.console import Console

console = Console()

def main():
    console.log("Starting game...")
    pygame.init()
    engine = logicfactory.GameEngine()
    engine.run_game(GAME.fps)


if __name__ == '__main__':
    main()