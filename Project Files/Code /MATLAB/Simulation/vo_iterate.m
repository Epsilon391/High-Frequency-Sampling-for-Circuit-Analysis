clear
clc

%% Initial cnd

% circuit component values
vin = 24;     % input DC voltage
Rdson = 0.1;  % transistor ESR (estimated)
RL = 0.2;     % inductor ESR (estimated)
RC = 0.01;    % capacitor ESR (estimated)
R = 15;       % load resistance
L = 0.0001;   % inductance
C = 0.0001;   % capacitance
VF = 0.7;     % diode forward voltage

% initial cicuit AC conditions
iL = 0;       % initial inductor current
vC = 0;       % initial capacitor voltage

% switch waveform
fsw = 50000;  % 50 kHz switching freq
Tstep = 1E-8; % 10 ns dt iteration step
D = 0.5;      % duty cycle

%% Switch
Tsw = 1/fsw;
t = 0:Tstep:0.1;
S = mod(t,Tsw)>Tsw*D;

%% Circuit analysis
vals = zeros([3 size(S,2)]);
vo = zeros([1 size(S,2)]);

for itr = 1:size(S,2)
    % switch independent component
    A = S(itr).*Rdson + RL + RC*R/(RC + R);
    Se = [-A./L (-1/L*(R/(RC+R)));
        (1/C*(R/(RC+R))) -(1/C*(1/(RC+R)));
        (RC*R/(RC+R)) R/(RC+R)];

    % switch dependent components
    Son = S(itr).*[vin/L;0;0];
    Soff = (1-S(itr)).*[-VF/L;0;0];
    
    % calculate change 
    vals = Se*[iL;vC] + Son + Soff;
    iL = Tstep*vals(1) + iL;
    vC = Tstep*vals(2) + vC;
    vo(itr) = vals(3);
end

%% Plot results
% output voltage
figure
subplot(211)
plot(t,vo)
title('Output voltage')
xlabel('Time (s)')
ylabel('Voltage (V)')

% show n switch cycles
n = 20;
subplot(212)
plot(t,vo)
ylim([11.42 11.48])
xlim([0.01 0.01+Tsw*n])
title('Output voltage ripple')
xlabel('Time (s)')
ylabel('Voltage (V)')