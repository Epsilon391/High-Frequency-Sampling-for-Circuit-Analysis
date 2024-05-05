#include <stdio.h>
#include <iostream>
#include <cmath>
#include <numeric>
#include <vector>
#include <algorithm>
#include <bits/stdc++.h>
#include <matplot/matplot.h>
using namespace matplot;
using namespace std;

// Global Variable Declaration
const double Tstep = 1E-8; // 10 ns dt iteration step
const int R1 = 3; // number of rows in Matrix-1
const int C1 = 2; // number of columns in Matrix-1 
const int R2 = 2; // number of rows in Matrix-2
const int C2 = 1; // number of columns in Matrix-2 

// function declarations
double Tstep_inc();
vector<vector<double>> mulMat(vector<vector<double>> mat1, vector<vector<double>> mat2);
vector<vector<double>> addMat(vector<vector<double>> mat1, vector<vector<double>> mat2);
void print_Results(vector<double> t, vector<double> vo, double Tsw);

int main(){
    
    // circuit component values
    const int vin = 24;     // input DC voltage
    const float Rdson = 0.1;  // transistor ESR (estimated)
    const float RL = 0.2;     // inductor ESR (estimated)
    const float RC = 0.01+0.12;    // capacitor ESR (estimated)
    const float R = 10.9;       // load resistance
    const float L = 0.0001;   // inductance
    const float C = 0.0001-0.0000;   // capacitance
    const float VF = 0.7;     // diode forward voltage

    // initial cicuit AC conditions
    double iL = 0;       // initial inductor current
    double vC = 0;       // initial capacitor voltage

    // Initial cnd
    double t_low = -1.0093E-5;
    double t_high = -1.01042E-5;
    double t_rise = abs(t_high-t_low);

    // switch waveform
    const double fsw = 50000.0;  // 50 kHz switching freq
    double D = 0.5;      // duty cycle
    double Tsw = 1/fsw; // switching period

    // declaring a time vector with size of 
    // number of time points = (0.1-Tstep) / Tstep
    vector<double> t((0.1) / Tstep);
 
    // initializing vector with loop
    double curr = 0.0;
    for(size_t i = 0; i < t.size(); i++) {
        t[i] = curr; 
        curr += Tstep;
    }
    
    // Creating switch signal vector 
    vector<int> S((0.1) / Tstep);
    for (size_t j = 0; j < S.size(); j++) {
        if(fmod(t[j], Tsw) > Tsw * D) {
            S[j] = 1; 
        } else {
            S[j] = 0;
        }
    }

    // Actual Mathmatical representation of circuit and analysis
    double A; 
    // 3 x 1 array of results {{il}, {vc}, {vo}}
    vector<vector<double>> vals(3, vector<double> (1, 0.0));
    // vo will be a 1D vector of just the vector outputs
    vector<double> vo((0.1) / Tstep); 
    // Se is the state equation matrix as defined in the paper 3x2
    vector<vector<double>> Se(3, vector<double> (2, 0.0));
    // declare switch dependant components  arrays 3x1
    vector<vector<double>> Son(3, vector<double> (1, 0.0));
    vector<vector<double>> Soff(3, vector<double> (1, 0.0));
    // vector for il and vc values 2x1
    vector<vector<double>> il_vc = {{iL}, {vC}};

    for(size_t k = 0; k < ((0.1) / Tstep); k++) {
        // switch independent component
        A = S[k] * Rdson + RL + RC * R / (RC + R);
        Se = {{-A/L, (-1/L*(R/(RC+R)))},
             {(1/C*(R/(RC+R))), -(1/C*(1/(RC+R)))},
             {(RC*R/(RC+R)), R/(RC+R)}};

        // switch dependent components
        Son = {{S[k] * vin/L}, {0}, {0}};
        Soff = {{(1-S[k]) * -VF/L}, {0}, {0}};
        
        // calculate change 
        vals = addMat(addMat(mulMat(Se, il_vc), Son), Soff);
        // cout << "il:" << vals[0][0] << "vc:" << vals[1][0] << "vo" << vals[2][0];
        iL += Tstep * vals[0][0];
        vC += Tstep * vals[1][0];
        il_vc = {{iL}, {vC}};
        vo[k] = vals[2][0];
    }
    // print results 
    print_Results(t, vo, Tsw);
    return 0;
}

/*
* Lamba function that returns 
*/
double Tstep_inc() {
    static double i = Tstep;
    return i + Tstep;
}

vector<vector<double>> mulMat(vector<vector<double>> mat1, vector<vector<double>> mat2) { 
    vector<vector<double>> rslt(R1, vector<double> (C2, 0.0)); 
  
    for (size_t i = 0; i < R1; i++) { 
        for (size_t j = 0; j < C2; j++) { 
            rslt[i][j] = 0; 
  
            for (size_t k = 0; k < R2; k++) { 
                rslt[i][j] += mat1[i][k] * mat2[k][j]; 
            }
        }
    } 
    return rslt;
}

// This function adds two matricies
vector<vector<double>> addMat(vector<vector<double>> mat1, vector<vector<double>> mat2){
    vector<vector<double>> rslt(R1, vector<double> (C2, 0.0));
    for (size_t i = 0; i < R1; i++) {
        for (size_t j = 0; j < C2; j++) {
            rslt[i][j] = mat1[i][j] + mat2[i][j];
        }
    }
    return rslt;
}

void print_Results(vector<double> t, vector<double> vo, double Tsw) {

    // Create a Plot object
    // Plot2D plot1;

    // // Set the x and y labels
    // plot.xlabel("Time (s)");
    // plot.ylabel("Voltage (V)");

    // // Draw a sine graph putting x on the x-axis and sin(x) on the y-axis
    // plot1.drawCurve(t, vo).label("Output Voltage").lineWidth(4);

    // // Create a second Plot object
    // Plot2D plot2;

    // // Set the x and y labels
    // plot.xlabel("Time (s)");
    // plot.ylabel("Voltage (V)");

    // // Set the x and y ranges
    // plot.xrange(11.29, 11.47);
    // plot.yrange(0.01, 0.01+Tsw*20);

    // // Draw a tangent graph putting x on the x-axis and tan(x) on the y-axis
    // plot2.drawCurve(t, vo).label("Output Voltage Ripple").lineWidth(4);

    // // Put both plots in a "figure" horizontally next to each other
    // Figure figure = (Undefined, Undefined);

    // // Create a canvas / drawing area to hold figure and plots
    // Canvas canvas = {{ figure }};
    // // Set color palette for all Plots that do not have a palette set (plot2) / the default palette
    // canvas.defaultPalette("set1");

    // // Show the canvas in a pop-up window
    // canvas.show();

    tiledlayout(2, 1);
    nexttile();
    plot(t, vo, "-o");
    title("Output Voltage");
    xlabel("Time (s)");
    ylabel("Voltage (V)");

    nexttile();
    plot(t, vo, "-o");
    title("Ripple Voltage");
    xlabel("Time (s)");
    ylabel("Voltage (V)");
    xlim({11.29, 11.47});
    ylim({0.01, 0.01+Tsw*20});

    show();
}
