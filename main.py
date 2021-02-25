import time
import smbus
import pigpio

def getTemp():
    handle = None
    i2c_bus = smbus.SMBus(1)
    D6T_Address = 0x0a
    BUFFER = 19  # Formula: 2 * (1 + n) + 1, whereas n=Number of sensor channel
    temperature_data = [0] * BUFFER

    pi = pigpio.pi()  # use defaults
    handle = pi.i2c_open(1, D6T_Address)  # open device at address 0x0a on bus 1
    tP = [0] * 8
    result = i2c_bus.write_byte(D6T_Address, 0x4c)  #Write command in register

    (bytes_read, temperature_data) = pi.i2c_read_device(handle, len(temperature_data))
    tPTAT = (256 * temperature_data[1] + temperature_data[0]) / 10
    tP[0] = (256 * temperature_data[3] + temperature_data[2]) / 10
    tP[1] = (256 * temperature_data[5] + temperature_data[4]) / 10
    tP[2] = (256 * temperature_data[7] + temperature_data[6]) / 10
    tP[3] = (256 * temperature_data[9] + temperature_data[8]) / 10
    tP[4] = (256 * temperature_data[11] + temperature_data[10]) / 10
    tP[5] = (256 * temperature_data[13] + temperature_data[12]) / 10
    tP[6] = (256 * temperature_data[15] + temperature_data[14]) / 10
    tP[7] = (256 * temperature_data[17] + temperature_data[16]) / 10
    #time.sleep(0.3)   Uncomment this line to use getTemp() function in a loop
    pi.i2c_close(handle)
    pi.stop()
    return (tP, tPTAT)

def startUp():
    '''Write on sensor register to initiate measurement'''
    data1 = [0x02, 0x00, 0x01, 0xee]
    data2 = [0x05, 0x90, 0x3a, 0xb8]
    data3 = [0x03, 0x00, 0x03, 0x8b]
    data4 = [0x03, 0x00, 0x07, 0x97]
    data5 = [0x02, 0x00, 0x00, 0xe9]
    writeToRegister(data1)
    writeToRegister(data2)
    writeToRegister(data3)
    writeToRegister(data4)
    writeToRegister(data5)
    time.sleep(1)
    return None

def writeToRegister(data):
    '''Procedure to send data to desired device'''
    handle=None
    pi = pigpio.pi()
    handle = pi.i2c_open(1, 0x0a)
    pi.i2c_write_device(handle, data)
    pi.i2c_close(handle)
    pi.stop()
    return None

startUp()                           #Starting sensor

temp = (getTemp())                  #Getting temperature readings
print("Temperature in each channel:", temp[0])
print("Ambient Temperature:", temp[1])
