# game.py
# setup for Baboom
# Haroon Khalid
# 08/19/2009

import pygame
import random
import os
from sys import exit

class Bomber:
    def __init__(self, screen_name, check):
        self.screen = screen_name
        self.image = pygame.image.load(os.path.join('graphics', 'bomber.png'))
        self.image.set_colorkey((46,167,0))
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 30
        self.ticks = 0
        self.b_ticks = 0
        self.move = 0
        self.bombs = []
        self.dropped = 0
        self.check = check
        self.font = pygame.font.Font(None, 100)
        self.score = 0
        self.game_over = 0
        self.sizzle = pygame.mixer.Sound(os.path.join('sounds', 'sizzle.ogg'))
        self.explode = pygame.mixer.Sound(os.path.join('sounds', 'explode.ogg'))
        self.caught = pygame.mixer.Sound(os.path.join('sounds', 'caught.ogg'))
        
    def create_bomb(self, speed):
        self.dropped += 1
        self.b_ticks = pygame.time.get_ticks()
        self.b = Bomb(self.screen, speed)
        self.b.rect.x = self.rect.x + 17
        self.b.rect.y = self.rect.y + 40
        self.bombs.append(self.b)
        self.sizzle.play()
 
    def update_bombs(self):
        for b in self.bombs:
            if b.rect.y > 320:
                self.explode.play()
                self.bombs.remove(b)
                self.game_over = 1
            b.update()
            
    def move_bomber(self, time_secs, bomb_y, bomber_x, low, high):
        self.secs = time_secs
        self.bomb_y = bomb_y
        self.bomber_x = bomber_x
        self.low = low
        self.high = high

        self.current_ticks = pygame.time.get_ticks()
        if (self.current_ticks > (self.ticks + self.secs)):
            random.seed()
            self.move = random.randint(0,1)
            self.ticks = pygame.time.get_ticks()
            self.create_bomb(self.bomb_y)
            
        if self.move == 0:
            self.rect.x += self.bomber_x
            self.boundry(low,high)
        else:
            self.rect.x -= self.bomber_x
            self.boundry(low,high)
                
    def set_move(self):
        if self.dropped <= 10:
            self.move_bomber(800,3,5,210,250)
        elif self.dropped > 10 and self.dropped <= 20:
            self.move_bomber(600,4,10,100,350)
        elif self.dropped > 20 and self.dropped <= 30:
            self.move_bomber(500,5,15,50, 400)
        elif self.dropped > 30 and self.dropped < 40:
            self.move_bomber(300,6,20,10,460)
        elif self.dropped > 40 and self.dropped < 50:
            self.move_bomber(200,7,25,10,460) 
        elif self.dropped > 50 and self.dropped < 60:
            self.move_bomber(100,8,30,10,460)  
            
    def drop_bomb(self):
        self.drop_current_ticks = pygame.time.get_ticks()
        
    def boundry(self, low, high):
        if self.rect.x > high:
            self.rect.x = high
        if self.rect.x < low:
            self.rect.x = low
            
    def check_hit(self):
        for b in self.bombs:
            if b.rect.colliderect(self.check.rect):
                self.caught.play()
                self.score += 10
                if b in self.bombs:
                    self.bombs.remove(b)
        
    def update(self):
        if self.game_over == 1:
            self.score_text = self.font.render("GAME OVER", True, (255,0,0))
            self.screen.blit(self.score_text, (30, 130))
        else:
            self.set_move()
            self.check_hit()
            self.screen.blit(self.image, (self.rect.x,self.rect.y))
            self.update_bombs()
    

class Bomb:
    def __init__(self, screen_name, speed):
        self.screen = screen_name
        self.image = pygame.image.load(os.path.join('graphics', 'bomb.png'))
        self.image.set_colorkey((46,167,0))
        self.rect = self.image.get_rect()
        self.rect.x = 220
        self.rect.y = 200
        self.loop = 1
        self.speed = speed
         
    def update(self):
        self.rect.y += self.speed
        self.screen.blit(self.image, (self.rect.x,self.rect.y))

class Player:
    def __init__(self, screen_name):
        self.screen = screen_name
        self.image = pygame.image.load(os.path.join('graphics', 'player.png'))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 220
        self.rect.y = 250
        self.loop = 1
        self.score = 0
 
    def get_input(self):
        #Get the current key state.
        key = pygame.key.get_pressed()
        
        #Move left/right
        if key[pygame.K_LEFT]:
            self.rect.x -= 15
        if key[pygame.K_RIGHT]:
            self.rect.x += 15
            
    def boundry(self):
        if self.rect.x > 422:
            self.rect.x = 422
        if self.rect.x < 20:
            self.rect.x = 20
            
    def run(self):
        self.get_input()
        self.boundry()
        self.screen.blit(self.image, (self.rect.x,self.rect.y))

                    
class Level_1:
    def __init__(self, screen_name):
        self.screen = screen_name
        self.background = pygame.image.load(os.path.join('graphics', 'background.png'))
        self.loop = 1
        self.p1 = Player(self.screen)
        self.b1 = Bomber(self.screen, self.p1)
        self.font = pygame.font.Font(None, 28)
       
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_RETURN:
                    print "RETURN HIT"

    def run(self):
        while self.loop == 1:
            self.get_input()
            self.screen.fill((255,255,255))
            self.screen.blit(self.background, (0,0))
            self.p1.run()
            self.b1.update()
            self.score_text = self.font.render("SCORE: " + str(self.b1.score), True, (255,255,255))
            self.screen.blit(self.score_text, (10, 10))
            pygame.display.update()
            pygame.time.delay(25)

class Intro:
    def __init__(self, screen_name):
        self.screen = screen_name
        self.intro_screen = pygame.image.load(os.path.join('graphics', 'intro_screen.png'))
        self.loop = 1
        self.lev_1 = Level_1(self.screen)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_RETURN:
                    print "RETURN HIT"
                    self.loop = 0
                    self.lev_1.run()
                    break

    def run(self):
        while self.loop == 1:
            #print "running in: Intro class"
            self.get_input()
            self.screen.fill((255,255,255))
            self.screen.blit(self.intro_screen, (0,0))
            pygame.display.update()
            pygame.time.delay(25)

class Setup:
    def __init__(self):
        self.resolution = (480, 320)
        self.screen = pygame.display.set_mode(self.resolution, 0, 32)
        self.window_title = pygame.display.set_caption("Baboom")
        self.start_screen = Intro(self.screen)

    def run(self):
        self.start_screen.run()