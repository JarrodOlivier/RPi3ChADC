# # Simple example of reading the MCP3008 analog input channels and printing
# # them all out.
# # License: Public Domain

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

count = 0											        #Determines T value determined by frequency button
T = 0.5                                									#This value is frequency
i = 0													#Linked to frequency

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

def timerFormat(t):
    t = t*10
    milli = t % 10
    t //= 10
    sec = t % 60
    t //= 60
    mins = t
    return '%02d:%02d.%d0' % (mins, sec, milli)
	

	
########## The functions of the buttons are defined below ##########

def Tvalue():
    global T, count
    if (count == 0):
        T = 0.5
    elif (count == 1):
        T = 1
    else:
        T = 2
    count += 1
    if (count > 2):
        count = 0

    return count

def stopFn():
    '''
    ch0[4] = "N/A"
    ch1[4] = "N/A"
    ch2[4] = "N/A"
    '''
    pass
##    ch0.insert(5,"N/A")
##    ch0.pop(0)
##    ch1.insert(5,"N/A")
##    ch1.pop(0)
##    ch2.insert(5,"N/A")
##    ch2.pop(0)						

def displayFn():
##    global timeL
##    length = len(timeL)
##    print(length)
    title = ["Time","Timer","Pot","Temp","Light"]
    print('| {0:>8} | {1:>8} | {2:>4} | {3:>4} | {4:>4} |'.format(*title))
    print('-' * 38)
    print(" ", Time[0], " ", Timer[0], "  ", ConvertVolts(ch0[0]), "  ", ConvertTemp(ch1[0]), "  ", ConvertPercentage(ch2[0]), "")
    print(" ", Time[1], " ", Timer[1], "  ", ConvertVolts(ch0[1]), "  ", ConvertTemp(ch1[1]), "  ", ConvertPercentage(ch2[1]), "")
    print(" ", Time[2], " ", Timer[2], "  ", ConvertVolts(ch0[2]), "  ", ConvertTemp(ch1[2]), "  ", ConvertPercentage(ch2[2]), "")
    print(" ", Time[3], " ", Timer[3], "  ", ConvertVolts(ch0[3]), "  ", ConvertTemp(ch1[3]), "  ", ConvertPercentage(ch2[3]), "")
    print(" ", Time[4], " ", Timer[4], "  ", ConvertVolts(ch0[4]), "  ", ConvertTemp(ch1[4]), "  ", ConvertPercentage(ch2[4]), "")

def resetFn():
    global i, wall, timerVal, Timer
    Timer = [0,0,0,0,0]
    wall = time.time()
    timerVal = wall
    i = 0
    #print("\n"*100)
    os.system('clear')
    return i

####### END OF BUTTON FUNTIONS ###########

####### CONVERSION FUNCTIONS #############
def continuous(Time, Timer, ch0, ch1, ch2):
    print('-' * 38)
    print(" ", Time[4], " ", Timer[4], "  ", ConvertVolts(ch0[4]), "  ", ConvertTemp(ch1[4]), "  ", ConvertPercentage(ch2[4]), "")
    
def ConvertVolts(data):

    if type(data) is str:
        return "N/A"
    
    volts = (data * 3.3) / float(1023)
    volts = round(volts,1)
    return str(volts) + " V"

def ConvertPercentage(data):

    if type(data) is str:
        return "N/A"
    
    percent = 100 - (data/570)*100
    percent = round(percent, 0)
    return str(percent) + " %"

#-40 : 0 and 150: 1023
def ConvertTemp(data):
    if type(data) is str:
        return "N/A"

    temp = (data/290) + 40 
    temp = round(temp, 1)
    return str(temp) + " C"

title = ["Time","Timer","Pot","Temp","Light"]
print('| {0:>8} | {1:>8} | {2:>4} | {3:>4} | {4:>4} |'.format(*title))

while True:
    timerVal = time.time() - wall
    start = time.time()
    if (timerVal >= i):

        ####### TIME #######
        timeL = time.strftime("%H:%M:%S", time.localtime())
        Time.insert(5,timeL)
        Time.pop(0)
        ####### END TIME ###

        while(time.time() < start + T):
            time.sleep(0.1)
        ####### TIMER ######
        Timer.insert(5,timerFormat(i))
        Timer.pop(0)
        ####### END TIMER ##
		
	####### Channel 0 ##
        ch0.insert(5,mcp.read_adc(0))
        ch0.pop(0)
	####### END Ch 0 ###
	
	####### Channel 1 ##
        ch1.insert(5,mcp.read_adc(1))
        ch1.pop(0)
	####### END Ch 1 ###
	
	####### Channel 2 ##
        ch2.insert(5,mcp.read_adc(7))								#This reads from channel 7
        ch2.pop(0)
	####### END Ch 2 ###
        
        if (stopState == 1):
            stopFn()      
        
        i += T
        #print(str(i))
        if stopState == 0:
            continuous(Time, Timer, ch0, ch1, ch2)
        else:
            pass
        #print(Time, Timer, ch0, ch1, ch2, sep="     ") #Works brilliantly

	
	

	
	
GPIO.cleanup()

































    
    
