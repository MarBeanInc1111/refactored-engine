// Importing required modules: mongoose for working with MongoDB and bcrypt for password hashing
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

// Defining the User schema with Mongoose
const userSchema = new mongoose.Schema({
  // Unique username field, required for each user
  username: {
    type: String,
    unique: true,
    required: true,
    minlength: 3,
    maxlength: 32,
    trim: true,
  },
  // Password field, required for each user
  password: {
    type: String,
    required: true,
    minlength: 8,
    maxlength: 1024,
  },
  // Virtual field for password confirmation during registration
  passwordConfirmation: {
    type: String,
    required: true,
    validate: {
      validator: function (value) {
        return value === this.password;
      },
      message: 'Passwords do not match',
    },
  },
});

// Pre-save hook for hashing the password before saving the user document
userSchema.pre('save', async function (next) {
  const user = this; // The user document being saved

  // Check if the password field has been modified
  if (!user.isModified('password')) return next(); // If not, continue to the next middleware

  // Hashing the password with bcrypt
  try {
    const hash = await bcrypt.hash(user.password, 10);
    user.password = hash;
    next(); // Proceed to the next middleware or save the user document
  } catch (err) {
    console.error('Error hashing password:', err);
    return next(err);
  }
});

// Adding a method for comparing the hashed password with a plaintext password
userSchema.methods.comparePassword = function (candidatePassword, callback) {
  bcrypt.compare(candidatePassword
