import serial
import csv
import matplotlib.pyplot as plt
import numpy as np
# This code waits for the user to send an s to the
# STM32 microcontroller then recieves the data read
# by the onboard ADC and prints the results to the screen.
# Author: Alecea Grosjean, Ethan Barnes, Jimmy Roach
def print_graph():
    # Lists to store time and voltage data
    time_data = []
    time_data2 = []
    voltage_data = []
    voltage_data2 = []
    voltage_data_sim = []
    voltage_data_sim2 = []

    # Read data from CSV file
    with open('/home/pi/Documents/data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        # Skip header rows
        for _ in range(13):
            next(csv_reader)
        for row in csv_reader:
            if len(row) == 1:  # Check if row contains data
                data = row[0].split(',')  # Split the row by comma
                if len(data) == 2:  # Ensure there are two elements
                    time_data.append(float(data[0]))
                    voltage_data.append(float(data[1]))


    # Print the data to debug
    g = 0
    for i in range(99):
        if voltage_data[i] > voltage_data[g]:
            g = i
    for i in range(g,g+40) :
        time_data2.append(time_data[i])
        voltage_data[i] = (voltage_data[i] / 4096.0 * 3.33 * 2 * 90.0 / 1640.0)
        voltage_data2.append(voltage_data[i])


    # Read data from CSV file
    with open('/home/pi/Documents/Capacitor_Ripple_Simulated_Voltage_30.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for i in range(10000):
            row = next(csv_reader)
            voltage_data_sim.append(float(row[0]))
    for i in range(0,4000,100) :
        voltage_data_sim2.append(voltage_data_sim[i])

    # Plotting the data
    sim_avg = sum(voltage_data_sim2)/len(voltage_data_sim2)
    for i in range(len(voltage_data_sim2)):
        voltage_data_sim2[i] -= sim_avg

    meas_avg = sum(voltage_data2)/len(voltage_data2)
    for i in range(len(voltage_data2)):
        voltage_data2[i] -= meas_avg

#    print(meas_avg)
#    meas_avg = sum(voltage_data2)/len(voltage_data2)
#    print(meas_avg)

    plt.plot(time_data2, voltage_data_sim2)
    plt.plot(time_data2, voltage_data2)
    plt.title('30 Ohm')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.grid(True)
    plt.show()

# define the serial port information
ser = serial.Serial('/dev/ttyUSB0',
    baudrate=115200,
    timeout=3.0)
# collect user input
user_in = ''
while (user_in != 's'):
    user_in = input("Please send 's' via UART and press Enter: ")

# handle the case
ser.write('s'.encode())


eof = False
# open csv and recieve data
with open('/home/pi/Documents/data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    try:
        while not eof:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            if not line:
                eof = True
            csvwriter.writerow([line])
    except KeyboardInterrupt:
       print("user interrupted")
    finally:
        ser.close()
        print("Completed writing to file data.csv")
        csvfile.close()
        print_graph()