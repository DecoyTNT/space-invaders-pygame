import pygame
from character import Character

class Player(Character):        
    def __init__(self, position_x, position_y, img, screen):
        super().__init__(position_x, position_y, img)
        self.screen = screen
        self.speed = 2
        self.position_x_change = 0

    def move(self, direction):
        if direction == 'left':
            self.position_x_change -= self.speed
        if direction == 'right':
            self.position_x_change += self.speed
            
    def stop_move(self):
        self.position_x_change = 0
    
    def update(self):
        self.position_x += self.position_x_change
        if self.position_x < 0:
            self.position_x = 0
        if self.position_x > self.screen.get_width() - 64:
            self.position_x = self.screen.get_width() - 64
    
    def make_player(self):
        img_player = pygame.image.load(self.img)
        self.screen.blit(img_player, (self.position_x, self.position_y))

