"use client"

import { useState, useEffect } from "react"

import {

  ChevronLeft,
  Home,
  Menu,
} from "lucide-react"
import { Button } from "@/components/ui/button"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,

} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

import RoadNetPage from "@/components/roadnet/page"
import FileUpload from "./FileUpload"
import { logout } from "@/lib/auth-util"
import { geoJsonApi } from "@/lib/api/geojson"

export default function Dashboard() {
  const [activeSection, setActiveSection] = useState("upload-geojson")
  const [isMobile, setIsMobile] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768)
    }

    handleResize()
    window.addEventListener("resize", handleResize)

    return () => {
      window.removeEventListener("resize", handleResize)
    }
  }, [])

 
  const renderBillingSystem = () => (
    <>

      <Dialog>
        <DialogTrigger asChild>
          <Button className="mb-6">New File</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[600px] w-full max-w-md mx-auto overflow-hidden min-h-[550px] flex flex-col bg-white dark:bg-zinc-900 border-zinc-200/50 dark:border-zinc-800/50 shadow-lg shadow-zinc-200/50 dark:shadow-zinc-900/50">
          <DialogHeader>
            <DialogTitle>New File</DialogTitle>
            <DialogDescription>A new file will update the previous.</DialogDescription>
          </DialogHeader>

          <FileUpload endpoint="upload" endpoint_method="POST"/>

        </DialogContent>
      </Dialog>
      <Dialog>
        <DialogTrigger asChild>
          <Button className="mb-6">Update File</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[600px] w-full max-w-md mx-auto overflow-hidden min-h-[550px] flex flex-col bg-white dark:bg-zinc-900 border-zinc-200/50 dark:border-zinc-800/50 shadow-lg shadow-zinc-200/50 dark:shadow-zinc-900/50">
          <DialogHeader>
            <DialogTitle>Update File</DialogTitle>
            <DialogDescription>A new file will update the previous.</DialogDescription>
          </DialogHeader>

          <FileUpload endpoint="update" endpoint_method="PUT"/>

        </DialogContent>
      </Dialog>

      <Button className="mb-6" onClick={async () => geoJsonApi.delete_roads()}>Delete All</Button>
    </>
  )


  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile Sidebar Toggle */}
      {isMobile && (
        <Button
          variant="outline"
          size="icon"
          className="fixed bottom-4 right-4 z-50 rounded-full h-12 w-12 shadow-lg bg-white"
          onClick={() => setSidebarOpen(true)}
        >
          <Menu className="h-6 w-6" />
        </Button>
      )}

      {/* Sidebar */}
      <div
        className={`${isMobile ? "fixed inset-0 z-50 transform transition-transform duration-300 ease-in-out" : "w-64"} ${isMobile && !sidebarOpen ? "-translate-x-full" : "translate-x-0"} bg-white border-r border-gray-200 flex flex-col`}
      >
        {isMobile && (
          <div className="flex justify-end p-4">
            <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(false)}>
              <ChevronLeft className="h-6 w-6" />
            </Button>
          </div>
        )}
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-2xl font-semibold text-purple-600">RoadNet</h1>
        </div>
        <div className="flex-1 py-4 overflow-y-auto">
          <nav className="space-y-1 px-2">

            <button
              onClick={() => setActiveSection("upload-geojson")}
              className={`flex items-center w-full px-4 py-3 text-sm font-medium rounded-r-md ${activeSection === "upload-geojson" ? "text-blue-600 bg-blue-50 border-l-4 border-blue-600" : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"}`}
            >
              <Home className="mr-3 h-5 w-5" />
              Upload GeoJson
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 flex items-center justify-between px-4 py-4 md:px-6">
          <div className="flex items-center">
            {isMobile && (
              <Button variant="ghost" size="icon" className="mr-2" onClick={() => setSidebarOpen(true)}>
                <Menu className="h-5 w-5" />
              </Button>
            )}
            <h1 className="text-xl font-semibold text-gray-800">
              Upload GeoJson
            </h1>
          </div>
          <div className="flex items-center space-x-4">
            
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src="/placeholder.svg?height=32&width=32" alt="User" />
                    <AvatarFallback>U</AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem 
                  onClick={() => {
                                logout()
                                location.reload();
                              }}>
                          Logout</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 bg-gray-50">
          {activeSection === "upload-geojson" && renderBillingSystem()}
          {activeSection === "upload-geojson" && <RoadNetPage/>}

        </main>
      </div>
    </div>
  )
}
