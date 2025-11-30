'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import { formatCurrency } from '@/lib/utils'
import Link from 'next/link'

export default function GoalsPage() {
  const [goals, setGoals] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadGoals()
  }, [])

  const loadGoals = async () => {
    try {
      const data = await apiClient.getGoals()
      setGoals(data)
    } catch (error) {
      console.error('Failed to load goals:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Link href="/dashboard" className="text-xl font-bold text-primary-600">Finance App</Link>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link href="/dashboard" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Dashboard
                </Link>
                <Link href="/accounts" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Accounts
                </Link>
                <Link href="/transactions" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Transactions
                </Link>
                <Link href="/budgets" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Budgets
                </Link>
                <Link href="/goals" className="border-primary-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Goals
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Goals</h2>
            <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
              Create Goal
            </button>
          </div>

          {loading ? (
            <div className="text-center py-12">Loading...</div>
          ) : goals.length === 0 ? (
            <div className="text-center py-12 text-gray-500">No goals found. Create your first goal!</div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {goals.map((goal) => {
                const progress = (goal.current_amount / goal.target_amount) * 100
                return (
                  <div key={goal.id} className="bg-white shadow rounded-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">{goal.name}</h3>
                        {goal.description && (
                          <p className="text-sm text-gray-500 mt-1">{goal.description}</p>
                        )}
                      </div>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        goal.status === 'completed' ? 'bg-green-100 text-green-800' :
                        goal.status === 'active' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {goal.status}
                      </span>
                    </div>
                    <div className="mb-2">
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>{formatCurrency(goal.current_amount)}</span>
                        <span>{formatCurrency(goal.target_amount)}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${Math.min(progress, 100)}%` }}
                        ></div>
                      </div>
                    </div>
                    <p className="text-sm text-gray-500 mt-2">
                      {progress.toFixed(1)}% complete
                    </p>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

