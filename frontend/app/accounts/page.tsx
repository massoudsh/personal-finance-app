'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api'
import { formatCurrency } from '@/lib/utils'
import Link from 'next/link'
import Navbar from '@/components/layout/Navbar'

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
      <Navbar />

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

