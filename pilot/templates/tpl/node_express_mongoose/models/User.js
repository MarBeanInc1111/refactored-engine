// Importing required modules: mongoose for working with MongoDB and bcrypt for password hashing
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

// Defining the User schema with Mongoose
const userSchema = new mongoose.Schema({
  // Unique username field, required for each user
  username: { type: String, unique: true, required: true },
  // Password field, required for each user
  password: { type: String, required: true }
});

// Pre-save hook for hashing the password before saving the user document
userSchema.pre('save', function(next) {
  const user = this; // The user document being saved

  // Check if the password field has been modified
  if (!user.isModified('password')) return next(); // If not, continue to the next middleware

  // Hashing the password with bcrypt
  bcrypt.hash(user.password, 10, (err, hash) => {
    if (err) { // If there's an error, log it and pass it to the next middleware
      console.error('Error hashing password:', err);
      return next(err);
    }

    // Replace the plain password with the hashed one
    user.password = hash;
    next(); // Proceed to the next middleware or save the user document
  });
});

// Creating the User model with the defined schema
const User = mongoose.model('User', userSchema);

// Exporting the User model for use in other parts of the application
module.exports = User;
