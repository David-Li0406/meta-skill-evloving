import React, { useState } from 'react';
import { useCodeMapStore } from '../stores/codemapStore';
import { Icon } from './icons';
import { TreeView } from './TreeView';
import GraphView from './GraphView';
import NodeDetails from './NodeDetails';
import { Button } from './ui/Button';
// import { Input } from './ui/Input';
import { Alert } from './ui/Alert';
import { EmptyState } from './ui/EmptyState';
import { LoadingSpinner } from './icons';
import { ProgressBar } from './ui/Loading';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from './ui/Dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@components/ui/Select';
import { ModelTier } from 'codemap';
import { cn } from '@components/ui';

const MainPanel: React.FC = () => {
  const {
    currentCodeMap,
    isLoading,
    error,
    viewMode,
    selectedNodeId,
    setSelectedNodeId,
    panelLayout,
    createCodeMap,
    showCreateDialog,
    setShowCreateDialog,
    initialPrompt,
    setInitialPrompt,
  } = useCodeMapStore();

  const [prompt, setPrompt] = useState('');
  const [modelTier, setModelTier] = useState<ModelTier>(ModelTier.Fast);
  const [progress, setProgress] = useState(0);

  React.useEffect(() => {
    if (!showCreateDialog && initialPrompt) {
      setInitialPrompt('');
      setPrompt('');
    }
  }, [showCreateDialog, initialPrompt, setInitialPrompt]);

  React.useEffect(() => {
    if (initialPrompt && showCreateDialog) {
      setPrompt(initialPrompt);
    }
  }, [initialPrompt, showCreateDialog]);

  const handleNodeClick = (node: any) => {
    setSelectedNodeId('node_id' in node ? node.node_id : node.id);
  };

  const handleCreate = async () => {
    if (!prompt.trim()) return;

    const projectRoot = '/Users/dengwenyu/.pi/agent/skills/codemap';

    try {
      for (let i = 0; i <= 100; i += 10) {
        setProgress(i);
        await new Promise((res) => setTimeout(res, 200));
      }

      await createCodeMap(prompt, [], projectRoot, modelTier);
      setShowCreateDialog(false);
      setProgress(0);
    } catch (err) {
      console.error('Failed to create codemap:', err);
      setProgress(0);
    }
  };

  return (
    <>
      {!currentCodeMap && !isLoading && !error && (
        <div className="flex-1 flex items-center justify-center p-8">
          <EmptyState
            icon="Map"
            title="No CodeMap Generated"
            description="Generate a visual map to understand your code execution flow"
            actionLabel="Create CodeMap"
            onAction={() => setShowCreateDialog(true)}
          />
        </div>
      )}

      {isLoading && (
        <div className="flex-1 flex flex-col items-center justify-center p-8">
          <LoadingSpinner size={48} className="mx-auto mb-4 text-primary animate-spin" />
          <h2 className="text-xl font-semibold mb-2">Generating CodeMap</h2>
          <p className="text-sm text-muted-foreground">
            {viewMode === 'tree' ? 'Building tree structure...' : 'Creating network graph...'}
          </p>
          <ProgressBar value={progress} showLabel size="lg" className="max-w-md" />
        </div>
      )}

      {error && (
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="max-w-lg w-full">
            <Alert variant="destructive" title="Generation Failed">
              <p className="mb-4">{error}</p>
              <div className="flex gap-2">
                <Button variant="outline" onClick={() => setShowCreateDialog(true)}>
                  <Icon.Plus size={16} className="mr-2" />
                  Try Again
                </Button>
              </div>
            </Alert>
          </div>
        </div>
      )}

      {currentCodeMap && (
        <div className="flex-1 flex overflow-hidden">
          <div
            className={cn(
              'flex-1 overflow-auto',
              panelLayout.showDetails && 'border-r border-border'
            )}
          >
            {viewMode === 'tree' ? (
              <TreeView
                nodes={currentCodeMap?.nodes || []}
                selectedNodeId={selectedNodeId || undefined}
                onNodeClick={handleNodeClick}
              />
            ) : (
              <GraphView />
            )}
          </div>

          {panelLayout.showDetails && selectedNodeId && (
            <div
              style={{ width: panelLayout.detailsWidth }}
              className="border-l border-border bg-card flex flex-col"
            >
              <NodeDetails />
            </div>
          )}
        </div>
      )}

      <CreateCodeMapDialog
        open={showCreateDialog}
        onOpenChange={setShowCreateDialog}
        prompt={prompt}
        onPromptChange={setPrompt}
        modelTier={modelTier}
        onModelTierChange={setModelTier}
        onCreate={handleCreate}
      />
    </>
  );
};

interface CreateCodeMapDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  prompt: string;
  onPromptChange: (prompt: string) => void;
  modelTier: ModelTier;
  onModelTierChange: (tier: ModelTier) => void;
  onCreate: () => void;
}

const CreateCodeMapDialog: React.FC<CreateCodeMapDialogProps> = ({
  open,
  onOpenChange,
  prompt,
  onPromptChange,
  modelTier,
  onModelTierChange,
  onCreate,
}) => {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create New CodeMap</DialogTitle>
          <DialogDescription>
            Describe the code flow or component you want to visualize
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          <div className="space-y-2">
            <label htmlFor="prompt" className="text-sm font-medium">
              What do you want to understand?
            </label>
            <textarea
              id="prompt"
              placeholder="e.g., 'Trace the user authentication flow from login to token issuance'"
              value={prompt}
              onChange={(e) => onPromptChange(e.target.value)}
              className="flex min-h-24 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none"
            />
            <p className="text-xs text-muted-foreground">
              Be specific about the flow or component you want to explore
            </p>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Analysis Mode</label>
            <Select
              value={modelTier}
              onValueChange={(v: string) => onModelTierChange(v as ModelTier)}
            >
              <SelectTrigger>
                <SelectValue>{modelTier === ModelTier.Fast ? 'Fast' : 'Smart'}</SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ModelTier.Fast}>
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 mt-0.5">
                      <Icon.Zap size={18} />
                    </div>
                    <div>
                      <div className="font-medium">Fast</div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        Quick analysis (~20s), moderate detail
                      </div>
                    </div>
                  </div>
                </SelectItem>
                <SelectItem value={ModelTier.Smart}>
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 mt-0.5">
                      <Icon.Brain size={18} />
                    </div>
                    <div>
                      <div className="font-medium">Smart</div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        Deep analysis (~60s), comprehensive detail
                      </div>
                    </div>
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="flex justify-end gap-3">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={false}>
            Cancel
          </Button>
          <Button onClick={onCreate} disabled={!prompt.trim()}>
            <Icon.Plus size={16} className="mr-2" />
            Generate CodeMap
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default MainPanel;
