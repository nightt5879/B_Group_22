rom YYJ import GPIO_RPi
from YYJ import Vision
import time

#超声波
Ul = GPIO_RPi.Ultrasonic(36, 38)
#MPU陀螺仪
MPU = GPIO_RPi.MPU6050()
#初始化L298N驱动
L= GPIO_RPi.L298N(18,16,31,29,35,33)

def Barrier(a,b):
    Sum = 0
    while True:
        Sum += MPU.GetZ()
        Dis = Ul.GetDistance()
        Correct = 0.05 * Sum
        if Correct >= 20:
            Correct = 20
        elif Correct <= -20:
            Correct = -20
        print('C',Correct,'D',Dis)
        if a<= Dis <= b:
            L.Stop()
            break
        if Sum <= -200:
            L.Forward(20 + Correct,20 - Correct)
        if Sum >= 200:
            L.Forward(20 + Correct,20 - Correct)
        else:
            L.Forward(20,20)
        time.sleep(0.05)
    

def TurnLeft(TurnTime = 6300):
    Flag = 0
    time.sleep(0.5) #给陀螺仪修正时间
    while True:
        print(Flag)
        Z = MPU.GetZ()
        Flag += Z
        if Flag >= TurnTime:
            break
        else:
            L.TurnLeft(40,40)
        time.sleep(0.01)
    L.Stop()
    print(Flag)
    print('Left done')
    
def TurnRight(TurnTime = 6300):
    Flag = 0
    time.sleep(0.5) #给陀螺仪修正时间
    while True:
        Z = MPU.GetZ()
        Flag += Z
        if Flag <= -TurnTime:
            break
        else:
            L.TurnRight(40,40)
        time.sleep(0.01)
    L.Stop()
    print(Flag)
    print('Right done')

Barrier(2,5)
TurnLeft(7500)
time.sleep(0.5)
Barrier(2,6)
TurnRight(7000)
time.sleep(0.5)
Barrier(2,6)
TurnRight(8000)
time.sleep(0.5)
Barrier(2,6)
TurnLeft(7000)
time.sleep(0.5)
L.Forward(40,40)
time.sleep(1)
L.Stop()