import numpy as np
import matplotlib.pyplot as plt

# Initial conditions
vin = 24.0  # input DC voltage
Rdson = 0.1  # transistor ESR (estimated)
RL = 0.2  # inductor ESR (estimated)
RC = 0.01  # capacitor ESR (estimated)
R = 15.0  # load resistance
L = 0.0001  # inductance
C = 0.0001  # capacitance
VF = 0.7  # diode forward voltage

# Initial circuit AC conditions
iL = 0.0  # initial inductor current
vC = 0.0  # initial capacitor voltage

# Switch waveform
fsw = 50000.0  # 50 kHz switching frequency
Tstep = 1E-8  # 10 ns dt iteration step
D = 0.5  # duty cycle

# Switch
Tsw = 1.0 / fsw
t = np.arange(0, 0.1, Tstep)
S = np.mod(t, Tsw) > Tsw * D

# Circuit analysis
vals = np.zeros((3, len(S)))
vo = np.zeros(len(S))

for itr in range(len(S)):
    # Switch-independent component
    A = S[itr] * Rdson + RL + RC * R / (RC + R)
    Se = np.array([[-A / L, -1 / L * (R / (RC + R))],
                   [1 / C * (R / (RC + R)), -1 / C * (1 / (RC + R))],
                   [RC * R / (RC + R), R / (RC + R)]])

    # Switch-dependent components
    Son = S[itr] * np.array([vin / L, 0, 0])
    Soff = (1 - S[itr]) * np.array([-VF / L, 0, 0])

    # Calculate change
    vals[:, itr] = np.dot(Se, np.array([iL, vC])) + Son + Soff
    iL = Tstep * vals[0, itr] + iL
    vC = Tstep * vals[1, itr] + vC
    vo[itr] = vals[2, itr]

# Plot results
plt.figure()

# Output voltage
plt.subplot(2, 1, 1)
plt.plot(t, vo)
plt.title('Output voltage')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')

# Show n switch cycles
n = 20
plt.subplot(2, 1, 2)
plt.plot(t, vo)
plt.ylim(11.42, 11.48)
plt.xlim(0.01, 0.01 + Tsw * n)
plt.title('Output voltage ripple')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')

plt.tight_layout()
plt.show()


