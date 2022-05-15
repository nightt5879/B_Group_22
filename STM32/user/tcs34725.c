
/******************************************************************************/
#define TCS34725_ADDRESS          (0x29)

#define TCS34725_COMMAND_BIT      (0x80)

#define TCS34725_ENABLE           (0x00)
#define TCS34725_ENABLE_AIEN      (0x10)    /* RGBC Interrupt Enable */
#define TCS34725_ENABLE_WEN       (0x08)    /* Wait enable - Writing 1 activates the wait timer */
#define TCS34725_ENABLE_AEN       (0x02)    /* RGBC Enable - Writing 1 actives the ADC, 0 disables it */
#define TCS34725_ENABLE_PON       (0x01)    /* Power on - Writing 1 activates the internal oscillator, 0 disables it */
#define TCS34725_ATIME            (0x01)    /* Integration time */
#define TCS34725_WTIME            (0x03)    /* Wait time (if TCS34725_ENABLE_WEN is asserted) */
#define TCS34725_WTIME_2_4MS      (0xFF)    /* WLONG0 = 2.4ms   WLONG1 = 0.029s */
#define TCS34725_WTIME_204MS      (0xAB)    /* WLONG0 = 204ms   WLONG1 = 2.45s  */
#define TCS34725_WTIME_614MS      (0x00)    /* WLONG0 = 614ms   WLONG1 = 7.4s   */
#define TCS34725_AILTL            (0x04)    /* Clear channel lower interrupt threshold */
#define TCS34725_AILTH            (0x05)
#define TCS34725_AIHTL            (0x06)    /* Clear channel upper interrupt threshold */
#define TCS34725_AIHTH            (0x07)
#define TCS34725_PERS             (0x0C)    /* Persistence register - basic SW filtering mechanism for interrupts */
#define TCS34725_PERS_NONE        (0b0000)  /* Every RGBC cycle generates an interrupt                                */
#define TCS34725_PERS_1_CYCLE     (0b0001)  /* 1 clean channel value outside threshold range generates an interrupt   */
#define TCS34725_PERS_2_CYCLE     (0b0010)  /* 2 clean channel values outside threshold range generates an interrupt  */
#define TCS34725_PERS_3_CYCLE     (0b0011)  /* 3 clean channel values outside threshold range generates an interrupt  */
#define TCS34725_PERS_5_CYCLE     (0b0100)  /* 5 clean channel values outside threshold range generates an interrupt  */
#define TCS34725_PERS_10_CYCLE    (0b0101)  /* 10 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_15_CYCLE    (0b0110)  /* 15 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_20_CYCLE    (0b0111)  /* 20 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_25_CYCLE    (0b1000)  /* 25 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_30_CYCLE    (0b1001)  /* 30 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_35_CYCLE    (0b1010)  /* 35 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_40_CYCLE    (0b1011)  /* 40 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_45_CYCLE    (0b1100)  /* 45 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_50_CYCLE    (0b1101)  /* 50 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_55_CYCLE    (0b1110)  /* 55 clean channel values outside threshold range generates an interrupt */
#define TCS34725_PERS_60_CYCLE    (0b1111)  /* 60 clean channel values outside threshold range generates an interrupt */
#define TCS34725_CONFIG           (0x0D)
#define TCS34725_CONFIG_WLONG     (0x02)    /* Choose between short and long (12x) wait times via TCS34725_WTIME */
#define TCS34725_CONTROL          (0x0F)    /* Set the gain level for the sensor */
#define TCS34725_ID               (0x12)    /* 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727 */
#define TCS34725_STATUS           (0x13)
#define TCS34725_STATUS_AINT      (0x10)    /* RGBC Clean channel interrupt */
#define TCS34725_STATUS_AVALID    (0x01)    /* Indicates that the RGBC channels have completed an integration cycle */
#define TCS34725_CDATAL           (0x14)    /* Clear channel data */
#define TCS34725_CDATAH           (0x15)
#define TCS34725_RDATAL           (0x16)    /* Red channel data */
#define TCS34725_RDATAH           (0x17)
#define TCS34725_GDATAL           (0x18)    /* Green channel data */
#define TCS34725_GDATAH           (0x19)
#define TCS34725_BDATAL           (0x1A)    /* Blue channel data */
#define TCS34725_BDATAH           (0x1B)

