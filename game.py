import pygame
import random
import sys

WIDTH = 400
HEIGHT = 600
FPS = 60
PIPE_SPEED = 3
PIPE_GAP = 150
GRAVITY = 0.5
FLAP_POWER = -8
MAX_LIVES = 3
HIT_DELAY = 30

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird (KP Version)")
clock = pygame.time.Clock()

try:
    bird_img = pygame.image.load("bird.png").convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (60, 60))
    heart_img = pygame.image.load("heart.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (30, 30))
    pygame.mixer.init()
    pygame.mixer.music.load("song.mp3")
except:
    print("Image or music not found")
    sys.exit()

def play_game():
    pygame.mixer.music.play(-1)
    kp_x = 80
    kp_y = HEIGHT // 2
    kp_speed = 0
    pipes = []
    pipe_timer = 0
    score = 0
    lives = MAX_LIVES
    is_game_over = False
    hit_timer = 0

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not is_game_over:
                if event.key == pygame.K_SPACE:
                    kp_speed = FLAP_POWER
            if event.type == pygame.KEYDOWN and is_game_over:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.play(-1)
                    return play_game()

        if not is_game_over:
            kp_speed += GRAVITY
            kp_y += kp_speed
            pipe_timer += 1
            if pipe_timer > 90:
                pipe_timer = 0
                top_height = random.randint(50, HEIGHT - 200)
                pipes.append([WIDTH, top_height])
            for p in pipes:
                p[0] -= PIPE_SPEED

            kp_rect = pygame.Rect(kp_x, kp_y, 50, 50)
            hit = False

            if hit_timer > 0:
                hit_timer -= 1

            for p in pipes:
                pipe_x = p[0]
                top_h = p[1]
                bottom_y = top_h + PIPE_GAP
                top_rect = pygame.Rect(pipe_x, 0, 70, top_h)
                bottom_rect = pygame.Rect(pipe_x, bottom_y, 70, HEIGHT - bottom_y)
                if hit_timer == 0 and (kp_rect.colliderect(top_rect) or kp_rect.colliderect(bottom_rect)):
                    hit = True
                if pipe_x + 70 < kp_x and "passed" not in p:
                    p.append("passed")
                    score += 1

            if hit_timer == 0 and (kp_y > HEIGHT - 80 or kp_y < 0):
                hit = True

            if hit:
                lives -= 1
                kp_y = HEIGHT // 2
                kp_speed = 0
                hit_timer = HIT_DELAY
                if lives <= 0:
                    is_game_over = True
                    pygame.mixer.music.stop()

            pipes = [p for p in pipes if p[0] > -80]

        win.fill((135, 206, 235))
        pygame.draw.rect(win, (200, 180, 120), (0, HEIGHT - 80, WIDTH, 80))
        for p in pipes:
            x = p[0]
            top_h = p[1]
            bottom_y = top_h + PIPE_GAP
            pygame.draw.rect(win, (0, 170, 0), (x, 0, 70, top_h))
            pygame.draw.rect(win, (0, 170, 0), (x, bottom_y, 70, HEIGHT - bottom_y))
            pygame.draw.rect(win, (255, 0, 0), (x, 0, 70, top_h), 2)
            pygame.draw.rect(win, (255, 0, 0), (x, bottom_y, 70, HEIGHT - bottom_y), 2)

        win.blit(bird_img, (kp_x, kp_y))
        pygame.draw.rect(win, (255, 0, 0), kp_rect, 2)

        for i in range(lives):
            win.blit(heart_img, (10 + i*40, 10))
        font = pygame.font.SysFont("Arial", 35, bold=True)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        win.blit(score_text, (WIDTH//2 - 80, 20))

        if is_game_over:
            go_font = pygame.font.SysFont("Arial", 55, bold=True)
            go_text = go_font.render("GAME OVER", True, (255, 0, 0))
            win.blit(go_text, (WIDTH//2 - 140, HEIGHT//2 - 50))
            restart_font = pygame.font.SysFont("Arial", 25)
            restart_text = restart_font.render("Press SPACE to restart", True, (255, 255, 255))
            win.blit(restart_text, (WIDTH//2 - 120, HEIGHT//2 + 20))

        pygame.display.update()

play_game()
