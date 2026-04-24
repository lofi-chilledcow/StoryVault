import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getJournals, getStories } from '../api/client'
import StatsBar from '../components/StatsBar'
import JournalCard from '../components/JournalCard'
import StoryCard from '../components/StoryCard'
import type { Journal, Story } from '../types'

export default function Home() {
  const [journals, setJournals]   = useState<Journal[]>([])
  const [stories, setStories]     = useState<Story[]>([])
  const [loading, setLoading]     = useState(true)

  useEffect(() => {
    Promise.all([getJournals(), getStories()])
      .then(([jRes, sRes]) => {
        setJournals((jRes.data as Journal[]).slice(0, 3))
        setStories((sRes.data as Story[]).slice(0, 3))
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Dashboard</h1>
      <p className="text-gray-500 dark:text-gray-400 mb-6">Your personal story bank at a glance.</p>

      <StatsBar />

      <div className="grid md:grid-cols-2 gap-8">
        {/* Latest Journals */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Latest Journals</h2>
            <Link
              to="/journals"
              className="text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              View all →
            </Link>
          </div>

          {loading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-32 rounded-xl bg-gray-200 dark:bg-gray-700 animate-pulse" />
              ))}
            </div>
          ) : journals.length === 0 ? (
            <div className="rounded-xl border-2 border-dashed border-gray-200 dark:border-gray-700 p-8 text-center text-gray-400 dark:text-gray-500">
              No journals yet. Start writing via Claude!
            </div>
          ) : (
            <div className="space-y-3">
              {journals.map(j => <JournalCard key={j.id} journal={j} />)}
            </div>
          )}
        </section>

        {/* Latest Stories */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Latest Stories</h2>
            <Link
              to="/stories"
              className="text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              View all →
            </Link>
          </div>

          {loading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-32 rounded-xl bg-gray-200 dark:bg-gray-700 animate-pulse" />
              ))}
            </div>
          ) : stories.length === 0 ? (
            <div className="rounded-xl border-2 border-dashed border-gray-200 dark:border-gray-700 p-8 text-center text-gray-400 dark:text-gray-500">
              No stories yet. Start writing via Claude!
            </div>
          ) : (
            <div className="space-y-3">
              {stories.map(s => <StoryCard key={s.id} story={s} />)}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
