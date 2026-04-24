import { render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import StatsBar from '../components/StatsBar'

// Mock the API client module
vi.mock('../api/client', () => ({
  getStats: vi.fn(),
}))

import { getStats } from '../api/client'

const mockStats = {
  total_journals: 5,
  total_stories: 3,
  streak_days: 2,
  words_used: ['resilient', 'deliberate', 'focus'],
}

describe('StatsBar', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows loading skeleton initially', () => {
    // Never resolves so we stay in loading state
    vi.mocked(getStats).mockReturnValue(new Promise(() => {}))
    const { container } = render(<StatsBar />)
    const pulseBoxes = container.querySelectorAll('.animate-pulse')
    expect(pulseBoxes).toHaveLength(4)
  })

  it('renders 4 stat cards after fetch resolves', async () => {
    vi.mocked(getStats).mockResolvedValue({ data: mockStats } as any)
    render(<StatsBar />)

    await waitFor(() => {
      expect(screen.getByText('Total Journals')).toBeInTheDocument()
      expect(screen.getByText('Total Stories')).toBeInTheDocument()
      expect(screen.getByText('Streak 🔥')).toBeInTheDocument()
      expect(screen.getByText('Words Used')).toBeInTheDocument()
    })
  })

  it('displays correct stat values after fetch resolves', async () => {
    vi.mocked(getStats).mockResolvedValue({ data: mockStats } as any)
    render(<StatsBar />)

    await waitFor(() => {
      expect(screen.getByText('5')).toBeInTheDocument()      // total_journals (unique)
      expect(screen.getByText('2 days')).toBeInTheDocument() // streak_days (unique)
      // total_stories and words_used.length are both 3 — check both appear
      expect(screen.getAllByText('3')).toHaveLength(2)
    })
  })
})
