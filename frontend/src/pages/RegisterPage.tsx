import React from 'react';
import { Container, Box } from '@mui/material';
import RegisterForm from '../components/auth/RegisterForm';
import { useAuth } from '../contexts/AuthContext';

const RegisterPage: React.FC = () => {
  const { register, error } = useAuth();

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <RegisterForm onSubmit={register} error={error} />
      </Box>
    </Container>
  );
};

export default RegisterPage; 