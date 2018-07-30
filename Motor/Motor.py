import RPi.GPIO as GPIO

# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.

def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

# setBit() returns an integer with the bit at 'offset' set to 1.

def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

# clearBit() returns an integer with the bit at 'offset' cleared.

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.

def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

MOTORLATCH = 18   # 12 on arduino - green wire (* good for visual reference to use same colors or change to correct color for reference)
MOTORCLK = 24     # 4 on arduino - purple wire
MOTORENABLE = 23  # 7 on arduino - yellow wire
MOTORDATA = 25    # 8 on arduino - blue wire

MOTOR1_A = 2
MOTOR1_B = 3
MOTOR2_A = 1
MOTOR2_B = 4
MOTOR4_A = 0
MOTOR4_B = 6
MOTOR3_A = 5
MOTOR3_B = 7

latch_state = 0

class AFMotorController:

    TimerInitialized = 0

    def __init__(self):
        TimerInitialized = 0

    def enable(self):
        global latch_state
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(MOTORENABLE, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(25, GPIO.OUT)

        latch_state = 0

        self.latch_tx(); #reset

        GPIO.output(MOTORENABLE, 0)

    def latch_tx(self):
        global latch_state
        
        GPIO.output(MOTORLATCH, 0)
        GPIO.output(MOTORDATA, 0)

        for i in range(0, 7):
            GPIO.output(MOTORCLK, 0)

            if testBit(latch_state, 7 - i) > 0:
                GPIO.output(MOTORDATA, 1)
            else:
                GPIO.output(MOTORDATA, 0)

            GPIO.output(MOTORCLK, 1)

        GPIO.output(MOTORLATCH, 1)

MC = AFMotorController()                

class AF_DCMotor:

    motornum = 0
    pwmFreq = 0
    
    def __init__(self, num, freq):
        motornum = num
        pwmFreq = freq
        global latch_state

        MC.enable()

        if num == 1:
            latch_state &= ~(1 << MOTOR1_A) & ~(1 << MOTOR1_B)
            MC.latch_tx()
            self.initPWM1(freq)

            #TODO if num == 2, 3 and 4

    def initPWM1(self, freq):
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11, 0) #arduino 11 also, brown wire
            
        
motor = AF_DCMotor(1, 9600)
input("Hæ!")
GPIO.cleanup()
        
        
