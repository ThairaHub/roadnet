import axios from "axios"
import Cookies from 'js-cookie';

const axiosClient = axios.create({
  baseURL: "/api/",
})

axiosClient.interceptors.request.use(config => {
  if (typeof window !== "undefined") {
    const token = Cookies.get("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  }
  return config
})

export default axiosClient
