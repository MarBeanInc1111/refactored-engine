# These constants define various limits and thresholds used throughout the system

# The maximum number of times a command can be debugged before it is considered a failure
MAX_COMMAND_DEBUG_TRIES = 3

# The maximum recursion layer allowed for function calls
MAX_RECURSION_LAYER = 3

# The minimum amount of time a command should take to run, in milliseconds (2 seconds)
MIN_COMMAND_RUN_TIME = 2000

# The maximum amount of time a command is allowed to run, in milliseconds (1 minute)
MAX_COMMAND_RUN_TIME = 60000

# The maximum length of command output allowed, in characters (50000)
MAX_COMMAND_OUTPUT_LENGTH = 50000

# The maximum number of questions allowed for a bug report
MAX_QUESTIONS_FOR_BUG_REPORT = 5
