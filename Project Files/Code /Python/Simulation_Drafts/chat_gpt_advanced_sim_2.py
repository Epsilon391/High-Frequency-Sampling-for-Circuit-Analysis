import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# Define the advanced buck converter function with advanced features
def advanced_buck_converter(t, states, params):
    Vin, L, C, R, fsw, D, parasitic_resistance, parasitic_capacitance, mosfet_loss, diode_loss, inductor_aging, capacitance_aging = params
    Vout, IL = states

    # Calculate switching frequency
    T = 1 / fsw

    # Nonlinear magnetic core effect (example nonlinear inductance)
    inductor_nonlinearity = 0.1  # Nonlinearity coefficient
    L_effective = L / (1 + inductor_nonlinearity * IL)

    # Parasitic components
    Vdrop_diode = IL * parasitic_resistance  # Voltage drop across parasitic resistance
    Vdrop_sw = (Vin * D - Vout) * parasitic_resistance  # Voltage drop across switch parasitic resistance
    Vdrop_diode += parasitic_capacitance * IL  # Voltage drop across parasitic capacitance

    # Differential equations
    dVout_dt = (Vin - Vout - Vdrop_sw) / (L_effective * D * T) - Vout / (R * C)
    dIL_dt = (Vin - Vout - Vdrop_diode) / L_effective - (1 - D) * Vin / L_effective

    # Advanced Features

    # MOSFET and diode losses
    dVout_dt -= mosfet_loss * IL
    dIL_dt += diode_loss * IL

    # Aging effects
    dL_dt = inductor_aging * t  # Example: Linear increase in inductance over time
    dC_dt = -capacitance_aging * t  # Example: Linear decrease in capacitance over time

    dVout_dt -= IL * dL_dt
    dIL_dt -= (Vout - Vin) / (L_effective + dL_dt)
    dIL_dt -= IL * dC_dt / C

    return [dVout_dt, dIL_dt]


# Simulation time parameters
t_start = 0.0
t_end = 10
t_step = 1
num_samples = int((t_end - t_start) / t_step)

# Circuit parameters with nominal values
Vin_nominal = 24.0
L_nominal = 100e-6
C_nominal = 1e-6
R_load_nominal = 10.0
fsw_nominal = 100e3
D_nominal = 0.5

# Advanced feature parameters
mosfet_loss_nominal = 0.01  # Nominal MOSFET loss coefficient
diode_loss_nominal = 0.005  # Nominal diode loss coefficient
inductor_aging_nominal = 1e-7  # Nominal inductor aging rate (change in inductance per second)
capacitance_aging_nominal = 1e-9  # Nominal capacitance aging rate (change in capacitance per second)

# Parasitic components (values are just placeholders, please replace with actual values)
parasitic_resistance = 0.01  # Parasitic resistance in switches and diodes (ohms)
parasitic_capacitance = 1e-9  # Parasitic capacitance (F)

# Initialize arrays to store results
time_points = np.linspace(t_start, t_end, num_samples)
Vout_simulated = np.zeros(num_samples)
IL_simulated = np.zeros(num_samples)

# Simulate advanced buck converter with features
for i, t in enumerate(time_points):
    duty_cycle = D_nominal
    params = (Vin_nominal, L_nominal, C_nominal, R_load_nominal, fsw_nominal, duty_cycle,
              parasitic_resistance, parasitic_capacitance,
              mosfet_loss_nominal, diode_loss_nominal,
              inductor_aging_nominal, capacitance_aging_nominal)

    solution = solve_ivp(
        lambda t, y: advanced_buck_converter(t, y, params),
        (t, t + t_step),
        [Vout_simulated[i - 1], IL_simulated[i - 1]],
        t_eval=[t, t + t_step],
        vectorized=True,
        method='RK45',
    )
    Vout_simulated[i] = solution.y[0][-1]
    IL_simulated[i] = solution.y[1][-1]

# Create separate plots for different aspects of the simulation
plt.figure(figsize=(12, 16))

# Plot 1: Output Voltage
plt.subplot(4, 1, 1)
plt.plot(time_points, Vout_simulated, label="Output Voltage")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid(True)
plt.title("Output Voltage")

# Plot 2: Inductor Current
plt.subplot(4, 1, 2)
plt.plot(time_points, IL_simulated, label="Inductor Current")
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.legend()
plt.grid(True)
plt.title("Inductor Current")

# Plot 3: MOSFET and Diode Losses
plt.subplot(4, 1, 3)
mosfet_losses = mosfet_loss_nominal * IL_simulated ** 2
diode_losses = diode_loss_nominal * IL_simulated ** 2
plt.plot(time_points, mosfet_losses, label="MOSFET Losses")
plt.plot(time_points, diode_losses, label="Diode Losses")
plt.xlabel("Time (s)")
plt.ylabel("Losses (W)")
plt.legend()
plt.grid(True)
plt.title("Switching Losses")

# Plot 4: Aging Effects
plt.subplot(4, 1, 4)
inductor_aging_values = L_nominal + inductor_aging_nominal * time_points
capacitance_aging_values = C_nominal + capacitance_aging_nominal * time_points
plt.plot(time_points, inductor_aging_values, label="Inductor Aging")
plt.plot(time_points, capacitance_aging_values, label="Capacitance Aging")
plt.xlabel("Time (s)")
plt.ylabel("Component Value")
plt.legend()
plt.grid(True)
plt.title("Component Aging")

plt.tight_layout()
plt.show()
