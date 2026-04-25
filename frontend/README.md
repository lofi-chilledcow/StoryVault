# StoryVault — Frontend

React + Vite + TypeScript dashboard for reading journals and stories.

## Stack

- **React 19** + **TypeScript**
- **Vite** — build tool and dev server
- **Tailwind CSS v4** — styling
- **React Router v7** — client-side routing
- **Axios** — API client
- **Vitest** + **React Testing Library** — component tests

## Project structure

```
frontend/src/
├── api/
│   └── client.ts        Axios instance + API helper functions
├── components/
│   ├── StatsBar.tsx      Writing stats (journals, stories, streak, words)
│   ├── JournalCard.tsx   Journal card with category badge + vocab pills
│   └── StoryCard.tsx     Story card, clickable → detail page
├── pages/
│   ├── Home.tsx          Dashboard: stats + latest 3 journals & stories
│   ├── Journals.tsx      Full journal list with category filter
│   ├── JournalDetail.tsx Single journal view
│   ├── Stories.tsx       Full story list with category filter
│   └── StoryDetail.tsx   Single story view
├── types/
│   └── index.ts          Shared TypeScript interfaces
└── tests/
    ├── setup.ts
    ├── StatsBar.test.tsx
    ├── JournalCard.test.tsx
    └── StoryCard.test.tsx
```

## Setup

```bash
npm install
cp .env .env.local   # or edit .env directly
npm run dev          # http://localhost:5173
```

## Environment variables

```
VITE_API_URL=http://localhost:8001
```

## Available scripts

```bash
npm run dev      # Dev server with HMR
npm run build    # Production build → dist/
npm run preview  # Preview production build
npm test         # Run Vitest component tests
```

## Routes

| Path             | Page          |
|------------------|---------------|
| `/`              | Home dashboard |
| `/journals`      | Journal list   |
| `/journals/:id`  | Journal detail |
| `/stories`       | Story list     |
| `/stories/:id`   | Story detail   |
