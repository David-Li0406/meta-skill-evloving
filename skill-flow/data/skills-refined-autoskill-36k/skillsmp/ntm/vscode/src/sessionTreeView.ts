import * as vscode from 'vscode';
import { NtmClient, SessionInfo, AgentInfo } from './ntmClient';

/**
 * Tree item representing a session or agent.
 */
class NtmTreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly itemType: 'session' | 'agent',
        public readonly data?: SessionInfo | AgentInfo
    ) {
        super(label, collapsibleState);

        if (itemType === 'session') {
            const session = data as SessionInfo;
            this.contextValue = 'session';
            this.iconPath = new vscode.ThemeIcon(session?.attached ? 'broadcast' : 'terminal');
            this.description = session?.attached ? 'attached' : 'detached';
            this.tooltip = `${session?.panes ?? 0} panes • ${session?.agents?.length ?? 0} agents`;
        } else if (itemType === 'agent') {
            const agent = data as AgentInfo;
            this.contextValue = 'agent';
            this.iconPath = new vscode.ThemeIcon(agent?.is_active ? 'debug-start' : 'debug-pause');
            this.description = agent?.variant || agent?.type;
            this.tooltip = `Pane: ${agent?.pane}`;
        }
    }
}

/**
 * Tree data provider for NTM sessions and agents.
 */
export class NtmSessionTreeProvider implements vscode.TreeDataProvider<NtmTreeItem> {
    private sessions: SessionInfo[] = [];

    private _onDidChangeTreeData = new vscode.EventEmitter<NtmTreeItem | undefined | null | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    constructor(private readonly client: NtmClient) {}

    /**
     * Refresh the tree data.
     */
    async refresh(): Promise<void> {
        try {
            const status = await this.client.getStatus();
            this.sessions = status.sessions || [];
        } catch {
            this.sessions = [];
        }
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: NtmTreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: NtmTreeItem): Thenable<NtmTreeItem[]> {
        if (!element) {
            // Root level: return sessions
            return Promise.resolve(
                this.sessions.map(session => new NtmTreeItem(
                    session.name,
                    session.agents && session.agents.length > 0
                        ? vscode.TreeItemCollapsibleState.Expanded
                        : vscode.TreeItemCollapsibleState.None,
                    'session',
                    session
                ))
            );
        } else if (element.itemType === 'session') {
            // Session level: return agents
            const session = element.data as SessionInfo;
            const agents = session.agents || [];
            return Promise.resolve(
                agents.map(agent => new NtmTreeItem(
                    agent.pane || agent.type,
                    vscode.TreeItemCollapsibleState.None,
                    'agent',
                    agent
                ))
            );
        }
        return Promise.resolve([]);
    }

    dispose(): void {
        this._onDidChangeTreeData.dispose();
    }
}

/**
 * Register the session tree view.
 */
export function registerSessionTreeView(
    context: vscode.ExtensionContext,
    client: NtmClient
): { provider: NtmSessionTreeProvider; view: vscode.TreeView<NtmTreeItem> } {
    const provider = new NtmSessionTreeProvider(client);

    const view = vscode.window.createTreeView('ntmSessions', {
        treeDataProvider: provider,
        showCollapseAll: true,
    });

    // Register refresh command
    const refreshCmd = vscode.commands.registerCommand('ntm.refreshSessions', () => {
        provider.refresh();
    });

    // Register attach command for sessions
    const attachCmd = vscode.commands.registerCommand('ntm.attachSession', (item: NtmTreeItem) => {
        if (item.itemType === 'session') {
            const session = item.data as SessionInfo;
            const terminal = vscode.window.createTerminal({ name: `NTM: ${session.name}` });
            terminal.show(true);
            terminal.sendText(`ntm attach ${session.name}`, true);
        }
    });

    // Initial refresh
    provider.refresh();

    // Refresh periodically
    const interval = setInterval(() => provider.refresh(), 10000);

    context.subscriptions.push(
        view,
        refreshCmd,
        attachCmd,
        { dispose: () => clearInterval(interval) },
        { dispose: () => provider.dispose() }
    );

    return { provider, view };
}