#define TCS34725_INTEGRATIONTIME_2_4MS   0xFF   /**<  2.4ms - 1 cycle    - Max Count: 1024  */
#define TCS34725_INTEGRATIONTIME_24MS    0xF6   /**<  24ms  - 10 cycles  - Max Count: 10240 */
#define TCS34725_INTEGRATIONTIME_50MS    0xEB   /**<  50ms  - 20 cycles  - Max Count: 20480 */
#define TCS34725_INTEGRATIONTIME_101MS   0xD5   /**<  101ms - 42 cycles  - Max Count: 43008 */
#define TCS34725_INTEGRATIONTIME_154MS   0xC0   /**<  154ms - 64 cycles  - Max Count: 65535 */
#define TCS34725_INTEGRATIONTIME_240MS   0x9C   /**<  240ms - 100 cycles - Max Count: 65535 */
#define TCS34725_INTEGRATIONTIME_700MS   0x00   /**<  700ms - 256 cycles - Max Count: 65535 */

#define TCS34725_GAIN_1X                 0x00   /**<  No gain  */
#define TCS34725_GAIN_4X                 0x01   /**<  4x gain  */
#define TCS34725_GAIN_16X                0x02   /**<  16x gain */
#define TCS34725_GAIN_60X                0x03   /**<  60x gain */
/******************************************************************************/
extern void delay_s(u32 i);

#define TCS_SDA_IN()  {GPIOB->CRH&=0xFFFF0FFF;GPIOB->CRH|=8<<12;}
#define TCS_SDA_OUT() {GPIOB->CRH&=0xFFFF0FFF;GPIOB->CRH|=3<<12;}
#define TCS_SDA_READ   GPIOB->IDR&(1<<11)

#define TCS_SCL_H     GPIO_SetBits(GPIOB,GPIO_Pin_10)
#define TCS_SCL_L     GPIO_ResetBits(GPIOB,GPIO_Pin_10)
#define TCS_SDA_H     GPIO_SetBits(GPIOB,GPIO_Pin_11)
#define TCS_SDA_L     GPIO_ResetBits(GPIOB,GPIO_Pin_11)
/******************************************************************************/
#define max3v(v1, v2, v3)   ((v1)<(v2)? ((v2)<(v3)?(v3):(v2)):((v1)<(v3)?(v3):(v1)))
#define min3v(v1, v2, v3)   ((v1)>(v2)? ((v2)>(v3)?(v3):(v2)):((v1)>(v3)?(v3):(v1)))

typedef struct{
	unsigned short  c;      //[0-65536]
	unsigned short  r;
	unsigned short  g;
	unsigned short  b;
}COLOR_RGBC;//RGBC

typedef struct{
	unsigned short h;       //[0,360]
	unsigned char  s;       //[0,100]
	unsigned char  l;       //[0,100]
}COLOR_HSL;//HSL

