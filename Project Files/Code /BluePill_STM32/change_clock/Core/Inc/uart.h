/*
 * uart.h
 *
 *  Created on: Apr 15, 2024
 *      Author: Alecea
 */

#ifndef INC_UART_H_
#define INC_UART_H_


void outputSerial(char s[], uint8_t o);
void outputCSV(uint8_t o);
void send_Data();
void printFloat(float v, int decimalDigits, char s[]);


#endif /* INC_UART_H_ */
