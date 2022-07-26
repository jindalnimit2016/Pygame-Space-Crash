import math
import pygame
import random
from pygame import mixer
# initialise the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,720))

# Title and Icon
title = pygame.display.set_caption("Space Shoot") # flaticon.com
Icon = pygame.display.set_icon(pygame.image.load("D:\Download_Chrome\spaceship.png"))

# Background Sound
mixer.music.load('D:\Download_Chrome\guitarup_full.wav')
mixer.music.play(-2)
# BACKground image
background = pygame.image.load("D:\Download_Chrome\galaxy_bc.jpg")
# PLayer
playerImg = pygame.image.load("D:\Download_Chrome\spaceship2.png")
playerX = 340
playerY = 600
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load("D:\Download_Chrome\Alien.png"))
    enemyX.append(random.randint(0,750))
    enemyY.append(random.randint(0,110))
    enemyX_change.append(0.3)
    enemyY_change.append(random.randint(0,200))

# Bullet
# Ready = you can't see bullet on screen
# Fire = the bullet is currently moving
bulletImg = pygame.image.load("D:\Download_Chrome\laddu.png")
bulletX = 0
bulletY = 600
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

#
score_value = 0
font = pygame.font.Font("D:\Download_Chrome\signatria.ttf", 48)
textX = 10
testY = 10

# Game Over text
over_front = pygame.font.Font("D:\Download_Chrome\signatria.ttf", 82)

def game_over_text():
    over_text = over_front.render("Tumsa  na  ho  Payega", True, (145, 240, 12))
    screen.blit(over_text, (160,250))

def show_score(x, y):
    score = font.render("Score : "  + str(score_value), True, (145, 140, 12))
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(playerImg, (x, y))
def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16, y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow((enemyX-bulletX),2)) + (math.pow((enemyY-bulletY),2)))
    if distance < 27 :
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # color (RGB) -(RED, GREEN, BLUE)
    screen.fill((0,0,0))
    # Background Image
    screen.blit(background,(-240,-1100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("D:\Download_Chrome\laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0

    # checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change
    if playerX <=0:
        playerX = 0
    elif playerX >=750:
        playerX = 750

    # Enemy movement
    for i in range(num_of_enemy):
        # GAME OVER
        if enemyY[i] > 620:
            over_sound = mixer.Sound("D:\Download_Chrome\sway_by_bay.wav")
            over_sound.play(-1)
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 750:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # COLLISion
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("D:\Download_Chrome\explosion.wav")
            explosion_sound.play()
            bulletY = 600
            bullet_state = 'ready'
            score_value += 10
            print(score_value)
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(0, 110)

        enemy(enemyX[i],enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 600
        bullet_state = 'ready'

    if bullet_state == 'fire' :
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX,testY)
    pygame.display.update()