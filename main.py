import pygame
import sys
import math
import os
from pygame.locals import *
from random import *
import time
os.getcwd()
bg_size = width, height = 1024,511


#球类继承自Sprite类
class Ball(pygame.sprite.Sprite):
    def __init__(self,glayball_image,greenball_image,position,speed,target):
        #初始动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.glayball_image = pygame.image.load(glayball_image)
        self.greenball_image = pygame.image.load(greenball_image)
        self.rect = self.glayball_image.get_rect()
        #将小球放在指定位置
        self.rect.left, self.rect.top = position
        self.side = [choice([-1,1]),choice([-1,1])]
        self.speed = speed
        #是否碰撞
        self.collide = False
        self.target = target
        self.control = False
        self.width, self.height = bg_size[0], bg_size[1]
        self.radius = self.rect.width / 2

    def move(self):
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((self.side[0] * self.speed[0], \
                self.side[1] * self.speed[1]))

        #左进右出，上进下出
        if self.rect.right <= 0:
            self.rect.left = self.width

        elif self.rect.left >= self.width:
            self.rect.right = 0

        if self.rect.bottom <= 0:
            self.rect.top = self.height

        elif self.rect.top >= self.height:
            self.rect.bottom = 0

    def check(self, motion):
        if self.target < motion < self.target + 5:
            return True
        else:
            return False

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

#玻璃面板
class Glass(pygame.sprite.Sprite):#不继承也行
    def __init__(self,glass_image,bg_size,mouse_image):
        #初始动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        self.glass_rect.left, self.glass_rect.top = \
            (bg_size[0] - self.glass_rect.width) // 2 ,\
                (bg_size[1] - self.glass_rect.height)

        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left, self.mouse_rect.top = \
            self.glass_rect.left, self.glass_rect.top
        pygame.mouse.set_visible(False)

def main():
    pygame.init()

    glay_image = "be.png"
    green_image = "e.png"
    mouse_image = "cursor.cur"
    glass_image = "glass.png"
    bg_image = "background.jpg"

    running = True

    #添加背景音乐
    pygame.mixer.music.load("bgm.ogg")
    pygame.mixer.music.play()

    #添加音效
    ok = pygame.mixer.Sound("ok.ogg")
    good = pygame.mixer.Sound("good.ogg")
    bed = pygame.mixer.Sound("bed.ogg")

    #音乐播放完时，游戏结束
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    #窗口
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("玩个球")
    background = pygame.image.load(bg_image)

    #洞
    hole = [(144,168,211,235),(357,381,82,106),\
        (457,481,324,348),(760,784,333,357),\
            (821,845,133,157)]

    msgs =[]

    #存放小球的列表
    balls = []
    group = pygame.sprite.Group()

    #创建5个小球
    #BALL_NAM = 5
    for i in range(5):
        #位置随机，速度随机
        position = randint(0,width-50),randint(0,height-50)
        speed = [randint(1,5),randint(1,5)]
        ball = Ball(glay_image,green_image,position,speed,5 * (i+1))

        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball,rect.top = randint(0, width-50),randint(0, height-50)
        balls.append(ball)
        group.add(ball)

        #也是自己写的碰撞检测的一部分
        #while collide_check(ball,balls):
        #    ball.rect.left, ball.rect.top = randint(0, width-55),randint(0, height-55)
        balls.append(ball)

    glass = Glass(glass_image, bg_size,mouse_image)

    #创建鼠标事件变量
    motion = 0
    #计时器
    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER, 1000)

    #设置长按响应
    pygame.key.set_repeat(100,100)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            elif event.type == GAMEOVER:
                bed.play()
                pygame.time.delay(100)
                running = False

            elif event.type == MYTIMER:
                if motion:
                    for each in group:
                        if each.check(motion):
                            each.speed = [0, 0]
                            each.control = True
                    motion = 0

            elif event.type == MOUSEMOTION:
                    motion += 1

            elif event.type == KEYDOWN:
                if event.key == K_w:
                    for each in group:
                        if each.control:
                            each.speed[1] -= 1

                if event.key == K_s:
                    for each in group:
                        if each.control:
                            each.speed[1] += 1

                if event.key == K_a:
                    for each in group:
                        if each.control:
                            each.speed[0] -= 1

                if event.key == K_d:
                    for each in group:
                        if each.control:
                            each.speed[0] += 1

                if event.key == K_SPACE:
                    for each in group:
                        if each.control:
                            for i in hole:
                                if i[0] <= each.rect.centerx <= i[1] and i[2] <= each.rect.centery <= i[3]:
                                    good.play()
                                    each.speed = [0,0]
                                    group.remove(each)
                                    temp = balls.pop(balls.index(each))
                                    balls.insert(0, temp)
                                    hole.remove(i)
                            if not hole:
                                pygame.mixer.music.stop()
                                ok.play()
                                pygame.time.delay(300)
                                msg = pygame.image.load("ok.png").convert_alpha()
                                msg_pos = (width - msg.get_width()) // 2,(height - msg.get_height()) // 2
                                msgs.append((msg, msg_pos))
                                os.system("pause")


        screen.blit(background,(0,0))
        screen.blit(glass.glass_image, glass.glass_rect)

        #鼠标
        glass.mouse_rect.left, glass.mouse_rect.top = pygame.mouse.get_pos()

        if glass.mouse_rect.left < glass.glass_rect.left:
            glass.mouse_rect.left = glass.glass_rect.left
        if glass.mouse_rect.left > glass.glass_rect.right - glass.mouse_rect.width:
            glass.mouse_rect.left = glass.glass_rect.right - glass.mouse_rect.width
        if glass.mouse_rect.top < glass.glass_rect.top:
            glass.mouse_rect.top = glass.glass_rect.top
        if glass.mouse_rect.top > glass.glass_rect.bottom - glass.mouse_rect.height:
            glass.mouse_rect.top = glass.glass_rect.bottom - glass.mouse_rect.height

        screen.blit(glass.mouse_image, glass.mouse_rect)

        for each in balls:
            each.move()
            if each.collide:
                each.speed = [randint(1,5), randint(1,5)]
                each.collide = False
            if each.control:
                #绿色小球
                screen.blit(each.greenball_image,each.rect)
            else:
                screen.blit(each.glayball_image,each.rect)

        for each in group:
            group.remove(each)

            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                #方向取反
                each.side[0] = -each.side[0]
                each.side[1] = -each.side[1]
                each.collide = True
                #碰撞脱离控制
                if each.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    each.control = False
                    each.control = False

            group.add(each)

        for msg in msgs:
            screen.blit(msg[0], msg[1])

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