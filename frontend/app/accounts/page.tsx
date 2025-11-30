'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import { formatCurrency } from '@/lib/utils'
import Link from 'next/link'

export default function AccountsPage() {
  const [accounts, setAccounts] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAccounts()
  }, [])

  const loadAccounts = async () => {
    try {
      const data = await apiClient.getAccounts()
      setAccounts(data)
    } catch (error) {
      console.error('Failed to load accounts:', error)
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
                <Link href="/accounts" className="border-primary-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
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
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Accounts</h2>
            <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
              Add Account
            </button>
          </div>

          {loading ? (
            <div className="text-center py-12">Loading...</div>
          ) : accounts.length === 0 ? (
            <div className="text-center py-12 text-gray-500">No accounts found. Create your first account!</div>
          ) : (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {accounts.map((account) => (
                <div key={account.id} className="bg-white shadow rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-900">{account.name}</h3>
                  <p className="text-sm text-gray-500 capitalize">{account.account_type.replace('_', ' ')}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-4">{formatCurrency(account.balance, account.currency)}</p>
                  {account.description && (
                    <p className="text-sm text-gray-500 mt-2">{account.description}</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

