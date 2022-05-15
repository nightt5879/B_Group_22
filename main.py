import serial
import time
import _thread  # 导入线程包
from YYJ import GPIO_RPi  #树莓派硬件库
from YYJ import Vision  #视觉库#初始化树莓派串口
 
#初始化
ser = serial.Serial("/dev/ttyAMA0", 115200) 
L= GPIO_RPi.L298N(18,16,31,29,35,33)
L.Stop()
MPU = GPIO_RPi.MPU6050()
Ul = GPIO_RPi.Ultrasonic(36, 38)
Led1 = GPIO_RPi.IO(11, 'OUT')
Led2 = GPIO_RPi.IO(37, 'OUT')
Led3 = GPIO_RPi.IO(12, 'OUT')
Led4 = GPIO_RPi.IO(7, 'OUT')
Led2.SetPWM(2)    #PWM用于调用闪烁，要使用的就是红色与橙色的灯
Led4.SetPWM(2)
Middle = GPIO_RPi.IO(40,'IN')
Right = GPIO_RPi.IO(15,'IN')
Left = GPIO_RPi.IO(13,'IN')

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

def LineTracking(Start = 30, Max = 47, Kp = 6,Ki =0, Kd = 0, Kdd = 0,Set = 1):
    #初始化摄像头
#     if Set == 1:
#         L.Forward(20,20)
#         time.sleep(2)
#         L.Stop()
    Cam =  Vision.Camera(0, 320, 240)
    Target = 120
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 70
    PWM = 0
    Max = Max
    Min = -Max
    i = 0
    Click = 0
    while True:
        LE = Left.Input()
        R = Right.Input()
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,White,All = Cam.LineTracking(Cam.Img,line,1)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line - 10]  #黑色像素点的数量
        if (Target - 25 <= Now <= Target + 25) or(Now == 0):
            Now = Target
        if (Now <= Target - 55) and (LE == 0):
#             Now = 60
            L.Forward(30,-30)
            time.sleep(0.5)
            L.Stop()
        elif (Now >= Target + 55) and (R == 0):
#             Now =180
            L.Forward(-30,30)
            time.sleep(0.5)
            L.Stop()
        # 串口发送数据
#         Bytes = str(Now) + ','
#         Bytes = bytes(Bytes, encoding = "utf8")
#         ser.write(Bytes)

        PWM = PID.TwoDin(Now, D)
#         PWM = round(PWM,3)
#         print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum
#               ,'White',White[line],'i',i,'ALL',All)
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
        if Set == 1:    #用于选择是哪一种寻线
            if (10<= (White[line]+White[line-10]+White[line-15]) <= 500) and (i>= 400):  #防止第一个三角形
                break
#         if LE == 0:
#             L.Forward(30,-30)
#         elif R == 0:
#             L.Forward(-30,30)
#         elif LE == 0 and D <= -8:
#             L.Forward(40,-40)
#         elif R == 0 and D >= 8:
#             L.Forward(-40,40)
#         else:
#             L.Forward(14,14)
        time.sleep(0.01)
        if Set == 2:
            if (7000<= All <= 15000) and i >= 300:
                i = 0
                Click += 1
                if Click >= 4:
                    break
                
        i += 1
        Cam.Delay(1)
    L.Stop()
    Cam.Release()
    print('Tracking done')
    print(Click,i)

def LineTracking2(Start = 30, Max = 47, Kp = 6,Ki =0, Kd = 0, Kdd = 0,SumMax = 20):
    #初始化摄像头
#     if Set == 1:
#         L.Forward(20,20)
#         time.sleep(2)
#         L.Stop()
    Cam =  Vision.Camera(0, 320, 240)
    Target = 120
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 80
    PWM = 0
    Max = Max
    Min = -Max
    i = 0
    while True:
        LE = Left.Input()
        R = Right.Input()
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,White,All = Cam.LineTracking(Cam.Img,line,1)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line - 10]  #黑色像素点的数量
        if (Target - 25 <= Now <= Target + 25) or(Now == 0):
            Now = Target
        if (Now <= Target - 55) and (LE == 0):
#             Now = 60
            L.Forward(30,-30)
            time.sleep(0.5)
            L.Stop()
        elif (Now >= Target + 55) and (R == 0):
#             Now =180
            L.Forward(-30,30)
            time.sleep(0.5)
            L.Stop()
        # 串口发送数据
#         Bytes = str(Now) + ','
#         Bytes = bytes(Bytes, encoding = "utf8")
#         ser.write(Bytes)

        PWM = PID.TwoDin(Now, D)
#         PWM = round(PWM,3)
#         print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum
#               ,'White',White[line],'i',i,'ALL',All)
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
#         if LE == 0:
#             L.Forward(30,-30)
#         elif R == 0:
#             L.Forward(-30,30)
#         elif LE == 0 and D <= -8:
#             L.Forward(40,-40)
#         elif R == 0 and D >= 8:
#             L.Forward(-40,40)
#         else:
#             L.Forward(14,14)
        if All >= 6500:
            break
#         if Sum <= SumMax:
#             break
        Cam.Delay(1)
    L.Stop()
    Cam.Release()
    print('Tracking done')
    
def LineTracking3(Start = 30, Max = 47, Kp = 6,Ki =0, Kd = 0, Kdd = 0,SumMax = 20):
    #初始化摄像头
#     if Set == 1:
#         L.Forward(20,20)
#         time.sleep(2)
#         L.Stop()
    Cam =  Vision.Camera(0, 320, 240)
    Target = 120
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 80
    PWM = 0
    Max = Max
    Min = -Max
    i = 0
    while True:
        LE = Left.Input()
        R = Right.Input()
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,White,All = Cam.LineTracking(Cam.Img,line,1)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line - 10]  #黑色像素点的数量
        if (Target - 25 <= Now <= Target + 25) or(Now == 0):
            Now = Target
        if (Now <= Target - 55) and (LE == 0):
