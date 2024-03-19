# Import the required modules: yaspin and a spinner type (Spinners.line)
from yaspin import yaspin
from yaspin.spinners import Spinners

def spinner_start(text="Processing..."):
    # Create a new spinner with the specified text and a line spinner type
    spinner = yaspin(Spinners.line, text=text)
    # Start the spinner animation
    spinner.start()
    # Return the spinner object for further use
    return spinner

def spinner_stop(spinner):
    # Check if the spinner object is not None
    if spinner is not None:
        # Stop the spinner animation
        spinner.stop()
