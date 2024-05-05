import numpy as np
from scipy.signal import StateSpace, lsim, square
import matplotlib.pyplot as plt
import control as co

# physical component variable declarations
Vin = 24.0         # Input voltage
R_load = 8         # Load resistance, Ohms
L = 0.0001         # Inductance, Henrys
C = 0.0001         # capacitance, Farads
# Parasitic components
Rt = 0.00001       # Parasitic resistance of transistor, ohms
Rd = 0.00001       # Parasitic resistance of diode, ohms
ESR = 0.01         # Parasitic Resistance of capacitor, ohms
RL = 0.02          # Parasitic Resistance of inductor, ohms
# PWM components
DC = 0.5           # Duty Cycle
t_init = 0.0       # initial time
t_final = 1.0      # final time
#h = 0.00000001     # time step 
h = 0.001           # time step
fsw = 20000             # switching frequency, Hz
T = 1 / fsw             # switching period, Seconds
samples = int((t_final - t_init) / h)     # number of samples for the linspace

# State Space Representation
# dx'(t) / dt = A * x(t) + B * u(t)
# y(t) = C * x(t) + E * u(t)

# Define State Space matricies "ON State"
A00 = (RL + Rt + ((R_load * ESR) / (R_load + ESR))) / (-L)
A01 = (-R_load) / (L * (R_load + ESR))
A10 = (R_load) / (C * (R_load + ESR))
A11 = (-1.0) / (C * (R_load + ESR))
A_on = np.array([[A00, A01],[A10, A11]])

B00 = 1 / L
B10 = 0.0
B_on = np.array([[B00], [B10]])

C00 = 1
C01 = 0.0
C10 = (R_load * ESR) / (R_load + ESR)
C11 = (R_load) / (R_load + ESR)
C_on = np.array([[C00, C01],[C10, C11]])

D_on = np.array([[0.0], [0.0]])

# Define State Space matricies "OFF State"
A00 = (RL + Rd + ((R_load * ESR) / (R_load + ESR))) / (-L)
A01 = (-R_load) / (L * (R_load + ESR))
A10 = (R_load) / (C * (R_load + ESR))
A11 = (-1.0) / (C * (R_load + ESR))
A_off = np.array([[A00, A01],[A10, A11]])

B00 = 0.0
B10 = 0.0
B_off = np.array([[B00], [B10]])

C00 = 0.0
C01 = 0.0
C10 = (R_load * ESR) / (R_load + ESR)
C11 = (R_load) / (R_load + ESR)
C_off = np.array([[C00, C01],[C10, C11]])

D_off = np.array([[0.0], [0.0]])

# Define the time vector
t_arr = np.arange(t_init, t_final, h)

# input: t is the time of the PWM signal
# def pwm(t):
#     # return the state of the transistor, 1 means the switch is "on" and 0 means "off"
#     return 1 if (t % T) < DC * T else 0

# Define the input function u(t)
# def u(t):
#     return np.full(samples, Vin)

# Create arrays
il_arr = np.zeros(samples)
vc_arr = np.zeros(samples)

# init conditions 
il0 = 0.0
vc0 = 0.0

# Simulate the system
for i in range(1, samples):
    if square(2 * np.pi * 5 * t_arr[i]) == 1:
        sys = co.StateSpace(A_on, B_on, C_on, D_on)
    else: 
        sys = co.StateSpace(A_off, B_off, C_off, D_off)
    t, y, x = co.forced_response(sys, [t_arr[i] - h, t_arr[i]], [Vin, Vin], [il0, vc0], return_x = True)
    #t, y, x = lsim(sys, [Vin, Vin], [t_arr[i] - h, t_arr[i]], [il0, vc0])
    # t contains the time, y contains the output, x contains the state trajectories
    # If y is a 2x1 array, you can extract the individual components
    #print(y[:, 0])
    il0 = y[1, 0]  # First component of y
    vc0 = y[1, 1]  # Second component of y
    #print(il0)
    #print(vc0)
    il_arr[i] = il0
    vc_arr[i] = vc0


# Simulate the system
#t, y, x = lsim(sys, u(t), t)

# Plot the results
plt.plot(t_arr, il_arr, label='Inductor Current')
plt.plot(t_arr, vc_arr, label='Output Voltage')
plt.xlabel('Time')
plt.ylabel('Output Voltage')
plt.legend()
plt.show()