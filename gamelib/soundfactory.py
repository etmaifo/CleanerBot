import pygame
import os

class Music(object):
    def __init__(self, music_file, volume, loop):
        music = os.path.join("assets", "music", music_file)
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(volume)
        #pygame.mixer.music.play(-1)

    def play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def fadeout(self, timeout):
        pygame.mixer.music.fadeout(timeout)

