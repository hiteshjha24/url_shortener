import type { ShortenPayload, TokenResponse, UrlRecord, UserResponse } from '../types'

const DEFAULT_API_BASE = '/api/v1'
const API_BASE = (import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE).replace(/\/$/, '')

async function parseResponse<T>(response: Response): Promise<T> {
  const text = await response.text()
  const data = text ? (JSON.parse(text) as T) : (null as T)

  if (!response.ok) {
    const detail = (data as { detail?: unknown })?.detail ?? 'Request failed.'
    const message = Array.isArray(detail)
      ? detail.map((item) => (typeof item === 'string' ? item : item?.msg || 'Invalid input')).join(', ')
      : typeof detail === 'string'
        ? detail
        : 'Request failed.'
    throw new Error(message)
  }

  return data
}

export const api = {
  async registerUser(email: string, password: string): Promise<UserResponse> {
    return fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    }).then((response) => parseResponse<UserResponse>(response))
  },

  async loginUser(email: string, password: string): Promise<TokenResponse> {
    const params = new URLSearchParams({ username: email, password })

    return fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    }).then((response) => parseResponse<TokenResponse>(response))
  },

  async createShortUrl(payload: ShortenPayload, token?: string): Promise<UrlRecord> {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (token) headers.Authorization = `Bearer ${token}`

    return fetch(`${API_BASE}/shorten`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        target_url: payload.target_url,
        custom_alias: payload.custom_alias || null,
        expires_in_days: payload.expires_in_days ?? null,
      }),
    }).then((response) => parseResponse<UrlRecord>(response))
  },

  async getMyUrls(token: string): Promise<UrlRecord[]> {
    return fetch(`${API_BASE}/urls/me`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then((response) => parseResponse<UrlRecord[]>(response))
  },

  async getStats(shortCode: string): Promise<UrlRecord> {
    return fetch(`${API_BASE}/stats/${shortCode}`).then((response) => parseResponse<UrlRecord>(response))
  },

  async deleteUrl(shortCode: string, token: string): Promise<{ message: string }> {
    return fetch(`${API_BASE}/shorten/${shortCode}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    }).then((response) => parseResponse<{ message: string }>(response))
  },
}
