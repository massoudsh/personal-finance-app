'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import { formatCurrency } from '@/lib/utils'
import Link from 'next/link'

export default function BudgetsPage() {
  const [budgets, setBudgets] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadBudgets()
  }, [])

  const loadBudgets = async () => {
    try {
      const data = await apiClient.getBudgets()
      setBudgets(data)
    } catch (error) {
      console.error('Failed to load budgets:', error)
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
                <Link href="/budgets" className="border-primary-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Budgets
                </Link>
                <Link href="/goals" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
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
            <h2 className="text-2xl font-bold text-gray-900">Budgets</h2>
            <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
              Create Budget
            </button>
          </div>

          {loading ? (
            <div className="text-center py-12">Loading...</div>
          ) : budgets.length === 0 ? (
            <div className="text-center py-12 text-gray-500">No budgets found. Create your first budget!</div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {budgets.map((budget) => (
                <div key={budget.id} className="bg-white shadow rounded-lg p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">{budget.name}</h3>
                      <p className="text-sm text-gray-500 capitalize mt-1">{budget.period}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-medium text-gray-900">{formatCurrency(budget.amount)}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

