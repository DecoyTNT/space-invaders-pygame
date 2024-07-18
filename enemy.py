from character import Character
import pygame
from random import choice

images = ['assets/enemigo.png', 'assets/enemigo2.png', 'assets/enemigo3.png', 'assets/enemigo4.png', 'assets/enemigo5.png' ]

class Enemy(Character):
    def __init__(self, position_x, position_y, screen):
        super().__init__(position_x, position_y, choice(images))
        self.screen = screen
        self.speed = choice([-1,1])
        self.position_x_change = 0
        self.position_y_change = 0.2

    def move(self):
        self.position_x_change = self.speed
        if self.position_x >= self.screen.get_width() - 64:
            self.speed = -1
        elif self.position_x <= 0:
            self.speed = 1
    
    def update(self):
        self.position_x += self.position_x_change
        self.position_y += self.position_y_change
        if self.position_x < 0:
            self.position_x = 0
        if self.position_x > self.screen.get_width() - 64:
            self.position_x = self.screen.get_width() - 64
    
    def change_speed(self):
        self.speed = choice([-1,1])
    
    def make_enemy(self):
        img_enemy = pygame.image.load(self.img)
        self.screen.blit(img_enemy, (self.position_x, self.position_y))