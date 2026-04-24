import { useEffect, useState } from 'react'
import { getStats } from '../api/client'
import type { Stats } from '../types'

export default function StatsBar() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getStats()
      .then(res => setStats(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[...Array(4)].map((_, i) => (
          <div
            key={i}
            className="h-20 rounded-xl bg-gray-200 dark:bg-gray-700 animate-pulse"
          />
        ))}
      </div>
    )
  }

  const cards = [
    { label: 'Total Journals', value: stats?.total_journals ?? 0 },
    { label: 'Total Stories',  value: stats?.total_stories  ?? 0 },
    { label: 'Streak 🔥',      value: `${stats?.streak_days ?? 0} days` },
    { label: 'Words Used',     value: stats?.words_used.length ?? 0 },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {cards.map(card => (
        <div
          key={card.label}
          className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4 text-center shadow-sm"
        >
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {card.value}
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {card.label}
          </div>
        </div>
      ))}
    </div>
  )
}
