import smbus
import math
from time import sleep
bus = smbus.SMBus(1)
degPerPixel = 0.0299947917
ledDistance = 1.3 #In Inches

class pyIRcam:

    def __init__(self):
        self.sensorAddress = 0x58 # address of camera
        self.device = smbus.SMBus(1)
        self.positions = {'found':False,'1':[0,0],'2':[0,0],'3':[0,0],'4':[0,0]}
        # Initialization of the IR sensor
        self.initCMDs = [0x30, 0x01, 0x30, 0x08, 0x06, 0x90, 0x08, 0xC0, 0x1A, 0x40, 0x33, 0x33]

        for i,j in zip(self.initCMDs[0::2], self.initCMDs[1::2]):
            self.device.write_byte_data(self.sensorAddress, i, j)
            sleep(0.01)

    def getPositions(self):
        self.device.write_byte(self.sensorAddress, 0x36)
        data = self.device.read_i2c_block_data(self.sensorAddress, 0x36, 16) # Read the data from the I2C bus
        x = [0x00]*4
        y = [0x00]*4
        i=0

        for j in xrange(1,11,3): # Decode the data coming from the I2C bus
            x[i]=data[j]+((data[j+2] & 0x30) << 4)
            y[i]=data[j+1]+((data[j+2] & 0xC0) << 2)
            i+=1
            i=0

        for j in ('1','2','3','4'): # Put the x and y positions into the dictionary
            self.positions[j][0]=x[i]
            self.positions[j][1]=y[i]
            i+=1

        if ( all(i == 1023 for i in x) and all(i == 1023 for i in y) ): # If all objects are 1023, then there is no IR object in front of the sensor
            self.positions['found'] = False

        else:
                self.positions['found'] = True

    def getDistance(self):
        #getting minimum distance
        distance12 = math.sqrt((self.positions['1'][0] - self.positions ['2'][0]) ** 2 + (self.positions['1'][1] - self.positions['2'][1]) ** 2)
        distance23 = math.sqrt((self.positions['2'][0] - self.positions ['3'][0]) ** 2 + (self.positions['2'][1] - self.positions['3'][1]) ** 2)
        distance13 = math.sqrt((self.positions['1'][0] - self.positions ['3'][0]) ** 2 + (self.positions['1'][1] - self.positions['3'][1]) ** 2)
        distance = min(distance12, distance23, distance13)
        theta = distance * degPerPixel
        phi = 90 - theta / 2
        d = (ledDistance / 2.0) * math.tan (phi * math.pi / 180.0)
        print d




