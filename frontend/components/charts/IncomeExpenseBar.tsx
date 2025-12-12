/**
 * Income vs Expenses chart.
 *
 * Purpose: Quick cashflow snapshot for the selected period.
 * Author: Cursor AI
 * Date: 2025-12-12
 */
'use client'

import { ResponsiveContainer, BarChart, CartesianGrid, XAxis, YAxis, Tooltip, Bar } from 'recharts'

export interface IncomeExpenseBarDatum {
  name: string
  income: number
  expenses: number
  net: number
}

export interface IncomeExpenseBarProps {
  data: IncomeExpenseBarDatum[]
}

export default function IncomeExpenseBar({ data }: IncomeExpenseBarProps) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="income" fill="#16a34a" radius={[6, 6, 0, 0]} />
        <Bar dataKey="expenses" fill="#dc2626" radius={[6, 6, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}


