# Import the required module yaspin and the Spinners class
import yaspin
from yaspin.spinners import Spinners

def create_spinner(text="Processing...") -> yaspin.Spinner:
    """
    Create a new spinner with the specified text and a line spinner type,
    start the spinner animation and return the spinner object for further use.
    """
    # Create a new spinner with the specified text and a line spinner type
    spinner = yaspin.Spinner(spinner=Spinners.line, text=text)
    # Start the spinner animation
    spinner.start()
    # Return the spinner object for further use
    return spinner

def stop_spinner(spinner: yaspin.Spinner) -> None:
    """
    Stop the spinner animation if the spinner object is not None.
    """
    # Stop the spinner animation
    spinner.stop()

# Example usage
spinner = create_spinner()
# Do some processing here
stop_spinner(spinner)
