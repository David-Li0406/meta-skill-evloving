import { Activity } from 'react'

type Props = {
  currentRoute: string
  children: React.ReactNode
}

// Pre-render routes user is likely to navigate to
export function AppShell({ currentRoute, children }: Props) {
  return (
    <>
      {children}
      {/* Pre-render settings in background */}
      <Activity mode={currentRoute === '/settings' ? 'visible' : 'hidden'}>
        <SettingsPage />
      </Activity>
    </>
  )
}

function SettingsPage() {
  return <div>Settings content</div>
}
