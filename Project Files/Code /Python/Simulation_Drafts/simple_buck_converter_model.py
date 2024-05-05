import sys
import io
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import math

# three/four decimal points for granularity
# 20% mark in capacitance
# methods for acting in real time for continuous solving
# A typical 4th-order Runge-Kutta method is used to linearize the differential equations 


# physical component variable declarations
Vin = 24  # Input voltage, volts will change from 9V to 24V, user input
################ I CURRENTLY DON'T KNOW THE Rdson ################## Should be Vdson / Idson
Rdson = 0.1  # drain source resistance, ohms
RL = 0.01  # Inductor resistance, Ohms
################ I CURRENTLY DON'T KNOW THE ESR #################### Should be Vc / Ic
ESR = 0.05  # equivalent series resistance of capacitor, Ohms
Rload = 9  # Load resistance, Ohms
L = 0.0001  # Inductance, Henrys
C = 0.0001  # capacitance, Farads
################ I CURRENTLY DON'T KNOW THE Vd, Rd ##################### should just measure diode forard voltage drop
Vd = 0.7  # diode forward voltage drop, Volts

# PWM variable declarations the duty cycle (DC), 
fsw = 100000  # Converter switching frequency, Hz
DC = .5  # Duty cycle

# time variables the initial and final simulation time (t_init, t_final), the sample period T, and the total number of iterations (iters)
t_init = 0  # initial time in seconds
t_final = 10  # the final simulation time in seconds
T = 0.1  # sample period in seconds
iters = int(t_final/T)  # The total number of iterations

# output variables
iL = 0  # inductor current Amps
vC = 0  # capacitor voltage Volts
v_out = 0  # output voltage Volts


# goal: model the buck converter in on and off state

# calculate diL/dt
def deriv_iL(S, Rdson, RL, ESR, Rload, L, iL0, vC0, Vin, Vd):
    A = (S * Rdson) + RL + ((ESR * Rload) / (ESR + Rload))
    deriv_iL = ((A) * (-1 / L) * iL0) + ((-1 / L) * (Rload / (ESR + Rload)) * vC0) + ((S / L) * Vin) + (
                (1 - S) * (-1 / L) * Vd)
    return deriv_iL


# calculate dVc/dt
def deriv_vC(ESR, Rload, C, iL0, vC0):
    deriv_vC = ((1 / C) * (Rload / (ESR + Rload)) * iL0) + ((-1 / C) * (1 / (ESR + Rload)) * vC0)
    return deriv_vC


# input arguments:
# the initial time, t_init 
# the sampling period, T
# the characteristics of the converter (Vin, Rdson, L, ESR, C, RL, and Rload) 
# and the initial conditions (the inductor current, iL0, and capacitor voltage, vC0, at the initial time).
# outputs: iL, iC, vC and v_out
def runge_kutta_calcs(t_begin, T, Vin, Rdson, L, ESR, C, Rload, iL0, vC0, RL, S, Vd):
    ka1 = deriv_iL(S, Rdson, RL, ESR, Rload, L, iL0, vC0, Vin, Vd)
    kb1 = deriv_vC(ESR, Rload, C, iL0, vC0)
    ka2 = deriv_iL(S, Rdson, RL, ESR, Rload, L, (iL0 + (T / 2) * ka1), (vC0 + (T / 2) * kb1), Vin, Vd)
    kb2 = deriv_vC(ESR, Rload, C, (iL0 + (T / 2) * ka1), (vC0 + (T / 2) * kb1))
    ka3 = deriv_iL(S, Rdson, RL, ESR, Rload, L, (iL0 + (T / 2) * ka2), (vC0 + (T / 2) * kb2), Vin, Vd)
    kb3 = deriv_vC(ESR, Rload, C, (iL0 + (T / 2) * ka2), (vC0 + (T / 2) * kb2))
    ka4 = deriv_iL(S, Rdson, RL, ESR, Rload, L, (iL0 + (T) * ka3), (vC0 + (T) * kb3), Vin, Vd)
    kb4 = deriv_vC(ESR, Rload, C, (iL0 + (T) * ka3), (vC0 + (T) * kb3))

    # print(kb1)

    # calculate iL
    iL = iL0 + ((T / 6) * (ka1 + (2 * ka2) + (2 * ka3) + ka4))
    # calculate vC
    vC = vC0 + ((T / 6) * (kb1 + (2 * kb2) + (2 * kb3) + kb4))
    # calculate v_out
    v_out = (((Rload * ESR) / (ESR + Rload)) * iL) + ((Rload / (ESR + Rload)) * vC)
    t_end = t_begin + T
    return [t_end, iL, vC, v_out]


# PWM generator input arguments:
#t = np.linspace(t_init, t_final, 10000000, endpoint=True)
#PWM = (signal.square(2 * np.pi * fsw * t))
#plt.plot(t, PWM)
#plt.show()

# main section of code calls other functions above
# initial state variable declarations
iL0 = 0  # inductor current at t_init
vC0 = 0  # capacitor voltage at t_init
curr_iter = 0

# final arrays
iLs = []
vCs = []
v_outs = []
time = []
results = []

while curr_iter < iters:

    if int(t_init % (1/fsw) < (1/fsw)*0.5) == 1.0:

        # state is on so S = 1
        S = 1
        results = runge_kutta_calcs(t_init, T, Vin, Rdson, L, ESR, C, Rload, iL0, vC0, RL, S, Vd)
    else:
        # state is off so S = 0
        S = 0
        results = runge_kutta_calcs(t_init, T, Vin, Rdson, L, ESR, C, Rload, iL0, vC0, RL, S, Vd)
    # update initial results for next iter
    t_init = results[0]
    iL0 = results[1]
    vC0 = results[2]
    curr_iter += 1
    # add values to numpy array for display
    time.append(results[0])
    iLs.append(results[1])
    vCs.append(results[2])
    v_outs.append(results[3])
    # update the iteration number
    curr_iter += 1
    #print(signal.square(2 * np.pi * fsw * t_init))
# print out simulation results
iL = np.array(iLs)
vC = np.array(vCs)
v_out = np.array(v_outs)

# plt.plot(time, iL, label = "Inductor Current")
plt.plot(time, vC, label="Capacitor Voltage")
plt.plot(time, v_out, label="Output Voltage")
plt.xlabel("time [s]")
plt.ylabel("Voltage [V]")
plt.legend()
plt.show()
