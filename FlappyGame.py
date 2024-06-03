# ===============================================================
# ==================== FLAPPY BIRD KNOCKOFF =====================
# ===============================================================


# --------------------------- Imports ---------------------------
import pygame
from pygame import mixer

import random

# --------------------------- Declarations ---------------------------

# Pygame Declaration
pygame.init()
clock = pygame.time.Clock()

# --------------------------- Constants ---------------------------

# --------------------------- Variables ---------------------------

gameRunning = True
onScreen = "title"
pause = False

bgSkyImg = 'moving_bg_skyOnly.png'
bgGrassImg = 'moving_grass.png'
bgSkyDisp = pygame.image.load(bgSkyImg)
bgGrassDisp = pygame.image.load(bgGrassImg)
bgSkyX = 0
bgGrassX = 0
bgY = 0

noOfSkins = 2
avatarSkins = ['ogFlappyBird.png', 'redFlappyBird.png']
avatarChoice = 0
avatarImg = avatarSkins[avatarChoice]
avatarDisp = pygame.image.load(avatarImg)
avatarX = 400
avatarY = 300
startingAvX = 400
startingAvY = 300
gameStartAvX = 200
gameStartAvY = 200
avatarAlive = True
avatarState = "ready_up"
avatarSpeed = 0

pipeUpImg = 'pipe2D_up.png'
pipeDownImg = 'pipe2D_down.png'
pipeUpDisp = pygame.image.load(pipeUpImg)
pipeDownDisp = pygame.image.load(pipeDownImg)
pipeX = []
minPipeY = 140                                              # starts at 140, min possible: 80
maxPipeY = 410                                              # starts at 410, max possible: 470
pipeY = []
pipeState = []
halfBirdSpace = 100                                         # starts at 100, min possible is 40
pipeDistX = 500
pipes_Num = 2

score = 0
highScore = -1

titleFontOutline = pygame.font.Font('SFPixelateShaded-Bold.ttf', 60)
titleFontInside = pygame.font.Font('SFPixelate-Bold.ttf', 60)
titleTextX = 190
titleTextY = 155
enterTextX = 192        # used hSb fonts
enterTextY = 385
pauseTextX = 270
pauseTextY = 255
gOFontOutline = pygame.font.Font('SFPixelateShaded-Bold.ttf', 55)
gOFontInside = pygame.font.Font('SFPixelate-Bold.ttf', 55)
gOTextX = 215
gOTextY = 200
scoreFontOutline = pygame.font.Font('SFPixelateShaded-Bold.ttf', 32)
scoreFontInside = pygame.font.Font('SFPixelate-Bold.ttf', 32)
scoreTextX = 384
scoreTextY = 40
hSsFontOutline = pygame.font.Font('SFPixelateShaded-Bold.ttf', 18)
hSsFontInside = pygame.font.Font('SFPixelate-Bold.ttf', 18)
hSsTextX = 391
hSsTextY = 80
hSbFontOutline = pygame.font.Font('SFPixelateShaded-Bold.ttf', 32)
hSbFontInside = pygame.font.Font('SFPixelate-Bold.ttf', 32)
hSbTextX = 267
hSbTextY = 300

jumpSound = mixer.Sound('cartoon-jump-6462.mp3')
deathSound = mixer.Sound('hard-slap-46388.mp3')
madeThruPipe = mixer.Sound('mixkit-arcade-game-jump-coin-216.wav')
achievementUnlocked = mixer.Sound('mixkit-achievement-completed-2068.wav')

# --------------------------- Functions ---------------------------


def ShowObject(img ,x, y):
    screen.blit(img, (x, y))

def DisplayBG():
    global bgX
    ShowObject(bgSkyDisp, bgX, bgY)
    ShowObject(bgGrassDisp, bgX, bgY + 550)
    if bgX >= -300:
        bgX -= 1
    else:
        bgX = 0

