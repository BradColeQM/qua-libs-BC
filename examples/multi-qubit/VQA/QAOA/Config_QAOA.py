import numpy as np




def gauss(amplitude, mu, sigma, delf, length):
    t = np.linspace(-length / 2, length / 2, length)
    gauss_wave = amplitude * np.exp(-((t - mu) ** 2) / (2 * sigma ** 2))
    # Detuning correction Eqn. (4) in Chen et al. PRL, 116, 020501 (2016)
    gauss_wave = gauss_wave*np.exp(2*np.pi*delf*t)
    return [float(x) for x in gauss_wave]

def gauss_der(amplitude, mu, sigma, delf, length):
    t = np.linspace(-length / 2, length / 2, length)
    gauss_der_wave = amplitude * (-2*(t-mu))*np.exp(-((t - mu) ** 2) / (2 * sigma ** 2))
    # Detuning correction Eqn. (4) in Chen et al. PRL, 116, 020501 (2016)
    gauss_der_wave = gauss_der_wave * np.exp(2 * np.pi * delf * t)
    return [float(x) for x in gauss_der_wave]


x90amp=0.4
x90std=0
x90mean=0
x90duration=1000
detuning=0
gauss_wave = gauss(x90amp, x90mean, x90std, detuning, x90duration )  #Assume you have calibration for a X90 pulse
lmda = 0.5  #Define scaling parameter for Drag Scheme
alpha = -1  #Define anharmonicity parameter
d_gauss = gauss_der(x90amp,x90mean,x90std, detuning, x90duration)

