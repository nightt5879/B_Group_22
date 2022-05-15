
#include "stm32f10x.h"
#include "config.h"
#include "sys.h"
#include "usart.h"

#include "timer.c"
#include "tcs34725.c"

/******************************************************************************/
void com2_order(void);
/******************************************************************************/
void delay_s(u32 i)
{
	while(i--);
}
/******************************************************************************/
void RCC_Configuration(void)
{
	RCC_DeInit();//RCC寄存器取消初始化设置
	RCC_HSEConfig(RCC_HSE_ON);//开启外部高速时钟
	RCC_WaitForHSEStartUp();//等待外部晶振启动
	FLASH_SetLatency(FLASH_Latency_2);//代码延时2周期
	FLASH_HalfCycleAccessCmd(FLASH_HalfCycleAccess_Disable);//半周期访问失能
	FLASH_PrefetchBufferCmd(FLASH_PrefetchBuffer_Enable);//预取指缓存使能
	RCC_PLLConfig(RCC_PLLSource_HSE_Div1, RCC_PLLMul_9);//外部高速时钟为PLL时钟输入源，9倍频
	RCC_PLLCmd(ENABLE);//使能PLL
	RCC_SYSCLKConfig(RCC_SYSCLKSource_PLLCLK);//PLL作为系统时钟
	RCC_HCLKConfig(RCC_SYSCLK_Div1);//AHB 时钟 = 系统时钟
	RCC_PCLK1Config(RCC_HCLK_Div2);//APB1 时钟 = HCLK / 2,即AHB时钟的一半
	RCC_PCLK2Config(RCC_HCLK_Div1);//APB2 时钟 = HCLK，即AHB时钟
	//RCC_ADCCLKConfig(RCC_PCLK2_Div6);//ADC 时钟 = PCLK / 6，即APB2时钟，72/6=12M
	RCC_LSEConfig(RCC_LSE_OFF);//关闭外部低速时钟
}
/******************************************************************************/
void GPIO_Config(void)
{
  GPIO_InitTypeDef GPIO_InitStructure;
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_GPIOB|RCC_APB2Periph_GPIOC|RCC_APB2Periph_AFIO, ENABLE);//使能GPIOA,GPIOB,GPIOC,AFIO;
	GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable,ENABLE);
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3;        //是LED
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; //复用推挽输出	
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_10MHz;//速度
	GPIO_Init(GPIOA, &GPIO_InitStructure);           //对选中管脚初始化
	GPIO_SetBits(GPIOA,GPIO_Pin_3);                  //上电点亮LED
}
/******************************************************************************/
/******************************************************************************/
uint16_t R1Min = 0, R1Max = 150, G1Min = 100, G1Max = 800, B1Min = 0, B1Max = 150;
uint16_t R2Min = 50, R2Max = 350, G2Min = 20, G2Max = 200, B2Min = 20, B2Max = 200;
uint16_t R3Min = 150, R3Max = 300, G3Min = 500, G3Max = 1000, B3Min = 500, B3Max = 1000;
uint16_t R4Min = 500, R4Max = 1200, G4Min = 800, G4Max = 1300, B4Min = 100, B4Max = 600;
int main(void)
{
	
	RCC_Configuration();
	GPIO_Config();
	uart_init(115200);
	delay_s(0x1fffff);
	TCS34725_Init();
	printf("Initial OK!\r\n");
	TIM2_Init(999,71);  //1ms定时
	while(1)
	{
		if(time1_cntr>=200)  //0.2s
			{
				time1_cntr=0;
				LED_blink;
			}
		if(time2_cntr>=50)  //1s
			{
				time2_cntr=0;
				TCS34725_GetRawData(&rgb);  //读两次，实际测试时发现读到的颜色总是上一次的颜色
				RGBtoHSL(&rgb,&hsl);
//				printf("R=%d G=%d B=%d C=%d\r\n",rgb.r,rgb.g,rgb.b,rgb.c);
				if( (rgb.r > R1Min) && (rgb.r < R1Max) && 
					(rgb.g > G1Min) && (rgb.g < G1Max) && 
					(rgb.b > B1Min) && (rgb.b < B1Max) )
					{
					printf("Green\n");
					}
				else if( (rgb.r > R2Min) && (rgb.r < R2Max) && 
					(rgb.g > G2Min) && (rgb.g < G2Max) && 
					(rgb.b > B2Min) && (rgb.b < B2Max) )
					{
					printf("Red\n");
					}
				else if( (rgb.r > R3Min) && (rgb.r < R3Max) && 
					(rgb.g > G3Min) && (rgb.g < G3Max) && 
					(rgb.b > B3Min) && (rgb.b < B3Max) )
					{
					printf("Blue\n");
					}
				else if( (rgb.r > R4Min) && (rgb.r < R4Max) && 
					(rgb.g > G4Min) && (rgb.g < G4Max) && 
					(rgb.b > B4Min) && (rgb.b < B4Max) )
					{
					printf("Yellow\n");
					}
				else 
					{
					printf("Other\n");
					}

//				printf("H=%d S=%d L=%d\r\n",hsl.h,hsl.s,hsl.l);
			}
	}
}
/******************************************************************************/
//{"color":{"h":240,"s":50,"l":50}}  //[0-359][0-100][0-100]

