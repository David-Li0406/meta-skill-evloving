/**
 * Unified Command Palette Example
 *
 * Demonstrates how to use all result type components together in a single
 * command palette with tab-based filtering and mixed result types.
 *
 * This example shows:
 * - Tab-based filtering (All, Actions, Files, People, Navigation)
 * - Mixed result types in a single list
 * - Keyboard navigation across different result types
 * - Search with fuzzy matching
 * - Recent items tracking
 */

import * as React from 'react';
import { Command } from 'cmdk';
import {
  PersonResult,
  FileResult,
  ActionResult,
  CardResult,
  NavigationResult,
  PersonResultSkeleton,
  FileResultSkeleton,
  ActionResultSkeleton,
} from './index';
import {
  Search,
  Save,
  Trash2,
  Settings,
  Home,
  FileText,
  Users,
} from 'lucide-react';

// Sample data types
interface Person {
  id: string;
  name: string;
  role: string;
  avatar?: string;
  status?: 'online' | 'offline' | 'away';
  metadata?: {
    email?: string;
    department?: string;
    location?: string;
  };
}

interface File {
  id: string;
  name: string;
  path: string;
  type: string;
  size: number;
  modified: Date;
  thumbnail?: string;
}

interface Action {
  id: string;
  icon: typeof Save;
  name: string;
  description: string;
  shortcut?: string;
  disabled?: boolean;
  destructive?: boolean;
  onExecute: () => void;
}

interface Route {
  id: string;
  icon?: typeof Home;
  name: string;
  path: string;
  section?: string;
  recent?: boolean;
  external?: boolean;
}

interface Card {
  id: string;
  image: string;
  title: string;
  description: string;
  tags: string[];
  starred?: boolean;
  author?: {
    name: string;
    avatar?: string;
  };
}

type ResultType = 'person' | 'file' | 'action' | 'route' | 'card';
type TabType = 'all' | 'actions' | 'files' | 'people' | 'navigation' | 'cards';

interface UnifiedResult {
  type: ResultType;
  data: Person | File | Action | Route | Card;
  keywords: string[]; // For fuzzy search
}

// Sample data
const samplePeople: Person[] = [
  {
    id: 'p1',
    name: 'Sarah Chen',
    role: 'Senior Engineer',
    avatar: '/avatars/sarah.jpg',
    status: 'online',
    metadata: {
      email: 'sarah@company.com',
      department: 'Engineering',
      location: 'San Francisco',
    },
  },
  {
    id: 'p2',
    name: 'Alex Johnson',
    role: 'Product Manager',
    status: 'away',
    metadata: {
      email: 'alex@company.com',
      department: 'Product',
    },
  },
];

const sampleFiles: File[] = [
  {
    id: 'f1',
    name: 'UserService.ts',
    path: '/src/services/user/UserService.ts',
    type: 'ts',
    size: 12458,
    modified: new Date('2025-01-13T10:30:00'),
  },
  {
    id: 'f2',
    name: 'Dashboard.tsx',
    path: '/src/components/Dashboard.tsx',
    type: 'tsx',
    size: 8934,
    modified: new Date('2025-01-13T09:15:00'),
  },
];

const sampleActions: Action[] = [
  {
    id: 'a1',
    icon: Save,
    name: 'Save Document',
    description: 'Save current changes to file',
    shortcut: 'Cmd+S',
    onExecute: () => console.log('Save executed'),
  },
  {
    id: 'a2',
    icon: Trash2,
    name: 'Delete Project',
    description: 'Permanently delete this project',
    shortcut: 'Cmd+Shift+D',
    destructive: true,
    onExecute: () => console.log('Delete executed'),
  },
  {
    id: 'a3',
    icon: Settings,
    name: 'Open Settings',
    description: 'Configure application preferences',
    shortcut: 'Cmd+,',
    onExecute: () => console.log('Settings opened'),
  },
];

const sampleRoutes: Route[] = [
  {
    id: 'r1',
    icon: Home,
    name: 'Dashboard',
    path: '/app/dashboard',
    section: 'Main',
    recent: true,
  },
  {
    id: 'r2',
    icon: Users,
    name: 'Team Members',
    path: '/app/team/members',
    section: 'Team',
  },
  {
    id: 'r3',
    icon: FileText,
    name: 'API Documentation',
    path: 'https://docs.api.com',
    section: 'Documentation',
    external: true,
  },
];

const sampleCards: Card[] = [
  {
    id: 'c1',
    image: '/thumbnails/ecommerce.jpg',
    title: 'E-commerce Dashboard',
    description:
      'Modern analytics dashboard for online stores with real-time metrics.',
    tags: ['React', 'TypeScript', 'Analytics'],
    starred: true,
    author: {
      name: 'Alex Johnson',
      avatar: '/avatars/alex.jpg',
    },
  },
];

