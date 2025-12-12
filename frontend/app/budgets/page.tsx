'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import { formatCurrency } from '@/lib/utils'
import Link from 'next/link'
import Navbar from '@/components/layout/Navbar'

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
      <Navbar />

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