def moveBG():
    global bgSkyX
    global bgGrassX

    if onScreen != "game over" and (onScreen != "pause" and not pause):
        if bgSkyX > -305:
            bgSkyX -= 0.1
        else:
            bgSkyX = 0

        if bgGrassX > -305:
            bgGrassX -= 0.5
        else:
            bgGrassX = 0

def DisplayAvatar():
    global avatarImg
    global avatarDisp
    avatarImg = avatarSkins[avatarChoice]
    avatarDisp = pygame.image.load(avatarImg)
    ShowObject(avatarDisp, avatarX - 23, avatarY - 16)

def MakePipes():
    for i in range(pipes_Num):
        pipeX.append(800 + 87 + (pipeDistX * i))
        pipeY.append(random.randint(minPipeY, maxPipeY))
        if i == 0:
            pipeState.append("bonk")
        else:
            pipeState.append("too far")

def DisplayPipes():
    for i in range(pipes_Num):
        ShowObject(pipeUpDisp, pipeX[i], pipeY[i] - 550 - halfBirdSpace)
        ShowObject(pipeDownDisp, pipeX[i], pipeY[i] + halfBirdSpace)

def MovePipes():
    if (avatarState != "dead") and (onScreen == "game"):

        for i in range(pipes_Num):
            pipeX[i] -= 1

            if (pipeX[i] < avatarX - 80):
                if (pipeState[i] != "passed"):
                    madeThruPipe.play()
                    global score
                    score += 1
                    pipeState[i] = "passed"

                if (i != pipes_Num - 1):
                    pipeState[i + 1] = "bonk"
                else:
                    pipeState[0] = "bonk"

            if pipeX[i] <= - 85:
                pipeX[i] = 800 + 87
                pipeY[i] = random.randint(minPipeY, maxPipeY)

def deathByPipe(avX, avY):

    global onScreen

    for i in range(pipes_Num):

        if (onScreen != "game over") and (pipeState[i] == "bonk"):

            if ((avX + 21 >= pipeX[i]) and ((avY - 16 <= pipeY[i] - halfBirdSpace) or (avY + 16 >= pipeY[i] + halfBirdSpace) or (avY < 0))):
                deathSound.play()
                global avatarState
                global highScore
                if highScore < score:
                    highScore = score
                avatarState = "deadFalling"
                onScreen = "game over"


def AvatarJump():

    global avatarState
    global avatarSpeed

    if (avatarState == "falling"):
        avatarState = "jumping"
        avatarSpeed = 0


def MoveAvatar():

    global onScreen
    global avatarY
    global avatarState
    global avatarSpeed

    if (onScreen == "title") or (onScreen == "char sel"):
        if (avatarState == "ready_up") and (avatarY > startingAvY - 15):
            avatarY -= 0.3
        elif avatarY <= startingAvY - 15:
            avatarState = "ready_down"

        if (avatarState == "ready_down") and (avatarY < startingAvY + 15):
            avatarY += 0.3
        elif avatarY >= startingAvY + 15:
            avatarState = "ready_up"

    elif not pause:
            avatarY -= avatarSpeed

            if (avatarSpeed < 0) and (avatarState != "falling") and (avatarState != "deadFalling"):
                avatarState = "falling"

            if (avatarState == "jumping"):
                if (avatarSpeed < 5):
                    avatarSpeed += 0.5
                else:
                    avatarState = "doneJumping"
            elif (avatarState == "falling") or (avatarState == "doneJumping") or (avatarState == "deadFalling"):
                if avatarState != "deadFalling":
                    if avatarSpeed > -1:
                        avatarSpeed -= 0.25
                else:
                    if avatarSpeed > -3:
                        avatarSpeed -= 0.5

            if (avatarY >= 550):
                if (avatarState != "dead"):
                    deathSound.play()
                    global highScore
                    if highScore < score:
                        highScore = score
                    onScreen = "game over"
                    avatarState = "dead"
                    avatarSpeed = 0


