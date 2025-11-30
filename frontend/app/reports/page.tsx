'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import { formatCurrency } from '@/lib/utils'
import Link from 'next/link'

export default function ReportsPage() {
  const [expensesByCategory, setExpensesByCategory] = useState<any[]>([])
  const [incomeVsExpenses, setIncomeVsExpenses] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadReports()
  }, [])

  const loadReports = async () => {
    try {
      const [expenses, incomeExpenses] = await Promise.all([
        apiClient.getExpensesByCategory(),
        apiClient.getIncomeVsExpenses()
      ])
      setExpensesByCategory(expenses)
      setIncomeVsExpenses(incomeExpenses)
    } catch (error) {
      console.error('Failed to load reports:', error)
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
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Reports</h2>

          {loading ? (
            <div className="text-center py-12">Loading...</div>
          ) : (
            <div className="space-y-6">
              {incomeVsExpenses && (
                <div className="bg-white shadow rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Income vs Expenses</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <p className="text-sm text-gray-500">Income</p>
                      <p className="text-xl font-bold text-green-600">{formatCurrency(incomeVsExpenses.income)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Expenses</p>
                      <p className="text-xl font-bold text-red-600">{formatCurrency(incomeVsExpenses.expenses)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Net</p>
                      <p className={`text-xl font-bold ${incomeVsExpenses.net >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatCurrency(incomeVsExpenses.net)}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Expenses by Category</h3>
                {expensesByCategory.length === 0 ? (
                  <p className="text-gray-500">No expense data available</p>
                ) : (
                  <ul className="divide-y divide-gray-200">
                    {expensesByCategory.map((item, index) => (
                      <li key={index} className="py-3 flex justify-between">
                        <span className="text-gray-900">Category {item.category_id || 'Uncategorized'}</span>
                        <span className="font-medium text-gray-900">{formatCurrency(item.total)}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

