from YYJ import GPIO_RPi
from YYJ import Vision
import time

#初始化L298N驱动
L= GPIO_RPi.L298N(18,16,31,29,35,33)
L.Stop()

L.Stop()
print('done')