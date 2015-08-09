from gamelib import logicfactory
import pygame

def main():
    pygame.init()
    engine = logicfactory.GameEngine()
    engine.run_game(30)


if __name__ == '__main__':
    main()