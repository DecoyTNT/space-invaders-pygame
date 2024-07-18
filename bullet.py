import pygame

class Bullet():
    def __init__(self, position_x, position_y, img, screen):
        self.position_x = position_x
        self.position_y = position_y
        self.img = img
        self.screen = screen
        self.speed = 3
    
    def shoot(self):
        img_bullet = pygame.image.load(self.img)
        self.screen.blit(img_bullet, (self.position_x, self.position_y))
    
    def move(self):
        self.position_y -= self.speed
        self.shoot()