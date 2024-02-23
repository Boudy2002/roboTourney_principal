import pygame


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = type
        self.image = pygame.image.load(f"Assets/icons/{type}_box.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 40 // 2, y + (40 - self.image.get_height()))

    def update(self, player,rate_scroll):
        self.rect.x += rate_scroll
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'ammo':
                player.ammo += 15
            self.kill()
