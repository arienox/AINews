import React from 'react';
import { Container, Box } from '@mui/material';
import LoginForm from '../components/auth/LoginForm';
import { useAuth } from '../contexts/AuthContext';

const LoginPage: React.FC = () => {
  const { login, error } = useAuth();

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <LoginForm onSubmit={login} error={error} />
      </Box>
    </Container>
  );
};

export default LoginPage; 