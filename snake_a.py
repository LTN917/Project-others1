import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque
import speech_recognition as sr  #聲音辨識
import pyaudio                   #輸入裝置

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
SIZE = 20
"""4增加背景音樂"""
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)
"""4"""
"""5語音辨識"""
def voice_totext():
    r = sr.Recognizer()
    with sr.Microphone() as source:   
        print("Please begin to speak:")
        audio= r.record(source,duration=3)
    try:
        Text = r.recognize_google(audio)     
    except r.UnknowValueError:
        Text = "無法翻譯"
    except sr.RequestError as e:
        Text = "無法翻譯{0}".format(e)
    return Text
    """5"""
def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def main():
    global DISPLAYSURF,BASICFONT
    def showStartScreen():
        titleFont = pygame.font.Font('freesansbold.ttf', 60)
        titleSurf1 = titleFont.render(' SNAKE ', True, (200,200,200),(0,0,0))
        degrees1 = 0
        while True:
            DISPLAYSURF.fill((100,200,150))
            rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
            rotatedRect1 = rotatedSurf1.get_rect()
            rotatedRect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

            drawPressKeyMsg()

            if checkForKeyPress():
                pygame.event.get()  
                return

            pygame.display.update()
            
        degrees1 += 2
    def checkForKeyPress():
        if len(pygame.event.get(QUIT)) > 0:
            terminate()

        keyUpEvents = pygame.event.get(KEYUP)

        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            terminate()
        return keyUpEvents[0].key
    def terminate():
        pygame.quit()
        sys.exit()
    def drawPressKeyMsg():
        pressKeySurf = BASICFONT.render('Press a key to play', True, (0,0,0))
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.center = (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 60)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)  
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    pygame.display.set_caption('語音貪食蛇')
    showStartScreen()
    """4"""
    pygame.mixer.music.load('advance\\pygame\\snake_game\\bg_music.mp3')
    pygame.mixer.music.play()
    """4"""
    Mode=1
    mode_ran=1
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('語音貪食蛇')
    light = (200, 200, 200)  # 蛇的顏色
    dark = (100, 100, 100)   # 食物顏色
    wallcolor=(0,0,0)

    font1 = pygame.font.SysFont("SimHei", 24)  # 得分的字體
    font2 = pygame.font.Font(None, 72)  # GAME OVER 的字體
    """"5題目庫和設定題目顯示位置"""
    question=[]
    with open("advance\\pygame\\snake_game\\q_list.txt",mode="r") as file:
        content=file.read()
        content_list=content.splitlines()
        for q in content_list:
            question.append(q)
    """5"""
    now_question=random.randint(0,len(question))

    red = (200, 30, 30)                 # GAME OVER 的字體顏色
    fwidth, fheight = font2.size("GAME OVER")
    line_width = 1                      # 網格線寬度
    black = (0, 0, 0)                   # 網格線顏色
    bgcolor = (40, 40, 60)              # 背景色

    # 方向，起始向右
    pos_x = 1
    pos_y = 0
    # 如果蛇正在向右移動，那麽快速點擊向下向左，由於程序刷新沒那麽快，向下事件會被向左覆蓋掉，導致蛇後退，直接GAME OVER
    # b 變量就是用於防止這種情況的發生
    b = True
    # 範圍
    scope_x = (0, SCREEN_WIDTH // SIZE - 1)
    scope_y = (2, SCREEN_HEIGHT // SIZE - 1)
    # 蛇
    snake = deque()
    '''6增加食物'''
    # 食物
    food_x = 0
    food_y = 0
    food2_x = 0
    food2_y = 0
    food3_x = 0
    food3_y = 0
    wall1_x = 0
    wall1_y = 0
    wall2_x = 0
    wall2_y = 0
    
    # 初始化蛇
    def _init_snake():
        nonlocal snake
        snake.clear()
        snake.append((2, scope_y[0]))
        snake.append((1, scope_y[0]))
        snake.append((0, scope_y[0]))

    # 食物 
    def _create_food():
        nonlocal food_x, food_y
        food_x = random.randint(scope_x[0], scope_x[1])
        food_y = random.randint(scope_y[0], scope_y[1])
       
        while (food_x, food_y) in snake:
            # 為了防止食物出到蛇身上
            food_x = random.randint(scope_x[0], scope_x[1])
            food_y = random.randint(scope_y[0], scope_y[1])
    def _create_food2():
        nonlocal food2_x,food2_y
        food2_x = random.randint(0,29)
        food2_y = random.randint(2,20)
       
        while (food2_x, food2_y) in snake:
            # 為了防止食物出到蛇身上
            food2_x = random.randint(0,29)
            food2_y = random.randint(2,20)
    def _create_food3():
        nonlocal food3_x,food3_y
        food3_x = random.randint(0,29)
        food3_y = random.randint(2,20)
       
        while (food3_x, food3_y) in snake:
            # 為了防止食物出到蛇身上
            food3_x = random.randint(0,29)
            food3_y = random.randint(2,20)
    def _create_wall1():
        nonlocal wall1_x,wall1_y
        wall1_x = random.randint(0,29-3)
        wall1_y = random.randint(2,20)
        while (wall1_x, wall1_y) in snake:
            # 為了防止食物出到蛇身上
            wall1_x = random.randint(0,29-3)
            wall1_y = random.randint(2,20)
    def _create_wall2():
        nonlocal wall2_x,wall2_y
        wall2_x = random.randint(0,29)
        wall2_y = random.randint(2,20-3)
        while (wall2_x, wall2_y) in snake:
            # 為了防止食物出到蛇身上
            wall2_x = random.randint(0,29)
            wall2_y = random.randint(2,20-3)

    _init_snake()
    _create_food()
    _create_food2()
    _create_food3()
    _create_wall1()
    _create_wall2()
    ''''''
    game_over = True
    start = False       # 是否開始，當start = True，game_over = True 時，才顯示 GAME OVER
    score = 0           # 得分
    orispeed = 0.25      # 原始速度
    speed = orispeed
    last_move_time = None
    pause = False       # 暫停

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        b = True
                        _init_snake()
                        _create_food()
                        _create_food2()
                        _create_food3()
                        pos_x = 1
                        pos_y = 0
                        # 得分
                        score = 0
                        Mode=1
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                        '''1新增加了不同模式的前進方式'''
                elif event.key in (K_w, K_UP):                 
                    # 這個判斷是為了防止蛇向上移時按了向下鍵，導致直接 GAME OVER
                    if (Mode==1)|(Mode==4):
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = -1
                            b = False
                    elif Mode==2:
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = 1
                            b = False
                    elif Mode==3:
                        if b and not pos_x:
                            pos_x = 1
                            pos_y = 0
                            b = False

                elif event.key in (K_s, K_DOWN):
                    if (Mode==1)|(Mode==4):
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = 1
                            b = False
                    elif Mode==2:
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = -1
                            b = False
                    elif Mode==3:
                        if b and not pos_x:
                            pos_x = -1
                            pos_y = 0
                            b = False

                elif event.key in (K_a, K_LEFT):
                    if (Mode==1)|(Mode==4):
                        if b and not pos_x:
                            pos_x = -1
                            pos_y = 0
                            b = False
                    elif Mode==2:
                        if b and not pos_x:
                            pos_x = 1
                            pos_y = 0
                            b = False
                    elif Mode==3:
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = -1
                            b = False
                            
                elif event.key in (K_d, K_RIGHT):
                    if (Mode==1)|(Mode==4):
                        if b and not pos_x:
                            pos_x = 1
                            pos_y = 0
                            b = False
                    elif Mode==2:
                         if b and not pos_x:
                            pos_x = -1
                            
                            pos_y = 0
                            b = False
                    elif Mode==3:
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = 1
                            b = False
                        '''1'''

        # 填充背景色
        screen.fill(bgcolor)
        # 畫網格線 豎線
        for x in range(SIZE, SCREEN_WIDTH, SIZE):
            pygame.draw.line(screen, black, (x, scope_y[0] * SIZE), (x, SCREEN_HEIGHT), line_width)
        # 畫網格線 橫線
        for y in range(scope_y[0] * SIZE, SCREEN_HEIGHT, SIZE):
            pygame.draw.line(screen, black, (0, y), (SCREEN_WIDTH, y), line_width)

        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2, (SCREEN_HEIGHT - fheight)//2, "GAME OVER", red)
        else:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos_x, snake[0][1] + pos_y)
                    if (next_s[0] == food_x and next_s[1] == food_y) or (next_s[0] == food2_x and next_s[1] == food2_y) or (next_s[0] == food3_x and next_s[1] == food3_y):
                        # 吃到了食物
                        '''5說出題目內容'''
                        if Mode==4:
                            text=voice_totext()
                            if text==question[now_question]:
                                score+=30
                            else:
                                score-=10
                        ''''''
                        _create_food()
                        _create_food2()
                        _create_food3()
                        _create_wall1()
                        _create_wall2()
                        snake.appendleft(next_s)
                        score += 10
                        """3蛇的顏色隨著模式而改變"""
                        mode_ran=random.randint(1,4)
                        if mode_ran==1:
                            dark=(150,150,150)
                        elif mode_ran==2:
                            dark=(0,0,150)
                        elif mode_ran==3:
                            dark=(150,0,0)
                        elif mode_ran==4:
                            dark=(0,150,0)
                            question_ran=random.randint(0,len(question)-1)
                            now_question=question_ran
                            '''3'''
                        speed = orispeed - 0.03 * (score // 100)
                    elif(wall1_x<=next_s[0]<=wall1_x+3 and next_s[1]==wall1_y) or (next_s[0]==wall2_x and wall2_y<=next_s[1]<=wall2_y+3):
                        game_over=True
                    else:
                        if scope_x[0] <= next_s[0] <= scope_x[1] and scope_y[0] <= next_s[1] <= scope_y[1] and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True

        # 畫食物和牆壁
        if not game_over:
            # 避免 GAME OVER 的時候把 GAME OVER 的字給遮住了
            """2食物顏色模式隨著模式而改變"""
            if mode_ran==1:
                Mode=1
                light=(200,200,200)
            elif mode_ran==2:
                Mode=2
                light=(0,0,200)          
            elif mode_ran==3:
                Mode=3
                light=(200,0,0)
            elif mode_ran==4:
                Mode=4
                light=(0,200,0)
                '''5模式4的文字方框出現'''
                print_text(screen, font1, 30,7, question[now_question], red)
                '''5'''
                """2"""      
            pygame.draw.rect(screen, light, (food_x * SIZE, food_y * SIZE, SIZE, SIZE), 0)
            pygame.draw.rect(screen, light, (food2_x * SIZE, food2_y * SIZE, SIZE, SIZE), 0)
            pygame.draw.rect(screen, light, (food3_x * SIZE, food3_y * SIZE, SIZE, SIZE), 0)
            pygame.draw.rect(screen, wallcolor, (wall1_x * SIZE, wall1_y * SIZE, SIZE*4, SIZE), 0)
            pygame.draw.rect(screen, wallcolor, (wall2_x * SIZE, wall2_y * SIZE, SIZE, SIZE*4), 0)


        # 畫蛇
        for s in snake:
            pygame.draw.rect(screen, dark, (s[0] * SIZE + line_width, s[1] * SIZE + line_width,
                                            SIZE - line_width * 2, SIZE - line_width * 2), 0)
        print_text(screen, font1, 450, 7, f"得分: {score}")
        pygame.display.update()


if __name__ == "__main__":
    main()
