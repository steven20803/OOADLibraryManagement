import React from 'react';
import { Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function LandingPage() {
  const navigate = useNavigate();
  const handleStart = () => {
    navigate('/collection');
  }

  return (
    <Container sx={{ pt : 5}}>
      <Typography variant="h4" component="h1" gutterBottom>
        OOAD Project 
      </Typography>
      <Typography variant='h4'>
        Library Management System
      </Typography>
      
      <br/>

      <Typography variant="body1" gutterBottom>
        My App is the best app ever. It has all the features you need and none of the ones you don't.
      </Typography>

      <Button variant="contained" color="primary" onClick={handleStart}>
        開始使用
      </Button>
    </Container>
  );
}

export default LandingPage;