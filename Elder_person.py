

import time
import serial
import pygame
import RPi.GPIO as GPIO

from time import sleep
from array import array


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

usbport = '/dev/ttyS0'
ser = serial.Serial(usbport, 9600)


Assert_key = 36
Water_key1 = 37
Help_key2 = 38
Shoe_Key = 40
IR_Obstacle = 16
Motor_1 = 13
Motor_2 = 15
##Accelerometer = 18

RF_TX1 = 22


GPIO.setup(Assert_key, GPIO.IN)
GPIO.setup(Water_key1, GPIO.IN)
GPIO.setup(Help_key2, GPIO.IN )
GPIO.setup(Shoe_Key, GPIO.IN)
GPIO.setup(IR_Obstacle, GPIO.IN)
##GPIO.setup(Accelerometer, GPIO.IN)

GPIO.setup(RF_TX1, GPIO.OUT)
GPIO.setup(Motor_1, GPIO.OUT)
GPIO.setup(Motor_2, GPIO.OUT)

GPIO.output(RF_TX1, GPIO.LOW)
GPIO.output(Motor_1, GPIO.LOW)
GPIO.output(Motor_2, GPIO.LOW)


UART_Rx_Str = ""
Drug_Alarm_Flag = 0


GPIO.output(RF_TX1, True)
sleep( 2 )
GPIO.output(RF_TX1, False)
sleep( 2 )


print ("Motor Anti Clock - Open")
GPIO.output(Motor_1, False)
GPIO.output(Motor_2, True)
sleep( 1 )
GPIO.output(Motor_1, False)
GPIO.output(Motor_2, False)
sleep( 2 )

print ("Motor Clock - Close")
GPIO.output(Motor_1, True)
GPIO.output(Motor_2, False)
sleep( 1 )
GPIO.output(Motor_1, False)
GPIO.output(Motor_2, False)
sleep( 2 )

pygame.mixer.init()
pygame.mixer.music.load('1water.mp3')
print ("Water Sound Play")
pygame.mixer.music.play()
sleep(10)
pygame.mixer.music.stop()
print ("Water Sound Stop")


ser.write("AT\r")
print ("GSM INITIALIZED")
sleep( 2 )
ser.flushInput()


ser.write("AT+CNMI=2,2,0,0,0\r")
print ("GSM RX ENABLED")
sleep( 2 )
ser.flushInput()


def GSM_Send_SMS( Mobile, SMS ):
    ser.write( "AT+CMGS=\"" )
    ser.write( Mobile )
    ser.write( "\"\r" )
    sleep( 2 )
    ser.write( SMS )
    ser.write( "\x1A" )
    sleep( 4 )



##GSM_Send_SMS( "7619349329", "SYSTEM START" )
##sleep(2)
##ser.flushInput()
##print "TEST SMS SENT"



response1 = raw_input("Please input time for alarm1 MORNING - HHMM: \n")
print("Alarm has been set for %s hrs" % response1)
alarm1 = int(response1)

response2 = raw_input("Please input time for alarm2 AFTERNOON - HHMM: \n")
print("Alarm has been set for %s hrs" % response2)
alarm2 = int(response2)


