// Importing required modules
const express = require('express'); // Web framework for Node.js
const User = require('../models/User'); // User model for handling user-related operations
const bcrypt = require('bcrypt'); // Library for hashing passwords

// Creating a new router object for handling routes related to authentication
const router = express.Router();

// GET request handler for the registration page
router.get('/auth/register', (req, res) => {
  // Rendering the registration page
  res.render('register');
});

// POST request handler for the registration page
router.post('/auth/register', async (req, res) => {
  try {
    // Destructuring the request body to get the username and password
    const { username, password } = req.body;

    // Creating a new user with the provided username and hashed password
    await User.create({ username, password });

    // Redirecting the user to the login page after successful registration
    res.redirect('/auth/login');
  } catch (error) {
    // Logging the error and sending a 500 status code with the error message
    console.error('Registration error:', error);
    res.status(500).send(error.message);
  }
});

// GET request handler for the login page
router.get('/auth/login', (req, res) => {
  // Rendering the login page
  res.render('login');
});

// POST request handler for the login page
router.post('/auth/login', async (req, res) => {
  try {
    // Destructuring the request body to get the username and password
    const { username, password } = req.body;

    // Finding a user with the provided username
    const user = await User.findOne({ username });

    // If the user is not found, sending a 400 status code with an appropriate error message
    if (!user) {
      return res.status(400).send('User not found');
    }

    // Comparing the provided password with the stored hashed password
    const isMatch = await bcrypt.compare(password, user.password);

    // If the passwords match, creating a session and redirecting the user to the homepage
    if (isMatch) {
      req.session.userId = user._id;
      return res.redirect('/');
    } else {
      // If the passwords do not match, sending a 400 status code with an appropriate error message
      return res.status(400).send('Password is
