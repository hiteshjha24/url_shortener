export type UrlRecord = {
  target_url: string
  short_code: string
  short_url: string
  created_at: string
  expires_at: string | null
  is_active: boolean
  clicks: number
}

export type ShortenPayload = {
  target_url: string
  custom_alias?: string | null
  expires_in_days?: number | null
}

export type TokenResponse = {
  access_token: string
  token_type: string
}

export type UserResponse = {
  id: number
  email: string
  is_active: boolean
  created_at: string
}

export type AuthSession = {
  token: string | null
  userEmail: string | null
}
