import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Buck converter parameters
Vin = 12.0  # Input voltage (V)
L = 0.0001  # Inductor value (H)
C = 0.0001  # Capacitor value (F)
R = 10000  # Load resistance (ohms)
fsw = 1000  # Switching frequency (Hz)
D = 0.5  # Duty cycle

# Simulation time parameters (changed to 10 milliseconds for a quicker simulation)
t_max = 1.0  # Simulation time (s)


# Define the PWM signal function
def pwm_signal(t):
    T = 1 / fsw
    return 1 if (t % T) < D * T else 0


# Define the differential equations
def buck_converter(t, states):
    Vout, IL = states
    Vin_eff = Vin * pwm_signal(t)

    # Avoid division by zero when PWM is off
    if pwm_signal(t) == 0:
        dVout_dt = 0
    else:
        dVout_dt = (Vin_eff - Vout) / (L * pwm_signal(t)) - Vout / (R * C)

    dIL_dt = (Vin_eff - Vout) / L
    return [dVout_dt, dIL_dt]


# Initial conditions
initial_state = [0.0, (Vin * D) / L]  # Starting output voltage and inductor current

# Time points
t_span = (0, t_max)

# Simulate the buck converter using solve_ivp
solution = solve_ivp(
    buck_converter,
    t_span,
    initial_state,
    t_eval=np.linspace(0, t_max, 1000),
    method='RK45',  # Use a different solver method for stability
)

# Extract the results
time = solution.t
Vout_actual = solution.y[0]

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(time, Vout_actual, label="Output Voltage")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid(True)
plt.title("Second-Order Buck Converter Simulation without Voltage Regulation")
plt.show()
