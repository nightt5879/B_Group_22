import serial
import time
import _thread  # 导入线程包
from YYJ import GPIO_RPi  #树莓派硬件库
from YYJ import Vision  #视觉库

#初始化树莓派串口
ser = serial.Serial("/dev/ttyAMA0", 115200)  

#初始化L298N驱动
L= GPIO_RPi.L298N(18,16,31,29,35,33)
L.Stop()

#MPU陀螺仪初始化
MPU = GPIO_RPi.MPU6050()

#超声波初始化
Ul = GPIO_RPi.Ultrasonic(36, 38)

#LED初始化
Led1 = GPIO_RPi.IO(11, 'OUT')
Led2 = GPIO_RPi.IO(37, 'OUT')
Led3 = GPIO_RPi.IO(12, 'OUT')
Led4 = GPIO_RPi.IO(7, 'OUT')
Led2.SetPWM(2)    #PWM用于调用闪烁，要使用的就是红色与橙色的灯
Led4.SetPWM(2)

#参数初始化
Color = None  #颜色的全局变量
def LedModle(Select):   #LED模块整体控制函数  四个颜色分别对于赛道的四个路段
    if Select == "Green\n":
        Led1.OutHigh()
        Led2.ChangePWM(0)  #红灯关
        Led3.OutLow()
        Led4.ChangePWM(50)  #黄灯闪烁
    elif Select == "Red\n":
        Led1.OutLow()
        Led2.ChangePWM(100)  #红灯亮
        Led3.OutLow()
        Led4.ChangePWM(50)  #黄灯闪烁
    elif Select == "Blue\n":
        Led1.OutLow()
        Led2.ChangePWM(0)  #红灯关闭
        Led3.OutHigh()
        Led4.ChangePWM(50)  #黄灯闪烁
    elif Select == "Yellow\n":
        Led1.OutLow()
        Led2.ChangePWM(50)  #红灯闪烁（由于要表示黄灯故使用另一个灯进行闪烁
        Led3.OutLow()
        Led4.ChangePWM(100)  #黄灯亮
    

def GetData():    #串口读取数据
    global Color  
    while True:
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回显
            recv = ser.read(count)
            ser.write(recv)
            Color = str(recv, encoding="utf-8")  #将bytes转为str
#             print(Str)
            LedModle(Color)  #传入闪烁模组的颜色值
        time.sleep(0.01)

def Job1(Start = 30, Max = 47, Kp = 6,Ki =0, Kd = 0, Kdd = 0):
    #初始化摄像头
    L.Forward(20,20)
    time.sleep(2)
    L.Stop()
    Cam =  Vision.Camera(0, 320, 240)
    Target = 120
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 75
    PWM = 0
    Max = Max
    Min = -Max
    i = 0
    while True:
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,While,All = Cam.LineTracking(Cam.Img,line)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line - 10]  #黑色像素点的数量
        if Target - 20 <= Now <= Target + 20:
            Now = Target
#             L.Stop()
        PWM = PID.OneDin(Now)
        PWM = round(PWM,3)
        print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum,'Color',Color)
        PWM_L = Start + PWM
        PWM_R = Start - PWM
#         if abs(PWM) >= 100:
#             PWM_L = PMW_R = 0
        if PWM_L <= Min:
            PWM_L = Min
        elif PWM_L >= Max:
            PWM_L = Max
        if PWM_R <= Min:
            PWM_R = Min
        elif PWM_R >= Max:
            PWM_R = Max
        L.Forward(PWM_R,PWM_L)
        if Color == "Green\n":
            break
        Cam.Delay(1)
    L.Stop()
    Cam.Release()
    print('Tracking done')
   
def Job2(Start = 30, Max = 47, Kp = 6,Ki =0, Kd = 0, Kdd = 0, SumMax = 20, Imax = 2):
    #初始化摄像头
    Cam =  Vision.Camera(0, 320, 240)
    Target = 110
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 75
    PWM = 0
    Max = Max
    Min = -Max
    i = 0
    while True:
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,While,All = Cam.LineTracking(Cam.Img,line)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line - 10]  #黑色像素点的数量
        if Target - 20 <= Now <= Target + 20:
            Now = Target
#             L.Stop()
        PWM = PID.TwoDin(Now , D)
        PWM = round(PWM,3)
        print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum)
        PWM_L = Start + PWM
        PWM_R = Start - PWM
#         if abs(PWM) >= 100:
#             PWM_L = PMW_R = 0
        if PWM_L <= Min:
            PWM_L = Min
        elif PWM_L >= Max:
            PWM_L = Max
        if PWM_R <= Min:
            PWM_R = Min
        elif PWM_R >= Max:
            PWM_R = Max
        if Sum <= SumMax:
            i += 1
            if i>= Imax:
                break   #到了大转弯推出了
        L.Forward(PWM_R,PWM_L)
        Cam.Delay(1)
    L.Stop()
    Cam.Release()
    print('Tracking done')
    
