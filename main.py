import pygame

from HealthBar import HealthBar
from World import World
from character import Character

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = (SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Protector")
font = pygame.font.SysFont('Futura', 30)
timer = pygame.time.Clock()
FPS = 60
world = World()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
boxes = pygame.sprite.Group()
PLAYER, enemies,boxes = world.process_data(enemies,boxes)
health_bar = HealthBar(10,10,PLAYER.health,PLAYER.max_health)
run = True
screen.fill((255, 255, 255))
moving_left = False
moving_right = False
while run:
    timer.tick(FPS)
    world.draw_bg(screen)
    world.draw(screen)
    PLAYER.update()
    PLAYER.draw(screen)
    for enemy in enemies:
        enemy.update()
        enemy.draw(screen)
        bullets.update(PLAYER, enemy, bullets)
    bullets.draw(screen)
    boxes.update(PLAYER)
    boxes.draw(screen)
    screen.blit(font.render(f"Ammo: {PLAYER.ammo}", True, (255,0,0)), (10, 35))
    health_bar.draw(PLAYER.health,screen)
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
