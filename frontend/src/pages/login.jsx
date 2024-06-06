import React, { useState } from 'react';
import { Button, TextField, Grid, Paper, Typography } from '@mui/material';
import { Navigate, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';


function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (event) => {
    event.preventDefault();
    fetch(`http://localhost:8000/user/login?username=${username}&password=${password}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((res) => {
        if (res.ok) {
          return res.json();
        }
        throw new Error('Login failed');
      })
    .then((data) => {
        console.log(data);
        Cookies.set('userId', data.id);
        Cookies.set('user', data.name);
        Cookies.set('role', data.role);
        window.location.href = '/';
    })
    .catch((error) => {
        alert('Login failed');
        console.error('Failed to login:', error);
    });
  }

  return (
    <Grid container justify="center">
      <Grid item xs={12} sm={8} md={6} lg={4}>
        <Paper elevation={3} style={{ margin: '2rem', padding: '2rem' }}>
          <Typography variant="h4" align="center">
            Login
          </Typography>
          <form onSubmit={handleLogin}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoFocus
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              style={{ marginTop: '1rem' }}
            >
              Login
            </Button>
          </form>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default LoginPage;