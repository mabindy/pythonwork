import pygame
import random
import time
pygame.init()

X = 400
Y = 400
navy_blue = (55, 0, 184)
white = (255, 255, 255)
orange = [255, 165, 0]
black = (0, 0, 0)

paddle1 = 250
paddle2 = 250


rect_x = 150
rect_y = 150

rand_location = random.randint(25, 350)
rand_direction = random.randint(-5, 5)


DISPLAY = pygame.display.set_mode([X, Y])
pygame.display.set_caption('Ping Pong')
font = pygame.font.Font(None, 75)
clock = pygame.time.Clock()

def countdown():
    for i in range(3, 0, -1):
        DISPLAY.fill(black)
        countdown_text = font.render(str(i), True, white)
        DISPLAY.blit(countdown_text, (185, 175))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        time.sleep(1)



countdown()

running = True

x_pos = 200
y_pos = rand_location
x_movement = 2.5
y_movement = 1
leftText = 0
rightText = 0




while running:
    DISPLAY.fill(black)
    leftScore = font.render(str(leftText), True, white)
    rightScore = font.render(str(rightText), True, white)
    dashText = font.render("-", True, white)
    pygame.draw.rect(DISPLAY, orange, [15,paddle1,10,25])
    pygame.draw.rect(DISPLAY, orange, [350,paddle2,10,25])
    pygame.draw.rect(DISPLAY, white, [x_pos, y_pos, 5, 5])
    pygame.draw.rect(DISPLAY, navy_blue, [0, 0, 400, 25])
    pygame.draw.rect(DISPLAY, navy_blue, (0, 375, 400, 25))
    DISPLAY.blit(leftScore, [135,150])
    DISPLAY.blit(dashText, [185, 150])
    DISPLAY.blit(rightScore, [225, 150])

    x_pos = x_pos + x_movement
    y_pos = y_pos + y_movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and paddle1 > 25:
        paddle1 = paddle1-3
    if keys[pygame.K_s] and paddle1 < 350:
        paddle1 = paddle1+3
    if keys[pygame.K_UP] and paddle2 > 25:
        paddle2 = paddle2 - 3
    if keys[pygame.K_DOWN] and paddle2 < 350:
        paddle2 = paddle2 + 3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   # Collision with left paddle (paddle1)
    if x_pos <= 25 and x_pos + 5 >= 15 and paddle1 <= y_pos <= paddle1 + 25:
        x_movement = -x_movement

    # Collision with right paddle (paddle2)
    if x_pos >= 345 and x_pos <= 350 and paddle2 <= y_pos <= paddle2 + 25:
        x_movement = -x_movement
    if y_pos < 25 or y_pos > 370:
        y_movement = y_movement * -1

    if x_pos >= 400:
        x_pos = 200
        y_pos = rand_location
        paddle1 = 250
        paddle2 = 250
        leftText = leftText + 1
        DISPLAY.blit(leftScore, [135,150])
        DISPLAY.blit(dashText, [185, 150])
        DISPLAY.blit(rightScore, [225, 150])
        countdown()
    if x_pos <= 0:
        x_pos = 200
        y_pos = rand_location
        paddle1 = 250
        paddle2 = 250
        rightText = rightText + 1
        DISPLAY.blit(leftScore, [135,150])
        DISPLAY.blit(dashText, [185, 150])
        DISPLAY.blit(rightScore, [225, 150])
        countdown()


    clock.tick(60)
    pygame.display.flip()
    
pygame.quit()
