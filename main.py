import sys

import pygame
from pygame import mixer

from HealthBar import HealthBar
from World import World
from button import Button

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = (SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Protector")
font = pygame.font.SysFont('Futura', 30)
timer = pygame.time.Clock()
mixer.pre_init(44100, -16, 2, 512)
mixer.init()
mixer.music.load("Assets/Music/music.wav")
mixer.music.play(-1, 0.0, 500)


def get_font(size):
    return pygame.font.Font("Assets/Fonts/font.ttf", size)


def main():
    pygame.display.set_caption("The Protector")
    while True:
        screen.fill((255, 255, 255))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 110))
        PLAY_BUTTON = Button(image=pygame.image.load("Assets/Buttons/Play Rect.png"), pos=(400, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Assets/Buttons/Quit Rect.png"), pos=(400, 400),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def pause():
    while True:
        screen.fill((255, 255, 255))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(70).render("PAUSED", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 110))
        EASY_BUTTON = Button(image=pygame.image.load("Assets/Buttons/Play Rect.png"), pos=(400, 400),
                             text_input="RESUME", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        screen.blit(MENU_TEXT, MENU_RECT)
        for button in [EASY_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    return

        pygame.display.update()


def play():
    pygame.display.set_caption("choose difficulty")
    while True:
        screen.fill((255, 255, 255))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(40).render("CHOOSE DIFFICULTY", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 110))
        EASY_BUTTON = Button(image=pygame.image.load("Assets/Buttons/Play Rect.png"), pos=(400, 250),
                             text_input="EASY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MEDIUM_BUTTON = Button(image=pygame.image.load("Assets/Buttons/Options Rect.png"), pos=(400, 400),
                               text_input="MEDIUM", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("Assets/Buttons/Quit Rect.png"), pos=(400, 550),
                             text_input="HARD", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("Assets/Buttons/Play Rect.png"), (50, 50)),
                             pos=(60, 50),
                             text_input="<", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        screen.blit(MENU_TEXT, MENU_RECT)
        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    level(3)
                if MEDIUM_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    level(2)
                if HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    level(1)
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main()

        pygame.display.update()


def level(difficulty):
    FPS = 60
    world = World()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    grounds = pygame.sprite.Group()
    waters = pygame.sprite.Group()
    exits = pygame.sprite.Group()
    PLAYER, enemies, boxes, grounds, waters, exits = world.process_data(enemies, boxes, grounds, waters, exits)
    health_bar = HealthBar(10, 10, PLAYER.health, PLAYER.max_health)
    run = True
    screen.fill((255, 255, 255))
    moving_left = False
    moving_right = False
    rate_scroll = 0
    rate_loop = 0
    PLAYER.ammo = difficulty * 10
    while run:
        timer.tick(FPS)
        world.draw_bg(screen)
        world.draw(screen, rate_scroll)
        PLAYER.update()
        PLAYER.draw(screen)
        for enemy in enemies:
            enemy.attack(PLAYER, bullets, rate_scroll)
            enemy.update()
            enemy.draw(screen)
            bullets.update(PLAYER, enemy, bullets, rate_scroll)
        bullets.draw(screen)
        boxes.update(PLAYER, rate_scroll)
        grounds.update(rate_scroll)
        waters.update(rate_scroll)
        exits.update(rate_scroll)
        boxes.draw(screen)
        grounds.draw(screen)
        waters.draw(screen)
        exits.draw(screen)
        screen.blit(font.render(f"Ammo: {PLAYER.ammo}", True, (255, 0, 0)), (10, 35))
        health_bar.draw(PLAYER.health, screen)
        if PLAYER.alive:
            if PLAYER.shooting:
                bullets = PLAYER.shoot(bullets)
            if PLAYER.in_air:
                PLAYER.update_action(2)
            elif moving_left or moving_right:
                PLAYER.update_action(1)
            else:
                PLAYER.update_action(0)
            rate_scroll = PLAYER.move(moving_right, moving_left)
            rate_loop -= rate_scroll
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
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


if __name__ == "__main__":
    main()

pygame.quit()
