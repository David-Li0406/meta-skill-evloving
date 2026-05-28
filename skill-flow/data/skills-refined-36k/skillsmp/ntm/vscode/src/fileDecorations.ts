import * as vscode from 'vscode';
import { NtmClient, MailReservation } from './ntmClient';

/**
 * FileDecorationProvider for showing NTM file reservation status in the explorer.
 * Files with active reservations show a lock badge indicating which agent holds them.
 */
export class NtmFileDecorationProvider implements vscode.FileDecorationProvider {
    private reservations: MailReservation[] = [];
    private workspaceRoot: string | undefined;

    private _onDidChangeFileDecorations = new vscode.EventEmitter<vscode.Uri | vscode.Uri[] | undefined>();
    readonly onDidChangeFileDecorations = this._onDidChangeFileDecorations.event;

    constructor(private readonly client: NtmClient) {
        this.workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    }

    /**
     * Update reservations from NTM and trigger decoration refresh.
     */
    async refresh(): Promise<void> {
        try {
            const mail = await this.client.getMail();
            this.reservations = mail.file_reservations || [];
            this._onDidChangeFileDecorations.fire(undefined); // Refresh all decorations
        } catch {
            // Mail unavailable - clear reservations
            this.reservations = [];
            this._onDidChangeFileDecorations.fire(undefined);
        }
    }

    /**
     * Provide decoration for a URI if it matches a reservation pattern.
     */
    provideFileDecoration(uri: vscode.Uri): vscode.FileDecoration | undefined {
        if (!this.workspaceRoot || this.reservations.length === 0) {
            return undefined;
        }

        // Get path relative to workspace
        const relativePath = uri.fsPath.replace(this.workspaceRoot + '/', '');

        // Check if any reservation matches this file
        for (const res of this.reservations) {
            if (this.matchesPattern(relativePath, res.pattern)) {
                return {
                    badge: res.exclusive ? '🔒' : '👁',
                    tooltip: `${res.exclusive ? 'Locked' : 'Watched'} by ${res.agent}${res.reason ? ` (${res.reason})` : ''}`,
                    color: res.exclusive
                        ? new vscode.ThemeColor('gitDecoration.modifiedResourceForeground')
                        : new vscode.ThemeColor('gitDecoration.untrackedResourceForeground'),
                };
            }
        }

        return undefined;
    }

    /**
     * Simple glob-like pattern matching.
     * Supports * (any characters) and ** (any path segments).
     */
    private matchesPattern(path: string, pattern: string): boolean {
        // Convert glob pattern to regex
        let regexPattern = pattern
            .replace(/[.+^${}()|[\]\\]/g, '\\$&')  // Escape regex special chars except * and ?
            .replace(/\*\*/g, '<<<GLOBSTAR>>>')    // Temp replace ** to avoid double processing
            .replace(/\*/g, '[^/]*')               // Single * matches within path segment
            .replace(/<<<GLOBSTAR>>>/g, '.*')      // ** matches across path segments
            .replace(/\?/g, '.');                  // ? matches single char

        regexPattern = '^' + regexPattern + '$';

        try {
            const regex = new RegExp(regexPattern);
            return regex.test(path);
        } catch {
            // Invalid pattern - try exact match
            return path === pattern;
        }
    }

    dispose(): void {
        this._onDidChangeFileDecorations.dispose();
    }
}

/**
 * Create and register the file decoration provider.
 * Returns disposable for cleanup.
 */
export function registerFileDecorations(
    context: vscode.ExtensionContext,
    client: NtmClient
): { provider: NtmFileDecorationProvider; disposable: vscode.Disposable } {
    const provider = new NtmFileDecorationProvider(client);

    // Register the decoration provider
    const disposable = vscode.window.registerFileDecorationProvider(provider);

    // Initial refresh
    provider.refresh();

    // Refresh periodically (every 10 seconds)
    const interval = setInterval(() => provider.refresh(), 10000);
    context.subscriptions.push({ dispose: () => clearInterval(interval) });

    return { provider, disposable };
}