def DisplayText():

    if onScreen == "title":

        titleTextOutline = titleFontOutline.render("Flappy Bird", True, (0, 0, 0))
        titleTextInside = titleFontInside.render("Flappy Bird", True, (255, 255, 255))
        screen.blit(titleTextInside, (titleTextX, titleTextY + 2))
        screen.blit(titleTextOutline, (titleTextX, titleTextY))

        enterTextOutline = hSbFontOutline.render("Press Enter to start", True, (0, 0, 0))
        enterTextInside = hSbFontInside.render("Press Enter to start", True, (255, 255, 255))
        screen.blit(enterTextInside, (enterTextX, enterTextY + 1.5))
        screen.blit(enterTextOutline, (enterTextX, enterTextY))

    elif onScreen == "game":
        global scoreTextX
        if (score >= 10) and (scoreTextX != 368):
            scoreTextX = 368
        elif (score >= 100) and (scoreTextX != 352):
            scoreTextX = 352

        scoreTextOutline = scoreFontOutline.render(str(score), True, (0, 0, 0))
        scoreTextInside = scoreFontInside.render(str(score), True, (255, 255, 255))
        screen.blit(scoreTextInside, (scoreTextX, scoreTextY + 1.5))
        screen.blit(scoreTextOutline, (scoreTextX, scoreTextY))

        if highScore > 0:
            global hSsTextX
            if (highScore >= 10) and (hSsTextX != 364):
                hSsTextX = 364
            elif (highScore >= 100) and (hSsTextX != 346):
                hSsTextX = 346

            hSsTextOutline = hSsFontOutline.render(str(highScore), True, (0, 0, 0))
            hSsTextInside = hSsFontInside.render(str(highScore), True, (255, 255, 255))
            screen.blit(hSsTextInside, (hSsTextX, hSsTextY + 2))
            screen.blit(hSsTextOutline, (hSsTextX, hSsTextY))


    elif onScreen == "game over":
        if avatarState == "dead":
            gOTextOutline = gOFontOutline.render("Game Over", True, (0, 0, 0))
            gOTextInside = gOFontInside.render("Game Over", True, (255, 255, 255))
            screen.blit(gOTextInside, (gOTextX, gOTextY + 1))
            screen.blit(gOTextOutline, (gOTextX, gOTextY))

            if (highScore >= 10) and (hSbTextX != 235):
                hSsTextX = 235
            elif (highScore >= 100) and (hSbTextX != 203):
                hSsTextX = 203

            hSbTextOutline = hSbFontOutline.render("High score: " + str(highScore), True, (0, 0, 0))
            hSbTextInside = hSbFontInside.render("High score: " + str(highScore), True, (255, 255, 255))
            screen.blit(hSbTextInside, (hSbTextX, hSbTextY + 1.5))
            screen.blit(hSbTextOutline, (hSbTextX, hSbTextY))

            if (highScore > score):
                hSbTextOutline = hSbFontOutline.render("Your score: " + str(score), True, (0, 0, 0))
                hSbTextInside = hSbFontInside.render("Your score: " + str(score), True, (255, 255, 255))
                screen.blit(hSbTextInside, (hSbTextX - 3, hSbTextY + 1.5 + 50))
                screen.blit(hSbTextOutline, (hSbTextX - 3, hSbTextY + 50))

    elif onScreen == "pause":

        if (score >= 10) and (scoreTextX != 368):
            scoreTextX = 368
        elif (score >= 100) and (scoreTextX != 352):
            scoreTextX = 352

        scoreTextOutline = scoreFontOutline.render(str(score), True, (0, 0, 0))
        scoreTextInside = scoreFontInside.render(str(score), True, (255, 255, 255))
        screen.blit(scoreTextInside, (scoreTextX, scoreTextY + 1.5))
        screen.blit(scoreTextOutline, (scoreTextX, scoreTextY))

        if highScore > 0:
            if (highScore >= 10) and (hSsTextX != 364):
                hSsTextX = 364
            elif (highScore >= 100) and (hSsTextX != 346):
                hSsTextX = 346

            hSsTextOutline = hSsFontOutline.render(str(highScore), True, (0, 0, 0))
            hSsTextInside = hSsFontInside.render(str(highScore), True, (255, 255, 255))
            screen.blit(hSsTextInside, (hSsTextX, hSsTextY + 2))
            screen.blit(hSsTextOutline, (hSsTextX, hSsTextY))

        pauseTextOutline = titleFontOutline.render("Paused", True, (0, 0, 0))
        pauseTextInside = titleFontInside.render("Paused", True, (255, 255, 255))
        screen.blit(pauseTextInside, (pauseTextX, pauseTextY + 2))
        screen.blit(pauseTextOutline, (pauseTextX, pauseTextY))

    elif onScreen == "char sel":

        enterTextOutline = hSbFontOutline.render("Choose your character", True, (0, 0, 0))
        enterTextInside = hSbFontInside.render("Choose your character", True, (255, 255, 255))
        screen.blit(enterTextInside, (enterTextX, enterTextY + 1.5))
        screen.blit(enterTextOutline, (enterTextX, enterTextY))

