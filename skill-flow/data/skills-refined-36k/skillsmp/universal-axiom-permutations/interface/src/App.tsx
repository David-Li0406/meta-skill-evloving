import { useEffect, useState } from 'react'
import { MainDashboard } from './components/dashboard/MainDashboard'
import { MainMenu } from './components/menu/MainMenu'
import { AiBenchmarkingModule } from './components/benchmarking/AiBenchmarkingModule'
import { MathSolutionsModule } from './components/solutions/MathSolutionsModule'
import './index.css'

type AppView = 'menu' | 'dashboard' | 'benchmarking' | 'math-solutions'
type ThemeMode = 'dark' | 'light'

const getInitialTheme = (): ThemeMode => {
  if (typeof window === 'undefined') {
    return 'dark'
  }

  const storedTheme = window.localStorage.getItem('theme')
  if (storedTheme === 'light' || storedTheme === 'dark') {
    return storedTheme
  }

  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'
}

function App() {
  const [view, setView] = useState<AppView>('menu')
  const [theme, setTheme] = useState<ThemeMode>(getInitialTheme)

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    window.localStorage.setItem('theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme((currentTheme) => (currentTheme === 'light' ? 'dark' : 'light'))
  }

  return (
    <div className="app">
      <button
        type="button"
        className="theme-toggle"
        onClick={toggleTheme}
        aria-pressed={theme === 'light'}
        aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      >
        {theme === 'light' ? 'Dark mode' : 'Light mode'}
      </button>
      {view === 'dashboard' && <MainDashboard onBackToMenu={() => setView('menu')} />}
      {view === 'benchmarking' && <AiBenchmarkingModule onBackToMenu={() => setView('menu')} />}
      {view === 'math-solutions' && <MathSolutionsModule onBackToMenu={() => setView('menu')} />}
      {view === 'menu' && (
        <MainMenu
          onSelectDashboard={() => setView('dashboard')}
          onSelectBenchmarking={() => setView('benchmarking')}
          onSelectMathSolutions={() => setView('math-solutions')}
        />
      )}
    </div>
  )
}

export default App
