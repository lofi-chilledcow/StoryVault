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

interface Props {
  journal: Journal
  onDelete?: (id: string) => void
}

export default function JournalCard({ journal, onDelete }: Props) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 shadow-sm flex flex-col gap-3">
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-gray-900 dark:text-white text-base leading-snug">
          {journal.title}
        </h3>
        <span className={`shrink-0 text-xs font-medium px-2 py-0.5 rounded-full ${categoryColors[journal.category] ?? 'bg-gray-100 text-gray-600'}`}>
          {journal.category}
        </span>
      </div>

      <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 leading-relaxed">
        {journal.content}
      </p>

      {journal.vocab_words.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {journal.vocab_words.map(word => (
            <span
              key={word}
              className="text-xs bg-indigo-50 text-indigo-600 dark:bg-indigo-900/30 dark:text-indigo-300 px-2 py-0.5 rounded-full"
            >
              {word}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between mt-auto pt-1">
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400 dark:text-gray-500">
            Written {fmtDate(journal.created_at)}
          </span>
          {journal.score != null && (
            <span className="text-xs font-semibold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300 px-2 py-0.5 rounded-full">
              Score: {journal.score}
            </span>
          )}
        </div>

        {onDelete && (
          <button
            onClick={() => onDelete(journal.id)}
            className="text-xs text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 transition-colors"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  )
}
