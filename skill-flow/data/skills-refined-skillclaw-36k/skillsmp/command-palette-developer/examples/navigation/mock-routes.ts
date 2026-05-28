// Mock routes for navigation palette example

export interface Route {
  id: string;
  name: string;
  path: string;
  section: 'App' | 'Settings' | 'Admin' | 'Public';
  icon: string; // Emoji for simplicity
  description?: string;
  external?: boolean;
  parent?: string; // Parent route ID for breadcrumbs
}

export const mockRoutes: Route[] = [
  // App Routes - Dashboard & Core Features
  {
    id: 'app-dashboard',
    name: 'Dashboard',
    path: '/app',
    section: 'App',
    icon: '📊',
    description: 'Main application dashboard',
  },
  {
    id: 'app-analytics',
    name: 'Analytics',
    path: '/app/analytics',
    section: 'App',
    icon: '📈',
    description: 'View analytics and metrics',
    parent: 'app-dashboard',
  },
  {
    id: 'app-reports',
    name: 'Reports',
    path: '/app/reports',
    section: 'App',
    icon: '📋',
    description: 'Generate and view reports',
    parent: 'app-dashboard',
  },

  // App Routes - Users
  {
    id: 'app-users',
    name: 'Users',
    path: '/app/users',
    section: 'App',
    icon: '👥',
    description: 'User management',
  },
  {
    id: 'app-users-list',
    name: 'All Users',
    path: '/app/users/list',
    section: 'App',
    icon: '📝',
    description: 'View all users',
    parent: 'app-users',
  },
  {
    id: 'app-users-create',
    name: 'Create User',
    path: '/app/users/create',
    section: 'App',
    icon: '➕',
    description: 'Add a new user',
    parent: 'app-users',
  },
  {
    id: 'app-users-profile',
    name: 'User Profile',
    path: '/app/users/:id',
    section: 'App',
    icon: '👤',
    description: 'View user profile',
    parent: 'app-users',
  },
  {
    id: 'app-users-permissions',
    name: 'User Permissions',
    path: '/app/users/:id/permissions',
    section: 'App',
    icon: '🔐',
    description: 'Manage user permissions',
    parent: 'app-users-profile',
  },

  // App Routes - Projects
  {
    id: 'app-projects',
    name: 'Projects',
    path: '/app/projects',
    section: 'App',
    icon: '📁',
    description: 'Project management',
  },
  {
    id: 'app-projects-active',
    name: 'Active Projects',
    path: '/app/projects/active',
    section: 'App',
    icon: '✅',
    description: 'View active projects',
    parent: 'app-projects',
  },
  {
    id: 'app-projects-archived',
    name: 'Archived Projects',
    path: '/app/projects/archived',
    section: 'App',
    icon: '📦',
    description: 'View archived projects',
    parent: 'app-projects',
  },
  {
    id: 'app-projects-create',
    name: 'Create Project',
    path: '/app/projects/create',
    section: 'App',
    icon: '🆕',
    description: 'Start a new project',
    parent: 'app-projects',
  },
  {
    id: 'app-projects-detail',
    name: 'Project Details',
    path: '/app/projects/:id',
    section: 'App',
    icon: '📄',
    description: 'View project details',
    parent: 'app-projects',
  },
  {
    id: 'app-projects-tasks',
    name: 'Project Tasks',
    path: '/app/projects/:id/tasks',
    section: 'App',
    icon: '✓',
    description: 'View project tasks',
    parent: 'app-projects-detail',
  },
  {
    id: 'app-projects-team',
    name: 'Project Team',
    path: '/app/projects/:id/team',
    section: 'App',
    icon: '👨‍👩‍👧‍👦',
    description: 'Manage project team',
    parent: 'app-projects-detail',
  },

  // App Routes - Tasks
  {
    id: 'app-tasks',
    name: 'Tasks',
    path: '/app/tasks',
    section: 'App',
    icon: '☑️',
    description: 'Task management',
  },
  {
    id: 'app-tasks-mine',
    name: 'My Tasks',
    path: '/app/tasks/mine',
    section: 'App',
    icon: '👆',
    description: 'View your assigned tasks',
    parent: 'app-tasks',
  },
  {
    id: 'app-tasks-all',
    name: 'All Tasks',
    path: '/app/tasks/all',
    section: 'App',
    icon: '📋',
    description: 'View all tasks',
    parent: 'app-tasks',
  },
  {
    id: 'app-tasks-create',
    name: 'Create Task',
    path: '/app/tasks/create',
    section: 'App',
    icon: '➕',
    description: 'Create a new task',
    parent: 'app-tasks',
  },

  // App Routes - Messages & Notifications
  {
    id: 'app-messages',
    name: 'Messages',
    path: '/app/messages',
    section: 'App',
    icon: '💬',
    description: 'View messages',
  },
  {
    id: 'app-notifications',
    name: 'Notifications',
    path: '/app/notifications',
    section: 'App',
    icon: '🔔',
    description: 'View notifications',
  },
  {
    id: 'app-calendar',
    name: 'Calendar',
    path: '/app/calendar',
    section: 'App',
    icon: '📅',
    description: 'View calendar and events',
  },

  // Settings Routes
  {
    id: 'settings',
    name: 'Settings',
    path: '/settings',
    section: 'Settings',
    icon: '⚙️',
    description: 'Application settings',
  },
  {
    id: 'settings-profile',
    name: 'Profile Settings',
    path: '/settings/profile',
    section: 'Settings',
    icon: '👤',
    description: 'Edit your profile',
    parent: 'settings',
  },
  {
    id: 'settings-account',
    name: 'Account Settings',
    path: '/settings/account',
    section: 'Settings',
    icon: '🔑',
    description: 'Manage account settings',
    parent: 'settings',
  },
  {
    id: 'settings-security',
    name: 'Security',
    path: '/settings/security',
    section: 'Settings',
    icon: '🔒',
    description: 'Security and privacy settings',
    parent: 'settings',
  },
  {
    id: 'settings-notifications',
    name: 'Notification Preferences',
    path: '/settings/notifications',
    section: 'Settings',
    icon: '🔔',
    description: 'Configure notifications',
    parent: 'settings',
  },
  {
    id: 'settings-appearance',
    name: 'Appearance',
    path: '/settings/appearance',
    section: 'Settings',
    icon: '🎨',
    description: 'Customize appearance',
    parent: 'settings',
  },
  {
    id: 'settings-team',
    name: 'Team Settings',
    path: '/settings/team',
    section: 'Settings',
    icon: '👥',
    description: 'Manage team settings',
    parent: 'settings',
  },
  {
    id: 'settings-billing',
    name: 'Billing',
    path: '/settings/billing',
    section: 'Settings',
    icon: '💳',
    description: 'Billing and subscription',
    parent: 'settings',
  },
  {
    id: 'settings-integrations',
    name: 'Integrations',
    path: '/settings/integrations',
    section: 'Settings',
    icon: '🔌',
    description: 'Third-party integrations',
    parent: 'settings',
  },
  {
    id: 'settings-api',
    name: 'API Keys',
    path: '/settings/api',
    section: 'Settings',
    icon: '🔑',
    description: 'Manage API keys',
    parent: 'settings',
  },

  // Admin Routes
  {
    id: 'admin',
    name: 'Admin Panel',
    path: '/admin',
    section: 'Admin',
    icon: '🛡️',
    description: 'Administration panel',
  },
  {
    id: 'admin-users',
    name: 'Manage All Users',
    path: '/admin/users',
    section: 'Admin',
    icon: '👥',
    description: 'User administration',
    parent: 'admin',
  },
  {
    id: 'admin-roles',
    name: 'Roles & Permissions',
    path: '/admin/roles',
    section: 'Admin',
    icon: '🎭',
    description: 'Manage roles and permissions',
    parent: 'admin',
  },
  {
    id: 'admin-logs',
    name: 'System Logs',
    path: '/admin/logs',
    section: 'Admin',
    icon: '📜',
    description: 'View system logs',
    parent: 'admin',
  },
  {
    id: 'admin-audit',
    name: 'Audit Trail',
    path: '/admin/audit',
    section: 'Admin',
    icon: '🔍',
    description: 'View audit trail',
    parent: 'admin',
  },
  {
    id: 'admin-config',
    name: 'System Configuration',
    path: '/admin/config',
    section: 'Admin',
    icon: '⚙️',
    description: 'Configure system settings',
    parent: 'admin',
  },
  {
    id: 'admin-database',
    name: 'Database Management',
    path: '/admin/database',
    section: 'Admin',
    icon: '🗄️',
    description: 'Database administration',
    parent: 'admin',
  },
  {
    id: 'admin-monitoring',
    name: 'System Monitoring',
    path: '/admin/monitoring',
    section: 'Admin',
    icon: '📡',
    description: 'Monitor system health',
    parent: 'admin',
  },
  {
    id: 'admin-backups',
    name: 'Backups',
    path: '/admin/backups',
    section: 'Admin',
    icon: '💾',
    description: 'Manage system backups',
    parent: 'admin',
  },

  // Public Routes
  {
    id: 'public-home',
    name: 'Home',
    path: '/',
    section: 'Public',
    icon: '🏠',
    description: 'Public homepage',
  },
  {
    id: 'public-about',
    name: 'About',
    path: '/about',
    section: 'Public',
    icon: 'ℹ️',
    description: 'About us',
  },
  {
    id: 'public-pricing',
    name: 'Pricing',
    path: '/pricing',
    section: 'Public',
    icon: '💰',
    description: 'View pricing plans',
  },
  {
    id: 'public-features',
    name: 'Features',
    path: '/features',
    section: 'Public',
    icon: '✨',
    description: 'Product features',
  },
  {
    id: 'public-docs',
    name: 'Documentation',
    path: '/docs',
    section: 'Public',
    icon: '📖',
    description: 'Read documentation',
    external: true,
  },
  {
    id: 'public-blog',
    name: 'Blog',
    path: '/blog',
    section: 'Public',
    icon: '📝',
    description: 'Read our blog',
  },
  {
    id: 'public-contact',
    name: 'Contact',
    path: '/contact',
    section: 'Public',
    icon: '📧',
    description: 'Contact us',
  },
  {
    id: 'public-help',
    name: 'Help Center',
    path: '/help',
    section: 'Public',
    icon: '❓',
    description: 'Get help and support',
    external: true,
  },
];

/**
 * Get breadcrumb trail for a route
 */
export function getBreadcrumbs(routeId: string, routes: Route[]): Route[] {
  const breadcrumbs: Route[] = [];
  const routeMap = new Map(routes.map((r) => [r.id, r]));

  let currentRoute = routeMap.get(routeId);

  while (currentRoute) {
    breadcrumbs.unshift(currentRoute);
    currentRoute = currentRoute.parent ? routeMap.get(currentRoute.parent) : undefined;
  }

  return breadcrumbs;
}

/**
 * Get section display name with count
 */
export function getSectionLabel(section: Route['section'], routes: Route[]): string {
  const count = routes.filter((r) => r.section === section).length;
  return `${section} (${count})`;
}
