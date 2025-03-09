import React, { useState, ChangeEvent, FormEvent } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Link,
  Alert
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  error?: string;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSubmit, error }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onSubmit(email, password);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 400, mx: 'auto' }}>
      <Typography variant="h5" component="h1" gutterBottom align="center">
        Login to AI News
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit}>
        <TextField
          label="Email"
          type="email"
          fullWidth
          margin="normal"
          value={email}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          required
          autoFocus
          autoComplete="email"
        />

        <TextField
          label="Password"
          type="password"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          size="large"
          disabled={isSubmitting}
          sx={{ mt: 3, mb: 2 }}
        >
          {isSubmitting ? 'Signing in...' : 'Sign In'}
        </Button>

        <Box sx={{ textAlign: 'center' }}>
          <Link component={RouterLink} to="/register" variant="body2">
            Don't have an account? Sign up
          </Link>
        </Box>
      </Box>
    </Paper>
  );
};

export default LoginForm; 