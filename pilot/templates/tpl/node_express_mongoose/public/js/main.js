// This is a function that takes in a string and returns a new string that is the reverse of the input string
const reverseString = (input) => {
  // Check if the input is a string
  if (typeof input !== 'string') {
    // If the input is not a string, throw an error
    throw new Error('Input must be a string');
  }

  // Return a new string that is the reverse of the input string
  return input.split('').reverse().join('');
};

// Call the reverseString function with an argument of "hello"
try {
  const reversedString = reverseString("hello");
  console.log(reversedString); // Output: "olleh"
} catch (error) {
  console.error(error.message); // Output: "Input must be a string"
}

