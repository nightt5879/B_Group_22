

/******************************************************************************/
void ADC1_2_Init(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	ADC_InitTypeDef ADC_InitStructure;
	DMA_InitTypeDef DMA_InitStructure;
	
	RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1,ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_GPIOB|RCC_APB2Periph_ADC1|RCC_APB2Periph_ADC2,ENABLE);
	RCC_ADCCLKConfig(RCC_PCLK2_Div6);//配置ADC时钟，为PCLK2的6分频，即12MHz

	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_7;         //PA7是AD_V
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0|GPIO_Pin_1;    //PB0是AD_U、PB1电池电压检测
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;   // 设置引脚模式
	GPIO_Init(GPIOB, &GPIO_InitStructure);            // 初始化
 
	DMA_DeInit(DMA1_Channel1);
	DMA_InitStructure.DMA_PeripheralBaseAddr = (u32)&ADC1->DR;//ADC地址
	DMA_InitStructure.DMA_MemoryBaseAddr = (u32)&ad_value; //内存地址
	DMA_InitStructure.DMA_DIR = DMA_DIR_PeripheralSRC; //方向(从外设到内存)
	DMA_InitStructure.DMA_BufferSize = 16; //传输内容的大小
	DMA_InitStructure.DMA_PeripheralInc = DMA_PeripheralInc_Disable; //外设地址固定
	DMA_InitStructure.DMA_MemoryInc = DMA_MemoryInc_Enable; //内存地址自动增加
	DMA_InitStructure.DMA_PeripheralDataSize = DMA_PeripheralDataSize_Word; //外设数据单位
	DMA_InitStructure.DMA_MemoryDataSize = DMA_MemoryDataSize_Word;    //内存数据单位
	DMA_InitStructure.DMA_Mode = DMA_Mode_Circular; //DMA模式：循环传输
	DMA_InitStructure.DMA_Priority = DMA_Priority_High; //优先级：高
	DMA_InitStructure.DMA_M2M = DMA_M2M_Disable;   //禁止内存到内存的传输
	DMA_Init(DMA1_Channel1, &DMA_InitStructure);  //配置DMA1的1通道
	DMA_Cmd(DMA1_Channel1,ENABLE);
 
	ADC_DeInit(ADC1);
	ADC_InitStructure.ADC_Mode = ADC_Mode_RegSimult;                              //ADC1同步规则组模式
	ADC_InitStructure.ADC_ScanConvMode = ENABLE;                                  //启动扫描
	ADC_InitStructure.ADC_ContinuousConvMode = ENABLE;                            //连续转换
	ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;           //无外部触发
	ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;                        //结果右对齐
	ADC_InitStructure.ADC_NbrOfChannel = 2;                                       //转换通道数4
	ADC_Init(ADC1, &ADC_InitStructure);                                           //配置ADC1
	ADC_TempSensorVrefintCmd(ENABLE);                                           //开启内部温度传感器
	ADC_RegularChannelConfig(ADC1, ADC_Channel_7, 1, ADC_SampleTime_7Cycles5);    //AD_V
	ADC_RegularChannelConfig(ADC1, ADC_Channel_16,2, ADC_SampleTime_7Cycles5);  //温度  ADCx_IN16和ADCx_IN17只能出现在主ADC1中
	ADC_DMACmd(ADC1, ENABLE); 

	ADC_DeInit(ADC2);
	ADC_InitStructure.ADC_Mode = ADC_Mode_RegSimult;                              //ADC2同步规则组模式
	ADC_InitStructure.ADC_ScanConvMode = ENABLE;                                  //启动扫描
	ADC_InitStructure.ADC_ContinuousConvMode = ENABLE;                            //连续转换
	ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;           //无外部触发
	ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;                        //结果右对齐
	ADC_InitStructure.ADC_NbrOfChannel = 2;                                       //转换通道数
	ADC_Init(ADC2, &ADC_InitStructure);                                           //配置ADC2
	ADC_RegularChannelConfig(ADC2, ADC_Channel_8, 1, ADC_SampleTime_7Cycles5);    //AD_U
	ADC_RegularChannelConfig(ADC2, ADC_Channel_9, 2, ADC_SampleTime_7Cycles5);    //AD_Bat
	ADC_ExternalTrigConvCmd(ADC2, ENABLE);                                        //使能ADC2的外部触发模式 

	ADC_Cmd(ADC1,ENABLE);
	ADC_ResetCalibration(ADC1);//复位校准寄存器
	while(ADC_GetResetCalibrationStatus(ADC1));//等待校准寄存器复位完成
	ADC_StartCalibration(ADC1);//ADC校准
	while(ADC_GetCalibrationStatus(ADC1));//等待校准完成

	ADC_Cmd(ADC2, ENABLE);                                                      //使能ADC2
	ADC_ResetCalibration(ADC2);                                                 //ADC2的校准
	while(ADC_GetResetCalibrationStatus(ADC2));
	ADC_StartCalibration(ADC2);
	while(ADC_GetCalibrationStatus(ADC2));

	ADC_SoftwareStartConvCmd(ADC1, ENABLE);     //软件启动ADC1，开始转换
}
/******************************************************************************/



