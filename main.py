import pygame
import sys
import math
import os
from pygame.locals import *
from random import *
os.getcwd()

#游戏背景尺寸
bg_size = width, height = 1024,511

#球类继承自Sprite类
class Ball(pygame.sprite.Sprite):
    def __init__(self,image,position,speed):
        #初始动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        #将小球放在指定位置
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.width, self.height = bg_size[0], bg_size[1]
        self.radius = self.rect.width / 2

    def move(self):
        self.rect = self.rect.move(self.speed)
        
        #左进右出，上进下出
        if self.rect.right < 0:
            self.rect.left = self.width

        elif self.rect.left > self.width:
            self.rect.right = 0

        if self.rect.bottom < 0:
            self.rect.top = self.height

        elif self.rect.top > self.height:
            self.rect.bottom = 0

#自己写的碰撞检测
#def collide_check(item,target):
#    col_balls = []
#    for each in target:
#        distance = math.sqrt(\
#            math.pow((item.rect.center[0] - each.rect.center[0]),2) + \
#            math.pow((item.rect.center[1] - each.rect.center[1]),2))
#        if distance <= (item.rect.width +each.rect.width) / 2:
#            col_balls.append(each)
#
#    return col_balls

def main():
    pygame.init()

    ball_image = "be.png"
    bg_image = "background.jpg"

    running = True

    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play the ball")

    background = pygame.image.load(bg_image)

    #存放小球的列表
    balls = []
    group = pygame.sprite.Group()

    #创建5个小球
    #BALL_NAM = 5
    for i in range(5):
        #位置随机，速度随机
        position = randint(0,width-55),randint(0,height-55)
        speed = [randint(-5,5),randint(-5,5)]
        ball = Ball(ball_image,position,speed)

        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball,rect.top = randint(0, width-55),randint(0, height-55)

        balls.append(ball)
        group.add(ball)

        #也是自己写的碰撞检测的一部分     
        #while collide_check(ball,balls):
        #    ball.rect.left, ball.rect.top = randint(0, width-55),randint(0, height-55)
        balls.append(ball)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        screen.blit(background,(0,0))

        for each in balls:
            each.move()
            screen.blit(each.image,each.rect)

        for each in group:
            group.remove(each)

            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                each.speed[0] = -each.speed[0]
                each.speed[1] = -each.speed[1]

            group.add(each)

        #for i in range(BALL_NAM):
        #    item = balls.pop(i)
        #
        #    if collide_check(item, balls):
        #        item.speed[0] = -item.speed[0]
        #        item.speed[1] = -item.speed[1]
        #
        #    balls.insert(i,item)

        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    main()