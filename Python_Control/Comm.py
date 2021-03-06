"""
This module includes all constants necessary for communication between
controller and Arduino
"""

# SENDING
S_STABILIZING_ON_COMMAND = b'S'
S_STABILIZING_OFF_COMMAND = b's'
S_SENSORS_ON_COMMAND = b'G'
S_SENSORS_OFF_COMMAND = b'g'
S_FLIGHT_REC_ON_COMMAND = b'R'
S_FLIGHT_REC_OFF_COMMAND = b'r'

S_RESET_COMMAND = b'X'
S_EMERGENCY_COMMAND = b'Z'

S_SPEED_PREFIX = b'A'
S_LR_PREFIX = b'D'
S_UD_PREFIX = b'E'
S_FRONT_PREFIX = b'B'
S_BACK_PREFIX = b'C'

# RECIEVING

R_STATUS_OK = b'A'
R_STATUS_BATTERY_FAULT = b'B'
R_STATUS_MOTOR_FAULT = b'C'
R_STATUS_SENSOR_FAULT = b'D'
R_STATUS_FLIGHT_REC_FAULT = b'E'
R_STATUS_ARDUINO_FAULT = b'F'
R_STATUS_UNKNOWN_FAULT = b'G'

R_STABILIZING_ON_CONFIRM    = b'H'
R_STABILIZING_OFF_CONFIRM   = b'h'
R_SENSORS_ON_CONFIRM        = b'I'
R_SENSORS_OFF_CONFIRM       = b'i'
R_FLIGHT_REC_ON_CONFIRM     = b'O'
R_FLIGHT_REC_OFF_CONFIRM    = b'o'

R_MPU_X_PREFIX = b'J'
R_MPU_Y_PREFIX = b'K'
R_MPU_Z_PREFIX = b'L'

# GROUPS
S_COMMANDS = [
    S_STABILIZING_ON_COMMAND,
    S_STABILIZING_OFF_COMMAND,
    S_SENSORS_ON_COMMAND,
    S_SENSORS_OFF_COMMAND,
    S_FLIGHT_REC_ON_COMMAND,
    S_FLIGHT_REC_OFF_COMMAND,
    S_RESET_COMMAND,
    S_EMERGENCY_COMMAND
]
S_PREFIXES = [
    S_BACK_PREFIX,
    S_FRONT_PREFIX,
    S_LR_PREFIX,
    S_SPEED_PREFIX,
    S_UD_PREFIX
]

R_STATUSES = [
    R_STATUS_ARDUINO_FAULT,
    R_STATUS_BATTERY_FAULT,
    R_STATUS_FLIGHT_REC_FAULT,
    R_STATUS_MOTOR_FAULT,
    R_STATUS_OK,
    R_STATUS_SENSOR_FAULT,
    R_STATUS_UNKNOWN_FAULT,
]

ALL_SENDING = []
ALL_RECIEVING = []
