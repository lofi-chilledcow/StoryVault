import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Home from './pages/Home'
import Journals from './pages/Journals'
import Stories from './pages/Stories'
import StoryDetail from './pages/StoryDetail'
import JournalDetail from './pages/JournalDetail'

function Nav() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `text-sm font-medium px-3 py-1.5 rounded-lg transition-colors ${
      isActive
        ? 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-300'
        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'
    }`

  return (
    <nav className="sticky top-0 z-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <NavLink to="/" className="text-lg font-bold text-indigo-600 dark:text-indigo-400 tracking-tight">
          StoryVault
        </NavLink>
        <div className="flex items-center gap-1">
          <NavLink to="/" end className={linkClass}>Home</NavLink>
          <NavLink to="/journals" className={linkClass}>Journals</NavLink>
          <NavLink to="/stories" className={linkClass}>Stories</NavLink>
        </div>
      </div>
    </nav>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-white">
        <Nav />
        <main className="max-w-5xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/"           element={<Home />} />
            <Route path="/journals"   element={<Journals />} />
            <Route path="/stories"    element={<Stories />} />
            <Route path="/journals/:id" element={<JournalDetail />} />
            <Route path="/stories/:id" element={<StoryDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