export function UnifiedPaletteExample() {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');
  const [activeTab, setActiveTab] = React.useState<TabType>('all');
  const [isLoading, setIsLoading] = React.useState(false);

  // Build unified results list
  const allResults: UnifiedResult[] = React.useMemo(() => {
    const results: UnifiedResult[] = [];

    // Add people
    samplePeople.forEach((person) => {
      results.push({
        type: 'person',
        data: person,
        keywords: [
          person.name,
          person.role,
          person.metadata?.email || '',
          person.metadata?.department || '',
        ],
      });
    });

    // Add files
    sampleFiles.forEach((file) => {
      results.push({
        type: 'file',
        data: file,
        keywords: [file.name, file.path, file.type],
      });
    });

    // Add actions
    sampleActions.forEach((action) => {
      results.push({
        type: 'action',
        data: action,
        keywords: [action.name, action.description],
      });
    });

    // Add routes
    sampleRoutes.forEach((route) => {
      results.push({
        type: 'route',
        data: route,
        keywords: [route.name, route.path, route.section || ''],
      });
    });

    // Add cards
    sampleCards.forEach((card) => {
      results.push({
        type: 'card',
        data: card,
        keywords: [card.title, card.description, ...card.tags],
      });
    });

    return results;
  }, []);

  // Filter results by active tab
  const filteredResults = React.useMemo(() => {
    if (activeTab === 'all') return allResults;

    const typeMap: Record<TabType, ResultType[]> = {
      all: ['person', 'file', 'action', 'route', 'card'],
      actions: ['action'],
      files: ['file'],
      people: ['person'],
      navigation: ['route'],
      cards: ['card'],
    };

    return allResults.filter((result) =>
      typeMap[activeTab].includes(result.type)
    );
  }, [allResults, activeTab]);

  // Keyboard shortcut to open palette
  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };

    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  // Handle result selection
  const handleSelect = (result: UnifiedResult) => {
    if (result.type === 'action') {
      const action = result.data as Action;
      action.onExecute();
      setOpen(false);
    } else if (result.type === 'route') {
      const route = result.data as Route;
      console.log('Navigate to:', route.path);
      setOpen(false);
    } else if (result.type === 'file') {
      const file = result.data as File;
      console.log('Open file:', file.path);
      setOpen(false);
    } else if (result.type === 'person') {
      const person = result.data as Person;
      console.log('Select person:', person.name);
      setOpen(false);
    } else if (result.type === 'card') {
      const card = result.data as Card;
      console.log('Open card:', card.title);
      setOpen(false);
    }
  };

  // Render result based on type
  const renderResult = (result: UnifiedResult, selected: boolean) => {
    switch (result.type) {
      case 'person':
        return (
          <PersonResult
            person={result.data as Person}
            selected={selected}
            onClick={() => handleSelect(result)}
          />
        );
      case 'file':
        return (
          <FileResult
            file={result.data as File}
            selected={selected}
            onClick={() => handleSelect(result)}
          />
        );
      case 'action':
        return (
          <ActionResult
            action={result.data as Action}
            selected={selected}
            onClick={() => handleSelect(result)}
          />
        );
      case 'route':
        return (
          <NavigationResult
            route={result.data as Route}
            selected={selected}
            onClick={() => handleSelect(result)}
          />
        );
      case 'card':
        return (
          <CardResult
            card={result.data as Card}
            selected={selected}
            onClick={() => handleSelect(result)}
          />
        );
    }
  };

  return (
    <>
      {/* Trigger button */}
      <button
        onClick={() => setOpen(true)}
        className="px-4 py-2 rounded-lg border border-border bg-background text-foreground hover:bg-muted"
      >
        <div className="flex items-center gap-2">
          <Search className="w-4 h-4" />
          <span>Search...</span>
          <kbd className="ml-2 px-2 py-0.5 rounded text-xs bg-muted border border-border">
            ⌘K
          </kbd>
        </div>
      </button>

      {/* Command palette dialog */}
      <Command.Dialog
        open={open}
        onOpenChange={setOpen}
        label="Unified Command Palette"
      >
        {/* Tabs */}
        <div className="flex gap-1 px-3 pt-3 border-b border-border">
          {(['all', 'actions', 'files', 'people', 'navigation'] as TabType[]).map(
            (tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-2 text-sm font-medium rounded-t-lg transition-colors ${
                  activeTab === tab
                    ? 'bg-background text-foreground border-t border-x border-border'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            )
          )}
        </div>

        {/* Search input */}
        <Command.Input
          value={search}
          onValueChange={setSearch}
          placeholder={`Search ${activeTab}...`}
          className="w-full px-4 py-3 text-sm border-b border-border focus:outline-none"
        />

        {/* Results */}
        <Command.List className="max-h-96 overflow-y-auto p-2">
          <Command.Empty className="px-4 py-8 text-center text-sm text-muted-foreground">
            No results found for "{search}"
          </Command.Empty>

          {isLoading ? (
            // Loading skeletons
            <div className="space-y-1">
              <PersonResultSkeleton />
              <FileResultSkeleton />
              <ActionResultSkeleton />
            </div>
          ) : (
            // Results grouped by type
            <>
              {activeTab === 'all' ? (
                // When showing all, group by type
                <>
                  {['action', 'file', 'person', 'route'].map((type) => {
                    const typeResults = filteredResults.filter(
                      (r) => r.type === type
                    );
                    if (typeResults.length === 0) return null;

                    return (
                      <Command.Group
                        key={type}
                        heading={type.charAt(0).toUpperCase() + type.slice(1) + 's'}
                      >
                        {typeResults.map((result) => {
                          const id =
                            (result.data as { id: string }).id || '';
                          return (
                            <Command.Item key={id} value={id}>
                              {({ selected }) => renderResult(result, selected)}
                            </Command.Item>
                          );
                        })}
                      </Command.Group>
                    );
                  })}
                </>
              ) : (
                // Single type view
                <Command.Group>
                  {filteredResults.map((result) => {
                    const id = (result.data as { id: string }).id || '';
                    return (
                      <Command.Item key={id} value={id}>
                        {({ selected }) => renderResult(result, selected)}
                      </Command.Item>
                    );
                  })}
                </Command.Group>
              )}
            </>
          )}
        </Command.List>

        {/* Footer with hint */}
        <div className="flex items-center justify-between px-4 py-2 text-xs text-muted-foreground border-t border-border">
          <div className="flex gap-4">
            <span>↑↓ Navigate</span>
            <span>↵ Select</span>
            <span>Esc Close</span>
          </div>
          <span>{filteredResults.length} results</span>
        </div>
      </Command.Dialog>
    </>
  );
}
