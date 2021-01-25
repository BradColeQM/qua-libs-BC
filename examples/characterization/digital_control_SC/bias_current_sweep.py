"""
bias_current_sweep.py: SFQ-based Rabi oscillations as a function of Ib
Author: Arthur Strauss - Quantum Machines
Created: 25/01/2021
Created on QUA version: 0.8.439
"""

# Importing the necessary from qm
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.qua import math
from qm import LoopbackInterface
from qm import SimulationConfig
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import curve_fit
from configuration import *

I_c = 130e-6  # 130 µA
I_min = 90e-6  # 90 µA
R = 1e3  # 1 kΩ
V_c = R * I_c  # 130 mV
V_min = R * I_min
dV = 0.001  # voltage sweeping step
N_V = int((V_c - V_min) / dV)
N_max = 3
t_max = int(500 / 4)
dt = 1
N_t = t_max // dt

qmManager = QuantumMachinesManager("3.122.60.129")
QM = qmManager.open_qm(config)  # Generate a Quantum Machine based on the configuration described above

with program() as bias_current_sweeping:  #
    I = declare(fixed)  # QUA variables declaration
    Q = declare(fixed)
    state = declare(bool)
    th = declare(fixed, value=2.0)  # Threshold assumed to have been calibrated by state discrimination exp
    t = declare(int)
    V_b = declare(fixed)  # Sweeping parameter over the set of amplitudes
    I_b = declare(fixed)
    Nrep = declare(int)  # Variable looping for repetitions of experiments
    I_b_stream = declare_stream()
    state_stream = declare_stream()
    t_stream = declare_stream()

    with for_(Nrep, 0, Nrep < N_max, Nrep + 1):
        with for_(V_b, V_min, V_b < V_c, V_b + dV):  # Sweep from 0 to V_c the bias voltage
            with for_(t, 0.00, t < t_max, t + dt):
                play("playOp" * amp(V_b), "SFQ_driver")
                play("gauss_pulse", 'qubit', duration=t)
                align("qubit", "RR")
                measure("meas_pulse", "RR", "samples", ("integW1", I), ("integW2", Q))
                play("pi_pulse", 'qubit', condition=I > th)
                assign(state, I > th)
                save(state, state_stream)
                save(t, t_stream)

            assign(I_b, V_b / R)
            save(I_b, I_b_stream)
    with stream_processing():
        I_b_stream.buffer(N_V).save("I_b")
        t_stream.buffer(N_t).save('t')
        state_stream.boolean_to_int().buffer(N_V, N_t).average().save("state")

job = qmManager.simulate(config, bias_current_sweeping,
                         SimulationConfig(int(50000),
                                          simulation_interface=LoopbackInterface([("con1", 1, "con1", 1)])
                                          )
                         )  # Use LoopbackInterface to simulate the response of the qubit
time.sleep(1.0)

# Retrieving results of the experiments
results = job.result_handles
I_b = results.I_b.fetch_all()
t = results.t.fetch_all()
state = results.state.fetch_all()

fig = plt.figure()

# Plot the surface.
plt.pcolormesh(I_b, t, state, shading="nearest")
plt.xlabel("Bias current I_b [µA]")
plt.ylabel("Pulse duration [ns]")
plt.colorbar()
plt.title("SFQ-based Rabi oscillations as a function of bias current to SFQ driver circuit")