import { useNavigate } from 'react-router-dom'
import type { Story } from '../types'

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

interface Props {
  story: Story
  onDelete?: (id: string) => void
}

export default function StoryCard({ story, onDelete }: Props) {
  const navigate = useNavigate()

  return (
    <div
      onClick={() => navigate(`/stories/${story.id}`)}
      className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 shadow-sm flex flex-col gap-3 cursor-pointer hover:border-indigo-400 dark:hover:border-indigo-500 hover:shadow-md transition-all"
    >
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-gray-900 dark:text-white text-base leading-snug">
          {story.title}
        </h3>
        <span className={`shrink-0 text-xs font-medium px-2 py-0.5 rounded-full ${categoryColors[story.category] ?? 'bg-gray-100 text-gray-600'}`}>
          {story.category}
        </span>
      </div>

      <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 leading-relaxed">
        {story.content}
      </p>

      {story.themes.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {story.themes.map(theme => (
            <span
              key={theme}
              className="text-xs bg-violet-50 text-violet-600 dark:bg-violet-900/30 dark:text-violet-300 px-2 py-0.5 rounded-full"
            >
              {theme}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between mt-auto pt-1">
        <span className="text-xs text-gray-400 dark:text-gray-500">
          Written {fmtDate(story.created_at)}
        </span>

        {onDelete && (
          <button
            onClick={e => { e.stopPropagation(); onDelete(story.id) }}
            className="text-xs text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 transition-colors"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  )
}