# ------------------------------------------------------------------
# --------------------------- Game Setup ---------------------------
# ------------------------------------------------------------------

# Screen Declaration
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Flappy Bird Knockoff")

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

MakePipes()

# Game Loop
while gameRunning:

    ShowObject(bgSkyDisp, bgSkyX, bgY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

        if event.type == pygame.KEYDOWN:
            if onScreen == "title":
                if (event.key == pygame.K_ESCAPE):
                    gameRunning = False
                elif (event.key == pygame.K_RETURN):
                    onScreen = "game"
                    avatarState = "falling"
                    avatarX = gameStartAvX
                    avatarY = gameStartAvY
                elif (event.key == pygame.K_TAB):
                    onScreen = "char sel"

            elif onScreen == "game":
                if avatarState != "dead":
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                        onScreen = "pause"
                    if (event.key == pygame.K_UP) or (event.key == pygame.K_w) or (event.key == pygame.K_SPACE):
                        jumpSound.play()
                        AvatarJump()

            elif onScreen == "game over":
                if (event.key == pygame.K_ESCAPE):
                    gameRunning = False
                if (event.key == pygame.K_RETURN):
                    onScreen = "game"
                    # reset procedure
                    avatarX = gameStartAvX
                    avatarY = gameStartAvY
                    pipeX = []
                    pipeY = []
                    pipeState = []
                    MakePipes()
                    score = 0
                    avatarState = "falling"
                    pause = False
                if (event.key == pygame.K_BACKSPACE):
                    onScreen = "title"
                    avatarX = startingAvX
                    avatarY = startingAvY
                    pipeX = []
                    pipeY = []
                    pipeState = []
                    MakePipes()
                    score = 0
                    avatarState = "ready_up"
                    pause = False

            elif onScreen == "char sel":
                if (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_RETURN) or (event.key == pygame.K_SPACE):
                    onScreen = "title"
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    print("here right")
                    #global avatarChoice
                    if avatarChoice < noOfSkins - 1:
                        avatarChoice += 1
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    print("here left")
                    if avatarChoice > 0:
                        avatarChoice -= 1

            elif pause:
                if (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_UP) or (event.key == pygame.K_w) or (
                        event.key == pygame.K_SPACE):
                    pause = False
                    onScreen = "game"

    deathByPipe(avatarX, avatarY)
    MovePipes()
    DisplayPipes()
    ShowObject(bgGrassDisp, bgGrassX, bgY + 550)
    moveBG()
    MoveAvatar()
    DisplayAvatar()
    DisplayText()
    #print(onScreen)
    pygame.display.update()