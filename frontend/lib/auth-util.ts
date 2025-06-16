import Cookies from 'js-cookie';
import axiosClient  from './axios';



export async function tryRefreshToken(): Promise<boolean> {
  const refreshToken = Cookies.get('refresh_token');
  if (!refreshToken) return false;

  try {
    const response = await axiosClient.post('/v1/refresh', {
      refresh_token: refreshToken,
    });
    const { access_token } = response.data.data;
    Cookies.set('access_token', access_token, { secure: true });
    return true;
  } catch {
    return false;
  }
}

export function logout() {

  Cookies.remove('access_token');
  Cookies.remove('refresh_token');
  localStorage.clear()


}
