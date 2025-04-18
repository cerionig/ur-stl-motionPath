# Service allows setting digital (DIO) and analog (AIO) IO, as well as flags
# and configuring tool voltage.
#
# This service has three request fields (see below).
#
# When setting DIO or AIO pins to new values:
#
#  fun    The function to perform
#  pin    Numeric ID of the pin to set, see constants definition below
#  state  Desired pin state (signal level for analog or STATE_(ON|OFF) for DIO and flags)
#
# When configuring tool voltage:
#
#  fun    Set to FUN_SET_TOOL_VOLTAGE
#  pin    Ignored
#  state  Desired tool voltage (use STATE_TOOL_VOLTAGE constants)

# constants
# pin mapping
# analog out
int8 PIN_AOUT0 = 0
int8 PIN_AOUT1 = 1

# digital out
int8 PIN_DOUT0 = 0
int8 PIN_DOUT1 = 1
int8 PIN_DOUT2 = 2
int8 PIN_DOUT3 = 3
int8 PIN_DOUT4 = 4
int8 PIN_DOUT5 = 5
int8 PIN_DOUT6 = 6
int8 PIN_DOUT7 = 7

# configurable out
int8 PIN_CONF_OUT0 = 8
int8 PIN_CONF_OUT1 = 9
int8 PIN_CONF_OUT2 = 10
int8 PIN_CONF_OUT3 = 11
int8 PIN_CONF_OUT4 = 12
int8 PIN_CONF_OUT5 = 13
int8 PIN_CONF_OUT6 = 14
int8 PIN_CONF_OUT7 = 15

# digital tool output
int8 PIN_TOOL_DOUT0 = 16
int8 PIN_TOOL_DOUT1 = 17

# valid function values
#
# Note: 'fun' is short for 'function' (ie: the function the service should perform).
int8 FUN_SET_DIGITAL_OUT = 1
int8 FUN_SET_FLAG = 2
int8 FUN_SET_ANALOG_OUT = 3
int8 FUN_SET_TOOL_VOLTAGE = 4

# valid values for 'state' when setting digital IO or flags
int8 STATE_OFF = 0
int8 STATE_ON = 1

# valid 'state' values when setting tool voltage
int8 STATE_TOOL_VOLTAGE_0V = 0
int8 STATE_TOOL_VOLTAGE_12V = 12
int8 STATE_TOOL_VOLTAGE_24V = 24

# request fields
int8 fun
int8 pin
float32 state
