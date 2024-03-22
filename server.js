// server.js

// Import necessary modules
const express = require('express');
const csurf = require('csurf');
const cookieParser = require('cookie-parser');

// Initialize express app
const app = express();

// Configure view engine
app.set('view engine', 'ejs');

// CSRF protection setup
const csrfProtection = csurf({ cookie: true });
app.use(cookieParser());
app.use(csrfProtection);

// Middleware to make CSRF token available in res.locals
app.use((req, res, next) => {
  res.locals.csrfToken = req.csrfToken();
  res.locals.title = 'My App';
  next();
});

// Routes
app.get('/', (req, res) => {
  res.render('index', { title: 'Home' });
});

app.get('/contact', csrfProtection, (req, res) => {
  res.render('contact', { title: 'Contact', csrfToken: req.csrfToken() });
});

app.post('/contact', csrfProtection, (req, res) => {
  res.send('Thank you for your message!');
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

module.exports = app;
