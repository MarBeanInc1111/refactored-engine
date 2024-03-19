// This is a placeholder for future JavaScript code

// Define a variable named `myVariable` and initialize it to an empty string
let myVariable = "";

// Define a function named `myFunction` that takes in a single parameter `input`
function myFunction(input) {
  // Check if the `input` parameter is a string
  if (typeof input === 'string') {
    // If `input` is a string, return a new string that is the reverse of `input`
    return input.split('').reverse().join('');
  } else {
    // If `input` is not a string, return a message indicating that the input was invalid
    return "Input was not a valid string";
  }
}

// Call the `myFunction` function with an argument of "hello"
const reversedString = myFunction("hello");

// Log the result of the function call to the console
console.log(reversedString); // Output: "olleh"
