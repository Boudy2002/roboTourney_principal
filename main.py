import pygame
from World import World
from character import Character

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = (SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Protector")
timer = pygame.time.Clock()
FPS = 60
world = World()
player = world.process_data()
run = True
screen.fill((255, 255, 255))
moving_left = False
moving_right = False
while run:
    timer.tick(FPS)
    world.draw_bg(screen)
    world.draw(screen)
    player.update_animation()
    player.draw(screen)

    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)  # 1: run
        else:
            player.update_action(0)  # 0: idle
        player.move(moving_right, moving_left)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()
pygame.quit()