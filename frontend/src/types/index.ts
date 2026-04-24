export interface Journal {
  id: string
  title: string
  content: string
  category: 'tech' | 'work' | 'life' | 'fun'
  vocab_words: string[]
  score: number | null
  created_at: string
}

export interface JournalCreate {
  title: string
  content: string
  category: string
  vocab_words: string[]
  score?: number
  created_at: string
}

export interface Story {
  id: string
  title: string
  content: string
  category: 'tech' | 'work' | 'life' | 'fun'
  themes: string[]
  created_at: string
}

export interface StoryCreate {
  title: string
  content: string
  category: string
  themes: string[]
  created_at: string
}

export interface Stats {
  total_journals: number
  total_stories: number
  streak_days: number
  words_used: string[]
}
