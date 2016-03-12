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
set_speed = [0x00]
right_motor = [0x00]
left_motor = [0x00]

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

while 1:
        e = pygame.event.poll() # イベントチェック
        # Joystick関連のイベントチェック
        if e.type == pygame.locals.JOYAXISMOTION: # 7
            x , y = j.get_axis(0), j.get_axis(1)
            #print ('x and y : ',  str(x) +' , '+ str(y))
            right_motor[0] = int(x * 100)
            left_motor[0] = int(y * 100)
            spi.xfer(set_speed)
            spi.xfer(right_motor)
            spi.xfer(left_motor)
            print x
            print y
            pygame.event.pump()
        elif e.type == pygame.locals.JOYHATMOTION: # 9
            print ('hat motion')
            time.sleep(1)
            spi.close()
            pygame.quit()
            break
        elif e.type == pygame.locals.NOEVENT:
            spi.xfer(set_speed)
            spi.xfer(right_motor)
            spi.xfer(left_motor)
            time.sleep(0.05)
# end of file
