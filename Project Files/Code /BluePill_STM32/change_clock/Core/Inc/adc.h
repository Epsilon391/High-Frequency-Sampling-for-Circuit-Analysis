/*
 * adc.h
 *
 *  Created on: Apr 15, 2024
 *      Author: Alecea
 */

#ifndef INC_ADC_H_
#define INC_ADC_H_

#define CLOCKTIM_PRESC 0
#define SYSCLK_FREQ 72000000
#define BUFFER_LEN 200

#define UPPER_VOLTAGE (atten * 3.3)
#define LOWER_VOLTAGE (atten * -3.3)

#define RISING 1
#define FALLING 0

void adc_uart_Init();
void transferLoop();
void setTimerFreq(uint32_t freq);
void findTrigger();
float adcToVoltage(uint16_t samp);
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc);
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);



#endif /* INC_ADC_H_ */
