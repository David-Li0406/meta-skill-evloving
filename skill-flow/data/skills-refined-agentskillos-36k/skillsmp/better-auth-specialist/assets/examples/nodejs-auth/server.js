// Complete Node.js/Express Authentication Server Example
// Install: npm install express cors dotenv pg bcryptjs jsonwebtoken

const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors({
  origin: process.env.CLIENT_URL || 'http://localhost:3000',
  credentials: true,
}));
app.use(express.json());

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

// JWT Secret
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';
const JWT_EXPIRES_IN = '7d';

// Middleware to verify JWT token
const authenticateToken = async (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    const result = await pool.query(
      'SELECT id, email, name, email_verified FROM users WHERE id = $1',
      [decoded.userId]
    );

    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'User not found' });
    }

    req.user = result.rows[0];
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Invalid or expired token' });
  }
};

// Routes

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Signup
app.post('/api/auth/signup', async (req, res) => {
  const { email, password, name } = req.body;

  // Validation
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  if (password.length < 8) {
    return res.status(400).json({ error: 'Password must be at least 8 characters' });
  }

  const client = await pool.connect();

  try {
    await client.query('BEGIN');

    // Check if user exists
    const existingUser = await client.query(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );

    if (existingUser.rows.length > 0) {
      await client.query('ROLLBACK');
      return res.status(400).json({ error: 'User already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create user
    const userResult = await client.query(
      'INSERT INTO users (email, name, email_verified) VALUES ($1, $2, $3) RETURNING id, email, name, email_verified, created_at',
      [email, name || null, false]
    );

    const user = userResult.rows[0];

    // Store hashed password
    await client.query(
      'INSERT INTO passwords (user_id, hashed_password) VALUES ($1, $2)',
      [user.id, hashedPassword]
    );

    // Assign default user role
    const roleResult = await client.query(
      'SELECT id FROM roles WHERE name = $1',
      ['user']
    );

    if (roleResult.rows.length > 0) {
      await client.query(
        'INSERT INTO user_roles (user_id, role_id) VALUES ($1, $2)',
        [user.id, roleResult.rows[0].id]
      );
    }

    await client.query('COMMIT');

    // Generate JWT token
    const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });

    res.status(201).json({
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        emailVerified: user.email_verified,
      },
      token,
    });
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Signup error:', error);
    res.status(500).json({ error: 'Internal server error' });
  } finally {
    client.release();
  }
});

// Signin
app.post('/api/auth/signin', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  try {
    // Get user
    const userResult = await pool.query(
      'SELECT u.id, u.email, u.name, u.email_verified, p.hashed_password FROM users u JOIN passwords p ON u.id = p.user_id WHERE u.email = $1',
      [email]
    );

    if (userResult.rows.length === 0) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    const user = userResult.rows[0];

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.hashed_password);

    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    // Generate JWT token
    const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });

    res.json({
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        emailVerified: user.email_verified,
      },
      token,
    });
  } catch (error) {
    console.error('Signin error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get current user
app.get('/api/auth/me', authenticateToken, (req, res) => {
  res.json({ user: req.user });
});

// Signout (client-side handles token removal)
app.post('/api/auth/signout', (req, res) => {
  res.json({ message: 'Signed out successfully' });
});

// Get user roles
app.get('/api/user/roles', authenticateToken, async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT r.id, r.name, r.description
       FROM roles r
       JOIN user_roles ur ON r.id = ur.role_id
       WHERE ur.user_id = $1`,
      [req.user.id]
    );

    res.json({ roles: result.rows });
  } catch (error) {
    console.error('Get roles error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Protected route example
app.get('/api/protected', authenticateToken, (req, res) => {
  res.json({
    message: 'This is a protected route',
    user: req.user,
  });
});

// Role-based route example (admin only)
app.get('/api/admin', authenticateToken, async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT r.name FROM roles r
       JOIN user_roles ur ON r.id = ur.role_id
       WHERE ur.user_id = $1 AND r.name = 'admin'`,
      [req.user.id]
    );

    if (result.rows.length === 0) {
      return res.status(403).json({ error: 'Admin access required' });
    }

    res.json({ message: 'Admin route accessed successfully' });
  } catch (error) {
    console.error('Admin route error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
