# Constants for user input validation
CHECK_AND_CONTINUE = "Is everything working? Let me know if something needs to be changed for this task or type 'continue' to proceed."
WHEN_USER_DONE = "Once you have completed, enter 'continue'."
AFFIRMATIVE_ANSWERS = ["", "y", "yes", "ok", "okay", "sure", "absolutely", "indeed", "correct", "affirmative"]
NEGATIVE_ANSWERS = ["n", "no", "skip", "negative", "not now", "cancel", "decline", "stop"]
STUCK_IN_LOOP = "I'm stuck in a loop."
NONE_OF_THESE = "none of these"
MAX_PROJECT_NAME_LENGTH = 50

# Function to check if user input is affirmative
def is_affirmative(input_str):
    return input_str.lower() in AFFIRMATIVE_ANSWERS

# Function to check if user input is negative
def is_negative(input_str):
    return input_str.lower() in NEGATIVE_ANSWERS

# Function to check if user input is none of the above options
def is_none_of_these(input_str):
    return input_str.lower() == NONE_OF_THESE

# Function to check if user input is valid
def is_valid_input(input_str):
    return is_affirmative(input_str) or is_negative(input_str) or is_none_of_these(input_str)

