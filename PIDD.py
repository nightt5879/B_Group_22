from YYJ import GPIO_RPi
from YYJ import Vision
import time


#MPU陀螺仪
MPU = GPIO_RPi.MPU6050()
#初始化L298N驱动
L= GPIO_RPi.L298N(18,16,31,29,35,33)
L.Stop()
# L.Forward(40,40)
# time.sleep(1)
# L.Stop()
# print('done')
#初始化摄像头


def TurnRight(TurnTime = 6300):
    Flag = 0
    time.sleep(0.5) #给陀螺仪修正时间
    while True:
        Z = MPU.GetZ()
        Flag += Z
        if Flag <= -TurnTime:
            break
        else:
            L.TurnRight(50,50)
        time.sleep(0.01)
    L.Stop()
    print(Flag)
    print('Trun done')


def Job1(Start = 30, Max = 47, Kp = 6,Ki =0, Kd = 0, Kdd = 0):
    #初始化摄像头
    Cam =  Vision.Camera(0, 320, 240)
    Target = 100
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 60
    PWM = 0
    Max = Max
    Min = -Max
    i = 0
    while True:
        Cam.ReadImg(60,260,30,120)
        Centre, Sum, Dst, Gray,White,All = Cam.LineTracking(Cam.Img,line,0)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line - 10]  #黑色像素点的数量
        if (Target - 20 <= Now <= Target + 20) or(Now == 0):
            Now = Target
        PWM = PID.TwoDin(Now, D)
        PWM = round(PWM,3)
        print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum
              ,'White',White[line],'i',i,'ALL',All)
        PWM_L = Start + PWM
        PWM_R = Start - PWM

        if PWM_L <= Min:
            PWM_L = Min
        elif PWM_L >= Max:
            PWM_L = Max
        if PWM_R <= Min:
            PWM_R = Min
        elif PWM_R >= Max:
            PWM_R = Max
        L.Forward(PWM_R,PWM_L)
        i += 1
        Cam.Delay(1)
    L.Stop()
    Cam.Release()
    print('Tracking done')

Job1(20,40,6,0,0,0)