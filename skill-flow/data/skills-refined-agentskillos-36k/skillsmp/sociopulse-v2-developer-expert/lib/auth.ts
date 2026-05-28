
import Cookies from 'js-cookie';
import { getApiUrl } from './config';

const API_URL = getApiUrl();

// Cookie options for proper persistence
const getCookieOptions = (): Cookies.CookieAttributes => {
  const isSecure = typeof window !== 'undefined' && window.location.protocol === 'https:';
  return {
    expires: 7, // 7 days
    path: '/',
    sameSite: 'lax',
    secure: isSecure,
  };
};

export interface LoginResponse {
  accessToken: string;
}

export const auth = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
      credentials: 'include', // Important for cookies
    });

    if (!response.ok) {
      if (response.status === 401 || response.status === 403) {
        throw new Error('Identifiants incorrects');
      }
      throw new Error('Une erreur est survenue lors de la connexion');
    }

    return response.json();
  },

  setToken(token: string) {
    // Set cookie with proper options for persistence
    Cookies.set('accessToken', token, getCookieOptions());
    console.log('[Auth] Token saved to cookie');
  },

  getToken() {
    return Cookies.get('accessToken');
  },

  logout() {
    Cookies.remove('accessToken', { path: '/' });
    // V2: Redirect to landing page after logout
    window.location.href = '/';
  },

  isAuthenticated() {
    return !!Cookies.get('accessToken');
  }
};
