import os
import pygame

from Bullet import Bullet


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, type, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.in_air = True
        self.type = type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.alive = True
        self.jump = False
        self.y = 0
        self.shooting = False
        self.SHOOTING_COOLDOWN = 0
        self.ammo = ammo
        self.health = 100
        self.max_health = self.health
        self.time = pygame.time.get_ticks()
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp = []
            for i in range(len(os.listdir(f'Assets/{type}/{animation}'))):
                img = pygame.image.load(f'Assets/{type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp.append(img)
            self.animation_list.append(temp)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks() - self.time > ANIMATION_COOLDOWN:
            self.time = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.animation_list[self.action]):
            if not self.alive:
                self.index = len(self.animation_list[self.action]) - 1
            else:
                self.index = 0

    def update_action(self, action):
        if action != self.action:
            self.action = action
            self.index = 0
            self.time = pygame.time.get_ticks()

    def move(self, moving_right, moving_left):
        y = 0
        if moving_right:
            self.rect.x += self.speed
            self.flip = False
            self.direction = 1
        elif moving_left:
            self.rect.x -= self.speed
            self.flip = True
            self.direction = -1

        if self.jump == True and self.in_air == False:
            self.y = -11
            self.jump = False
            self.in_air = True
        y += self.y
        self.y += 0.75

        y += self.y

        # check collision with floor
        if self.rect.bottom + y > 440:
            y = 440 - self.rect.bottom
            self.in_air = False
        self.rect.y += y

    def shoot(self, bullets):
        if self.SHOOTING_COOLDOWN == 0 and self.ammo > 0:
            self.ammo -= 1
            self.SHOOTING_COOLDOWN = 20
            _bullet = Bullet((self.rect.centerx + (self.rect.size[0] * 0.6 * self.direction)), self.rect.centery,
                             self.direction)
            bullets.add(_bullet)
        return bullets

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.SHOOTING_COOLDOWN > 0:
            self.SHOOTING_COOLDOWN -= 1

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
