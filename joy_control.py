#! /usr/bin/env python
# coding: utf-8
# coding=utf-8
# -*- coding: utf-8 -*-
# vim: fileencoding=utf-8

import spidev
import time
import pygame
from pygame.locals import *

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
spi.mode = 0b00
protocol_sign = 0xaf
set_speed = 0x00
off_control = 0x01
dummy = 0x00
line = 0x0a
right_motor = 0x00
left_motor = 0x00
alpha = 0.5

def set_motor_value(x, y):
        global right_motor
        global left_motor
        right_motor = int((-y  - x * alpha)* limit)
        left_motor = int((y - x * alpha) * limit)
        if right_motor > 100:
            right_motor = 100
        elif right_motor < -100:
            right_motor = -100
        if left_motor > 100:
            left_motor = 100
        elif left_motor < -100:
            left_motor = -100

print (pygame.version.ver)
pygame.init()
pygame.joystick.init()
try:
        j = pygame.joystick.Joystick(0) # create a joystick instance
        j.init() # init instance
        print ("Joystick " , j.get_name())
except pygame.error:
        print ('No Joystick')
pygame.display.init()
command = [protocol_sign, set_speed, right_motor, left_motor, line]
msg = ''
limit = 50
while 1:
        e = pygame.event.poll() # イベントチェック
        # Joystick関連のイベントチェック
        if e.type == pygame.locals.JOYAXISMOTION: # 7
            x , y = j.get_axis(0), j.get_axis(1)
            set_motor_value(x,y)
            command = [protocol_sign, set_speed, right_motor, left_motor, line]
            r = spi.xfer(command) #戻り値は配列
            print x
            print y
            pygame.event.pump()
        elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
                if e.button == 2:
                        print ('terminate')
                        command = [protocol_sign, off_control, dummy, dummy, line]
                        time.sleep(1)
                        spi.close()
                        pygame.quit()
                        break
                if e.button == 1:
                        limit = 100
                        set_motor_value(x,y)
                        command = [protocol_sign, set_speed, right_motor, left_motor, line]
                        print limit
        elif e.type == pygame.locals.JOYBUTTONUP:
                if e.button == 1:
                        limit = 50
                        set_motor_value(x,y)
                        command = [protocol_sign, set_speed, right_motor, left_motor, line]
                        print limit
        elif e.type == pygame.locals.NOEVENT:
            r = spi.xfer(command) #戻り値は配列
            time.sleep(0.02)
        # if r[0][0] != 0x00:
        #     msg += chr(r[0][0]) + chr(r[1][0]) + chr(r[2][0])
        #     if [0x0a] in r:
        #         print msg
        #         msg = ''
# end of file
