import csv

import pygame

from ItemBox import ItemBox
from character import Character


class Ground(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 40 // 2, y + (40 - self.image.get_height()))

    def update(self, rate_scroll):
        self.rect.x += rate_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 40 // 2, y + (40 - self.image.get_height()))

    def update(self, rate_scroll):
        self.rect.x += rate_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 40 // 2, y + (40 - self.image.get_height()))

    def update(self, rate_scroll):
        self.rect.x += rate_scroll


class World:
    def __init__(self, level):
        self.obstacles = []
        self.img_list = []
        self.world_data = []
        self.level = level
        self.bg = pygame.image.load("Assets/background/background.jpg")
        for x in range(21):
            img = pygame.image.load(f'Assets/tile/{x}.png')
            img = pygame.transform.scale(img, (40, 40))
            self.img_list.append(img)
        for row in range(16):
            r = [-1] * 150
            self.world_data.append(r)
        with open(f'Assets/Map/level{self.level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

    def process_data(self, enemies, boxes, grounds, waters, exits):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * 40
                    img_rect.y = y * 40
                    tile_data = (img, img_rect)
                    if 0 <= tile <= 8:
                        self.obstacles.append(tile_data)
                    elif 9 <= tile <= 10:
                        water = Water(img, x * 40, y * 40)
                        waters.add(water)
                    elif 11 <= tile <= 14:
                        ground = Ground(img, x * 40, y * 40)
                        grounds.add(ground)
                    elif tile == 15:
                        player = Character((x * 40), (y * 40), 1.65, 4, "player", 20)
                        player.set_obstacles(self.obstacles)
                    elif tile == 16:
                        enemy = Character((x * 40), (y * 40), 1.65, 2, "enemy", 20)
                        enemy.set_obstacles(self.obstacles)
                        enemies.add(enemy)
                    elif tile == 17:
                        ammo_box = ItemBox('ammo', x * 40, y * 40)
                        boxes.add(ammo_box)
                    elif tile == 19:
                        health_box = ItemBox('health', x * 40, y * 40)
                        boxes.add(health_box)
                    elif 20 <= tile <= 21:
                        exit = Exit(img, x * 40, y * 40)
                        exits.add(exit)
                    else:
                        pass
        return player, enemies, boxes, grounds, waters, exits

    def draw(self, screen, rate):
        for obstacle in self.obstacles:
            obstacle[1][0] += rate
            screen.blit(obstacle[0], obstacle[1])

    def draw_bg(self, screen):
        screen.blit(self.bg, (0, 0))
