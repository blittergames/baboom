# game.py
# setup for Baboom
# Haroon Khalid
# 08/19/2009

import pygame
import random
import os
from sys import exit

class Bomber:
    def __init__(self, screen_name):
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
        
    def create_bomb(self):
        self.dropped += 1
        self.b_ticks = pygame.time.get_ticks()
        self.b = Bomb(self.screen)
        self.b.rect.x = self.rect.x + 17
        self.b.rect.y = self.rect.y + 40
        self.bombs.append(self.b)
        #self.b.sizzle.play()
 
    def update_bombs(self):
        for b in self.bombs:
            if b.rect.y > 320:
                #self.b.explode.play()
                self.bombs.remove(b)
            b.update()
        
    def set_move(self):
        self.current_ticks = pygame.time.get_ticks()
        if (self.current_ticks > (self.ticks + 500)):
            random.seed()
            self.move = random.randint(0,1)
            self.ticks = pygame.time.get_ticks()
            self.create_bomb()
            
        if self.move == 0:
            self.rect.x += 2
            #self.ticks = pygame.time.get_ticks()
        else:
            self.rect.x -= 2
            #self.ticks = pygame.time.get_ticks()
        print "/////////////////////////////////"    
        print "self.move: " + str(self.move)
        print "self.ticks: " + str(self.ticks)
        print "self.current_ticks: " + str(self.current_ticks)
        print "/////////////////////////////////"    
        
    def boundry(self):
        if self.rect.x > 422:
            self.rect.x = 422
        if self.rect.x < 20:
            self.rect.x = 20
        
    def update(self):
        #self.spawn_bombs()
        self.set_move()
        self.boundry()
        self.screen.blit(self.image, (self.rect.x,self.rect.y))
        self.update_bombs()
    

class Bomb:
    def __init__(self, screen_name):
        self.screen = screen_name
        self.image = pygame.image.load(os.path.join('graphics', 'bomb.png'))
        self.image.set_colorkey((81, 81, 81))
        self.rect = self.image.get_rect()
        self.rect.x = 220
        self.rect.y = 200
        self.loop = 1
        self.sizzle = pygame.mixer.Sound(os.path.join('sounds', 'sizzle.ogg'))
        self.explode = pygame.mixer.Sound(os.path.join('sounds', 'explode.ogg'))
         
    def update(self):
        self.rect.y += 7
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
        self.caught = pygame.mixer.Sound(os.path.join('sounds', 'caught.ogg'))
        self.font = pygame.font.Font(None, 16)
 
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
        self.score_text = self.font.render("SCORE: " + str(self.score), True, (255,255,255))
        self.screen.blit(self.score_text, (10, 10))
                    
class Level_1:
    def __init__(self, screen_name):
        self.screen = screen_name
        self.background = pygame.image.load(os.path.join('graphics', 'background.png'))
        self.loop = 1
        self.p1 = Player(self.screen)
        self.b1 = Bomber(self.screen)
        self.bombs = []
        self.ticks = 0
        self.bombs_dropped = 0
        
    def check_hit(self):
        for b in self.bombs:
            if b.rect.colliderect(self.p1.rect):
                self.p1.caught.play()
                self.p1.score += 10
                print "-------------HIT---------------"
                
                if b in self.bombs:
                    self.bombs.remove(b)
       
    def create_bomb(self):
        self.ticks = pygame.time.get_ticks()
        self.b = Bomb(self.screen)
        random.seed()
        self.b.rect.x = random.randrange(10, 430)
        self.b.rect.y = 80    
        self.bombs.append(self.b)
        self.b.sizzle.play()
 
    def update_bombs(self):
        for b in self.bombs:
            if b.rect.y > 320:
                self.b.explode.play()
                self.bombs.remove(b)
            b.update()
    
    def spawn_bombs(self):
        #print "current_tick: " + str(current_ticks)
        #print "self.ticks: " + str(self.ticks + 1000)  
        current_ticks = pygame.time.get_ticks()
        if (current_ticks > (self.ticks + 1000) and (self.bombs_dropped < 11)):
            self.create_bomb()
            self.bombs_dropped += 1
            print str(self.bombs_dropped)
        
        if (current_ticks > (self.ticks + 500) and (self.bombs_dropped > 10)):
                self.create_bomb()
                self.bombs_dropped += 1
                print str(self.bombs_dropped)
               
            #print "///////////////////////"
            #print "current_tick: " + str(current_ticks)
            #print "self.ticks: " + str(self.ticks + 1000)
            #print "///////////////////////"



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
            #print "running in: Level 1 class"
            self.get_input()
            self.screen.fill((255,255,255))
            self.screen.blit(self.background, (0,0))
            self.check_hit()
            self.p1.run()
            #self.spawn_bombs()
            self.update_bombs()
            self.b1.update()
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