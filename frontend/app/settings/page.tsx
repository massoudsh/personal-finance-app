'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import Navbar from '@/components/layout/Navbar'

export default function SettingsPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [isGuest, setIsGuest] = useState(false)

  useEffect(() => {
    loadUser()
  }, [])

  const loadUser = async () => {
    try {
      const data = await apiClient.getCurrentUser()
      setUser(data)
    } catch (error) {
      console.error('Failed to load user:', error)
      const status = (error as any)?.response?.status
      if (status === 401) {
        setIsGuest(true)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.replace('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Settings</h2>

          {loading ? (
            <div className="text-center py-12">Loading...</div>
          ) : isGuest ? (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Guest Mode</h3>
              <p className="text-sm text-gray-600">
                Create an account to manage profile settings.
              </p>
              <div className="mt-6">
                <Link
                  href="/register"
                  className="inline-flex items-center bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 text-sm font-medium"
                >
                  Create account
                </Link>
              </div>
            </div>
          ) : user ? (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Profile Information</h3>
              <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Email</dt>
                  <dd className="mt-1 text-sm text-gray-900">{user.email}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Username</dt>
                  <dd className="mt-1 text-sm text-gray-900">{user.username}</dd>
                </div>
                {user.full_name && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Full Name</dt>
                    <dd className="mt-1 text-sm text-gray-900">{user.full_name}</dd>
                  </div>
                )}
              </dl>

              <div className="mt-8 pt-6 border-t border-gray-200">
                <button
                  onClick={handleLogout}
                  className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
                >
                  Logout
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">Failed to load user information</div>
          )}
        </div>
      </main>
    </div>
  )
}

