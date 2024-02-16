import pygame

from World import World

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = (SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Protector")
timer = pygame.time.Clock()
FPS = 60
world = World()
PLAYER = world.process_data()
bullets = pygame.sprite.Group()
run = True
screen.fill((255, 255, 255))
moving_left = False
moving_right = False
while run:
    timer.tick(FPS)
    world.draw_bg(screen)
    world.draw(screen)
    PLAYER.update_animation()
    PLAYER.draw(screen)
    bullets.update()
    bullets.draw(screen)
    if PLAYER.alive:
        if PLAYER.shooting:
            bullets = PLAYER.shoot(bullets)
        if PLAYER.in_air:
            PLAYER.update_action(2)
        elif moving_left or moving_right:
            PLAYER.update_action(1)  # 1: run
        else:
            PLAYER.update_action(0)  # 0: idle
        PLAYER.move(moving_right, moving_left)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and PLAYER.alive:
                PLAYER.jump = True
            if event.key == pygame.K_SPACE:
                PLAYER.shooting = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                PLAYER.shooting = False

    pygame.display.update()
pygame.quit()