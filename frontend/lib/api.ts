/**
 * API client for backend communication.
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import { DashboardSummarySchema, type DashboardSummary } from '@/lib/schemas/dashboard'
import { AccountsSchema, type Accounts } from '@/lib/schemas/account'
import {
  ExpensesByCategorySchema,
  IncomeVsExpensesSchema,
  type ExpensesByCategory,
  type IncomeVsExpenses,
} from '@/lib/schemas/reports'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Handle unauthorized - clear token.
          // NOTE: We intentionally do NOT redirect to /login here to allow "guest mode"
          // and avoid forcing auth UX for users who just want to explore the app.
          this.clearToken();
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  private clearToken(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  setToken(token: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('access_token', token);
  }

  setRefreshToken(token: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('refresh_token', token);
  }

  // Auth endpoints
  async register(data: { email: string; username: string; password: string; full_name?: string }) {
    const response = await this.client.post('/auth/register', data);
    return response.data;
  }

  async login(username: string, password: string) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await this.client.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    if (response.data.access_token) {
      this.setToken(response.data.access_token);
      this.setRefreshToken(response.data.refresh_token);
    }
    
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  // Account endpoints
  async getAccounts() {
    const response = await this.client.get('/accounts');
    return AccountsSchema.parse(response.data) as Accounts;
  }

  async getAccount(id: number) {
    const response = await this.client.get(`/accounts/${id}`);
    return response.data;
  }

  async createAccount(data: any) {
    const response = await this.client.post('/accounts', data);
    return response.data;
  }

  async updateAccount(id: number, data: any) {
    const response = await this.client.put(`/accounts/${id}`, data);
    return response.data;
  }

  async deleteAccount(id: number) {
    await this.client.delete(`/accounts/${id}`);
  }

  // Transaction endpoints
  async getTransactions(params?: any) {
    const response = await this.client.get('/transactions', { params });
    return response.data;
  }

  async getTransaction(id: number) {
    const response = await this.client.get(`/transactions/${id}`);
    return response.data;
  }

  async createTransaction(data: any) {
    const response = await this.client.post('/transactions', data);
    return response.data;
  }

  async updateTransaction(id: number, data: any) {
    const response = await this.client.put(`/transactions/${id}`, data);
    return response.data;
  }

  async deleteTransaction(id: number) {
    await this.client.delete(`/transactions/${id}`);
  }

  // Budget endpoints
  async getBudgets() {
    const response = await this.client.get('/budgets');
    return response.data;
  }

  async getBudget(id: number) {
    const response = await this.client.get(`/budgets/${id}`);
    return response.data;
  }

  async createBudget(data: any) {
    const response = await this.client.post('/budgets', data);
    return response.data;
  }

  async updateBudget(id: number, data: any) {
    const response = await this.client.put(`/budgets/${id}`, data);
    return response.data;
  }

  async deleteBudget(id: number) {
    await this.client.delete(`/budgets/${id}`);
  }

  // Goal endpoints
  async getGoals() {
    const response = await this.client.get('/goals');
    return response.data;
  }

  async getGoal(id: number) {
    const response = await this.client.get(`/goals/${id}`);
    return response.data;
  }

  async createGoal(data: any) {
    const response = await this.client.post('/goals', data);
    return response.data;
  }

  async updateGoal(id: number, data: any) {
    const response = await this.client.put(`/goals/${id}`, data);
    return response.data;
  }

  async deleteGoal(id: number) {
    await this.client.delete(`/goals/${id}`);
  }

  // Dashboard endpoints
  async getDashboardSummary() {
    const response = await this.client.get('/dashboard/summary');
    return DashboardSummarySchema.parse(response.data) as DashboardSummary;
  }

  // Report endpoints
  async getExpensesByCategory(startDate?: string, endDate?: string) {
    const response = await this.client.get('/reports/expenses-by-category', {
      params: { start_date: startDate, end_date: endDate },
    });
    return ExpensesByCategorySchema.parse(response.data) as ExpensesByCategory;
  }

  async getIncomeVsExpenses(startDate?: string, endDate?: string) {
    const response = await this.client.get('/reports/income-vs-expenses', {
      params: { start_date: startDate, end_date: endDate },
    });
    return IncomeVsExpensesSchema.parse(response.data) as IncomeVsExpenses;
  }
}

export const apiClient = new ApiClient();

