const express = require('express');
const router = express.Router();
const csurf = require('csurf');
const { body, validationResult } = require('express-validator');

const csrfProtection = csurf({ cookie: true });

router.get('/register', csrfProtection, (req, res) => {
  res.render('auth/register', { csrfToken: req.csrfToken() });
});

router.post('/register',
  csrfProtection,
  [
    body('username').isLength({ min: 4, max: 16 }).withMessage('Username must be between 4 and 16 characters.'),
    body('email').isEmail().withMessage('Invalid email address.'),
    body('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters.')
  ],
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).render('auth/register', {
        csrfToken: req.csrfToken(),
        errors: errors.array()
      });
    }

    // Registration logic goes here
    // ...
  }
);

module.exports = router;


const express = require('express');
const router = express.Router();
const csurf = require('csurf');
const { body, validationResult } = require('express-validator');

const csrfProtection = csurf({ cookie: true });

router.get('/login', csrfProtection, (req, res) => {
  res.render('auth/login', { csrfToken: req.csrfToken() });
});


