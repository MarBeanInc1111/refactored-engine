const express = require('express');
const router = express.Router();
const csurf = require('csurf');

// Create a CSRF protection middleware
const csrfProtection = csurf({ cookie: true });

// Apply CSRF protection to the GET route for registration
router.get('/register', csrfProtection, (req, res) => {
  res.render('auth/register', { csrfToken: req.csrfToken() });
});

// Apply CSRF protection to the POST route for registration
router.post('/register', csrfProtection, (req, res) => {
  // Registration logic goes here
  // ...
});

// Apply CSRF protection to the GET route for login
router.get('/login', csrfProtection, (req, res) => {
  res.render('auth/login', { csrfToken: req.csrfToken() });
});

// Apply CSRF protection to the POST route for login
router.post('/login', csrfProtection, (req, res) => {
  // Login logic goes here
  // ...
});

module.exports = router;