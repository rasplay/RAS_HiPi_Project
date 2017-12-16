#!/usr/bin/python
# Joystick MPD (Volumio) Controller
#
# Created by www.openmake.cc
#
# Defendency 
# $ pip install python-mpd2
# more commands, visit
# http://pythonhosted.org/python-mpd2/topics/commands.html
#

import sys,os
import RPi.GPIO as gpio
import time
import logging
import mpd

path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(path+'/log'):
    os.makedirs(path+'/log')
logging.basicConfig(filename=path+'/log/joystick.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S', filemode='a', level=logging.INFO)

pipe = None

IS_PRINT_LOG = True

def LOG(level, message):
    if level is 'info':
        logging.info(message)
    if level is 'error':
        logging.error(message)
    if level is 'debug':
        logging.debug(message)
    if IS_PRINT_LOG:
        print(message)

def main():
    global pipe
    pipe = open('/dev/input/js0','r')

    readJoystick()

def readJoystick():
    action = []

    while 1:
        for character in pipe.read(1):
                action += ['%02X' % ord(character)]

                if len(action) == 8:

                        num = int(action[5], 16) # Translate back to integer form
                        percent254 = str(((float(num)-128.0)/126.0)-100)[4:6] # Calculate the percentage of push
                        percent128 = str((float(num)/127.0))[2:4]

                        LOG('debug','%s' % action)

                        if percent254 == '.0':
                                percent254 = '100'
                        if percent128 == '0':
                                percent128 = '100'

                        if action[6] == '01': # Button
                                if action[4] == '01':
                                        LOG('debug','You pressed button: ' + action[7])
                                        if action[7] == '00':
                                            pressRDPadLeft()
                                        if action[7] == '01':
                                            pressRDPadUp()
                                        if action[7] == '02':
                                            pressRDPadDown()
                                        if action[7] == '03':
                                            pressRDPadRight()

                                        if action[7] == '04':
                                            pressL1Button()
                                        if action[7] == '05':
                                            pressL2Button()
                                        if action[7] == '06':
                                            pressR1Button()
                                        if action[7] == '07':
                                            pressR2Button()

                                        if action[7] == '08':
                                            pressSelectButton()
                                        if action[7] == '09':
                                            pressStartButton()

                                else:
                                        LOG('debug','You released button: ' + action[7])

                        ######
                        # Left D-pad Section
                        ######
                        # D-pad left/right
                        elif action[7] == '00': 
                                if action[4] == 'FF':
                                        pressLDPadRight()
                                elif action[4] == '01':
                                        pressLDPadLeft()
                                else:
                                        LOG('debug','You released the D-pad')
                        # D-pad up/down
                        elif action[7] == '01': 
                                if action[4] == 'FF':
                                        pressLDPadDown()
                                elif action[4] == '01':
                                        pressLDPadUp()
                                else:
                                        LOG('debug','You released the D-pad')


                        ######
                        # Left Joystick Section
                        ######
                        # Left Joystick left/right
                        elif action[7] == '04': 
                                if action[4] == 'FF':
                                        pressLJoyDigitalRight()
                                elif action[4] == '01':
                                        pressLJoyDigitalLeft()
                                else:
                                        LOG('debug','You released the left joystick')
                        # Left Joystick up/down
                        elif action[7] == '05': 
                                if action[4] == 'FF':
                                        pressLJoyDigitalDown()
                                elif action[4] == '01':
                                        pressLJoyDigitalUp()
                                else:
                                        LOG('debug','You released the left joystick')

                        ######
                        # Right Analog Joystick Section
                        ######
                        # Right Analog Joystick left/right
                        elif action[7] == '02': 
                                num = int(action[5], 16) # Translate back into integer form
                                if num >= 128:
                                        pressRJoyAnalogLeft()
                                elif num <= 127 \
                                and num != 0:
                                        pressRJoyDigitalRight()
                                else:
                                        LOG('debug','You stopped moving the right joystick')
                        # Right Analog Joystick up/ down
                        elif action[7] == '03': 
                                if num >= 128:
                                        pressRJoyAnalogUp()
                                elif num <= 127 \
                                and num != 0:
                                        pressRJoyAnalogDown()
                                else:
                                        LOG('debug','You stopped moving the right joystick')

                        action = []

######
# Left D-PAD
######
def pressLDPadLeft():
    LOG('debug', 'You Pressed Left button on LeftDPad ')
def pressLDPadRight():
    LOG('debug', 'You Pressed Right button on LeftDPad ')
def pressLDPadUp():
    LOG('debug', 'You Pressed Up button on LeftDPad ')
def pressLDPadDown():
    LOG('debug', 'You Pressed Down button on LeftDPad ')

