import random
import sys
import pygame
import time
from pygame.locals import *
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
groundy = SCREENHEIGHT*0.8-18
GAME_SPRITES = {}
GAME_SOUND = {}
PLAYER = 'res\sprites\ird.png'
BACKGROUND = 'res\sprites\sky.png'
pipe = 'res\sprites\pipe.png'
f=open("res\score\hs.txt","r")
high_score=f.read()
f.close()
def welcomescreen():
    f=open("res\score\hs.txt","r")
    high_score=f.read()
    f.close()
    playerx = int(SCREENWIDTH/5)+65
    playery = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2-20
    messagex = int(SCREENWIDTH - GAME_SPRITES['welcome'].get_height())/2+100
    messagey = int(SCREENHEIGHT*0.13)-25
    seax=-99
    while True:
        SCREEN.blit(GAME_SPRITES['background'], (0,0)) 
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        SCREEN.blit(GAME_SPRITES['welcome'], (messagex, messagey))
        SCREEN.blit(GAME_SPRITES['sea'], (seax, groundy))
        SCREEN.blit(GAME_SPRITES['high'], (5, SCREENHEIGHT-32))

        mydigit =[int(x) for x in list(str(high_score))]
        width = 0
        for digit in mydigit:
            width += GAME_SPRITES['number'][digit].get_width()
        scorex = GAME_SPRITES['high'].get_width()+10
        for digit in mydigit:
            SCREEN.blit(GAME_SPRITES['number'][digit], (scorex, SCREENHEIGHT-38))
            scorex += GAME_SPRITES['number'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(1)

            elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_UP):
                return maingame()
            
                
                 
def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    seax = -99
    newpipe1 = getpipe()
    newpipe2 = getpipe()
    upperpipes = [
        {'x': SCREENWIDTH+200, 'y':newpipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newpipe2[0]['y']},
    ]
    lowerpipes = [
        {'x': SCREENWIDTH+200, 'y':newpipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newpipe2[1]['y']},
    ]

    pipevelc = -4
    playervely = -9
    playermaxvely = 10
    playerminvely = -8
    playeraccy = 1
    playerflapaccv = -8
    playerflapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(1)
            if event.type == KEYDOWN and(event.key == K_UP):
                if playery > 0:
                    playervely = playerflapaccv
                    playerflapped = True
                    GAME_SOUND['wing'].play()
        crash = iscrash(playerx, playery, upperpipes, lowerpipes)
        if crash:
            if(score>int(high_score)):
                f=open("res\score\hs.txt","w")
                f.write(str(score))
                f.close()
            time.sleep(0.7)
            return welcomescreen()

        playermidpos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipemidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidpos<= playermidpos < pipemidpos+4:
                score+=1
                print(f"score: {score}")
                GAME_SOUND['point'].play()
        if playervely<playermaxvely and not playerflapped:
            playervely += playeraccy
        if playerflapped:
            playerflapped = False
        playerheight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playervely, groundy - playery - playerheight)

        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] +=pipevelc
            lowerpipe['x'] +=pipevelc
        
        if 0<upperpipes[0]['x']<5:
            newpipe = getpipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['sea'], (seax, groundy))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        mydigit =[int(x) for x in list(str(score))]
        width = 0
        for digit in mydigit:
            width += GAME_SPRITES['number'][digit].get_width()
        scorex = 5
        for digit in mydigit:
            SCREEN.blit(GAME_SPRITES['number'][digit], (scorex, 5))
            scorex += GAME_SPRITES['number'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)





def getpipe():
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/4
    y2 = offset + random.randrange(0, int(SCREENHEIGHT- GAME_SPRITES['sea'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},
        {'x': pipex, 'y': y2},
    ]
    return pipe

def iscrash(playerx, playery, upperpipes, lowerpipes):
    if playery>(groundy-GAME_SPRITES['player'].get_height()-1):
        GAME_SOUND['hit'].play()
        return True
    for pipe in upperpipes:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if( playery< pipeheight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()-27):
            GAME_SOUND['hit'].play()
            return True
    
    for pipe in lowerpipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()-27):
            GAME_SOUND['hit'].play()
            return True
    
    return False


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('@half.quotes_')
    GAME_SPRITES['number'] = (
        pygame.image.load('res\sprites\zero.png').convert_alpha(),
        pygame.image.load('res\sprites\one.png').convert_alpha(),
        pygame.image.load('res\sprites\wo.png').convert_alpha(),
        pygame.image.load('res\sprites\hree.png').convert_alpha(),
        pygame.image.load('res\sprites\our.png').convert_alpha(),
        pygame.image.load('res\sprites\ive.png').convert_alpha(),
        pygame.image.load('res\sprites\six.png').convert_alpha(),
        pygame.image.load('res\sprites\seven.png').convert_alpha(),
        pygame.image.load('res\sprites\eight.png').convert_alpha(),
        pygame.image.load('res\sprites\ine.png').convert_alpha(),
    )
    GAME_SPRITES['high'] = pygame.image.load('res\sprites\high.png').convert_alpha()
    GAME_SPRITES['welcome'] = pygame.image.load('res\sprites\welcome.png').convert_alpha()
    GAME_SPRITES['sea'] = pygame.image.load('res\sprites\sea.png').convert_alpha()
    GAME_SPRITES['pipe'] = pygame.image.load('res\sprites\pipe.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )

    GAME_SOUND['do'] = pygame.mixer.Sound('res\sound\do.wav')
    GAME_SOUND['hit'] = pygame.mixer.Sound('res\sound\hit.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('res\sound\point.wav')
    GAME_SOUND['swooosh'] = pygame.mixer.Sound('res\sound\swoosh.wav')
    GAME_SOUND['wing'] = pygame.mixer.Sound('res\sound\wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        GAME_SOUND['do'].play(-1)
        welcomescreen()
        