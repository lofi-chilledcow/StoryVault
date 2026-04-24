import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { vi } from 'vitest'
import JournalCard from '../components/JournalCard'
import type { Journal } from '../types'

const baseJournal: Journal = {
  id: 'j-1',
  title: 'My Tech Journal',
  content: 'Today I learned about FastAPI and resilient patterns in distributed systems.',
  category: 'tech',
  vocab_words: ['resilient', 'distributed'],
  score: 85,
  created_at: '2026-04-19 10:00:00',
}

function renderCard(props: Partial<Parameters<typeof JournalCard>[0]> = {}) {
  return render(
    <MemoryRouter>
      <JournalCard journal={baseJournal} {...props} />
    </MemoryRouter>
  )
}

describe('JournalCard', () => {
  it('renders title and content', () => {
    renderCard()
    expect(screen.getByText('My Tech Journal')).toBeInTheDocument()
    expect(screen.getByText(/FastAPI/)).toBeInTheDocument()
  })

  it('renders category badge', () => {
    renderCard()
    expect(screen.getByText('tech')).toBeInTheDocument()
  })

  it('renders vocab_words as pills', () => {
    renderCard()
    expect(screen.getByText('resilient')).toBeInTheDocument()
    expect(screen.getByText('distributed')).toBeInTheDocument()
  })

  it('renders score badge when score is present', () => {
    renderCard()
    expect(screen.getByText('Score: 85')).toBeInTheDocument()
  })

  it('does not render score badge when score is null', () => {
    renderCard({ journal: { ...baseJournal, score: null } })
    expect(screen.queryByText(/Score:/)).not.toBeInTheDocument()
  })

  it('does not render delete button when onDelete is not provided', () => {
    renderCard()
    expect(screen.queryByText('Delete')).not.toBeInTheDocument()
  })

  it('calls onDelete with journal id when delete button clicked', () => {
    const onDelete = vi.fn()
    renderCard({ onDelete })
    fireEvent.click(screen.getByText('Delete'))
    expect(onDelete).toHaveBeenCalledWith('j-1')
  })

  it('renders the formatted date', () => {
    renderCard()
    expect(screen.getByText(/Written/)).toBeInTheDocument()
    expect(screen.getByText(/Apr 19, 2026/)).toBeInTheDocument()
  })
})