def Alarm_Scan( ):
# function to continuously check time, buzzer for the set alarm time
# get time as an integer value
        curr_time = int(time.strftime("%H%M"))
        if(curr_time == alarm1):
            Drug_Alarm_Flag = 1
            print("Morning Alarm")
            pygame.mixer.init()
            pygame.mixer.music.load('3morn_alarm.mp3')
            print ("Morning Alarm Sound Play")
            pygame.mixer.music.play()
            sleep(20)
            print ("waiting")
            sleep(20)
            pygame.mixer.music.stop()
            print ("Morning Alarm Sound Stop")
            sleep(5)
            
            print ("Motor Anti Clock - Open")
            GPIO.output(Motor_1, False)
            GPIO.output(Motor_2, True)
            sleep( 1 )
            GPIO.output(Motor_1, False)
            GPIO.output(Motor_2, False)
            sleep( 5 )

            while True:
                if( (GPIO.input(IR_Obstacle) == False) & (Drug_Alarm_Flag == 1) ):
                    print("Drug consumed")
                    sleep(10)
                    Drug_Alarm_Flag = 0
                    break

                elif( (GPIO.input(IR_Obstacle) == True) & (Drug_Alarm_Flag == 1) ):
                    print("Drug not consumed")
                    pygame.mixer.init()
                    pygame.mixer.music.load('8notconsumed.mp3')
                    print ("Drug Not Consumed Sound Play")
                    pygame.mixer.music.play()

                    GSM_Send_SMS( "8792227446", "Drug not consumed, please call and guide your seniors" )
                    sleep(2)
                    ser.flushInput()
                    print ("SMS sent to care taker")

                    sleep(30)
                    pygame.mixer.music.stop()
                    print ("Drug Not Consumed Sound Stop")
                    Drug_Alarm_Flag = 0
                    break

            print ("Motor Clock - Close")
            GPIO.output(Motor_1, True)
            GPIO.output(Motor_2, False)
            sleep( 1 )
            GPIO.output(Motor_1, False)
            GPIO.output(Motor_2, False)
            sleep( 2 )

                
        if(curr_time == alarm2):
            Drug_Alarm_Flag = 1
            print("Afternoon Alarm")
            pygame.mixer.init()
            pygame.mixer.music.load('4noon_alarm.mp3')
            print ("Afternoon Alarm Sound Play")
            pygame.mixer.music.play()
            sleep(20)
            print ("waiting")
            sleep(20)
            pygame.mixer.music.stop()
            print ("Afternoon Alarm Sound Stop")
            sleep(5)
            
            print ("Motor Anti Clock - Open")
            GPIO.output(Motor_1, False)
            GPIO.output(Motor_2, True)
            sleep( 1 )
            GPIO.output(Motor_1, False)
            GPIO.output(Motor_2, False)
            sleep( 5 )
            while True:
                if( (GPIO.input(IR_Obstacle) == False) & (Drug_Alarm_Flag == 1) ):
                    print("Drug consumed")
                    sleep(10)
                    Drug_Alarm_Flag = 0
                    break

                elif( (GPIO.input(IR_Obstacle) == True) & (Drug_Alarm_Flag == 1) ):
                    print("Drug not consumed")
                    pygame.mixer.init()
                    pygame.mixer.music.load('8notconsumed.mp3')
                    print ("Drug Not Consumed Sound Play")
                    pygame.mixer.music.play()

                    GSM_Send_SMS( "8792227446", "Drug not consumed, please call and guide your seniors" )
                    sleep(2)
                    ser.flushInput()
                    print ("SMS sent to care taker")

                    sleep(30)
                    pygame.mixer.music.stop()
                    print ("Drug Not Consumed Sound Stop")
                    Drug_Alarm_Flag = 0
                    break

            print ("Motor Clock - Close")
            GPIO.output(Motor_1, True)
            GPIO.output(Motor_2, False)
            sleep( 1 )
            GPIO.output(Motor_1, False)
            GPIO.output(Motor_2, False)
            sleep( 2 )


Drug_Alarm_Flag = 0
while True:
    Alarm_Scan( )

    time.sleep(5)
    print("other logic of project")


    if( GPIO.input(Water_key1) == False ):
        print("WATER")
        pygame.mixer.init()
        pygame.mixer.music.load('1water.mp3')
        print ("Water Sound Play")
        pygame.mixer.music.play()
        sleep(10)
        pygame.mixer.music.stop()
        print ("Water Sound Stop")



    if( GPIO.input(Help_key2) == False ):
        print("HELP")
        pygame.mixer.init()
        pygame.mixer.music.load('2help.mp3')
        print ("Help Sound Play")
        pygame.mixer.music.play()
        sleep(10)
        pygame.mixer.music.stop()
        print ("Help Sound Stop")


    if( GPIO.input(Assert_key) == False ):
        print("ASSERT CHECK")
        GPIO.output(RF_TX1, True)
        pygame.mixer.init()
        pygame.mixer.music.load('5assert.mp3')
        print ("Assert Sound Play")
        pygame.mixer.music.play()
        sleep(10)
        pygame.mixer.music.stop()
        GPIO.output(RF_TX1, False)
        print ("Assert Sound Stop")


    if( GPIO.input(Shoe_Key) == False ):
        print("Shoe Key")
        pygame.mixer.init()
        pygame.mixer.music.load('6Shoe.mp3')
        print ("Shoe key Sound Play")
        pygame.mixer.music.play()
        sleep(10)
        pygame.mixer.music.stop()
        print ("Shoe key Sound Stop")

##
##
##    if( GPIO.input(Accelerometer) == False ):
##        print("Fall Detect")
##        pygame.mixer.init()
##        pygame.mixer.music.load('7Fall.mp3')
##        print "Fall Detect Sound Play"
##        pygame.mixer.music.play()
##        sleep(10)
##        pygame.mixer.music.stop()
##        print "Fall Detect Sound Stop"
##
## 
        



