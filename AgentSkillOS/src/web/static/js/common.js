/**
 * Common JavaScript utilities for Skill Orchestrator WebUI
 */

/**
 * WebSocket connection manager with auto-reconnect and heartbeat
 */
class WebSocketManager {
    constructor(options = {}) {
        this.onMessage = options.onMessage || (() => {});
        this.onConnect = options.onConnect || (() => {});
        this.onDisconnect = options.onDisconnect || (() => {});
        this.reconnectDelay = options.reconnectDelay || 2000;
        this.pingTimeout = options.pingTimeout || 30000;
        this.ws = null;
        this.connected = false;
    }

    connect() {
        if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
            return;
        }

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

        this.ws.onopen = () => {
            this.connected = true;
            this.onConnect();
        };

        this.ws.onclose = () => {
            this.connected = false;
            this.onDisconnect();
            // Auto-reconnect
            setTimeout(() => this.connect(), this.reconnectDelay);
        };

        this.ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                // Handle ping/pong internally
                if (msg.type === 'ping') {
                    this.send({ type: 'pong' });
                    return;
                }
                this.onMessage(msg);
            } catch (e) {
                console.error('Failed to parse WebSocket message:', e);
            }
        };
    }

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
            return true;
        }
        return false;
    }

    isConnected() {
        return this.connected && this.ws && this.ws.readyState === WebSocket.OPEN;
    }
}

/**
 * Format elapsed time from seconds to "M:SS" format
 * @param {number} totalSeconds - Total seconds elapsed
 * @returns {string} Formatted time string
 */
function formatElapsed(totalSeconds) {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

/**
 * Parse elapsed time string "M:SS" to seconds
 * @param {string} elapsed - Elapsed time string
 * @returns {number} Total seconds
 */
function parseElapsed(elapsed) {
    if (!elapsed) return 0;
    const parts = elapsed.split(':');
    if (parts.length !== 2) return 0;
    return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
}

/**
 * Escape HTML entities to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Get SVG icon for status
 * @param {string} status - Status string (completed, running, failed, pending, skipped)
 * @returns {string} SVG HTML string
 */
function getStatusIconSvg(status) {
    const icons = {
        completed: `<svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
        </svg>`,
        running: `<svg class="w-4 h-4 text-amber-500 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>`,
        failed: `<svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
        </svg>`,
        pending: `<svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>`,
        skipped: `<svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7"/>
        </svg>`
    };
    return icons[status] || `<svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
    </svg>`;
}

/**
 * Get text status icon (for use in SVG text elements)
 * @param {string} status - Status string
 * @returns {string} Unicode icon
 */
function getStatusIcon(status) {
    const icons = {
        completed: '\u2713',  // ✓
        running: '\u21bb',    // ↻
        failed: '\u2717',     // ✗
        pending: '\u25cb',    // ○
        skipped: '\u2192'     // →
    };
    return icons[status] || '?';
}

/**
 * Get SVG icon for log level
 * @param {string} level - Log level (info, tool, send, recv, ok, error, warn)
 * @returns {string} SVG HTML string
 */
function getLogIconSvg(level) {
    const icons = {
        info: `<svg class="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>`,
        tool: `<svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
        </svg>`,
        send: `<svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12"/>
        </svg>`,
        recv: `<svg class="w-3.5 h-3.5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 13l-5 5m0 0l-5-5m5 5V6"/>
        </svg>`,
        ok: `<svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
        </svg>`,
        error: `<svg class="w-3.5 h-3.5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>`,
        warn: `<svg class="w-3.5 h-3.5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>`
    };
    return icons[level] || `<span class="w-3.5 h-3.5 text-gray-500">\u2022</span>`;
}

/**
 * Get CSS class for node status border
 * @param {string} status - Node status
 * @returns {string} Tailwind CSS class
 */
function getNodeBorderClass(status) {
    const classes = {
        'running': 'border-yellow-500',
        'completed': 'border-green-500',
        'failed': 'border-red-500',
        'pending': 'border-gray-600',
        'skipped': 'border-gray-600'
    };
    return classes[status] || 'border-gray-600';
}

/**
 * Get CSS class for node status text
 * @param {string} status - Node status
 * @returns {string} Tailwind CSS class
 */
function getNodeTextClass(status) {
    const classes = {
        'running': 'text-yellow-400',
        'completed': 'text-green-400',
        'failed': 'text-red-400',
        'pending': 'text-gray-400',
        'skipped': 'text-gray-500'
    };
    return classes[status] || 'text-gray-400';
}

/**
 * Extended skill colors palette (16 colors)
 */
const SKILL_COLORS = [
    '#8b5cf6', '#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#ec4899', '#06b6d4', '#f97316',
    '#6366f1', '#14b8a6', '#84cc16', '#a855f7', '#f43f5e', '#0ea5e9', '#d946ef', '#10b981'
];

/**
 * Get color for skill by index
 * @param {number} index - Skill index
 * @returns {string} Hex color
 */
function getSkillColor(index) {
    return SKILL_COLORS[index % SKILL_COLORS.length];
}

/**
 * Theme Management Utilities
 */

/**
 * Get the current theme from localStorage or system preference
 * @returns {string} 'light' or 'dark'
 */
function getTheme() {
    const stored = localStorage.getItem('theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

/**
 * Set the theme and persist to localStorage
 * @param {string} theme - 'light' or 'dark'
 */
function setTheme(theme) {
    localStorage.setItem('theme', theme);
    if (theme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
}

/**
 * Toggle between light and dark themes
 * @returns {string} The new theme after toggling
 */
function toggleTheme() {
    const current = getTheme();
    const newTheme = current === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    return newTheme;
}

/**
 * Check if dark mode is currently active
 * @returns {boolean} True if dark mode is active
 */
function isDarkMode() {
    return document.documentElement.classList.contains('dark');
}

// Export for use in other modules (if using ES modules)
if (typeof window !== 'undefined') {
    window.WebSocketManager = WebSocketManager;
    window.formatElapsed = formatElapsed;
    window.parseElapsed = parseElapsed;
    window.escapeHtml = escapeHtml;
    window.getStatusIconSvg = getStatusIconSvg;
    window.getStatusIcon = getStatusIcon;
    window.getLogIconSvg = getLogIconSvg;
    window.getNodeBorderClass = getNodeBorderClass;
    window.getNodeTextClass = getNodeTextClass;
    window.SKILL_COLORS = SKILL_COLORS;
    window.getSkillColor = getSkillColor;
    window.getTheme = getTheme;
    window.setTheme = setTheme;
    window.toggleTheme = toggleTheme;
    window.isDarkMode = isDarkMode;
}
