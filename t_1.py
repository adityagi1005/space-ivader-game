from turtle import distance
import pygame
from pygame import mixer
import random
import math

#Initialize the pygame
pygame.init()


#Create the screen
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('space_back.jpg')

#Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)     
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text,(200, 250))

#score
Score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render("Score : " + str(Score_value),True,(255,255,255))
    screen.blit(score,(x,y))


#Title and Icon
pygame.display.set_caption("SPACE")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)


#Player
PlayerImg = pygame.image.load('ufo_4.png')
PlayerX = 370
PlayerY = 480
PlayerX_Change = 0
PlayerY_Change = 0

def Player(x,y):
    screen.blit(PlayerImg, (x, y))


#Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_Change = []
EnemyY_Change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('invader.png'))
    EnemyX.append(random.randint(0,750))
    EnemyY.append(random.randint(50,150))
    EnemyX_Change.append(0.8)
    EnemyY_Change.append(40)

def Enemy(x,y,i):
    screen.blit(EnemyImg[i],(x,y))


#Bullet
BulletImg = pygame.image.load('Bullet.png')
BulletX = 0
BulletY = 480
BulletX_Change = 0
BulletY_Change = 1
Bullet_State = "ready"

def Fire_Bullet(x, y):
    global Bullet_State 
    Bullet_State = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))

#For collision
def isCollision(BulletX,BulletY,EnemyX,EnemyY):
    distance = math.sqrt(math.pow(BulletX - EnemyX,2) + math.pow(BulletY - EnemyY,2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:


    #to change background color
    #RGB - Red, Blue, Green
    screen.fill((100,100,100))


    #Background image
    screen.blit(background,(0,0))


    #To last the screen till we click on close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
 
            if event.key == pygame.K_LEFT:
                PlayerX_Change = -1
            if event.key == pygame.K_RIGHT:
                PlayerX_Change = 1
            if event.key == pygame.K_UP:
                PlayerY_Change = 0
            if event.key == pygame.K_DOWN:
                PlayerY_Change = 0
            if event.key == pygame.K_SPACE:
                if Bullet_State is "ready":
                    Bullet_Sound = mixer.Sound('laser.wav')
                    Bullet_Sound.play()
                    BulletX = PlayerX
                    Fire_Bullet(BulletX,BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                PlayerX_Change = 0
                PlayerY_Change = 0


    #Making boundaries
    PlayerX += PlayerX_Change    
    PlayerY += PlayerY_Change

    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 760:
        PlayerX = 760
    elif PlayerY >= 540:
        PlayerY = 540
    elif PlayerY <= 0:
        PlayerY = 0


    #Enemy movements
    for i in range(num_of_enemies):

        if EnemyY[i] > 400:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break


        EnemyX[i] += EnemyX_Change[i]
        
        
        if EnemyX[i] <= 0:
            EnemyX_Change[i] = 0.3
            EnemyY[i] += EnemyY_Change[i]
        elif EnemyX[i] >= 730:
            EnemyX_Change[i] = -0.3
            EnemyY[i] += EnemyY_Change[i]
        #Collision
        Collision = isCollision(BulletX,BulletY,EnemyX[i],EnemyY[i])
        if Collision:
            Collision_Sound = mixer.Sound('explosion.wav')
            Collision_Sound.play()
            BulletY = 480
            Bullet_State = "ready"
            Score_value += 1
            EnemyX[i] = random.randint(0,750)
            EnemyY[i] = random.randint(50,150)
        
        Enemy(EnemyX[i],EnemyY[i],i)
    

    #Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_State = "ready"

    if Bullet_State is "fire":
        Fire_Bullet(BulletX, BulletY)
        BulletY -= BulletY_Change


    Player(PlayerX,PlayerY)
    show_score(textX,textY)
    


    #this line to update the changes
    pygame.display.update()

    