import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.speed = 5
        self.image = pygame.image.load("Assets/icons/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.obstacles = []

    def update(self, player, enemy, bullets,rate_scroll):
        self.rect.x += self.direction * self.speed + rate_scroll
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
        for tile in self.obstacles:
            if tile[1].colliderect(self.rect):
                self.kill()
        if pygame.sprite.spritecollide(player, bullets, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullets, False):
            if enemy.alive:
                enemy.health -= 20
                self.kill()