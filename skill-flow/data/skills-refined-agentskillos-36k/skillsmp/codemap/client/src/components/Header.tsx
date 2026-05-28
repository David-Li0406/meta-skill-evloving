import React, { useState } from 'react';
import { useCodeMapStore } from '@stores/codemapStore';
import { Icon } from '@components/icons';
import { ModelTier, ViewMode } from 'codemap';
import { Button } from '@components/ui/Button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@components/ui/Select';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@components/ui/Dialog';
import { Separator } from '@components/ui/Separator';

const Header: React.FC = () => {
  const { currentCodeMap, viewMode, setViewMode } = useCodeMapStore();
  const [showExportDialog, setShowExportDialog] = useState(false);
  const [showHelpDialog, setShowHelpDialog] = useState(false);

  const handleExport = async (format: 'json' | 'markdown' | 'html') => {
    try {
      if (!currentCodeMap) return;

      const projectRoot = await window.__TAURI__.core.invoke('get_project_root');
      const exportPath = await window.__TAURI__.core.invoke('export_codemap', {
        id: currentCodeMap.codemap_id,
        format: format,
        projectRoot: projectRoot,
      });

      alert(`Exported to: ${exportPath}`);
      setShowExportDialog(false);
    } catch (error) {
      console.error('Failed to export:', error);
      alert('Failed to export codemap');
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Icon.Logo size={24} className="text-primary" />
            <h1 className="text-lg font-semibold tracking-tight">CodeMap</h1>
          </div>

          {currentCodeMap && (
            <>
              <Separator orientation="vertical" className="h-6" />
              <span className="text-sm text-muted-foreground">{currentCodeMap.title}</span>
            </>
          )}
        </div>

        {currentCodeMap && (
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs text-muted-foreground font-medium">Model</span>
              <Select value={currentCodeMap?.generation?.model_tier || ModelTier.Fast}>
                <SelectTrigger className="h-8 w-28 text-xs">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ModelTier.Fast}>
                    <div className="flex items-center gap-2">
                      <Icon.Zap size={12} />
                      <span>Fast</span>
                    </div>
                  </SelectItem>
                  <SelectItem value={ModelTier.Smart}>
                    <div className="flex items-center gap-2">
                      <Icon.Brain size={12} />
                      <span>Smart</span>
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="inline-flex items-center justify-center rounded-lg bg-muted p-1">
              <Button
                variant={viewMode === ViewMode.Tree ? 'default' : 'ghost'}
                size="sm"
                className="h-7 text-xs"
                onClick={() => setViewMode(ViewMode.Tree)}
              >
                <Icon.Layers size={14} className="mr-1.5" />
                Tree
              </Button>
              <Button
                variant={viewMode === ViewMode.Graph ? 'default' : 'ghost'}
                size="sm"
                className="h-7 text-xs"
                onClick={() => setViewMode(ViewMode.Graph)}
              >
                <Icon.Network size={14} className="mr-1.5" />
                Graph
              </Button>
            </div>
          </div>
        )}

        <div className="flex items-center gap-1">
          {!currentCodeMap && <NewCodeMapButton />}

          {currentCodeMap && (
            <>
              <Button
                variant="ghost"
                size="icon"
                className="h-9 w-9"
                onClick={() => setShowExportDialog(true)}
                aria-label="Export"
              >
                <Icon.Download size={16} />
              </Button>
              <Separator orientation="vertical" className="h-6" />
            </>
          )}

          <Button
            variant="ghost"
            size="icon"
            className="h-9 w-9"
            onClick={() => setShowHelpDialog(true)}
            aria-label="Help"
          >
            <Icon.HelpCircle size={16} />
          </Button>
        </div>
      </div>

      <Dialog open={showExportDialog} onOpenChange={setShowExportDialog}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Export CodeMap</DialogTitle>
            <DialogDescription>Choose the format to export your CodeMap data</DialogDescription>
          </DialogHeader>
          <div className="space-y-2">
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => handleExport('json')}
            >
              <Icon.FileCode size={16} className="mr-2" />
              Export as JSON
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => handleExport('markdown')}
            >
              <Icon.FileText size={16} className="mr-2" />
              Export as Markdown
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => handleExport('html')}
            >
              <Icon.File size={16} className="mr-2" />
              Export as HTML
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={showHelpDialog} onOpenChange={setShowHelpDialog}>
        <DialogContent className="sm:max-w-2xl">
          <DialogHeader>
            <DialogTitle>Help & Documentation</DialogTitle>
            <DialogDescription>Get started with CodeMap</DialogDescription>
          </DialogHeader>
          <div className="space-y-6">
            <section>
              <h4 className="font-semibold mb-2 text-sm">Getting Started</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                1. Click "New CodeMap" to create a new code map
                <br />
                2. Enter a prompt describing what you want to understand
                <br />
                3. Select the analysis mode (Fast or Smart)
                <br />
                4. Click "Generate CodeMap" to analyze your code
              </p>
            </section>

            <section>
              <h4 className="font-semibold mb-2 text-sm">Keyboard Shortcuts</h4>
              <div className="grid gap-2 text-sm text-muted-foreground">
                <div className="flex items-center justify-between">
                  <span>Open create dialog</span>
                  <kbd className="px-2 py-1 text-xs font-semibold bg-muted rounded-md">
                    Cmd/Ctrl + K
                  </kbd>
                </div>
                <div className="flex items-center justify-between">
                  <span>Close dialogs</span>
                  <kbd className="px-2 py-1 text-xs font-semibold bg-muted rounded-md">Esc</kbd>
                </div>
                <div className="flex items-center justify-between">
                  <span>Toggle help</span>
                  <kbd className="px-2 py-1 text-xs font-semibold bg-muted rounded-md">
                    Cmd/Ctrl + /
                  </kbd>
                </div>
              </div>
            </section>

            <section>
              <h4 className="font-semibold mb-2 text-sm">Tips</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                - Use specific prompts for better results
                <br />
                - Switch between Tree and Graph views for different perspectives
                <br />
                - Click on nodes to see detailed information
                <br />- Export your code maps to share with your team
              </p>
            </section>
          </div>
        </DialogContent>
      </Dialog>
    </header>
  );
};

const NewCodeMapButton: React.FC = () => {
  return (
    <Button size="sm">
      <Icon.Plus size={16} className="mr-2" />
      New CodeMap
    </Button>
  );
};

export default Header;
