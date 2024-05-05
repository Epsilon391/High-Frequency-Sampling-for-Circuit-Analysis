function vo = Buck_Converter_Simulation(delta_RC, delta_C)
    %% Initial cnd
    % circuit component values
    vin = 24;     % input DC voltage
    Rdson = 0.1;  % transistor ESR (estimated)
    RL = 0.2;     % inductor ESR (estimated)
    RC = 0.1366+delta_RC;    % capacitor ESR (estimated)
    R = 10.9;       % load resistance
    L = 0.0001;   % inductance
    C = 0.00068-delta_C;   % capacitance
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
end