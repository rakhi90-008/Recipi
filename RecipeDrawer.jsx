import React from 'react'

export default function RecipeDrawer({ recipe, onClose }) {
  if (!recipe) return null
  return (
    <div style={overlay} onClick={onClose}>
      <div style={drawer} onClick={e => e.stopPropagation()}>
        <h2 style={{ marginTop: 0 }}>{recipe.title}</h2>
        <p><b>Cuisine:</b> {recipe.cuisine || '—'}</p>
        <p><b>Rating:</b> {recipe.rating ?? '—'}</p>
        <p><b>Prep/Cook/Total:</b> {recipe.prep_time ?? '—'} / {recipe.cook_time ?? '—'} / {recipe.total_time ?? '—'}</p>
        <p style={{ whiteSpace: 'pre-wrap' }}>{recipe.description}</p>
        <h3>Nutrients</h3>
        <pre style={{ background: '#f8fafc', padding: 12, borderRadius: 8 }}>{JSON.stringify(recipe.nutrients, null, 2)}</pre>
        <div style={{ textAlign: 'right' }}><button onClick={onClose}>Close</button></div>
      </div>
    </div>
  )
}

const overlay = { position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.4)', display: 'grid', placeItems: 'center' }
const drawer = { background: 'white', width: 600, maxWidth: '90vw', borderRadius: 12, padding: 16, boxShadow: '0 10px 30px rgba(0,0,0,0.2)' }
