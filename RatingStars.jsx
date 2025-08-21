// (Optional) Simple visual stars, not wired into table yet
import React from 'react'
export default function RatingStars({ value=0, outOf=5 }) {
  const full = Math.round((value || 0))
  return <span>{[...Array(outOf)].map((_,i) => i<full ? '★' : '☆')}</span>
}
