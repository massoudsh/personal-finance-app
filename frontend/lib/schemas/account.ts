/**
 * Account schemas (zod) for runtime validation of API responses.
 *
 * Purpose: Keep frontend resilient to backend response changes.
 * Author: Cursor AI
 * Date: 2025-12-12
 */
import { z } from 'zod'

export const AccountSchema = z.object({
  id: z.number(),
  user_id: z.number().optional(),
  name: z.string(),
  account_type: z.string(),
  balance: z.number(),
  currency: z.string().default('USD'),
  description: z.string().nullable().optional(),
  is_active: z.boolean().optional(),
})

export type Account = z.infer<typeof AccountSchema>

export const AccountsSchema = z.array(AccountSchema)
export type Accounts = z.infer<typeof AccountsSchema>