######
# Left Joystick - Digital
######
def pressLJoyDigitalLeft():
    LOG('debug', 'You Controled Left on LeftJoystick Digital Mode ')
def pressLJoyDigitalRight():
    LOG('debug', 'You Controled Right on LeftJoystick Digital Mode ')
def pressLJoyDigitalUp():
    LOG('debug', 'You Controled Up on LeftJoystick Digital Mode ')
def pressLJoyDigitalDown():
    LOG('debug', 'You Controled Down on LeftJoystick Digital Mode ')

######
# Left Joystick - Analog
######
def pressLJoyAnalogLeft():
    LOG('debug', 'You Controled Left on LeftJoystick Analog Mode ')
def pressLJoyAnalogRight():
    LOG('debug', 'You Controled Right on LeftJoystick Analog Mode ')
def pressLJoyAnalogUp():
    LOG('debug', 'You Controled Up on LeftJoystick Analog Mode ')
def pressLJoyAnalogDown():
    LOG('debug', 'You Controled Down on LeftJoystick Analog Mode ')

######
# Right D-PAD
######
def pressRDPadLeft():
    LOG('debug', 'You Pressed Left button on RightDPad ')
def pressRDPadRight():
    LOG('debug', 'You Pressed Right button on RightDPad ')
def pressRDPadUp():
    LOG('debug', 'You Pressed Up button on RightDPad ')
def pressRDPadDown():
    LOG('debug', 'You Pressed Down button on RightDPad ')

######
# Right Joystick - Digital
######
def pressRJoyDigitalLeft():
    LOG('debug', 'You Controled Left on RightJoystick Digital Mode ')
def pressRJoyDigitalRight():
    LOG('debug', 'You Controled Right on RightJoystick Digital Mode ')
def pressRJoyDigitalUp():
    LOG('debug', 'You Controled Up on RightJoystick Digital Mode ')
def pressRJoyDigitalDown():
    LOG('debug', 'You Controled Down on RightJoystick Digital Mode ')

######
# Right Joystick - Analog
######
def pressRJoyAnalogLeft():
    LOG('debug', 'You Controled Left on RightJoystick Analog Mode ')
def pressRJoyAnalogRight():
    LOG('debug', 'You Controled Right on RightJoystick Analog Mode ')
def pressRJoyAnalogUp():
    LOG('debug', 'You Controled Up on RightJoystick Analog Mode ')
def pressRJoyAnalogDown():
    LOG('debug', 'You Controled Down on RightJoystick Analog Mode ')

######
# Other Buttons
######
global TEST_MPD_HOST, TEST_MPD_PORT, TEST_MPD_PASSWORD
TEST_MPD_HOST     = "localhost"
TEST_MPD_PORT     = "6600"
TEST_MPD_PASSWORD = "volumio"   # password for Volumio / MPD

# Connect with MPD
client = mpd.MPDClient()
connected = False
while connected == False:
        connected = True
        try:
             client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
        except SocketError as e:
             connected = False
        if connected == False:
                LOG('info', 'Couldn\'t connect. Retrying')
                time.sleep(5)
LOG('info', 'MPD Connected')

volumval = 10

def pressL1Button():    # Complete
    global volumval
    LOG('debug', 'You Pressed Left 1 Button')
    volumval = int(client.status()['volume']) + 10
    if volumval>100:
        volumval=100
    LOG('info', 'Volumio Set Volum [%d]!!' % volumval)
    client.setvol(volumval)
    client.ping()
    #time.sleep(1)

def pressL2Button():    # Complete
    global volumval
    LOG('debug', 'You Pressed Left 2 Button')
    volumval = int(client.status()['volume']) - 10
    if volumval<0:
        volumval=0
    LOG('info', 'Volumio Set Volum [%d]!!' % volumval)
    client.setvol(volumval)
    client.ping()
    #time.sleep(1)

def pressR1Button():    # Complete
    LOG('debug', 'You Pressed Right1 Button')
    LOG('info', 'Volumio Next!!')
    client.next()
    client.ping()
    #time.sleep(1)

def pressR2Button():    # Complete
    LOG('debug', 'You Pressed Right 2 Button')
    LOG('info', 'Volumio Previous!!')
    client.previous()
    client.ping()
    #time.sleep(1)
    
def pressSelectButton():
    LOG('debug', 'You Pressed Select Button')
    LOG('info', 'Volumio Stop!!')
    client.stop()
    client.ping()
    #time.sleep(1)
    
def pressStartButton():
    LOG('debug', 'You Pressed Start Button')
    LOG('info', 'Volumio Play!!')
    client.play(0)
    client.ping()
    #time.sleep(1)
    
if __name__ == "__main__":
    main()
