import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import StoryCard from '../components/StoryCard'
import type { Story } from '../types'

const baseStory: Story = {
  id: 's-1',
  title: 'How I Overcame My First Challenge',
  content: 'It was a deliberate decision to push through the adversity and find growth.',
  category: 'life',
  themes: ['challenge', 'growth'],
  created_at: '2026-04-19 11:00:00',
}

function renderCard(props: Partial<Parameters<typeof StoryCard>[0]> = {}) {
  return render(
    <MemoryRouter>
      <StoryCard story={baseStory} {...props} />
    </MemoryRouter>
  )
}

describe('StoryCard', () => {
  it('renders title and content preview', () => {
    renderCard()
    expect(screen.getByText('How I Overcame My First Challenge')).toBeInTheDocument()
    expect(screen.getByText(/deliberate/)).toBeInTheDocument()
  })

  it('renders category badge', () => {
    renderCard()
    expect(screen.getByText('life')).toBeInTheDocument()
  })

  it('renders themes as pills', () => {
    renderCard()
    expect(screen.getByText('challenge')).toBeInTheDocument()
    expect(screen.getByText('growth')).toBeInTheDocument()
  })

  it('renders the formatted date', () => {
    renderCard()
    expect(screen.getByText(/Written/)).toBeInTheDocument()
    expect(screen.getByText(/Apr 19, 2026/)).toBeInTheDocument()
  })

  it('does not render delete button when onDelete is not provided', () => {
    renderCard()
    expect(screen.queryByText('Delete')).not.toBeInTheDocument()
  })
})
