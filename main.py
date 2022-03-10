# Feed the Dragon
import pygame
import random

# initialize the pygame
pygame.init()

# defining game constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600

FPS = 60

RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

MAX_LIVES = 3
DEFAULT_SCORE = 0
COIN_VELOCITY = 5
DRAGON_VELOCITY = 30
BUFFER_DISTANCE = -150

# Creating window and set the title
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Feed the Dragon')

# set up the background
background = pygame.image.load('data/dragon_night.jpg')
background_rect = background.get_rect()
background_rect.topleft = (0, 0)

# set up the actors
coin = pygame.image.load('data/coin.png')
coin_rect = coin.get_rect()
coin_rect.left = BUFFER_DISTANCE
coin_rect.top = random.randint(64, WINDOW_HEIGHT-64)

dragon = pygame.image.load('data/dragon.png')
dragon_rect = dragon.get_rect()
dragon_rect.centery = WINDOW_HEIGHT//2
dragon_rect.right = WINDOW_WIDTH - 10

# set up the sound and music
pickup = pygame.mixer.Sound('data/pickup.wav')
loss = pygame.mixer.Sound('data/loss.wav')

pygame.mixer.music.load('data/background_music.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1) # -1 infinite loop

# game values
current_player_lives = MAX_LIVES
current_player_score = DEFAULT_SCORE
current_coin_velocity = COIN_VELOCITY
game_status = 1

# font
game_font = pygame.font.Font('data/AttackGraffiti.ttf', 32) #fontname, font-size

# texts
lives = game_font.render('Lives: ' + str(current_player_lives), True, GREEN)
lives_rect = lives.get_rect()
lives_rect.top = 10
lives_rect.left = 50

title = game_font.render('Feed the Dragon', True, GREEN)
title_rect = title.get_rect()
title_rect.top = 10
title_rect.centerx = WINDOW_WIDTH // 2

score =  game_font.render('Score: ' + str(current_player_score), True, GREEN)
score_rect = score.get_rect()
score_rect.top = 10
score_rect.right = WINDOW_WIDTH - 50

game_ends = game_font.render('Game Ends!!!', True, RED)
game_ends_rect = game_ends.get_rect()
game_ends_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

replay = game_font.render('Press r to REPLAY!', True, GREEN)
replay_rect = replay.get_rect()
replay_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)


# define a main game loop (life of the game)
running = True
clock = pygame.time.Clock()
while running:
    # apply the background
    display_surface.blit(background, background_rect)

    # read the events
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN: #any key pressed
            if ev.key == pygame.K_DOWN and dragon_rect.bottom < WINDOW_HEIGHT and game_status == 1: # down arrow key pressed and game is running
                dragon_rect.top += DRAGON_VELOCITY
            elif ev.key == pygame.K_UP and dragon_rect.top > 64 and game_status == 1: # up arrow key pressed and game is running
                dragon_rect.top -= DRAGON_VELOCITY
            elif ev.key == pygame.K_r and game_status == 2:
                current_player_score = DEFAULT_SCORE
                current_player_lives = MAX_LIVES
                current_coin_velocity = COIN_VELOCITY

                score = game_font.render('Score: ' + str(current_player_score), True, GREEN)
                lives = game_font.render('Lives: ' + str(current_player_lives), True, GREEN)

                dragon_rect.centery = WINDOW_HEIGHT//2
                dragon_rect.right = WINDOW_WIDTH - 10

                coin_rect.left = BUFFER_DISTANCE
                coin_rect.top = random.randint(64, WINDOW_HEIGHT-64)

                game_status = 1
                pygame.mixer.music.play(-1)

    if game_status == 1:
        coin_rect.right += current_coin_velocity
        if coin_rect.colliderect(dragon_rect):
            # coin picked
            pickup.play()
            current_player_score += 1
            current_coin_velocity += 0.3
            score = game_font.render('SCore: ' + str(current_player_score), True, GREEN)
            coin_rect.left = BUFFER_DISTANCE
            coin_rect.top = random.randint(64, WINDOW_HEIGHT-64)
        elif coin_rect.right > WINDOW_WIDTH:
            # coin loss
            loss.play()
            current_player_lives -= 1
            lives = game_font.render('Lives: ' + str(current_player_lives), True, GREEN)
            coin_rect.left = BUFFER_DISTANCE
            coin_rect.top = random.randint(64, WINDOW_HEIGHT-64)
            if current_player_lives == 0:
                # game ends
                game_status = 2
                pygame.mixer.music.stop()

    # draw the HUD
    display_surface.blit(lives, lives_rect)
    display_surface.blit(title, title_rect)
    display_surface.blit(score, score_rect)

    if game_status == 1:
        # draw the actors
        display_surface.blit(coin, coin_rect)
        display_surface.blit(dragon, dragon_rect)
    elif game_status == 2:
        # game ends
        display_surface.blit(game_ends, game_ends_rect)
        display_surface.blit(replay, replay_rect)

    # refresh
    pygame.display.update()

    # to achieve cooperative multitasking
    # to make the game run at the same speed across different CPU's
    clock.tick(FPS)


# deallocating memory
pygame.quit()
