import React from 'react'

export default function RecipeFilters({ value, onChange, limit, onLimitChange }) {
  const set = (k, v) => onChange({ ...value, [k]: v })
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 8, marginBottom: 12 }}>
      <input placeholder="Title contains…" value={value.title} onChange={e => set('title', e.target.value)} />
      <input placeholder="Cuisine (exact)" value={value.cuisine} onChange={e => set('cuisine', e.target.value)} />
      <input placeholder="Rating (e.g. >=4.5)" value={value.rating} onChange={e => set('rating', e.target.value)} />
      <input placeholder="Total time (<=60)" value={value.total_time} onChange={e => set('total_time', e.target.value)} />
      <input placeholder="Calories (<=400)" value={value.calories} onChange={e => set('calories', e.target.value)} />
      <select value={limit} onChange={e => onLimitChange(parseInt(e.target.value))}>
        {[15,20,25,30,40,50].map(n => <option key={n} value={n}>{n}/page</option>)}
      </select>
    </div>
  )
}
