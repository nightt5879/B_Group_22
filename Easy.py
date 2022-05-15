from YYJ import GPIO_RPi
from YYJ import Vision
import time

#初始化L298N驱动
L= GPIO_RPi.L298N(18,16,31,29,35,33)
L.Stop()

def PIDLineTracking():
    #初始化摄像头
    Cam =  Vision.Camera(0, 320, 240)
    PWM_L = 0
    PWM_R = 0
    line = 60  #需要看的是哪一行
    PWM = 0
    Max = 50   #上限值
    Target = 120  #PID中的目标值
    PID = GPIO_RPi.PID(0.2,8,0,0,Target, 0)  #PID的初始化 具体去看YYJ库
    while True:
        Cam.ReadImg(40,280,30,110)
        Centre, Sum, Dst,Bl,White,All= Cam.LineTracking(Cam.Img,line,1)
        Cam.ShowImg(Cam.Img)
        Cam.ShowImg(Dst,'Dst')  #最终处理的图像
        Cam.ShowImg(Bl,'Bl')    #灰度化后的图像
        Now = Centre[line]   #现在的值
        if (Target - 20 <= Now <= Target + 20) or(Now == 0):  #当在一定范围或者突变至没有二值化，则Now与Target没有差值
            Now = Target
        Future = Centre[line - 10]  #“未来”要去到的值
        D = Future - Now  #差值
        Sum = Sum[line] + Sum[line-10]  #黑色像素点的数量
        PWM = PID.TwoDin(Now , D)
        PWM = round(PWM,3)
        """
        PWM: PID计算后的PWM输出
        PWM_L, PWM_R: 实际加载到轮子上的PWM
        """
        print(PWM,'Now', Centre[line],'D', D,'L', PWM_L,'R', PWM_R,'Sum',Sum
              ,'All',All,'White',White[line])
        PWM_L = 12 + PWM
        PWM_R = 12 - PWM
        """
        下面几行是用于控制PWM上下限
        默认两轮上线下限绝对值都为Max一个相同参数
        可以自己根据需要灵活修改
        """
        if PWM_L <= -Max:
            PWM_L = -Max
        elif PWM >= Max:
            PWM_L = Max
        if PWM_R <= -Max:
            PWM_R = -Max
        elif PWM_R >= Max:
            PWM_R = Max
        Cam.Delay(1)

PIDLineTracking()
