import React, { useEffect, useState } from 'react';
import { useCodeMapStore } from '@stores/codemapStore';
import { ErrorBoundary } from '@components/ErrorBoundary';
import { ThemeToggle } from '@components/theme/ThemeToggle';
import Sidebar from '@components/Sidebar';
import MainPanel from '@components/MainPanel';
import CodeBrowser from '@components/CodeBrowser';
import { IntegratedCodePanel } from '@components/IntegratedCodePanel';
import { Icon } from '@components/icons';
import { Button } from '@components/ui/Button';

type ViewMode = 'codemap' | 'codebrowser';

const App: React.FC = () => {
  const { loadHistory, loadSuggestedTopics, showCodePanel } = useCodeMapStore();
  const [viewMode, setViewMode] = useState<ViewMode>('codemap');

  useEffect(() => {
    loadHistory();
    loadSuggestedTopics();
  }, [loadHistory, loadSuggestedTopics]);

  return (
    <ErrorBoundary>
      <div className="h-screen flex flex-col bg-background">
        <header className="flex items-center justify-between px-4 py-3 border-b border-border bg-card/95 backdrop-blur-sm">
          <div className="flex items-center gap-2">
            <Icon.Map size={20} className="text-primary" />
            <h1 className="text-lg font-semibold text-foreground">CodeMap</h1>
          </div>

          <div className="flex items-center gap-2">
            <ThemeToggle />
            <div className="w-px h-6 bg-border mx-1" />
            <Button
              variant={viewMode === 'codemap' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('codemap')}
            >
              <Icon.Map size={16} className="mr-2" />
              CodeMap
            </Button>
            <Button
              variant={viewMode === 'codebrowser' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('codebrowser')}
            >
              <Icon.FileText size={16} className="mr-2" />
              Code Browser
            </Button>
          </div>
        </header>

        {viewMode === 'codemap' ? (
          <div className="flex-1 flex overflow-hidden">
            <Sidebar />
            <MainPanel />
            {showCodePanel && <IntegratedCodePanel />}
          </div>
        ) : (
          <CodeBrowser />
        )}
      </div>
    </ErrorBoundary>
  );
};

export default App;