#             Now = 60
            L.Forward(30,-30)
            time.sleep(0.5)
            L.Stop()
        elif (Now >= Target + 55) and (R == 0):
#             Now =180
            L.Forward(-30,30)
            time.sleep(0.5)
            L.Stop()
        # 串口发送数据
#         Bytes = str(Now) + ','
#         Bytes = bytes(Bytes, encoding = "utf8")
#         ser.write(Bytes)

        PWM = PID.TwoDin(Now, D)
#         PWM = round(PWM,3)
#         print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum
#               ,'White',White[line],'i',i,'ALL',All)
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
#         if LE == 0:
#             L.Forward(30,-30)
#         elif R == 0:
#             L.Forward(-30,30)
#         elif LE == 0 and D <= -8:
#             L.Forward(40,-40)
#         elif R == 0 and D >= 8:
#             L.Forward(-40,40)
#         else:
#             L.Forward(14,14)
        if Sum <= SumMax or Color =="Yellow\n":
            break
        Cam.Delay(1)
    L.Stop()
    Cam.Release()
    print('Tracking done')
   
def LineTracking4(Start = 30, Max = 47, Kp = 6,Ki =0, Kd = 0, Kdd = 0,SumMax = 20):
    #初始化摄像头
#     if Set == 1:
#         L.Forward(20,20)
#         time.sleep(2)
#         L.Stop()
    Cam =  Vision.Camera(0, 320, 240)
    Target = 120
    PID = GPIO_RPi.PID(0.2,Kp,Ki,Kd,Target, Kdd)
    PWM_L = 0
    PWM_R = 0
    line = 80
    PWM = 0
    Max = Max
    Min = -Max
    i = 0
    while True:
        LE = Left.Input()
        R = Right.Input()
        Cam.ReadImg(40,280,30,120)
        Centre, Sum, Dst, Gray,White,All = Cam.LineTracking(Cam.Img,line,1)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')
        Cam.ShowImg(Gray,'Gray')
        Now = Centre[line]   #现在的值
        Future = Centre[line - 20]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line - 10]  #黑色像素点的数量
        if (Target - 25 <= Now <= Target + 25) or(Now == 0):
            Now = Target
        if (Now <= Target - 55) and (LE == 0):
#             Now = 60
            L.Forward(30,-30)
            time.sleep(0.5)
            L.Stop()
        elif (Now >= Target + 55) and (R == 0):
#             Now =180
            L.Forward(-30,30)
            time.sleep(0.5)
            L.Stop()
        # 串口发送数据
#         Bytes = str(Now) + ','
#         Bytes = bytes(Bytes, encoding = "utf8")
#         ser.write(Bytes)

        PWM = PID.TwoDin(Now, D)
#         PWM = round(PWM,3)
#         print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'SUM',Sum
#               ,'White',White[line],'i',i,'ALL',All)
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
#         if LE == 0:
#             L.Forward(30,-30)
#         elif R == 0:
#             L.Forward(-30,30)
#         elif LE == 0 and D <= -8:
#             L.Forward(40,-40)
#         elif R == 0 and D >= 8:
#             L.Forward(-40,40)
#         else:
#             L.Forward(14,14)
        if All >= 6500 and i>= 100:
            break
#         if Sum <= SumMax:
#             break
        i += 1
        Cam.Delay(1)
    L.Stop()
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
#         print('C',Correct,'D',Dis)
        if a<= Dis <= b:
            L.Stop()
            break
        if Sum <= -200:
            L.Forward(20 + Correct,20 - Correct)
        if Sum >= 200:
            L.Forward(20 + Correct,20 - Correct)
        else:
            L.Forward(20,20)
            
def TurnLeft(TurnTime = 6300):
    Flag = 0
    time.sleep(0.5) #给陀螺仪修正时间
    while True:
#         print(Flag)
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
    
def CSB():
    Barrier(2,5)
    TurnLeft(7500)
    time.sleep(0.5)
    
    Barrier(2,8)
    TurnRight(7900)
    time.sleep(0.5)
    Barrier(3,6)
    
    TurnRight(7500)
    time.sleep(0.5)
    Barrier(2,6)
    TurnLeft(7400)
    
    time.sleep(0.5)
    L.Forward(20,20)
    time.sleep(1.5)
    L.Stop()
    
if __name__ == '__main__':
    _thread.start_new_thread(GetData, ())  # 开启线程，执行GetData
    Led2.ChangePWM(100)  #红灯亮
    while True:
        Answer = Middle.Input()
        if Answer == 1:
            break
        time.sleep(0.01)
    Led1.OutHigh()
    L.Forward(20,20)
    time.sleep(1.5)
    L.Stop()
    LineTracking(20,40,6,0,0,0,1)
    L.Forward(20,20)
    time.sleep(0.2)
    L.Stop()
    TurnRight(11000)
    LineTracking(25,50,7,0,-1,0,2)
    CSB()
    LineTracking2(18,30,6,0,0,0,20)
    L.Forward(20,20)
    time.sleep(0.3)
    L.Stop()
    TurnRight(7000)
    L.Forward(20,20)
    time.sleep(1)
    L.Stop()
    LineTracking3(25,35,6,0,-2,0,20)
    TurnLeft(4000)
    LineTracking4(18,30,6,0,0,0,2000)
    L.Forward(20,20)
    time.sleep(0.7)
    L.Stop()
    TurnRight(7000)
    L.Forward(20,20)
    time.sleep(1.5)
    L.Stop()
#     L.Forward(20,20)
#     time.sleep(1.5)
#     L.Stop()