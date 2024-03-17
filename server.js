// server.js

// Import necessary modules
const express = require('express');
const csrf = require('csurf');

// Initialize express app
const app = express();

// CSRF protection setup
const csrfProtection = csrf({ cookie: false });
app.use(csrfProtection);

// Middleware to make CSRF token available in res.locals
app.use((req, res, next) => {
  res.locals.csrfToken = req.csrfToken();
  next();
});

// Other middleware and routes will be added here

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

module.exports = app;