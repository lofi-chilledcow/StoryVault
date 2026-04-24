import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getJournal } from '../api/client'
import type { Journal } from '../types'

const categoryColors: Record<string, string> = {
  tech: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
  work: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
  life: 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300',
  fun:  'bg-pink-100 text-pink-700 dark:bg-pink-900/40 dark:text-pink-300',
}

function fmtDate(raw: string) {
  const d = new Date(raw.replace(' ', 'T'))
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

export default function JournalDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [journal, setJournal] = useState<Journal | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(false)

  useEffect(() => {
    if (!id) return
    getJournal(id)
      .then(res => setJournal(res.data))
      .catch(() => setError(true))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) {
    return (
      <div className="space-y-4 max-w-2xl">
        <div className="h-8 w-2/3 rounded-lg bg-gray-200 dark:bg-gray-700 animate-pulse" />
        <div className="h-4 w-1/4 rounded bg-gray-200 dark:bg-gray-700 animate-pulse" />
        <div className="h-48 rounded-xl bg-gray-200 dark:bg-gray-700 animate-pulse" />
      </div>
    )
  }

  if (error || !journal) {
    return (
      <div className="text-center py-16">
        <p className="text-gray-500 dark:text-gray-400 mb-4">Journal not found.</p>
        <button onClick={() => navigate('/journals')} className="text-indigo-600 dark:text-indigo-400 hover:underline">
          ← Back to Journals
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-2xl">
      <button
        onClick={() => navigate('/journals')}
        className="text-sm text-indigo-600 dark:text-indigo-400 hover:underline mb-6 inline-block"
      >
        ← Back to Journals
      </button>

      <div className="flex items-center gap-3 mb-3">
        <span className={`text-xs font-medium px-2.5 py-0.5 rounded-full ${categoryColors[journal.category] ?? 'bg-gray-100 text-gray-600'}`}>
          {journal.category}
        </span>
        <span className="text-sm text-gray-400 dark:text-gray-500">
          Written {fmtDate(journal.created_at)}
        </span>
        {journal.score != null && (
          <span className="text-xs font-semibold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300 px-2 py-0.5 rounded-full">
            Score: {journal.score}
          </span>
        )}
      </div>

      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4 leading-snug">
        {journal.title}
      </h1>

      {journal.vocab_words.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-6">
          {journal.vocab_words.map(word => (
            <span
              key={word}
              className="text-sm bg-indigo-50 text-indigo-600 dark:bg-indigo-900/30 dark:text-indigo-300 px-3 py-1 rounded-full"
            >
              {word}
            </span>
          ))}
        </div>
      )}

      <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
        {journal.content}
      </p>
    </div>
  )
}
