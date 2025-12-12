/**
 * Dashboard schemas (zod) for runtime validation of API responses.
 *
 * Purpose: Keep frontend resilient to backend response changes.
 * Author: Cursor AI
 * Date: 2025-12-12
 */
import { z } from 'zod'

export const DashboardRecentTransactionSchema = z.object({
  id: z.number(),
  amount: z.number(),
  type: z.enum(['income', 'expense', 'transfer']),
  description: z.string().nullable().optional(),
  date: z.string(), // ISO string
})

export type DashboardRecentTransaction = z.infer<typeof DashboardRecentTransactionSchema>

export const DashboardSummarySchema = z.object({
  total_balance: z.number(),
  month_income: z.number(),
  month_expenses: z.number(),
  month_net: z.number(),
  active_budgets: z.number(),
  active_goals: z.number(),
  recent_transactions: z.array(DashboardRecentTransactionSchema),
})

export type DashboardSummary = z.infer<typeof DashboardSummarySchema>


