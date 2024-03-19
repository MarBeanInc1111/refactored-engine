const isAuthenticated = (req, res, next) => {
  if (typeof next !== 'function') {
    return res.status(500).send('Internal Server Error: next() is not a function');
  }

  if (req.session && req.session.userId) {
    return next(); // User is authenticated, proceed to the next middleware/route handler
  } else {
    return res.status(401).send('You are not authenticated'); // User is not authenticated
  }
};

module.exports = {
  isAuthenticated
};
