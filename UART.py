# -*- coding: utf-8 -*
import serial
import time
# 打开串口
ser = serial.Serial("/dev/ttyAMA0", 115200)

def main():
    i = 0
    while True:
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回显
            recv = ser.read(count)
            ser.write(recv)
#             print(recv)
            Str = str(recv, encoding="utf-8")
            print(Str)
            print(i)
            i += 1
#             print(type(Str))
            
        # 清空接收缓冲区
#         ser.flushInput()
        ser.write(b'1,')
#         ser.write(b'1')
        # 必要的软件延时
        time.sleep(0.01)
#         print(1)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
            