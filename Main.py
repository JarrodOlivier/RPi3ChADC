#Prac4 Main python file
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os

#Globals
Time = [0,0,0,0,0]
Timer = [0,0,0,0,0]
ch0 = [0,0,0,0,0]
ch1 = [0,0,0,0,0]
ch2 = [0,0,0,0,0]                             

count = 0				              #Determines T value determined by frequency button
T = 0.5                               #This value is frequency
i = 0						          #Linked to frequency

index = 0

stopState = 0
wall = time.time()  

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#Button Configuration
reset = 26
frequency = 5
stop = 6
display = 22

#Button setup
GPIO.setup(reset,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(frequency,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(stop,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(display,GPIO.IN, pull_up_down = GPIO.PUD_UP)

def timerFormat(t):                             #Displays time in MM:SS:mm
    t = t*10
    milli = t % 10
    t //= 10
    sec = t % 60
    t //= 60
    mins = t
    return '%02d:%02d.%d0' % (mins, sec, milli)

########## Callback Fns #############################################

def stopOP(channel):
    global stopState
    if(stopState == 1):
        stopState = 0
    else:
        stopState = 1
        stopFn()
    time.sleep(0.5)
    return stopState
	
def frequencyOP(channel):
    Tvalue()
def resetOP(channel):
    resetFn()
def displayOP(channel):
    
    global index, T
    index = index + 1
    print("Button pressed: ", index, "Frequency: ", T)
    displayFn()
######################################################################

#Interrupts
GPIO.add_event_detect(reset, GPIO.FALLING, callback = resetOP, bouncetime = 500)
GPIO.add_event_detect(frequency, GPIO.FALLING, callback = frequencyOP, bouncetime = 500)
GPIO.add_event_detect(stop, GPIO.FALLING, callback = stopOP, bouncetime = 200)
GPIO.add_event_detect(display, GPIO.FALLING, callback = displayOP, bouncetime = 4000)       
