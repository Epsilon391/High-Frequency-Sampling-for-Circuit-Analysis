clear;
clc;
%% Plot Vc at Variable ESR and C
% Physical data
figure
Tvc = table2array(readtable('V2_DC.csv'));
vc = Tvc(14:10013,2);
% Get the average of the dc offset
vc_dc = sum(vc)/10000;
% plot the physical results of the AC capacitor voltage signal plus
% the averaged DC offset
Tvc = table2array(readtable('V2_AC.csv'));
vc = Tvc(14:10013,2);
vc = vc + vc_dc;
tc = Tvc(14:10013,1);
ps = 0;
t = tc((ps)+1E3:(ps)+3E3-1, 1);
ps = 0;
vo_measured = vc((ps)+1E3:(ps)+3E3-1, 1);
hold on
plot(vo_measured);

% Variable C
% Simulation under ideal conditions
ideal_cap = 0.000680; % Farads
vo1 = Buck_Converter_Simulation(0.0, 0.0);
ps = 0;
vo_samp1 = transpose(vo1(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
% Simulation under 5% decrease in capacitance
c = 0.05 * ideal_cap;
vo2 = Buck_Converter_Simulation(0.0, c); 
ps = 0;
vo_samp2 = transpose(vo2(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1)); 
% Simulation under 10% decrease in capacitance
c = 0.1 * ideal_cap;
vo3 = Buck_Converter_Simulation(0.0, c); 
ps = 0;
vo_samp3 = transpose(vo3(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
% Simulation under 15% decrease in capacitance
c = 0.15 * ideal_cap;
vo4 = Buck_Converter_Simulation(0.0, c); 
ps = 0;
vo_samp4 = transpose(vo4(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
% Simulation under 20% decrease in capacitance
c = 0.2 * ideal_cap;
vo5 = Buck_Converter_Simulation(0.0, c); 
ps = 0;
vo_samp5 = transpose(vo5(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));

% plot the mathmatically modeled data over top
plot(vo_samp1, 'LineWidth',2.0)
plot(vo_samp2, 'LineWidth',2.0)
plot(vo_samp3, 'LineWidth',2.0)
plot(vo_samp4, 'LineWidth',2.0)
plot(vo_samp5, 'LineWidth',2.0)
hold off
title('Capacitor Ripple Voltage')
xlabel('Samples')
ylabel('Voltage (V)')
xlim([1060 1070])
ylim([11.457 11.46])
legend('Measured','Ideal','5% Decrease in Capacitance', ...
    '10% Decrease in Capacitance', '15% Decrease in Capacitance', ...
    '20% Decrease in Capacitance');
%% Variable ESR
% Simulation under ideal conditions
ideal_ESR = 0.1366; % Farads
vo1 = Buck_Converter_Simulation(0.0, 0.0);
ps = 0;
vo_samp1 = transpose(vo1(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
% Simulation under 20% increase in ESR
ESR = 0.2 * ideal_ESR;
vo2 = Buck_Converter_Simulation(ESR, 0.0); 
ps = 0;
vo_samp2 = transpose(vo2(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1)); 
% Simulation under 25% increase in ESR
ESR = 0.25 * ideal_ESR;
vo3 = Buck_Converter_Simulation(ESR, 0.0); 
ps = 0;
vo_samp3 = transpose(vo3(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
% Simulation under 30% increase in ESR
ESR = 0.30 * ideal_ESR;
vo4 = Buck_Converter_Simulation(ESR, 0.0); 
ps = 0;
vo_samp4 = transpose(vo4(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
% Simulation under 35% increase in ESR
ESR = 0.35 * ideal_ESR;
vo5 = Buck_Converter_Simulation(ESR, 0.0); 
ps = 0;
vo_samp5 = transpose(vo5(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
% Simulation under 40% increase in ESR
ESR = 0.40 * ideal_ESR;
vo6 = Buck_Converter_Simulation(ESR, 0.0); 
ps = 0;
vo_samp6 = transpose(vo6(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));

% plot the mathmatically modeled data over top
hold on
%plot(vo_measured);
plot(vo_samp1, 'LineWidth',2.0)
plot(vo_samp2, 'LineWidth',2.0)
plot(vo_samp3, 'LineWidth',2.0)
plot(vo_samp4, 'LineWidth',2.0)
plot(vo_samp5, 'LineWidth',2.0)
plot(vo_samp6, 'LineWidth',2.0)
hold off
%xlim([0 2000]);
%ylim([11.2 11.7]);
title('Capacitor Ripple Voltage')
xlabel('Sample')
ylabel('Voltage (V)')
legend('Measured','Ideal','20% Increase in ESR','25% Increase in ESR', ...
    '30% Increase in ESR', '35% Increase in ESR', '40% Increase in ESR');

%% Model 6 different "levels" of degrdation
% Simulation under ideal conditions
ideal_cap = 0.000680; % Farads
ideal_ESR = 0.1366;

figure
subplot(2,3,1);
% Simulation under 20% increase in ESR 20% decrease in capacitance
ESR = 0.2 * ideal_ESR;
c = 0.1 * ideal_cap;
vo1 = Buck_Converter_Simulation(ESR, c); 
ps = 0;
vo_samp1 = transpose(vo1(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
plot(vo_samp1, 'LineWidth',2.0)
% Simulation under 30% increase in ESR 30% decrease in capacitance
subplot(2,3,2);
ESR = 0.3 * ideal_ESR;
c = 0.1 * ideal_cap;
vo2 = Buck_Converter_Simulation(ESR, c); 
ps = 0;
vo_samp2 = transpose(vo2(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
plot(vo_samp2, 'LineWidth',2.0)
% Simulation under 40% increase in ESR 40% decrease in capacitance
subplot(2,3,3);
ESR = 0.4 * ideal_ESR;
c = 0.1 * ideal_cap;
vo3 = Buck_Converter_Simulation(ESR, c); 
ps = 0;
vo_samp3 = transpose(vo3(1,(ps)+9E6+1E3:(ps)+9E6+3E3-1));
plot(vo_samp3, 'LineWidth',2.0)

