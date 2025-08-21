import React, { useEffect, useState } from 'react'
import { fetchRecipes, searchRecipes } from './lib/api'
import RecipeTable from './components/RecipeTable'
import RecipeFilters from './components/RecipeFilters'
import RecipeDrawer from './components/RecipeDrawer'

export default function App() {
  const [recipes, setRecipes] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(15)
  const [filters, setFilters] = useState({ title: '', cuisine: '', rating: '', total_time: '', calories: '' })
  const [selected, setSelected] = useState(null)
  const [loading, setLoading] = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      let res
      if (filters.title || filters.cuisine || filters.rating || filters.total_time || filters.calories) {
        res = await searchRecipes({ ...filters, page, limit })
      } else {
        res = await fetchRecipes({ page, limit })
      }
      setRecipes(res.data || [])
      setTotal(res.total || 0)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [page, limit]) // eslint-disable-line
  useEffect(() => { setPage(1); load() }, [filters]) // eslint-disable-line

  return (
    <div style={{ fontFamily: 'Inter, system-ui, sans-serif', maxWidth: 1100, margin: '24px auto', padding: '0 16px' }}>
      <h1>Recipes</h1>
      <RecipeFilters value={filters} onChange={setFilters} limit={limit} onLimitChange={setLimit} />
      <RecipeTable rows={recipes} loading={loading} page={page} limit={limit} total={total}
        onPageChange={setPage} onSelect={setSelected} />
      <RecipeDrawer recipe={selected} onClose={() => setSelected(null)} />
    </div>
  )
}
