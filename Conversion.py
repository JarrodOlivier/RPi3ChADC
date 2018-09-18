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

#0 : 423 and 100%: 0
def ConvertPercentage(data):

    if type(data) is str:
        return "N/A"
    
    percent = 100 - (data/570)*100
    percent = round(percent, 0)
    return str(percent) + " %"
#220 : 22 C
def ConvertTemp(data):
    if type(data) is str:
        return "N/A"
    
    temp = (data/1023) * 100
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
        ch2.insert(5,mcp.read_adc(7))								#This reads from channel 7 of ADC
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
        #print(Time, Timer, ch0, ch1, ch2, sep="     ")

	
	

	
	
GPIO.cleanup()

































    
    
