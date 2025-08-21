const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function fetchRecipes({ page=1, limit=15 }={}) {
  const res = await fetch(`${API_BASE}/api/recipes?page=${page}&limit=${limit}`)
  return res.json()
}

export async function searchRecipes(params) {
  const query = new URLSearchParams(Object.entries(params).filter(([,v]) => v !== '' && v !== null && v !== undefined))
  const res = await fetch(`${API_BASE}/api/recipes/search?${query.toString()}`)
  return res.json()
}
