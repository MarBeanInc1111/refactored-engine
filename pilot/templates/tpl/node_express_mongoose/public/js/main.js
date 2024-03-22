// This is a function that takes in a string and returns a new string that is the reverse of the input string
const reverseString = (input) => {
  // Check if the input is a string
  if (typeof input !== 'string') {
    // If the input is not a string, throw an error with a more informative message
    throw new Error('The reverseString function expects a string as its only argument. Please provide a string.');
  }

  // Check if the input string is empty
  if (input.length === 0) {
    // If the input string is empty, return an empty string
    return '';
  }

  // Return a new string that is the reverse of the input string
  return input.split('').reverse().join('');
};

// Call the reverseString function with an argument of "hello"
try {
  const reversedString = reverseString("hello");
  console.log(reversedString); // Output: "olleh"
} catch (error) {
  console.error(error.message); // Output: "The reverseString function expects a string as its only argument. Please provide a string."
}

// Call the reverseString function with an argument of 42
try {
  const reversedString = reverseString(42);
  console.log(reversedString);
} catch (error) {
  console.error(error.message); // Output: "The reverseString function expects a string as its only argument. Please provide a string."
}

// Call the reverseString function with an argument of []
try {
  const reversedString = reverseString([]);
  console.log(reversedString);
} catch (error) {
  console.error(error.message); // Output: "The reverseString function expects a string as its only argument. Please provide a string."
}