COLOR_RGBC rgb;
COLOR_HSL  hsl;
/******************************************************************************/
void TCS34725_I2C_Init()
{
	GPIO_InitTypeDef GPIO_InitStructure;
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10|GPIO_Pin_11;//PB10/PB10=外接I2C
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;//通用推挽输出	
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//速度
	GPIO_Init(GPIOB, &GPIO_InitStructure);//对选中管脚初始化
	GPIO_SetBits(GPIOB,GPIO_Pin_10|GPIO_Pin_11);   //高电平
}
/*********************************************/
void TCS34725_I2C_Start()
{
	TCS_SDA_OUT();
	TCS_SDA_H;
	TCS_SCL_H;
	delay_s(40);//delay_us(4);
	TCS_SDA_L;
	delay_s(40);//delay_us(4);
	TCS_SCL_L;
}
/*********************************************/
void TCS34725_I2C_Stop()
{
	TCS_SDA_OUT();
	TCS_SCL_L;
	TCS_SDA_L;
	delay_s(40);//delay_us(4);
	TCS_SCL_H;
	TCS_SDA_H;
	delay_s(40);//delay_us(4);							   	
}
/*********************************************/
//返回值：1，接收应答失败
//        0，接收应答成功
u8 TCS34725_I2C_Wait_ACK()
{
	u32 t=0;
	
	TCS_SDA_IN();//SDA设置为输入  
	TCS_SDA_H; 
	delay_s(10);//delay_us(1);
	TCS_SCL_H; 
	delay_s(10);//delay_us(1);
	while(TCS_SDA_READ)
	{
		t++;
		if(t > 250)
		{
			TCS34725_I2C_Stop();
			return 1;
		}
	}
	TCS_SCL_L;
	return 0;	
}
/*********************************************/
//产生ACK应答
void TCS34725_I2C_ACK()
{
	TCS_SCL_L;
	TCS_SDA_OUT();//sda线输出
	TCS_SDA_L;
	delay_s(20);//delay_us(2);
	TCS_SCL_H;
	delay_s(20);//delay_us(2);
	TCS_SCL_L;
}
/*********************************************/
//不产生ACK应答		    
void TCS34725_I2C_NACK()
{
	TCS_SCL_L;
	TCS_SDA_OUT();//sda线输出
	TCS_SDA_H;
	delay_s(20);//delay_us(2);
	TCS_SCL_H;
	delay_s(20);//delay_us(2);
	TCS_SCL_L;
}
/*********************************************/
//I2C发送一个字节		  
void TCS34725_I2C_Send_Byte(u8 byte)
{
	u8 i;
	
	TCS_SDA_OUT();//sda线输出
	TCS_SCL_L;//拉低时钟开始数据传输
	for(i = 0; i < 8; i++)
	{
		if(((byte&0x80)>>7)==1)TCS_SDA_H;
		else
			TCS_SDA_L;
		byte <<= 1;
		
		delay_s(20);//delay_us(2);
		TCS_SCL_H;
		delay_s(20);//delay_us(2);
		TCS_SCL_L;
		delay_s(20);//delay_us(2);
	} 
}
/*********************************************/
//读1个字节，ack=1时，发送ACK，ack=0，发送nACK   
u8 TCS34725_I2C_Read_Byte(u8 ack)
{
	u8 i,receive = 0;
	
	TCS_SDA_IN();
	for(i = 0; i < 8; i++)
	{
		TCS_SCL_L;
		delay_s(20);//delay_us(2);
		TCS_SCL_H;
		receive <<= 1;
		if(TCS_SDA_READ) receive++;
		delay_s(10);//delay_us(1);
	}
	if (!ack) TCS34725_I2C_NACK();//发送nACK
	else TCS34725_I2C_ACK(); //发送ACK 
	
	return receive;
}
/*********************************************/
/*******************************************************************************
 * @brief Writes data to a slave device.
 *
 * @param slaveAddress - Adress of the slave device.
 * @param dataBuffer - Pointer to a buffer storing the transmission data.
 * @param bytesNumber - Number of bytes to write.
 * @param stopBit - Stop condition control.
 *                  Example: 0 - A stop condition will not be sent;
 *                           1 - A stop condition will be sent.
*******************************************************************************/
void TCS34725_I2C_Write(u8 slaveAddress, u8* dataBuffer,u8 bytesNumber, u8 stopBit)
{
	u8 i = 0;
	
	TCS34725_I2C_Start();
	TCS34725_I2C_Send_Byte((slaveAddress << 1) | 0x00);	   //发送从机地址写命令
	TCS34725_I2C_Wait_ACK();
	for(i = 0; i < bytesNumber; i++)
	{
		TCS34725_I2C_Send_Byte(*(dataBuffer + i));
		TCS34725_I2C_Wait_ACK();
	}
	if(stopBit == 1) TCS34725_I2C_Stop();
}
/*******************************************************************************
 * @brief Reads data from a slave device.
 *
 * @param slaveAddress - Adress of the slave device.
 * @param dataBuffer - Pointer to a buffer that will store the received data.
 * @param bytesNumber - Number of bytes to read.
 * @param stopBit - Stop condition control.
 *                  Example: 0 - A stop condition will not be sent;
 *                           1 - A stop condition will be sent.
*******************************************************************************/
void TCS34725_I2C_Read(u8 slaveAddress, u8* dataBuffer, u8 bytesNumber, u8 stopBit)
{
	u8 i = 0;
	
	TCS34725_I2C_Start();
	TCS34725_I2C_Send_Byte((slaveAddress << 1) | 0x01);	   //发送从机地址读命令
	TCS34725_I2C_Wait_ACK();
	for(i = 0; i < bytesNumber; i++)
	{
		if(i == bytesNumber - 1)
		{
			*(dataBuffer + i) = TCS34725_I2C_Read_Byte(0);//读取的最后一个字节发送NACK
		}
		else
		{
			*(dataBuffer + i) = TCS34725_I2C_Read_Byte(1);
		}
	}
	if(stopBit == 1) TCS34725_I2C_Stop();
}
/*******************************************************************************
 * @brief Writes data into TCS34725 registers, starting from the selected
 *        register address pointer.
 *
 * @param subAddr - The selected register address pointer.
 * @param dataBuffer - Pointer to a buffer storing the transmission data.
 * @param bytesNumber - Number of bytes that will be sent.
 *
 * @return None.
*******************************************************************************/
void TCS34725_Write(u8 subAddr, u8* dataBuffer, u8 bytesNumber)
{
    u8 sendBuffer[10] = {0, };
    u8 byte = 0;
    
    sendBuffer[0] = subAddr | TCS34725_COMMAND_BIT;
    for(byte = 1; byte <= bytesNumber; byte++)
    {
        sendBuffer[byte] = dataBuffer[byte - 1];
    }
	TCS34725_I2C_Write(TCS34725_ADDRESS, sendBuffer, bytesNumber + 1, 1);
}
/*******************************************************************************
 * @brief Reads data from TCS34725 registers, starting from the selected
 *        register address pointer.
 *
 * @param subAddr - The selected register address pointer.
 * @param dataBuffer - Pointer to a buffer that will store the received data.
 * @param bytesNumber - Number of bytes that will be read.
 *
 * @return None.
*******************************************************************************/
void TCS34725_Read(u8 subAddr, u8* dataBuffer, u8 bytesNumber)
{
	subAddr |= TCS34725_COMMAND_BIT;
	
	TCS34725_I2C_Write(TCS34725_ADDRESS, (u8*)&subAddr, 1, 0);
	TCS34725_I2C_Read(TCS34725_ADDRESS, dataBuffer, bytesNumber, 1);
}
/*******************************************************************************
 * @brief TCS34725设置积分时间
 *
 * @return None
*******************************************************************************/
void TCS34725_SetIntegrationTime(u8 time)
{
	TCS34725_Write(TCS34725_ATIME, &time, 1);
}
/*******************************************************************************
 * @brief TCS34725设置增益
 *
 * @return None
*******************************************************************************/
void TCS34725_SetGain(u8 gain)
{
	TCS34725_Write(TCS34725_CONTROL, &gain, 1);
}
/*******************************************************************************
 * @brief TCS34725使能
 *
 * @return None
*******************************************************************************/
void TCS34725_Enable(void)
{
	u8 cmd = TCS34725_ENABLE_PON;
	
	TCS34725_Write(TCS34725_ENABLE, &cmd, 1);
	cmd = TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN;
	TCS34725_Write(TCS34725_ENABLE, &cmd, 1);
	//delay_s(600000);//delay_ms(3);//延时应该放在设置AEN之后
}
/*******************************************************************************
 * @brief TCS34725失能
 *
 * @return None
*******************************************************************************/
void TCS34725_Disable(void)
{
	u8 cmd = 0;
	
	TCS34725_Read(TCS34725_ENABLE, &cmd, 1);
	cmd = cmd & ~(TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN);
	TCS34725_Write(TCS34725_ENABLE, &cmd, 1);
}
/*******************************************************************************
 * @brief TCS34725初始化
 *
 * @return ID - ID寄存器中的值
*******************************************************************************/
u8 TCS34725_Init(void)
{
	u8 id=0;
	
	TCS34725_I2C_Init(); 
	TCS34725_Read(TCS34725_ID, &id, 1);  //TCS34725 的 ID 是 0x44 可以根据这个来判断是否成功连接,0x4D是TCS34727;
	if(id==0x4D | id==0x44)
		{
			TCS34725_SetIntegrationTime(TCS34725_INTEGRATIONTIME_50MS);
			TCS34725_SetGain(TCS34725_GAIN_1X);
			TCS34725_Enable();
			return 1;
		}
	return 0;
}
/*******************************************************************************
 * @brief TCS34725获取单个通道数据
 *
 * @return data - 该通道的转换值
*******************************************************************************/
u16 TCS34725_GetChannelData(u8 reg)
{
	u8 tmp[2] = {0,0};
	u16 data;
	
	TCS34725_Read(reg, tmp, 2);
	data = (tmp[1] << 8) | tmp[0];
	
	return data;
}
/*******************************************************************************
 * @brief TCS34725获取各个通道数据
 *
 * @return 1 - 转换完成，数据可用
 *   	   0 - 转换未完成，数据不可用
*******************************************************************************/
u8 TCS34725_GetRawData(COLOR_RGBC *rgbc)
{
	u8 status = TCS34725_STATUS_AVALID;
	
	TCS34725_Read(TCS34725_STATUS, &status, 1);
	
	if(status & TCS34725_STATUS_AVALID)
	{
		rgbc->c = TCS34725_GetChannelData(TCS34725_CDATAL);	
		rgbc->r = TCS34725_GetChannelData(TCS34725_RDATAL);	
		rgbc->g = TCS34725_GetChannelData(TCS34725_GDATAL);	
		rgbc->b = TCS34725_GetChannelData(TCS34725_BDATAL);
		return 1;
	}
	return 0;
}
/******************************************************************************/
//RGB转HSL
void RGBtoHSL(COLOR_RGBC *Rgb, COLOR_HSL *Hsl)
{
	u8 maxVal,minVal,difVal;
	u8 r = Rgb->r*100/Rgb->c;   //[0-100]
	u8 g = Rgb->g*100/Rgb->c;
	u8 b = Rgb->b*100/Rgb->c;
	
	maxVal = max3v(r,g,b);
	minVal = min3v(r,g,b);
	difVal = maxVal-minVal;
	
	//计算亮度
	Hsl->l = (maxVal+minVal)/2;   //[0-100]
	
	if(maxVal == minVal)//若r=g=b,灰度
	{
		Hsl->h = 0; 
		Hsl->s = 0;
	}
	else
	{
		//计算色调
		if(maxVal==r)
		{
			if(g>=b)
				Hsl->h = 60*(g-b)/difVal;
			else
				Hsl->h = 60*(g-b)/difVal+360;
		}
		else
			{
				if(maxVal==g)Hsl->h = 60*(b-r)/difVal+120;
				else
					if(maxVal==b)Hsl->h = 60*(r-g)/difVal+240;
			}
		
		//计算饱和度
		if(Hsl->l<=50)Hsl->s=difVal*100/(maxVal+minVal);  //[0-100]
		else
			Hsl->s=difVal*100/(200-(maxVal+minVal));
	}
}
/******************************************************************************/


