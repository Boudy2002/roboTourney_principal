import os
import random

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
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.move_counter = 0
        self.idle = False
        self.idle_counter = 0
        self.sight = pygame.Rect(0, 0, 150, 20)
        self.obstacles = []

    def set_obstacles(self,obstacle):
        self.obstacles = obstacle
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
        rate_scroll = 0
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump == True and self.in_air == False:
            self.y = -13
            self.jump = False
            self.in_air = True
        self.y += 0.75
        if self.y > 10:
            self.y
        dy += self.y
        for tile in self.obstacles:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.y < 0:
                    self.y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.y >= 0:
                    self.y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy
        if self.type == "player":
            if self.rect.right > 800 - 200 or self.rect.left < 800 - 200:
                self.rect.x -= dx
                rate_scroll = -dx

        return rate_scroll


    def shoot(self, bullets):
        if self.SHOOTING_COOLDOWN == 0 and self.ammo > 0:
            self.ammo -= 1
            self.SHOOTING_COOLDOWN = 20
            _bullet = Bullet((self.rect.centerx + (self.rect.size[0] * 0.6 * self.direction)), self.rect.centery,
                             self.direction)
            _bullet.obstacles = self.obstacles
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

    def attack(self, player, bullets,rate_scroll):
        if self.alive and player.alive:
            if random.randint(1, 200) == 1 and self.idle == False:
                self.update_action(0)
                self.idle = True
                self.idle_counter = 50
            if self.sight.colliderect(player.rect):
                self.update_action(0)
                self.shoot(bullets)
            else:
                if self.idle == False:
                    if self.direction == 1:
                        enemy_moving_right = True
                    else:
                        enemy_moving_right = False
                    enemy_moving_left = not enemy_moving_right
                    self.move(enemy_moving_right, enemy_moving_left)
                    self.update_action(1)
                    self.move_counter += 1
                    self.sight.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > 40:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idle = False
        self.rect.x += rate_scroll
