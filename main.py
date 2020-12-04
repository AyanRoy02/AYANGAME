# AYANGAME
import random
import math
import pygame
from pygame import mixer


pygame.init()

# DISPLAY AND ICON
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('AYANGAME')
icon = pygame.image.load('caption_logo.png')
pygame.display.set_icon(icon)

# BACKGROUND
background = pygame.image.load('background.jpg')

# SCORE
score_count = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

# GAME OVER
over_font = pygame.font.Font('freesansbold.ttf', 64)

# PLAYER
playerImg = pygame.image.load('player1.png')
playerX = 370
playerY = 500
playerChange = 0

# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy1.png'))
    enemyX.append(random.randint(0, 734))
    enemyY.append(random.randint(50, 80))
    enemyChangeX.append(0.5)
    enemyChangeY.append(30)

# ARROW
arrowImg = pygame.image.load('arrow.png')
arrowX = 0
arrowY = 500
arrowX_change = 0
arrowY_change = 2
arrow_state = 'draw'


# FUNCTIONS
def release_arrow(x, y):
    global arrow_state
    arrow_state = 'release'
    screen.blit(arrowImg, (x + 16, y - 20))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, arrowX, arrowY):
    distance = math.sqrt(math.pow(enemyX - arrowX, 2) + (math.pow(enemyY - arrowY, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score : " + str(score_count), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    global playerX
    playerX = 700
    over_score = over_font.render('GAME OVER', True, (0, 35, 202))
    screen.blit(over_score, (200, 250))
    over_score2 = font.render("Press KEYPAD_ENTER to Start Again", True, (0,0,0))
    screen.blit(over_score2, (0,500))


# THE LOOP
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # USER INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChange -= 0.6
            if event.key == pygame.K_RIGHT:
                playerChange += 0.6
            if event.key == pygame.K_SPACE:
                if arrow_state == 'draw':
                    wooshSound=mixer.Sound('woosh.wav')
                    wooshSound.play()
                    arrowX = playerX
                    release_arrow(arrowX, arrowY)
            # RESET
            if event.key == pygame.K_KP_ENTER:
                score_count = 0
                playerX = 370
                for i in range(num_of_enemies):
                    enemyX[i]=random.randint(0, 734)
                    enemyY[i]=random.randint(50, 80)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerChange = 0

    # PLAYER BOUNDARY
    playerX += playerChange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # ENEMY MOVEMENT AND COLLISIONS
    for i in range(num_of_enemies):
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        # ENEMY BOUNDARY
        enemyX[i] += enemyChangeX[i]
        if enemyX[i] <= 0:
            enemyChangeX[i] = 0.5
            enemyY[i] += enemyChangeY[i]
        elif enemyX[i] >= 736:
            enemyChangeX[i] = -0.5
            enemyY[i] += enemyChangeY[i]

        # COLLISION
        collision = isCollision(enemyX[i], enemyY[i], arrowX, arrowY)
        if collision:
            hitSound=mixer.Sound('hit.wav')
            hitSound.play()
            arrowY = 500
            arrow_state = 'draw'
            score_count += 1
            enemyX[i] = random.randint(0, 734)
            enemyY[i] = random.randint(50, 80)

        enemy(enemyX[i], enemyY[i], i)

    # ARROW MOVEMENT
    if arrowY <= 0:
        arrowY = 500
        arrow_state = 'draw'
    if arrow_state == 'release':
        release_arrow(arrowX, arrowY)
        arrowY -= arrowY_change

    player(playerX, playerY)
    show_score(scoreX, scoreY)

    pygame.display.update()
