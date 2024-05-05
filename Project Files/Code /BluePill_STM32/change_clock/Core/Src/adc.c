/*
 * adc.c
 *
 *  Created on: Apr 15, 2024
 *      Author: Alecea
 */
#include <stdio.h>
#include "main.h"
#include "adc.h"
#include "uart.h"

/// Hardware handles
extern ADC_HandleTypeDef hadc1;
extern DMA_HandleTypeDef hdma_adc1;
extern TIM_HandleTypeDef htim3;

uint16_t adcBuf[BUFFER_LEN];             // this is where we'll store data
volatile uint8_t finishedConversion = 0; // this lets us know when we're done capturing data

int atten = 2;  // Attenuation
float vdiv = 2; // Volts per division

uint8_t trigged;       // whether or not we're triggered
int trigPoint;         // triggering point
float trigVoltage = 0; // Trigger level
uint8_t trig = RISING; // Trigger slope

float tdiv = 20;   // uS per division
uint32_t sampRate; // Sample rate
float sampPer;     // Sample period in uS (how long it takes to measure one sample)

float maxVoltage, minVoltage; // Voltage measurements
float measuredFreq, sigPer;   // Time measurements

extern UART_HandleTypeDef huart2;
uint8_t uartBuf[15];

/*
 * Send Welcome message through UART with directions
 * Calculates sample rate, sample period, and sets the timer frequency
 */
void adc_uart_Init()
{
	uint8_t msg[65] = "Welcome, please enter 's' to receive the data in CSV format: \n\r";
    // Print Original Message to Serial Monitor
	HAL_UART_Transmit(&huart2, msg, 65, 1000);

	// Calculations for the sample rate, and sample period in us
	// Sets the timer frequency based off of this
    sampRate = (16000 * 1000) / tdiv;
    sampPer = tdiv / 16.0;
    setTimerFreq(sampRate);

    // Recieve from uart based on a interrupt
    HAL_UART_Receive_IT(&huart2, uartBuf, 1);


    HAL_TIM_Base_Start(&htim3);                          // Start the timebase timer
    HAL_ADC_Start_DMA(&hadc1, (uint32_t *)&adcBuf, 200); // Start the ADC
    HAL_NVIC_EnableIRQ(ADC1_IRQn);
}

// This runs in an infinite loop
void transferLoop()
{
    if (finishedConversion) // We finished aquiring one buffer
    {
        // Find the trigger point
        findTrigger();
        //if (trigged)
            //HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, 0);

        // Send the data to the UART if requested
        send_Data();

        // Reset
        //HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, 1);
        //uint8_t msg[65] = "Welcome, please enter 's' to receive the data in CSV format: \n\r";
        // Print Original Message to Serial Monitor
        //HAL_UART_Transmit(&huart2, msg, 65, 1000);
        finishedConversion = 0;
        HAL_ADC_Start_DMA(&hadc1, (uint32_t *)&adcBuf, BUFFER_LEN);
    }
}

// This sets the sampling rate
void setTimerFreq(uint32_t freq)
{
    uint16_t arr = (SYSCLK_FREQ / ((CLOCKTIM_PRESC + 1) * freq)) - 1;
    htim3.Instance->ARR = arr;
}

// This function finds the trigger point and also computes the frequency of thge signal
void findTrigger()
{
    int trigLevel = (4096.0 * (trigVoltage / (2.0 * atten) + 1.65)) / 3.3; // ADC level at which we should trigger
    int trigPoint2;                                                        // another trigger point, this will help us determine the period of the signal

    trigPoint = 0;
    trigged = 0;
    measuredFreq = 0;

    // The trigged variable will be 0 if we're not triggering, 1 if we only found 1 trigger point and 2 if we have at least two trigger points

    for (int i = 1; i < BUFFER_LEN / 2 && trigged != 2; i++) // we're looking for trigger points in the first half of the buffer
        if ((trig == RISING && adcBuf[i] >= trigLevel && adcBuf[i - 1] < trigLevel) || (trig == FALLING && adcBuf[i] <= trigLevel && adcBuf[i - 1] > trigLevel))
        {
            if (!trigged) // Looking for the first trigger point
            {
                trigPoint = i;
                trigged = 1;
            }
            else // Looking for the second one
            {
                trigPoint2 = i;
                trigged = 2;
            }
        }

    if (trigged == 2) // If we found at least two trigger points
    {
        sigPer = sampPer * (trigPoint2 - trigPoint); // we compute the period of the signal in uS
        measuredFreq = 1000000.0 / sigPer;           // and then we convert it into frequency, in Hz
    }
}

// Convert ADC value to volts
float adcToVoltage(uint16_t samp)
{
    //return atten * 2 * (((3.3 * samp) / 4096.0) - 1.65);
	return samp;
}

// This runs after the ADC has finished sampling one whole buffer
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc)
{
    finishedConversion = 1;

}

// This runs after receiving a character over the UART
void HAL_UART_RxCpltCallback(UART_HandleTypeDef* huart)
{
	extern uint8_t outputFlag;
    if(uartBuf[0] == 's' || uartBuf[0] == 'S')
        outputFlag = 1;
    HAL_UART_Receive_IT(&huart2, uartBuf, 1);
}



