import React, { useState } from 'react';
import { useCodeMapStore } from '@stores/codemapStore';
import { Icon } from '@components/icons';
import { Button } from '@components/ui/Button';
import { Input } from '@components/ui/Input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@components/ui/Tabs';
import { ScrollArea } from '@components/ui/ScrollArea';
import { Badge } from '@components/ui/Badge';
import { EmptyState } from '@components/ui/EmptyState';
import { HistoryEditDialog } from './HistoryEditDialog';
import { open } from '@tauri-apps/plugin-dialog';
import type { CodeMapMeta } from 'codemap';

const Sidebar: React.FC = () => {
  const {
    history,
    suggestedTopics,
    searchQuery,
    setSearchQuery,
    loadCodeMapById,
    removeFromHistory,
    updateHistory,
    exportHistory,
    importHistory,
    setShowCreateDialog,
    setInitialPrompt,
  } = useCodeMapStore();

  const [activeTab, setActiveTab] = useState<'history' | 'suggestions'>('suggestions');
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<CodeMapMeta | null>(null);
  const [isImporting, setIsImporting] = useState(false);

  const filteredHistory = history.filter(
    (item) =>
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.query.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredSuggestions = suggestedTopics.filter(
    (topic) =>
      topic.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      topic.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSuggestedTopicClick = async (topic: import('codemap').SuggestedTopic) => {
    const fullPrompt = topic.title + ': ' + topic.description;
    setInitialPrompt(fullPrompt);
    setShowCreateDialog(true);
  };

  const handleEditClick = (item: CodeMapMeta, e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedItem(item);
    setEditDialogOpen(true);
  };

  const handleDeleteClick = (item: CodeMapMeta, e: React.MouseEvent) => {
    e.stopPropagation();
    removeFromHistory(item.id);
  };

  const handleImport = async () => {
    try {
      setIsImporting(true);
      const selected = await open({
        multiple: false,
        filters: [
          {
            name: 'CodeMap',
            extensions: ['json'],
          },
        ],
      });

      if (selected && typeof selected === 'string') {
        await importHistory(selected);
      }
    } catch (error) {
      console.error('Failed to import:', error);
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <aside className="w-80 border-r border-border flex flex-col bg-card">
      <div className="p-3">
        <div className="relative">
          <Icon.Search
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
          />
          <Input
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            leftIcon="Search"
          />
        </div>
      </div>

      <Tabs
        value={activeTab}
        onValueChange={(v) => setActiveTab(v as any)}
        className="flex-1 flex flex-col"
      >
        <TabsList className="grid w-full grid-cols-2 m-0 rounded-none border-b border-border gap-0">
          <TabsTrigger value="suggestions" className="text-xs gap-1.5">
            <Icon.Star size={14} />
            Suggestions
          </TabsTrigger>
          <TabsTrigger value="history" className="text-xs gap-1.5">
            <Icon.Clock size={14} />
            History
          </TabsTrigger>
        </TabsList>

        <TabsContent value="suggestions" className="flex-1 m-0 overflow-hidden">
          <ScrollArea>
            <div className="p-3 space-y-2">
              {filteredSuggestions.length === 0 ? (
                <EmptyState
                  icon="Star"
                  title="No suggestions"
                  description={
                    searchQuery ? 'Try a different search term' : 'Start by analyzing your code'
                  }
                  variant="minimal"
                />
              ) : (
                filteredSuggestions.map((topic) => (
                  <SuggestedTopicItem
                    key={topic.id}
                    topic={topic}
                    onClick={handleSuggestedTopicClick}
                  />
                ))
              )}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="history" className="flex-1 m-0 overflow-hidden flex flex-col">
          <div className="p-2 border-b border-border">
            <Button
              variant="outline"
              size="sm"
              className="w-full"
              onClick={handleImport}
              disabled={isImporting}
            >
              {isImporting ? (
                <>
                  <Icon.Loader2 size={14} className="mr-2 animate-spin" />
                  Importing...
                </>
              ) : (
                <>
                  <Icon.Upload size={14} className="mr-2" />
                  Import
                </>
              )}
            </Button>
          </div>

          <ScrollArea>
            <div className="p-3 space-y-2">
              {filteredHistory.length === 0 ? (
                <EmptyState
                  icon="Clock"
                  title="No history"
                  description={searchQuery ? 'No matching codemaps' : 'Create your first codemap'}
                  variant="minimal"
                />
              ) : (
                filteredHistory.map((item) => (
                  <HistoryItem
                    key={item.id}
                    item={item}
                    onClick={() => loadCodeMapById(item.id)}
                    onEdit={handleEditClick}
                    onDelete={handleDeleteClick}
                  />
                ))
              )}
            </div>
          </ScrollArea>
        </TabsContent>
      </Tabs>

      <HistoryEditDialog
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
        item={selectedItem}
        onSave={updateHistory}
        onExport={exportHistory}
      />
    </aside>
  );
};

interface SuggestedTopicItemProps {
  topic: import('codemap').SuggestedTopic;
  onClick: (topic: import('codemap').SuggestedTopic) => void;
}

const SuggestedTopicItem: React.FC<SuggestedTopicItemProps> = ({ topic, onClick }) => {
  return (
    <button
      type="button"
      onClick={() => onClick(topic)}
      className="w-full text-left p-3 rounded-lg hover:bg-accent transition-colors group"
    >
      <div className="flex items-start gap-2">
        <div className="flex-shrink-0 mt-0.5 text-primary">
          {topic.icon ? <span className="text-lg">{topic.icon}</span> : <Icon.Star size={16} />}
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-medium line-clamp-2 group-hover:text-primary transition-colors">
            {topic.title}
          </h4>
          <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{topic.description}</p>
        </div>
      </div>
    </button>
  );
};

interface HistoryItemProps {
  item: import('codemap').CodeMapMeta;
  onClick: () => void;
  onEdit: (item: CodeMapMeta, e: React.MouseEvent) => void;
  onDelete: (item: CodeMapMeta, e: React.MouseEvent) => void;
}

const HistoryItem: React.FC<HistoryItemProps> = ({ item, onClick, onEdit, onDelete }) => {
  return (
    <button
      type="button"
      onClick={onClick}
      className="group relative w-full text-left p-3 rounded-lg hover:bg-accent transition-colors"
    >
      <div className="flex items-start gap-2">
        <div className="flex-shrink-0 mt-0.5 text-primary">
          <Icon.Map size={16} />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-medium line-clamp-2">{item.title}</h4>
          <p className="text-xs text-muted-foreground mt-1 line-clamp-1">{item.query}</p>
          <div className="flex items-center gap-2 mt-2 flex-wrap">
            <span className="text-xs text-muted-foreground">
              {new Date(item.created_at).toLocaleDateString()}
            </span>
            {item.tags.length > 0 && (
              <>
                <span className="text-xs text-muted-foreground">•</span>
                <div className="flex gap-1 flex-wrap">
                  {item.tags.slice(0, 2).map((tag) => (
                    <Badge key={tag} variant="secondary" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                  {item.tags.length > 2 && (
                    <Badge variant="outline" className="text-xs">
                      +{item.tags.length - 2}
                    </Badge>
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
        <button
          type="button"
          onClick={(e) => onEdit(item, e)}
          className="p-1 rounded-md hover:bg-primary/10 hover:text-primary transition-colors"
          title="Edit"
        >
          <Icon.Edit size={14} />
        </button>
        <button
          type="button"
          onClick={(e) => onDelete(item, e)}
          className="p-1 rounded-md hover:bg-destructive/10 hover:text-destructive transition-colors"
          title="Delete"
        >
          <Icon.Trash2 size={14} />
        </button>
      </div>
    </button>
  );
};

export default Sidebar;