def Job3(Start = 30, Max = 47, Kp = 6, Ki =0, Kd = 0, Kdd = 0):
    #初始化摄像头
    Cam =  Vision.Camera(0, 320, 240)
    Target = 110
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 75
    PWM = 0
    Max = Max
    Min = -Max
    while True:
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,While,All = Cam.LineTracking(Cam.Img,line)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        if Target - 20 <= Now <= Target + 20:
            Now = Target
#             L.Stop()
        PWM = PID.TwoDin(Now , D)
        PWM = round(PWM,3)
        print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum)
        PWM_L = Start + PWM
        PWM_R = Start - PWM
#         if abs(PWM) >= 100:
#             PWM_L = PMW_R = 0
        if PWM_L <= Min:
            PWM_L = Min
        elif PWM_L >= Max:
            PWM_L = Max
        if PWM_R <= Min:
            PWM_R = Min
        elif PWM_R >= Max:
            PWM_R = Max
        if Color == "Red\n":
            break   #到了寻线结束就退出
        L.Forward(PWM_R,PWM_L)
        Cam.Delay(1)
    L.Stop()
    
#     TurnRight(2500)
    Cam.Release()
    print('Tracking done')

def Barrier(a,b):   #直走直到超声波检测距离在一定值范围内
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
    L.Stop()
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
    
def Job4():
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
 
def Job5(Start = 30, Max = 47, Kp = 6,Ki =0, Kd = 0, Kdd = 0, SumMax = 20, Imax = 2):
    #初始化摄像头
#     L.Forward(40,40)
#     time.sleep(1)
#     L.Stop()
    Cam =  Vision.Camera(0, 320, 240)
    Target = 110
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 75
    PWM = 0
    Max = Max
    Min = -Max
    i = 0
    while True:
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,While,All = Cam.LineTracking(Cam.Img,line)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line - 10]  #黑色像素点的数量
        if Target - 20 <= Now <= Target + 20:
            Now = Target
#             L.Stop()
        PWM = PID.TwoDin(Now , D)
        PWM = round(PWM,3)
        print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum)
        PWM_L = Start + PWM
        PWM_R = Start - PWM
#         if abs(PWM) >= 100:
#             PWM_L = PMW_R = 0
        if PWM_L <= Min:
            PWM_L = Min
        elif PWM_L >= Max:
            PWM_L = Max
        if PWM_R <= Min:
            PWM_R = Min
        elif PWM_R >= Max:
            PWM_R = Max
        if Sum <= SumMax:
            i += 1
            if i>= Imax:
                break   #到了大转弯推出了
        L.Forward(PWM_R,PWM_L)
        Cam.Delay(1)
    L.Stop()
    
    L.Forward(20,20)
    time.sleep(0.3)
    TurnRight(7000)  #需要转一下
    Cam.Release()
    print('Tracking done')
    
def Job6(Start = 30, Max = 47, Kp = 6, Ki =0, Kd = 0, Kdd = 0):
    #初始化摄像头
    Cam =  Vision.Camera(0, 320, 240)
    Target = 110
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 75
    PWM = 0
    Max = Max
    Min = -Max
    while True:
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,While,All = Cam.LineTracking(Cam.Img,line)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        if Target - 20 <= Now <= Target + 20:
            Now = Target
#             L.Stop()
        PWM = PID.TwoDin(Now , D)
        PWM = round(PWM,3)
        print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum,)
        PWM_L = Start + PWM
        PWM_R = Start - PWM
#         if abs(PWM) >= 100:
#             PWM_L = PMW_R = 0
        if PWM_L <= Min:
            PWM_L = Min
        elif PWM_L >= Max:
            PWM_L = Max
        if PWM_R <= Min:
            PWM_R = Min
        elif PWM_R >= Max:
            PWM_R = Max
        if Color == "Yellow\n":
            break   #到了寻线结束就退出
        L.Forward(PWM_R,PWM_L)
        Cam.Delay(1)
    L.Stop()
    
    TurnLeft(4500)  #需要转一下
    Cam.Release()
    print('Tracking done')
    
if __name__ == '__main__':
    _thread.start_new_thread(GetData, ())  # 开启线程，执行GetData
    
    Job1(20,40,4,0,0,0)
#     Job2(30,47,6,0,0,0,20,2)
#     Job3(10,30,6,0,0,0)
#     Job4()
#     Job5(20,47,6,0,0,0,20,2)
#     Job6(30,47,6,0,0,0)
#     Job5(30,47,6,0,0,0,20,2)
#     L.Forward(20,20)
#     time.sleep(1)
#     L.Stop()
