from gamelib import logicfactory
import pygame
from gamelib.constants import GAME

def main():
    pygame.init()
    engine = logicfactory.GameEngine()
    engine.run_game(GAME.fps)


if __name__ == '__main__':
    main()