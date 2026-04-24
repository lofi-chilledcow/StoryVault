import { useEffect, useState } from 'react'
import { getJournals } from '../api/client'
import JournalCard from '../components/JournalCard'
import type { Journal } from '../types'

const CATEGORIES = ['All', 'tech', 'work', 'life', 'fun'] as const

export default function Journals() {
  const [journals, setJournals] = useState<Journal[]>([])
  const [loading, setLoading]   = useState(true)
  const [active, setActive]     = useState<string>('All')

  useEffect(() => {
    setLoading(true)
    const cat = active === 'All' ? undefined : active
    getJournals(cat)
      .then(res => setJournals(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [active])

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Journals</h1>

      {/* Category tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {CATEGORIES.map(cat => (
          <button
            key={cat}
            onClick={() => setActive(cat)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors capitalize ${
              active === cat
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-36 rounded-xl bg-gray-200 dark:bg-gray-700 animate-pulse" />
          ))}
        </div>
      ) : journals.length === 0 ? (
        <div className="rounded-xl border-2 border-dashed border-gray-200 dark:border-gray-700 p-12 text-center text-gray-400 dark:text-gray-500">
          No journals yet. Start writing via Claude!
        </div>
      ) : (
        <div className="space-y-4">
          {journals.map(j => <JournalCard key={j.id} journal={j} />)}
        </div>
      )}
    </div>
  )
}
