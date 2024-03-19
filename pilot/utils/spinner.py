# Import the required module yaspin and a spinner type (Spinners.line)
import yaspin
from yaspin.spinners import Spinners

def start_spinner(text="Processing..."):
    """
    Create a new spinner with the specified text and a line spinner type,
    start the spinner animation and return the spinner object for further use.
    """
    # Create a new spinner with the specified text and a line spinner type
    spinner = yaspin(Spinners.line, text=text)
    # Start the spinner animation
    spinner.start()
    # Return the spinner object for further use
    return spinner

def stop_spinner(spinner):
    """
    Stop the spinner animation if the spinner object is not None.
    """
    # Check if the spinner object is not None
    if spinner is not None:
        # Stop the spinner animation
        spinner.stop()
