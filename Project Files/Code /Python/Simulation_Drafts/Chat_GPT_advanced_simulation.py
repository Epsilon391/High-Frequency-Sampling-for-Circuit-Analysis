import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# Define the advanced buck converter function
def advanced_buck_converter(t, states, params):
    Vin, L, C, R, fsw, D, parasitic_resistance, parasitic_capacitance = params
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

    return [dVout_dt, dIL_dt]


# Simulation time parameters
t_start = 0.0  # Start time (s)
t_end = 10  # End time (s) - Reduced from 5.0 to 0.1 for faster simulation
t_step = 0.1  # Time step (s) - Increased from 1e-6 to 1e-5 for faster simulation
num_samples = int((t_end - t_start) / t_step)

# Circuit parameters with nominal values
Vin_nominal = 24.0  # Nominal input voltage (V)
L_nominal = 100e-6  # Nominal inductor value (H)
C_nominal = 1e-6  # Nominal capacitor value (F)
R_load_nominal = 10.0  # Nominal load resistance (ohms)
fsw_nominal = 100e3  # Nominal switching frequency (Hz)
D_nominal = 0.5  # Nominal duty cycle (50% initially)

# Nonlinear magnetic core effect
inductor_nonlinearity = 0.1  # Nonlinearity coefficient (higher values mean stronger nonlinearity)

# Parasitic components
parasitic_resistance = 0.01  # Parasitic resistance in switches and diodes (ohms)
parasitic_capacitance = 1e-9  # Parasitic capacitance (F)

# Initialize arrays to store results
time_points = np.linspace(t_start, t_end, num_samples)
Vout_simulated = np.zeros(num_samples)
IL_simulated = np.zeros(num_samples)

# Simulate nonlinear core effects, parasitic components, and thermal effects
for i, t in enumerate(time_points):
    # Calculate duty cycle
    duty_cycle = D_nominal

    # Update parameters
    params = (Vin_nominal, L_nominal, C_nominal, R_load_nominal, fsw_nominal, duty_cycle,
              parasitic_resistance, parasitic_capacitance)

    # Simulate the buck converter
    solution = solve_ivp(
        lambda t, y: advanced_buck_converter(t, y, params),
        (t, t + t_step),
        [Vout_simulated[i - 1], IL_simulated[i - 1]],  # Use previous values as initial conditions
        t_eval=[t, t + t_step],
        vectorized=True,
        method='RK45',
    )
    Vout_simulated[i] = solution.y[0][-1]
    IL_simulated[i] = solution.y[1][-1]

# Plot voltage and current waveforms with advanced features
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(time_points, Vout_simulated, label="Output Voltage")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid(True)
plt.title("Advanced Buck Converter Voltage Waveform with Nonlinear Core, Parasitics, and Thermal Effects")

plt.subplot(2, 1, 2)
plt.plot(time_points, IL_simulated, label="Inductor Current")
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.legend()
plt.grid(True)
plt.title("Advanced Buck Converter Inductor Current Waveform with Nonlinear Core, Parasitics, and Thermal Effects")

plt.tight_layout()
plt.show()
