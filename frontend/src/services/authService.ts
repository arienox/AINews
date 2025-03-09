import axios from 'axios';

const API_URL = '/api';

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
}

class AuthService {
  private token: string | null = null;

  constructor() {
    this.token = localStorage.getItem('token');
    if (this.token) {
      this.setAuthHeader(this.token);
    }
  }

  private setAuthHeader(token: string) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  async login(email: string, password: string): Promise<void> {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post<LoginResponse>(`${API_URL}/auth/token`, formData);
    const { access_token } = response.data;
    
    localStorage.setItem('token', access_token);
    this.token = access_token;
    this.setAuthHeader(access_token);
  }

  async register(email: string, password: string, fullName: string): Promise<void> {
    await axios.post(`${API_URL}/users/`, {
      email,
      password,
      full_name: fullName
    });
  }

  async getCurrentUser(): Promise<User | null> {
    if (!this.token) return null;

    try {
      const response = await axios.get<User>(`${API_URL}/auth/test-token`);
      return response.data;
    } catch {
      this.logout();
      return null;
    }
  }

  logout(): void {
    localStorage.removeItem('token');
    this.token = null;
    delete axios.defaults.headers.common['Authorization'];
  }

  isAuthenticated(): boolean {
    return !!this.token;
  }
}

export const authService = new AuthService(); 