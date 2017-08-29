"""
This module includes all constants necessary for communication between
controller and Arduino
"""

# SENDING
S_STABILIZING_ON_MESSAGE = b'S'
S_STABILIZING_OFF_MESSAGE = b's'
S_SENSORS_ON_MESSAGE = b'G'
S_SENSORS_OFF_MESSAGE = b'g'
S_FLIGHT_REC_ON_MESSAGE = b'R'
S_FLIGHT_REC_OFF_MESSAGE = b'r'

S_RESET_MESSAGE = b'X'
S_EMERGENCY_MESSAGE = b'Z'

# RECIEVING
R_SPEED_PREFIX = b'A'
R_LR_PREFIX = b'D'
R_UD_PREFIX = b'E'
R_FRONT_PREFIX = b'B'
R_BACK_PREFIX = b'C'
