/**
 * Reports schemas (zod) for runtime validation of API responses.
 *
 * Purpose: Keep frontend resilient to backend response changes.
 * Author: Cursor AI
 * Date: 2025-12-12
 */
import { z } from 'zod'

export const ExpensesByCategoryItemSchema = z.object({
  category_id: z.number().nullable(),
  total: z.number(),
})

export type ExpensesByCategoryItem = z.infer<typeof ExpensesByCategoryItemSchema>

export const ExpensesByCategorySchema = z.array(ExpensesByCategoryItemSchema)
export type ExpensesByCategory = z.infer<typeof ExpensesByCategorySchema>

export const IncomeVsExpensesSchema = z.object({
  income: z.number(),
  expenses: z.number(),
  net: z.number(),
})

export type IncomeVsExpenses = z.infer<typeof IncomeVsExpensesSchema>


