import Cookies from 'js-cookie';
import axiosClient from '../axios';

import { logout } from '../auth-util';
import { toast } from '@/components/ui/use-toast';


interface TokenOut {
  access_token: string;
  token_type: string;
  user_id: number;
}


class AuthApi {

  async login(username: string, password: string): Promise<ResponseWrapper<object>> {


    const response = await axiosClient.request<TokenOut>({
      method: 'POST',
      url: 'auth/login',
      data: { username, password },
      headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    const data = response.data

    localStorage.setItem("id", `${data.user_id}`)
    Cookies.set('access_token', data.access_token, { secure: true });
    Cookies.set('refresh_token', data.token_type, { secure: true });


    return { error: null, success: true, data: {'isAuthenticated':true} }
  }

  async register(username: string, email:string, password: string): Promise<{
    error: string | null; success:boolean, data:string
}> {

    const payload = { username, email, password}
    console.log(payload)

    const response = await axiosClient.request<string>({
      method: 'POST',
      url: 'auth/register',
      data: payload,
      headers: {
      'Content-Type': 'application/json'
      }
    });

    const data = response.data

    console.log(data)

    return { error: null, success: true, data: data }
  }


  async me(): Promise<UserOut | null> {

    try {
      const res = await axiosClient.request<UserOut>({
        method: 'GET',
        url: '/users/me',
      })
      return res.data
    } catch (err: any) {
      if (err.response?.status === 401) {
  
        logout()
  
        toast({
          title: "Session expired",
          description: "Please log in again.",
        })
  
        return null
        // Or optionally: throw new Error("Session expired. Please log in again.")
      }
  
      throw err // rethrow other errors
    }

  }
  

}

export const authApi = new AuthApi();
