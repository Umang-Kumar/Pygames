import math
import random
import pygame
from pygame import mixer

# Initializing the game
pygame.init()

# defining game constants
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 600
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
WHITE = pygame.Color(255, 255, 255)
MAX_LIVES = 3
score = 0


# Create a screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Background
bg = pygame.image.load('Space_Invaders/background.png')

# Sounds
mixer.music.load('Space_Invaders/background.wav')
mixer.music.play(-1)
loss = pygame.mixer.Sound('Space_Invaders/loss.wav')

# Icons, Fonts and Captions
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('Space_Invaders/ufo.png')
pygame.display.set_icon(icon)
font = pygame.font.Font('Space_Invaders/ARCADE.TTF', 32)

# game values
current_player_lives = MAX_LIVES
current_player_score = score
game_status = 1

textX = 10
textY = 10

# Player
playerImg = pygame.image.load('Space_Invaders/player.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemies
enemyImg = []
enemyImg_rect = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('Space_Invaders/enemy.png'))
    enemyImg_rect.append(enemyImg[i].get_rect())
    enemyX.append(random.randint(0, 660))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def show_score(x, y):
    score_val = font.render("SCORE: " + str(current_player_score), True, WHITE)
    screen.blit(score_val, (x, y))


def lives(x, y):
    lives_val = font.render("LIVES: " + str(current_player_lives), True, WHITE)
    screen.blit(lives_val, (x, y))


def endgame(x, y):
    end = font.render("GAME ENDS!!", True, WHITE)
    screen.blit(end, (x, y))


# Bullets
# ready - bullet loaded, not shown
# fired - bullet fired, moving
bulletImg = pygame.image.load("Space_Invaders/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 10, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if dist < 27:
        return True
    else:
        return False


def set_bg():
    global bg
    # clear screen with RGB
    screen.fill((0, 0, 0))

    # Draw on background image
    screen.blit(bg, (0, 0))


def move_bullet():
    global bulletY, bulletX, bullet_state
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


def paused():
    global font
    mixer.pause()
    pause = font.render("PAUSED!!", True, RED)
    pause_rect = pause.get_rect()
    pause_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    conti = font.render("Press C to Continue, or Q to Quit!!", True, RED)
    conti_rect = conti.get_rect()
    conti_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)

    game_pause = True

    while game_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game_pause = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # screen.fill(WHITE)
        screen.blit(pause, pause_rect)
        screen.blit(conti, conti_rect)
        pygame.display.update()


# Game Loop
running = True
while running:
    set_bg()

    # Quit the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            elif event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound('Space_Invaders/laser.wav')
                    bulletSound.play()
                    # Give bullet the current x coordinates of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_p:
                paused()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 660:
        playerX = 660

    # Enemy movement
    for i in range(no_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 660:
            enemyX_change[i] -= 4
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

        # Bullet hits the enemies
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound("Space_Invaders/explosion.wav")
            explosion.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 660)
            enemyY[i] = random.randint(50, 150)

        if enemyImg_rect[i].bottom >= playerX:
            loss.play()
            current_player_lives -= 1
            if current_player_lives == 0:
                # game ends
                game_status = 2 
                pygame.mixer.music.stop()

    move_bullet()

    player(playerX, playerY)
    show_score(textX, textY)
    lives(WINDOW_WIDTH - 135, 10)

    # update screen
    pygame.display.update()
