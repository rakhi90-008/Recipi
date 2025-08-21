import React from 'react'

export default function RecipeTable({ rows, loading, page, limit, total, onPageChange, onSelect }) {
  const totalPages = Math.max(1, Math.ceil((total || 0) / (limit || 1)))
  return (
    <div>
      <div style={{ overflowX: 'auto', border: '1px solid #e5e7eb', borderRadius: 12 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={th}>Title</th>
              <th style={th}>Cuisine</th>
              <th style={th}>Rating</th>
              <th style={th}>Total Time</th>
              <th style={th}></th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} style={{ padding: 16, textAlign: 'center' }}>Loading…</td></tr>
            ) : rows.length === 0 ? (
              <tr><td colSpan={5} style={{ padding: 16, textAlign: 'center' }}>No results</td></tr>
            ) : rows.map(r => (
              <tr key={r.id} style={{ borderTop: '1px solid #f3f4f6' }}>
                <td style={td}>{r.title}</td>
                <td style={td}>{r.cuisine || '—'}</td>
                <td style={td}>{r.rating ?? '—'}</td>
                <td style={td}>{r.total_time ?? '—'}</td>
                <td style={td}><button onClick={() => onSelect(r)}>Details</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 12 }}>
        <button onClick={() => onPageChange(Math.max(1, page-1))} disabled={page<=1}>Prev</button>
        <span>Page {page} / {totalPages}</span>
        <button onClick={() => onPageChange(Math.min(totalPages, page+1))} disabled={page>=totalPages}>Next</button>
      </div>
    </div>
  )
}

const th = { textAlign: 'left', padding: 12, background: '#fafafa', borderBottom: '1px solid #e5e7eb' }
const td = { padding: 12 }
