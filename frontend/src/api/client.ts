import axios from 'axios'
import type { JournalCreate, StoryCreate } from '../types'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

export const getJournals = (category?: string) =>
  client.get('/api/journals', { params: category ? { category } : undefined })

export const getJournal = (id: string) =>
  client.get(`/api/journals/${id}`)

export const createJournal = (data: JournalCreate) =>
  client.post('/api/journals', data)

export const getStories = (category?: string, themes?: string) =>
  client.get('/api/stories', {
    params: {
      ...(category ? { category } : {}),
      ...(themes ? { themes } : {}),
    },
  })

export const getStory = (id: string) =>
  client.get(`/api/stories/${id}`)

export const createStory = (data: StoryCreate) =>
  client.post('/api/stories', data)

export const getStats = () => {
  const now = new Date()
  const date = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
  return client.get('/api/stats', { params: { date } })
}

export default client
