import pygame
import shelve
import os
from pygame.locals import *
from constants import COLOR, MENU, SCREEN, STATE, RESULT, FILES, GAME
from fontfactory import GameText
import pygame.mixer as mixer


class ScoreScreen(object):
    def __init__(self):
        mixer.init()
        self.timer = 0
        self.set_highscore(0)

        self.title = GameText("Scoreboard", 94)
        self.title.centerx = SCREEN.width / 2
        self.title.y = 48
        self.title.color = COLOR.half_black

        self.hi_score = GameText("Hi-score: 0", 38)
        self.hi_score.centerx = SCREEN.width / 2
        self.hi_score.y = 172
        self.hi_score.color = COLOR.light_gray

        self.p1 = GameText("P1", 24, True)
        self.p1.x = 92
        self.p1.y = 280
        self.p1.color = COLOR.blue_sea

        self.p2 = GameText("P2", 24, True)
        self.p2.x = 92
        self.p2.y = 340
        self.p2.color = COLOR.petal_green

        self.p1_scores = []
        self.p2_scores = []
        for i in xrange(5):
            p1_score = GameText("0", 24, True)
            p1_score.centerx = 92 + 144 + 96 * i
            p1_score.y = 280
            p1_score.color = COLOR.gray7
            self.p1_scores.append(p1_score)

            p2_score = GameText("0", 24, True)
            p2_score.centerx = 92 + 144 + 96 * i
            p2_score.y = 340
            p2_score.color = COLOR.gray7
            self.p2_scores.append(p2_score)

        self.p1_total = GameText("0", 24, True)
        self.p1_total.right = SCREEN.width - SCREEN.width/4
        self.p1_total.y = 280
        self.p1_total.color = COLOR.blue_sea

        self.p2_total = GameText("0", 24, True)
        self.p2_total.right = SCREEN.width - SCREEN.width/4
        self.p2_total.y = 340
        self.p2_total.color = COLOR.petal_green

        self.p1_results = GameText("", 24, True)
        self.p1_results.x = SCREEN.width - SCREEN.width/4 + 64
        self.p1_results.y = 280
        self.p1_results.color = COLOR.burnt_orange

        self.p2_results = GameText("", 24, True)
        self.p2_results.x = SCREEN.width - SCREEN.width/4 +64
        self.p2_results.y = 340
        self.p2_results.color = COLOR.burnt_orange

        self.bg = MENU.scoreScreen
        self.state = STATE.scorescreen
        self.stage = 1

        self.title.create()
        self.hi_score.create()
        self.p1.create()
        self.p2.create()

        for score in self.p1_scores:
            score.create()
        for score in self.p2_scores:
            score.create()

        self.p1_total.create()
        self.p2_total.create()
        self.p1_results.create()
        self.p2_results.create()

        self.controller = self.get_controller()

        self.select_sound = mixer.Sound(os.path.join("assets", "sfx", "sfx_twoTone.ogg"))
        self.select_sound.set_volume(0.5)

    def get_controller(self):
        number_of_joysticks = pygame.joystick.get_count()
        if number_of_joysticks > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            return joystick
        return None

    def handle_events(self, event):
        self.state = STATE.scorescreen

        if event.type == KEYDOWN:
            if event.key == K_e or event.key == K_RETURN:
                self.state = STATE.nextlevel
                self.select_sound.play()

        elif event.type == JOYBUTTONDOWN:
            if self.controller.get_button(0):
                self.state = STATE.nextlevel
                self.select_sound.play()

    def update(self, stage, player, hi_score):

        score1 = 0
        score2 = 0
        for i in range(len(self.p1_scores)):
            score1 += int(self.p1_scores[i].text)
            score2 += int(self.p2_scores[i].text)
        self.p1_total.text = str(score1)
        self.p2_total.text = str(score2)

        self.title.update()
        self.p1.update()
        self.p2.update()
        for score in self.p1_scores:
            score.update()
        for score in self.p2_scores:
            score.update()
        self.p1_total.update()
        self.p2_total.update()

        self.p1_results.text = ''
        self.p2_results.text = ''
        if stage == 5:
            if int(self.p1_total.text) > int(self.p2_total.text):
                self.p1_results.text = RESULT.win
            elif int(self.p1_total.text) < int(self.p2_total.text):
                self.p2_results.text = RESULT.win
            else:
                self.p1_results.text = RESULT.draw
                self.p2_results.text = RESULT.draw
        self.p1_results.update()
        self.p2_results.update()
        self.stage = stage

        p1_total = int(self.p1_total.text)
        p2_total = int(self.p2_total.text)
        if p1_total > self.get_highscore():
            self.set_highscore(p1_total)
        elif p2_total > self.get_highscore():
            self.set_highscore(p2_total)

        self.hi_score.text = "Hi-score: " + str(self.get_highscore())
        self.hi_score.update()

        self.animate_flash()

    def draw(self, screen):
        screen.fill(COLOR.black)
        screen.blit(self.bg, (0, 0))
        self.title.draw_to(screen)
        self.hi_score.draw_to(screen)
        self.p1.draw_to(screen)
        self.p2.draw_to(screen)

        for i in range(self.stage):
            self.p1_scores[i].draw_to(screen)
            self.p2_scores[i].draw_to(screen)

        self.p1_total.draw_to(screen)
        self.p2_total.draw_to(screen)
        self.p1_results.draw_to(screen)
        self.p2_results.draw_to(screen)

    def get_highscore(self):
        d = shelve.open(FILES.hiscore)
        score = d['score']
        return int(score)

    def set_highscore(self, score):
        d = shelve.open(FILES.hiscore)
        d['score'] = score
        d.close()

    def animate_flash(self):
        self.timer += 1
        if self.timer < GAME.fps/8:
            self.p1_results.color = COLOR.gray
            self.p2_results.color = COLOR.gray
        elif self.timer < GAME.fps/4:
            self.p1_results.color = COLOR.burnt_orange
            self.p2_results.color = COLOR.burnt_orange
        else:
            self.timer = 0
