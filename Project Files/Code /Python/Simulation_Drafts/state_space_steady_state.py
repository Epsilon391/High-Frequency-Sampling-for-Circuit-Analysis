import numpy as np
from scipy.signal import StateSpace, lsim
import matplotlib.pyplot as plt

# physical component variable declarations
Vin = 12.0            # Input voltage
R_load = 8         # Load resistance, Ohms
L = 0.0001          # Inductance, Henrys
C = 0.0001          # capacitance, Farads
# Parasitic components
Rt = 0.00001       # Parasitic resistance of transistor, ohms
Rd = 0.00001       # Parasitic resistance of diode, ohms
ESR = 0.01      # Parasitic Resistance of capacitor, ohms
RL = 0.02       # Parasitic Resistance of inductor, ohms
# PWM components
D = 0.5

# State Space Representation
# dx'(t) / dt = A * x(t) + B * u(t)
# y(t) = C * x(t) + E * u(t)

# Define State Space matricies
A00 = (RL + (D * Rt) + ((1 - D) * Rd) + ((R_load * ESR) / (R_load + ESR))) / (-L)
A01 = (-R_load) / (L * (R_load + ESR))
A10 = (R_load) / (C * (R_load + ESR))
A11 = (-1.0) / (C * (R_load + ESR))
A = np.array([[A00, A01],[A10, A11]])

B00 = D / L
B10 = 0.0
B = np.array([[B00], [B10]])

C00 = D
C01 = 0.0
C10 = (R_load * ESR) / (R_load + ESR)
C11 = (R_load) / (R_load + ESR)
C = np.array([[C00, C01],[C10, C11]])

E = np.array([[0.0], [0.0]])

#print(A)
#print(B)
#print(C)
#print(E)

# Define the time vector
t = np.linspace(0, 0.001, 1000)

# Define the input function u(t)
def u(t):
    return np.full(1000, Vin)

# Create StateSpace system
sys = StateSpace(A, B, C, E)

# Simulate the system
t, y, x = lsim(sys, u(t), t)

# y contains the output, x contains the state trajectories

# If y is a 2x1 array, you can extract the individual components
y1 = y[:, 0]  # First component of y
y2 = y[:, 1]  # Second component of y

# Plot the results
plt.plot(t, y1, label='Output 1')
plt.plot(t, y2, label='Output 2')
plt.xlabel('Time')
plt.ylabel('Output Voltage')
plt.legend()
plt.show()



