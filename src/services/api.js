// Détecte automatiquement l'adresse du serveur backend
const BASE_URL = import.meta.env.VITE_API_URL || 
                 `http://${window.location.hostname}:8000`

// Holds the last successful API response so the UI stays populated if the
// backend goes down between refreshes.
let _cache = null

export async function fetchData(months = 12) {
  try {
    const res = await fetch(`${BASE_URL}/api/data?months=${months}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    _cache = data
    return data
  } catch (err) {
    if (_cache) {
      console.warn('[api] Fetch failed — returning cached data:', err.message)
      return _cache
    }
    // No cache yet: re-throw so Dashboard falls back to static mock data
    throw err
  }
}

export async function refreshData() {
  const res = await fetch(`${BASE_URL}/api/refresh`, { method: 'POST' })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}
