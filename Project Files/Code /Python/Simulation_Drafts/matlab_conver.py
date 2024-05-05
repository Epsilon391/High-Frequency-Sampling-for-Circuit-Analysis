import numpy as np
from scipy.signal import StateSpace, lsim
import matplotlib.pyplot as plt

# circuit component values
vin = 24     # input DC voltage
Rdson = 0.1  # transistor ESR (estimated)
RL = 0.2     # inductor ESR (estimated)
RC = 0.01    # capacitor ESR (estimated)
R = 15       # load resistance
L = 0.0001   # inductance
C = 0.0001   # capacitance
VF = 0.7     # diode forward voltage

# initial cicuit AC conditions
iL = 0       # initial inductor current
vC = 0       # initial capacitor voltage

# switch waveform
fsw = 50000  # 50 kHz switching freq
Tstep = 1E-8 # 10 ns dt iteration step
D = 0.5      # duty cycle

# Switch
Tsw = 1/fsw
t = np.arange(0, 0.1, Tstep)
S = t % Tsw > Tsw * D

# Circuit analysis
# array is a 3 by 
vals = np.zeros([3, np.size(S,2)])
vo = np.zeros([1, np.size(S,2)])

for i in range (1, np.size(S,2)):
    # switch independent component
    A = S(i) * Rdson + RL + RC * R / (RC + R)
    Se = [[-A / L, (-1 / L * (R / (RC + R)))],
        [(1 / C * (R / (RC + R))), -(1 / C * (1 / (RC + R)))],
        [(RC * R / (RC + R)), R / (RC + R)]]

    # switch dependent components
    Son = S(i) * [[vin/L],[0],[0]]
    Soff = (1-S(i))*[[-VF/L],[0],[0]]
    
    # calculate change 
    vals = Se * [[iL], [vC]] + Son + Soff
    iL = Tstep * vals(1) + iL
    vC = Tstep * vals(2) + vC
    vo[i] = vals(3)

# Plot results
# output voltage
# Plot the results

plt.plot(t, vo, label='Output Voltage')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.show()


# show n switch cycles
# n = 20
# subplot(212)
# plot(t,vo)
# ylim([11.42 11.48])
# xlim([0.01 0.01+Tsw*n])
# title('Output voltage ripple')
# xlabel('Time (s)')
# ylabel('Voltage (V)')