clear
clc

%% Initial cnd
% circuit component values
vin = 24;     % input DC voltage
Rdson = 0.1;  % transistor ESR (estimated)
RL = 0.2;     % inductor ESR (estimated)
RC = 0.1366+0.0;    % capacitor ESR (estimated) originally 0.01
R = 10.9;       % load resistance
L = 0.0001;   % inductance
C = 0.00068-0.0000;   % capacitance originally 0.000680
VF = 0.7;     % diode forward voltage

% initial cicuit AC conditions
iL = 0;       % initial inductor current
vC = 0;       % initial capacitor voltage

% switch waveform
fsw = 50000;  % 50 kHz switching freq
Tstep = 1E-8; % 10 ns dt iteration step (Sample Rate of oscilloscope used)
D = 0.5;      % duty cycle

%% Switch Modeling
Tsw = 1/fsw;
t = 0:Tstep:0.1-Tstep;
S = mod(t,Tsw)>Tsw*D;
%% Circuit analysis
% The S array represents the state of the switch at each point in time
vals = zeros([3 size(S,2)]);
vo = zeros([1 size(S,2)]);

for itr = 1:size(S,2)
    % switch independent component of State Space Equations
    A = S(itr).*Rdson + RL + RC*R/(RC + R);
    Se = [-A./L (-1/L*(R/(RC+R)));
        (1/C*(R/(RC+R))) -(1/C*(1/(RC+R)));
        (RC*R/(RC+R)) R/(RC+R)];

    % switch dependent components of State Space Equations
    Son = S(itr).*[vin/L;0;0];
    Soff = (1-S(itr)).*[-VF/L;0;0];
    
    % Store delta in vals and Calculate Change 
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
title('Output Voltage')
xlabel('Time (s)')
ylabel('Voltage (V)')

% show n switch cycles
n = 20;
subplot(212)
plot(t,vo)
ylim([11.29 11.47])
xlim([0.01 0.01+Tsw*n])
title('Output Voltage Ripple')
xlabel('Time (s)')
ylabel('Voltage (V)')

%% Plot vc Physical
ps = 0;
vo_samp = vo(1,(ps)+9E6:(ps)+9E6+1E4-1);
vo_samp = transpose(vo_samp);

fig = figure()
Tvc = table2array(readtable('V2_DC.csv'));
vc = Tvc(14:10013,2);
tc = Tvc(14:10013,1);
% Get the average of the dc offset
vc_dc = sum(vc)/10000;
% plot(tc,vc)
% title("VC")
% ylabel(string(vc_dc),'FontWeight','bold','Rotation',0)

% plot the physical results of the AC capacitor voltage signal plus
% the averaged DC offset
Tvc = table2array(readtable('V2_AC.csv'));
vc = Tvc(14:10013,2);
tc = Tvc(14:10013,1);
vc = vc + vc_dc;
%d = norm(vc - vo_samp);
%d2 = norm(vo_samp - vc);
%corrplot(vc)
%figure
plot(tc,vc)
hold on
% plot the mathmatically modeled data over top
plot(tc,vo_samp, 'LineWidth', 2.5)
writematrix(vo_samp, "Capacitor_Ripple_Simulated_Voltage.csv");
%xlim([0.0 10000.0])
ylim([11.29 11.47])
yticks([11.3:0.04:11.48])
fontsize(fig, 24,"point")
title('Capacitor Ripple Voltage')
ylabel('Voltage (V)')
legend('Measured','Simulated');
hold off
%xy=[vc;vo_samp]; 
%sd=std(xy);

%% Plot VC filtered through highpass to remove DC offset
y = highpass((vc),5,fsw) + 1;
y2 = vo_samp - vc_dc + 1;

figure 
plot(y)
hold on

plot(y2)
%writematrix(y, "Capacitor_Ripple_Simulated_Voltage.csv");
%xlim([0.0 10000.0])
ylim([0.0 2.0])
title('Capacitor Ripple Voltage')
ylabel('Voltage (V)')
legend('Measured','Simulated');
hold off