IBMconfig = {
    'version': 1,
    'controllers': {
        "con1": {
            'type': 'opx1',
            'analog_outputs': {
                1: {'offset': +0.0},
                2: {'offset': +0.0},
                3: {'offset': +0.0},
                4: {'offset': +0.0},
                5: {'offset': +0.0},
                6: {'offset': +0.0},
                7: {'offset': +0.0},
                8: {'offset': +0.0},
            },
            'analog_inputs': {
                1: {'offset': +0.0},
                2: {'offset': +0.0},

            }
        },
        "con2": {
            'type': 'opx1',
            'analog_outputs': {
                1: {'offset': +0.0},
                2: {'offset': +0.0},
                3: {'offset': +0.0},
                4: {'offset': +0.0},
                5: {'offset': +0.0},
                6: {'offset': +0.0},
                7: {'offset': +0.0},
                8: {'offset': +0.0},
            },
            'analog_inputs': {
                1: {'offset': +0.0},
                2: {'offset': +0.0},

            }
        }
    },


    'elements': {
        "qubit0": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                'lo_frequency': 5.10e7,
                'mixer': 'mixer_qubit'
            },
            'intermediate_frequency': 0,  # 5.2723e9,
            'operations': {
                'DragOp_I': "DragPulse_I",
                'DragOp_Q': "DragPulse_Q",
            },
        },
        "CPW0": {
            'mixInputs': {
                'I': ('con1', 3),
                'Q': ('con1', 4),
                'lo_frequency': 6.00e7,
                'mixer': 'mixer_res'
            },
            'intermediate_frequency': 0,
            'operations': {
                'meas_pulse': 'meas_pulse_in',
            },
            'time_of_flight': 180,  # Measurement parameters
            'smearing': 0,
            'outputs': {
                'out1': ('con1', 1)
            }

        },
        "qubit1": {
            "mixInputs": {
                "I": ("con1", 5),
                "Q": ("con1", 6),
                'lo_frequency': 5.10e7,
                'mixer': 'mixer_qubit'
            },
            'intermediate_frequency': 0,  # 5.2122e9,
            'operations': {
                'DragOp_I': "DragPulse_I",
                'DragOp_Q': "DragPulse_Q",
            },

        },
        "CPW1": {
            'mixInputs': {
                'I': ('con1', 7),
                'Q': ('con1', 8),
                'lo_frequency': 6.00e7,
                'mixer': 'mixer_res'
            },
            'intermediate_frequency': 0,  # 6.12e7,
            'operations': {
                'meas_pulse': 'meas_pulse_in',
            },
            'time_of_flight': 180,  # Measurement parameters
            'smearing': 0,
            'outputs': {
                'out1': ('con1', 2)
            }

        },

        "qubit2": {
            "mixInputs": {
                "I": ("con2", 1),
                "Q": ("con2", 2),
                'lo_frequency': 5.10e7,
                'mixer': 'mixer_qubit'
            },
            'intermediate_frequency': 0,  # 5.0154e9,
            'operations': {
                'DragOp_I': "DragPulse_I",
                'DragOp_Q': "DragPulse_Q",
            },

        },
        "CPW2": {
            'mixInputs': {
                'I': ('con2', 3),
                'Q': ('con2', 4),
                'lo_frequency': 6.00e7,
                'mixer': 'mixer_res'
            },
            'intermediate_frequency': 0,  # 6.12e7,
            'operations': {
                'meas_pulse': 'meas_pulse_in',
            },
            'time_of_flight': 180,  # Measurement parameters
            'smearing': 0,
            'outputs': {
                'out1': ('con2', 1)
            }

        },
        "qubit3": {
            "mixInputs": {
                "I": ("con2", 5),
                "Q": ("con2", 6),
                'lo_frequency': 5.10e7,
                'mixer': 'mixer_qubit'
            },
            'intermediate_frequency': 0,  # 5.2805e9,
            'operations': {
                'DragOp_I': "DragPulse_I",
                'DragOp_Q': "DragPulse_Q",
            },
        },

        "CPW3": {
            'mixInputs': {
                'I': ('con2', 7),
                'Q': ('con2', 8),
                'lo_frequency': 6.00e7,
                'mixer': 'mixer_res'
            },
            'intermediate_frequency': 0,  # 6.12e7,
            'operations': {
                'meas_pulse': 'meas_pulse_in',
            },
            'time_of_flight': 180,  # Measurement parameters
            'smearing': 0,
            'outputs': {
                'out1': ('con2', 2)
            }
        },

        # "CPW012": {
        #     "singleInput": {
        #         "port": ("con2", 1)
        #     },
        #     'intermediate_frequency': 0,  # 7e9,
        #     'operations': {
        #         'playOp': "constPulse",
        #     },
        # },
        # "CPW234": {
        #     "singleInput": {
        #         "port": ("con2", 2)
        #     },
        #     'intermediate_frequency': 0,  # 6.6e9,
        #     'operations': {
        #         'playOp': "constPulse",
        #     },
        # },
    },
    "pulses": {
        'meas_pulse_in': {  # Readout pulse
            'operation': 'measurement',
            'length': 200,
            'waveforms': {
                'I': 'exc_wf',  # Decide what pulse to apply for each component
                'Q': 'zero_wf'
            },
            'integration_weights': {
                'integW1': 'integW1',
                'integW2': 'integW2',
            },
            'digital_marker': 'marker1'
        },
        "mixedConst": {
            'operation': 'control',
            'length': 1000,
            'waveforms': {
                'I': 'const_wf',
                'Q': 'const_wf'
            }
        },
        "mixedGauss": {
            'operation': 'control',
            'length': 1000,
            'waveforms': {
                'I': 'gauss_wf',
                'Q': 'zero_wf'
            },
        },
        "constPulse": {
            'operation': 'control',
            'length': 1000,
            'waveforms': {
                'single': 'const_wf'
            }
        },
        "DragPulse_I": {
            'operation': 'control',
            'length': 1000,
            'waveforms': {
                'I': 'gauss_wf',
                'Q': 'd_gauss_wf'
            }
        },
        "DragPulse_Q": {
            'operation': 'control',
            'length': 1000,
            'waveforms': {
                'I': 'd_gauss_wf',
                'Q': 'gauss_wf'
            }
        },

        "gaussianPulse": {
            'operation': 'control',
            'length': 1000,
            'waveforms': {
                'single': 'gauss_wf'
            }
        },
    },
    "waveforms": {
        'const_wf': {
            'type': 'constant',
            'sample': 0.2
        },
        'zero_wf': {
            'type': 'constant',
            'sample': 0.
        },
        'gauss_wf': {
            'type': 'arbitrary',
            'samples': gauss_wave
        },
        'd_gauss_wf': {
            'type': 'arbitrary',
            'samples': d_gauss
        },
        'exc_wf': {
            'type': 'constant',
            'sample': 0.479
        },
    },
    'digital_waveforms': {
        'marker1': {
            'samples': [(1, 4), (0, 2), (1, 1), (1, 0)]
        }
    },
    'integration_weights': {  # Define integration weights for measurement demodulation
        'integW1': {
            'cosine': [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
                       4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
                       4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
                       4.0, 4.0, 4.0, 4.0, 4.0, 4.0],
            'sine': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        },
        'integW2': {
            'cosine': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'sine': [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
                     4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
                     4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
                     4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
        }
    },

    'mixers': {  # Potential corrections to be brought related to the IQ mixing scheme
        'mixer_res': [
            {'intermediate_frequency': 0, 'lo_frequency': 6.00e7, 'correction': [1.0, 0.0, 0.0, 1.0]}
        ],
        'mixer_qubit': [
            {'intermediate_frequency': 0, 'lo_frequency': 5.10e7, 'correction': [1.0, 0.0, 0.0, 1.0]}
        ],
    }
}
