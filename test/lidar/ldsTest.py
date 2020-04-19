# -*- coding: utf-8 -*

import serial
import time

# 打开串口
ser = serial.Serial("/dev/ttyS0", 115200, timeout=1)

RPLIDAR_CMD_SYNC_BYTE = 0xA5
RPLIDAR_CMD_GET_DEVICE_HEALTH = 0x52

def data_split(bytes_input):
    start_flag = b'\xfa'
    bytes_left = bytes_input
    lst_data = []
    start_index = bytes_left.find(start_flag)
    while start_index != -1:
        if start_index == 0:
            bytes_left = bytes_left[start_index+1 : ]
            start_index = bytes_left.find(start_flag)
            continue
        if start_index < 21:
            if len(bytes_left) > 21 and bytes_left[21] == start_flag[0]:
                start_index = 21
        data_part = bytes_left[0:start_index]
        lst_data.append(data_part)
        bytes_left = bytes_left[start_index+1 : ]
        start_index = bytes_left.find(start_flag)
    return lst_data

def data_analysis(data_input):
    if len(data_input) != 21:
        return None
    raw_bytes = data_input
    start_idx = 0
    data_idx = data_input[start_idx + 0]
    # accumulate count for avg. time increment
    motor_speed = (raw_bytes[start_idx + 2] << 8) + raw_bytes[start_idx + 1] 
    rpms=(raw_bytes[start_idx + 2]<<8|raw_bytes[start_idx + 1])/64
    records =[]
    for i in range(4):
        byte0 = raw_bytes[start_idx + 3 + i * 4]
        byte1 = raw_bytes[start_idx + 3 + i * 4 + 1]
        # No return/max range/too low of reflectivity
        flag_invalid = byte1 >> 7
        # Object too close, possible poor reading due to proximity kicks in at < 0.6m
        flag_warning = (byte1 >> 6)&0x1
        
        distance = ((byte1 & 0x3F)<< 8) + byte0;

        byte2 = raw_bytes[start_idx + 3 + i * 4 + 2]
        byte3 = raw_bytes[start_idx + 3 + i * 4 + 3]
        intensity = (byte3 << 8) + byte2;
        records.append([flag_invalid, flag_warning, distance/1000, intensity])
    ret = [data_idx, rpms, records]
    return ret
    

def main():
    print('send data')
    #hexer=bytes([0XA5,0X52]) 
    #print(hexer)
    #ser.write(hexer)
    ser.write(b'startlds$')

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
            data_parts = data_split(recv)
            for item in data_parts:
                parse_ret = data_analysis(item)
                if parse_ret is None:
                    continue
                idx = parse_ret[0]
                speed = parse_ret[1]
                distance0 = parse_ret[2][0][2]
                distance1 = parse_ret[2][1][2]
                distance2 = parse_ret[2][2][2]
                distance3 = parse_ret[2][3][2]
                print('idx:{} speed:{} distance:{},{},{},{},'.format(idx, speed, distance0, distance1, distance2, distance3))
                #print(len(item))
                #print(item)
            #print(recv)
        # 清空接收缓冲区
        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
