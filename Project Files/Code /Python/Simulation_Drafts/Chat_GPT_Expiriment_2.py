import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Buck converter parameters (modify these as per your lab setup)
Vin = 24.0  # Input voltage (V)
L = 100e-6  # Inductor value (H)
C = 1e-6  # Capacitor value (F)
R = 10.0  # Load resistance (ohms)
fsw = 100e3  # Switching frequency (Hz)
D = 0.5  # Initial duty cycle (set to 50% initially)

# Simulation time parameters
t_max = 1.0  # Simulation time (s)


# Define the PWM signal function
def pwm_signal(t, duty_ratio):
    T = 1 / fsw
    return 1 if (t % T) < duty_ratio * T else 0


# Define the differential equations
def buck_converter(t, states, duty_ratio):
    Vout, IL = states
    Vin_eff = Vin * pwm_signal(t, duty_ratio)

    # Avoid division by zero when PWM is off
    if pwm_signal(t, duty_ratio) == 0:
        dVout_dt = 0
    else:
        dVout_dt = (Vin_eff - Vout) / (L * pwm_signal(t, duty_ratio)) - Vout / (R * C)

    dIL_dt = (Vin_eff - Vout) / L
    return [dVout_dt, dIL_dt]


# Initial conditions
initial_state = [0.0, (Vin * D) / L]  # Starting output voltage and inductor current

# Time points
t_span = (0, t_max)

# Simulate the buck converter using solve_ivp
solution = solve_ivp(
    lambda t, y: buck_converter(t, y, D),  # Pass D as an argument
    t_span,
    initial_state,
    t_eval=np.linspace(0, t_max, 1000),
    method='RK45',  # Use a different solver method for stability
)

# Extract the results
time = solution.t
Vout_actual = solution.y[0]

# Plot results (modify as needed for specific measurements)
plt.figure(figsize=(10, 6))
plt.plot(time, Vout_actual, label="Output Voltage")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid(True)
plt.title("Buck Converter Simulation")
plt.show()
