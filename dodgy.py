import pygame
import time
import random
pygame.font.init()


WIDTH = 800
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodgy Game")
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5

ENEMY_WIDTH = 5
ENEMY_HEIGHT = 10
ENEMY_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, enemies):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {str(int(elapsed_time))}", 1, (255, 255, 255))
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, (255, 0, 0), player)

    for enemy in enemies:
        pygame.draw.rect(WIN, "white", enemy)
    pygame.display.update()


def dodgy():
    run = True
    hit = False

    player = pygame.Rect(200, HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    enemy_increment = 2000
    enemy_count = 0
    enemies = []

    while run:
        enemy_count += clock.tick(60)
        elapsed_time = time.time()-start_time

        if enemy_count >= enemy_increment:
            for _ in range(3):
                enemy_x = random.randint(0, WIDTH-ENEMY_WIDTH)
                enemy_y = -ENEMY_HEIGHT
                enemy = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)
                enemies.append(enemy)
            enemy_increment=max(200, enemy_increment-50)
            enemy_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x-PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        elif keys[pygame.K_RIGHT] and player.x+PLAYER_VELOCITY+PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VELOCITY

        for enemy in enemies[:]:
            enemy.y += ENEMY_VEL
            if enemy.y>HEIGHT:
                enemies.remove(enemy)
            elif enemy.y+ENEMY_HEIGHT >= player.y and enemy.colliderect(player):
                hit = True
                break
        
        if hit:
            lost_text = FONT.render("You lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2-lost_text.get_width()/2, HEIGHT/2-lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            run=False

        draw(player, elapsed_time, enemies)

    pygame.quit()


if __name__ == "__main__":
    print("Starting game")

    dodgy()
