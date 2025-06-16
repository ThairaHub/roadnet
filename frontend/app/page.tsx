"use client"

import { useState, useEffect } from "react"
import Cookies from 'js-cookie';
import Dashboard from "@/components/Dashboard";
import { LoginForm } from "@/components/LoginForm";
import { authApi } from "@/lib/api/auth";
import { RegisterForm } from "@/components/RegisterForm";


export default function Home() {

  const [token, setToken] = useState("")
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isLogin, setIsLogin] = useState(true)

  const isMe = async () =>{
    const isMe = await authApi.me()

    if(isMe){
      setIsAuthenticated(true)
      setIsLoading(false)
      return
    }

    setIsAuthenticated(false)
    setIsLoading(false)

  }

  useEffect(() =>{
    isMe()
  })


  console.log("token", token)

  if (isLoading) {
    return (
      <div className="min-h-screen bg-zinc-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-500 mx-auto mb-4"></div>
          <p>Loading ...</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      {isAuthenticated ? (
        <Dashboard />
      ) : (
        isLogin ? (
        <div className="p-6 max-w-xl mx-auto space-y-4 flex items-center justify-center h-full">
          <LoginForm isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} onSwitchToRegister={() => setIsLogin(false)} />
        </div>        
        ) : (
          <div className="p-6 max-w-xl mx-auto space-y-4 flex items-center justify-center h-full">
          <RegisterForm onSwitchToLogin={() => setIsLogin(true)} />
          </div> 
        )

      )}
    </div>
  )
}
