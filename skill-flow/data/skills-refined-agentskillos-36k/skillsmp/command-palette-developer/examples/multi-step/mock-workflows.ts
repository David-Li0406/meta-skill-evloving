import {
  GitBranch,
  Rocket,
  Settings,
  Users,
  FileText,
  GitPullRequest,
  Archive,
  Trash2,
  Copy,
  Check,
  X,
} from 'lucide-react';
import type { Command } from './useCommandFlow';

/**
 * Mock 3-level command hierarchy for demonstration
 *
 * Level 0: Select Repository (5 repos)
 * Level 1: Choose Action (10 actions per repo)
 * Level 2: Confirm or Select Branch (context-aware)
 */

export interface CommandTree {
  repositories: Command[];
}

// Level 2 confirmation commands
const createConfirmationCommands = (
  actionName: string,
  onConfirm: () => void
): Command[] => [
  {
    id: `confirm-${actionName}`,
    name: 'Confirm',
    description: `Execute ${actionName}`,
    icon: Check,
    action: onConfirm,
  },
  {
    id: `cancel-${actionName}`,
    name: 'Cancel',
    description: 'Go back',
    icon: X,
    action: () => console.log('Cancelled'),
  },
];

// Level 2 branch selection commands
const createBranchCommands = (repoName: string): Command[] => [
  {
    id: `${repoName}-main`,
    name: 'main',
    description: 'Main production branch',
    icon: GitBranch,
    action: () => console.log(`Switched to main in ${repoName}`),
  },
  {
    id: `${repoName}-develop`,
    name: 'develop',
    description: 'Development branch',
    icon: GitBranch,
    action: () => console.log(`Switched to develop in ${repoName}`),
  },
  {
    id: `${repoName}-feature-auth`,
    name: 'feature/auth',
    description: 'Authentication feature',
    icon: GitBranch,
    action: () => console.log(`Switched to feature/auth in ${repoName}`),
  },
  {
    id: `${repoName}-hotfix`,
    name: 'hotfix/security',
    description: 'Security hotfix',
    icon: GitBranch,
    action: () => console.log(`Switched to hotfix/security in ${repoName}`),
  },
];

// Level 1 actions for each repository
const createRepositoryActions = (repoName: string): Command[] => [
  {
    id: `${repoName}-deploy`,
    name: 'Deploy',
    description: 'Deploy to production',
    icon: Rocket,
    nextLevel: createConfirmationCommands(
      'Deploy to production',
      () => console.log(`Deploying ${repoName}...`)
    ),
  },
  {
    id: `${repoName}-branches`,
    name: 'Switch Branch',
    description: 'Change active branch',
    icon: GitBranch,
    nextLevel: createBranchCommands(repoName),
  },
  {
    id: `${repoName}-pull-request`,
    name: 'Create Pull Request',
    description: 'Open new PR',
    icon: GitPullRequest,
    action: () => console.log(`Creating PR in ${repoName}`),
  },
  {
    id: `${repoName}-settings`,
    name: 'Repository Settings',
    description: 'Manage repo configuration',
    icon: Settings,
    action: () => console.log(`Opening settings for ${repoName}`),
  },
  {
    id: `${repoName}-collaborators`,
    name: 'Manage Collaborators',
    description: 'Add or remove team members',
    icon: Users,
    action: () => console.log(`Managing collaborators for ${repoName}`),
  },
  {
    id: `${repoName}-readme`,
    name: 'Edit README',
    description: 'Update repository documentation',
    icon: FileText,
    action: () => console.log(`Editing README for ${repoName}`),
  },
  {
    id: `${repoName}-archive`,
    name: 'Archive Repository',
    description: 'Make repository read-only',
    icon: Archive,
    nextLevel: createConfirmationCommands(
      'Archive repository',
      () => console.log(`Archiving ${repoName}...`)
    ),
  },
  {
    id: `${repoName}-clone`,
    name: 'Clone Repository',
    description: 'Copy to local machine',
    icon: Copy,
    action: () => console.log(`Cloning ${repoName}...`),
  },
  {
    id: `${repoName}-delete`,
    name: 'Delete Repository',
    description: 'Permanently remove repository',
    icon: Trash2,
    nextLevel: createConfirmationCommands(
      'Delete repository (DANGER)',
      () => console.log(`Deleting ${repoName}...`)
    ),
  },
  {
    id: `${repoName}-view`,
    name: 'View Repository',
    description: 'Open repository page',
    icon: FileText,
    action: () => console.log(`Viewing ${repoName}`),
  },
];

// Level 0: Repository list
export const workflowTree: CommandTree = {
  repositories: [
    {
      id: 'repo-web-app',
      name: 'web-app',
      description: 'Main web application (React + TypeScript)',
      icon: FileText,
      nextLevel: createRepositoryActions('web-app'),
    },
    {
      id: 'repo-api-server',
      name: 'api-server',
      description: 'Backend API service (Node.js + Express)',
      icon: Rocket,
      nextLevel: createRepositoryActions('api-server'),
    },
    {
      id: 'repo-mobile-app',
      name: 'mobile-app',
      description: 'iOS and Android app (React Native)',
      icon: FileText,
      nextLevel: createRepositoryActions('mobile-app'),
    },
    {
      id: 'repo-design-system',
      name: 'design-system',
      description: 'Shared component library',
      icon: Copy,
      nextLevel: createRepositoryActions('design-system'),
    },
    {
      id: 'repo-documentation',
      name: 'documentation',
      description: 'Product and API docs',
      icon: FileText,
      nextLevel: createRepositoryActions('documentation'),
    },
  ],
};
