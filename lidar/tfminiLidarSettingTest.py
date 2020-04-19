# -*- coding: utf-8 -*

import serial
import time

# 打开串口
ser = serial.Serial("/dev/ttyS0", 115200, timeout=1)



def original_setting_test():
    print('change to original settings:')
    #           42     57    02   00   00    00 01 02
    #           42     57    02   00   00    00 01 02
    print('into setting mode:')
    hexer=bytes([0X42,0X57, 0X02, 0X0, 0X0, 0X0, 0x01, 0X02]) 
    print(hexer)
    ser.write(hexer)
    time.sleep(0.1)
    
    print('set back to the original settings:')
    #             42   57    02    00   FF    FF    FF   FF
    hexer=bytes([0X42,0X57, 0X02, 0X0, 0XFF, 0XFF, 0xFF, 0XFF]) 
    print(hexer)
    ser.write(hexer)
    time.sleep(0.1)
    print('quit setting mode:')
    #            42     57    02  00    00    00    00 02 退出配置模式。
    hexer=bytes([0X42,0X57, 0X02, 0X00, 0X00, 0X00, 0x00,0X02]) 
    print(hexer)
    ser.write(hexer)
    
    print('to read data')
    while True:
        time.sleep(0.1)
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回显
            recv = ser.read(count)
            #ser.write(recv)
            print(recv)
        # 清空接收缓冲区
        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)

def set_output_type(tp):
    
    
    
    print('change to original settings:')
    #           42     57    02   00   00    00 01 02
    #           42     57    02   00   00    00 01 02
    print('into setting mode:')
    hexer=bytes([0X42,0X57, 0X02, 0X0, 0X0, 0X0, 0x01, 0X02]) 
    print(hexer)
    ser.write(hexer)
    time.sleep(0.1)
    
    print('set back to the original settings:')
    # 42 57 02 00 00 00 01 06   standard mode
    # 42 57 02 00 00 00 04 06   Pixhawk
    #               42  57    02   00    00   00   04    06   Pixhawk
    hexer=bytes([0X42,0X57, 0X02, 0X0, 0X00, 0X00, 0x04, 0X06]) 
    print(hexer)
    ser.write(hexer)
    time.sleep(0.1)
    print('quit setting mode:')
    #            42     57    02  00    00    00    00 02 退出配置模式。
    hexer=bytes([0X42,0X57, 0X02, 0X00, 0X00, 0X00, 0x00,0X02]) 
    print(hexer)
    ser.write(hexer)
    
    print('to read data')
    while True:
        time.sleep(0.1)
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回显
            recv = ser.read(count)
            #ser.write(recv)
            print(recv)
        # 清空接收缓冲区
        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)

def trigger_test():
    print('send data')
    hexer = bytes([0X42,0X57, 0X02, 0X0, 0X0, 0X0, 0x0,0X41]) 
    print(hexer)
    ser.write(hexer)
    time.sleep(0.1)

    #hexer = chr(0xA5) 
    #print(hexer)
    #ser.write('abc'.encode('utf-8'))


    #myinput=bytes([0X01,0X03,0X00,0X00,0X00,0X01,0X84,0X0A])    # 
    #print(myinput)
    #ser.write(myinput)  
    print('to read data')
    while True:
        time.sleep(0.1)
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回显
            recv = ser.read(count)
            #ser.write(recv)
            print(recv)
        # 清空接收缓冲区
        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)


def getTFminiData():
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 'Y' and recv[1] == 'Y': # 0x59 is 'Y'
                low = int(recv[2].encode('hex'), 16)
                high = int(recv[3].encode('hex'), 16)
                distance = low + high * 256
                print(distance)


def tf_lidar_test():
    try:
        if ser.is_open == False:
            ser.open()
        getTFminiData()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close() 

if __name__ == '__main__':
    try:
        set_output_type(4)
        #trigger_test()
        #original_setting_test()
        #tf_lidar_test()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
