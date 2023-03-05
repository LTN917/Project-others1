import random
import pygame
import sys
import pyautogui
from pygame.locals import *

Snakespeed = 10
Window_Width = 600
Window_Height = 600
Cell_Size = 20  

Cell_W = int(Window_Width / Cell_Size)  
Cell_H = int(Window_Height / Cell_Size)  

White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)  
Green = (0, 255, 0)
DARKGreen = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
Red_DARK = (150, 0, 0)
BLUE = (0, 0, 255)
BLUE_DARK = (0, 0, 150)

BGCOLOR = White  

UP = 'up'
DOWN = 'down'      
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  

def main():
    global SnakespeedCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    SnakespeedCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((Window_Width, Window_Height))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    pygame.display.set_caption('聲控貪食蛇')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    startx = random.randint(6, Cell_W - 6)
    starty = random.randint(6, Cell_H - 6)
    wormCoords = [{'x': startx, 'y': starty},{'x': startx - 1, 'y': starty},{'x': startx - 2, 'y': starty}]
    
    score=(len(wormCoords) - 3)
    '''1.三個食物'''
    direction = RIGHT

    apple = getRandomLocation()
    
    apple2 = apple2Random()
    
    apple3 = apple3Random()
    ''''''
    '''2.牆壁的隨機位置'''
    block = blockRandom()
    
    block2 = block2Random()
    ''''''
    Snakespeed = 5
    
    
    while True: 
        for event in pygame.event.get():  
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        '''3.速度加快'''
        if 15>len(wormCoords)>=10 :
            Snakespeed = 7
        elif 20>len(wormCoords)>=15  :
            Snakespeed = 9
        elif 25>len(wormCoords)>=20  :
            Snakespeed = 11
        elif 30>len(wormCoords)>=25  :
            Snakespeed = 12
        elif 35>len(wormCoords)>=30  :
            Snakespeed = 13
        ''''''            
        
        
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == Cell_W or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == Cell_H:
            return     
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  
        
        if ((wormCoords[HEAD]['x'] == block[0][0] or wormCoords[HEAD]['x'] == block[1][0] or wormCoords[HEAD]['x'] == block[2][0] or wormCoords[HEAD]['x'] == block[3][0]) and wormCoords[HEAD]['y'] == block[0][1]) or ((wormCoords[HEAD]['y'] == block2[0][1] or wormCoords[HEAD]['y'] == block2[1][1] or wormCoords[HEAD]['y'] == block2[2][1] or wormCoords[HEAD]['y'] == block2[3][1]) and wormCoords[HEAD]['x'] == block2[0][0]):
            return
        
        
        
        '''2.撞到牆壁的處理'''
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()
            block = blockRandom() 
            block2 = block2Random() 
            score=score+1
          
        elif wormCoords[HEAD]['x'] == apple2['x'] and wormCoords[HEAD]['y'] == apple2['y']:
            apple2 = apple2Random()
            block = blockRandom()
            block2 = block2Random()
            score=score+3
            
        elif wormCoords[HEAD]['x'] == apple3['x'] and wormCoords[HEAD]['y'] == apple3['y']:
            apple3 = apple3Random()
            block = blockRandom()
            block2 = block2Random()
            score=score+5
            ''''''
        else:
            del wormCoords[-1]  
        
    
        
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'],'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'],'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)

        

        DISPLAYSURF.fill(BGCOLOR)        
        
        drawWorm(wormCoords)
        '''1.畫三個蘋果'''
        drawApple(apple)
        drawApple2(apple2)
        drawApple3(apple3)
        ''''''
        '''2.畫障礙物'''
        drawblock(block)
        drawblock2(block2)
        ''''''
        drawScore(score)
        
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play', True, Black)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (Window_Width - 300, Window_Height - 60)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)

    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 60)
    titleSurf1 = titleFont.render(' SNAKE ', True, White,Black)
    degrees1 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (Window_Width / 2, Window_Height / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  
            return

        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)
        
        degrees1 += 2  

def terminate():
    pygame.quit()
    sys.exit()
'''4.蘋果和障礙物出現的位置'''
def getRandomLocation():
    return {'x': random.randint(0, Cell_W - 1), 'y': random.randint(0, Cell_H - 1)}

def apple2Random():
    return {'x': random.randint(0, Cell_W - 1), 'y': random.randint(0, Cell_H - 1)}

def apple3Random():
    return {'x': random.randint(0, Cell_W - 1), 'y': random.randint(0, Cell_H - 1)}

def blockRandom():
    blockx=random.randint(0, Cell_W - 1)
    blocky=random.randint(0, Cell_H - 1)
    return [[blockx,blocky],[blockx-1,blocky],[blockx-2,blocky],[blockx-3,blocky]]

def block2Random():
    blockx2=random.randint(0, Cell_W - 1) 
    blocky2=random.randint(0, Cell_H - 1) 
    return [[blockx2,blocky2],[blockx2,blocky2+1],[blockx2,blocky2+2],[blockx2,blocky2+3]]
    ''''''

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 60)
    gameSurf = gameOverFont.render('GAME', True, Black)
    overSurf = gameOverFont.render('OVER', True, Black)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (Window_Width / 2,60)
    overRect.midtop = (Window_Width / 2,130)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    drawPressKeyMsg()

    pygame.display.update()

    pygame.time.wait(500)

    checkForKeyPress()
    while True:
        if checkForKeyPress():
            pygame.event.get()  
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, Black)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Window_Width - 120, 30)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        wormSegmentRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(DISPLAYSURF, BLUE_DARK, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)
        pygame.draw.rect(DISPLAYSURF, BLUE, wormInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    appleRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(DISPLAYSURF, Red_DARK, appleRect)
    appleInnerSegmentRect = pygame.Rect(x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)
    pygame.draw.rect(DISPLAYSURF, Red, appleInnerSegmentRect)

def drawApple2(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    apple2Rect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(DISPLAYSURF, YELLOW, apple2Rect)
    
def drawApple3(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    apple3Rect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(DISPLAYSURF, DARKGreen , apple3Rect)
    apple3InnerSegmentRect = pygame.Rect(x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)
    pygame.draw.rect(DISPLAYSURF, Green, apple3InnerSegmentRect)
    

def drawblock(block):
    for coord in block:
        x = coord[0] * Cell_Size
        y = coord[1] * Cell_Size
        blockRect = pygame.Rect(x, y,Cell_Size, Cell_Size)
        pygame.draw.rect(DISPLAYSURF, Black, blockRect)
        
def drawblock2(block2):
    for coord in block2:
        x = coord[0] * Cell_Size
        y = coord[1] * Cell_Size
        block2Rect = pygame.Rect(x, y,Cell_Size, Cell_Size)
        pygame.draw.rect(DISPLAYSURF, Black, block2Rect)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass

