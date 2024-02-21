import csv
import pygame
import os

from ItemBox import ItemBox
from character import Character


class World:
    def __init__(self):
        self.obstacles = []
        self.img_list = []
        self.world_data = []
        for x in range(21):
            img = pygame.image.load(f'Assets/tile/{x}.png')
            img = pygame.transform.scale(img, (40, 40))
            self.img_list.append(img)
        for row in range(16):
            r = [-1] * 150
            self.world_data.append(r)
        with open('Assets/Map/level0_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

    def process_data(self,enemies,boxes):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * 40
                    img_rect.y = y * 40
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacles.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        pass
                    elif tile >= 11 and tile <= 14:
                        pass
                    elif tile == 15:
                        player = Character((x * 40), (y * 40), 1.65, 3, "player", 20)
                    elif tile == 16:
                        enemy = Character((x * 40), (y * 40), 1.65, 3, "enemy", 20)
                        enemies.add(enemy)
                    elif tile == 17:
                        ammo_box = ItemBox('ammo', x * 40, y * 40)
                        boxes.add(ammo_box)
                    elif tile == 19:
                        health_box = ItemBox('health', x * 40, y * 40)
                        boxes.add(health_box)
                    else:
                        pass
        return player, enemies, boxes

    def draw(self, screen):
        for obstacle in self.obstacles:
            screen.blit(obstacle[0], obstacle[1])

    def draw_bg(self, screen):
        screen.fill((255, 255, 255))
