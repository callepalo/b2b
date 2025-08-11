import { reactive, readonly } from 'vue'
import { supabase } from './supabaseClient'

const state = reactive({
  session: null,
  profile: null,
  loading: true,
  error: null,
  lastProfileResponse: null,
})

async function init() {
  const { data: { session } } = await supabase.auth.getSession()
  state.session = session
  state.loading = false
  // Optionally fetch profile from backend to get role
  if (session) await fetchProfile()
  supabase.auth.onAuthStateChange(async (_event, sess) => {
    state.session = sess
    if (sess) {
      await fetchProfile()
    } else {
      state.profile = null
    }
  })
}

async function fetchProfile() {
  try {
    const token = state.session?.access_token
    if (!token) { state.profile = null; return }
    const base = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || ''
    const res = await fetch(`${base}/api/v1/profiles/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    const text = await res.text()
    let data = null
    try { data = text ? JSON.parse(text) : null } catch { /* keep raw */ }
    state.lastProfileResponse = data || text || null
    if (!res.ok) {
      const msg = (data && (data.detail || data.message)) || text || res.statusText
      throw new Error(msg)
    }
    state.profile = data
  } catch (e) {
    state.error = String(e?.message || e)
  }
}

function getAccessToken() {
  return state.session?.access_token || null
}

async function signIn(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password })
  if (error) throw error
  state.session = data.session
  await fetchProfile()
}

async function signOut() {
  await supabase.auth.signOut()
  state.session = null
  state.profile = null
}

function isAdmin() {
  return state.profile?.role === 'admin'
}

init()

export const auth = {
  state: readonly(state),
  signIn,
  signOut,
  getAccessToken,
  isAdmin,
  fetchProfile,
}
