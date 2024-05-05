/*
 * uart.c
 *
 *  Created on: Apr 15, 2024
 *      Author: Alecea
 */
#include <stdio.h>
#include <string.h>
#include "main.h"
#include "adc.h"
#include "uart.h"


// All kinds of variables, you'll see what these do in adc.c
extern uint16_t adcBuf[BUFFER_LEN];
extern int atten;
extern float vdiv;
extern float trigVoltage;
extern uint8_t trig;
extern int trigPoint;

extern float tdiv;
extern uint32_t sampRate;
extern float sampPer;

extern float maxVoltage, minVoltage;
extern float measuredFreq, sigPer;

int currentMenu = 1;
volatile uint8_t outputFlag = 0; // whether or not we should output data to the UART

extern UART_HandleTypeDef huart2;

void send_Data()
{
	if (outputFlag) // If the computer requested data, we send it.
	{
		outputCSV(outputFlag);
		outputFlag = 0;
	}
}


/*
 * Figure out what all of this means
 */
void outputSerial(char s[], uint8_t o)
{
    switch (o)
    {
    case 1:
        HAL_UART_Transmit(&huart2, s, strlen(s), HAL_MAX_DELAY);
        break;
    default:
        break;
    }
}

// This function dumps the captured waveform as TekScope-compatible CSV data
/*
 *
 */
void outputCSV(uint8_t o)
{
    char st[10];
    char s1[10];
    uint8_t buffer[30] = "";

    sprintf(buffer, "\033[2J\033[H\033[3J");
    outputSerial(buffer, o);

    sprintf(buffer, "Model,TekscopeSW\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, "Label,CH1\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, "Waveform Type,ANALOG\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, "Horizontal Units,s\n\r");
    outputSerial(buffer, o);

    printFloat(sampPer, 2, st);
    sprintf(buffer, "Sample Interval,%sE-06\n\r", st);
    outputSerial(buffer, o);

    sprintf(buffer, "Record Length,%d\n\r", BUFFER_LEN);
    outputSerial(buffer, o);

    sprintf(buffer, "Zero Index,%d\n\r", trigPoint);
    outputSerial(buffer, o);
    HAL_Delay(5);

    sprintf(buffer, "Vertical Units,V\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, ",\n\rLabels,\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, "TIME,CH1\n\r");
    outputSerial(buffer, o);

    for (int i = 0; i < BUFFER_LEN; i++)
    {
        float voltage = adcToVoltage(adcBuf[i]);
        printFloat(voltage, 1, st);
        printFloat((float)i * sampPer, 3, s1);
        sprintf(buffer, "%sE-06,%s\n\r", s1, st);
        outputSerial(buffer, o);
    }
    sprintf(buffer, "Completed Transfer.\n\r");
    outputSerial(buffer, o);
}


void printFloat(float v, int decimalDigits, char s[])
{
  uint8_t neg = 0;
  if (v < 0)
  {
    neg = 1;
    v = v - (2.0 * v);
  }
  int i = 1;
  int intPart, fractPart;
  for (; decimalDigits != 0; i *= 10, decimalDigits--)
    ;
  intPart = (int)v;
  fractPart = (int)((v - (float)(int)v) * i);
  if (fractPart < 0)
    fractPart *= -1;
  if (neg)
    sprintf(s, "-%i.%i", intPart, fractPart);
  else
    sprintf(s, "%i.%i", intPart, fractPart);
}


