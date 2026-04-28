const BASE_URL = import.meta.env.VITE_API_URL ||
                 `http://${window.location.hostname}:8000`

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
      console.warn('fetch failed, using cache:', err.message)
      return _cache
    }
    throw err
  }
}

export async function refreshData() {
  const res = await fetch(`${BASE_URL}/api/refresh`, { method: 'POST' })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}
