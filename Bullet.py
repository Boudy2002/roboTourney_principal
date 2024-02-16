import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.speed = 10
        self.image = pygame.image.load("Assets/icons/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
