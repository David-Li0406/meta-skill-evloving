import type { HookEvent } from '../types';

/**
 * SwimLaneRenderer - Event Bubble Visualization
 *
 * Renders individual events as rounded rectangle bubbles positioned by exact timestamp.
 * Implements vertical stacking to prevent overlaps when events occur at similar times.
 *
 * Key differences from ChartRenderer:
 * - Individual event bubbles (not aggregated bars)
 * - Timestamp-based X positioning (not bucket-based)
 * - Vertical layout algorithm for overlap prevention
 */

export interface SwimLaneDimensions {
  width: number;
  height: number;
  padding: {
    top: number;
    right: number;
    bottom: number;
    left: number;
  };
}

export interface SwimLaneConfig {
  bubbleHeight: number;        // Height of each event bubble
  bubbleMinWidth: number;       // Minimum bubble width
  bubbleMaxWidth: number;       // Maximum bubble width
  bubbleSpacing: number;        // Minimum horizontal spacing between bubbles
  iconSize: number;             // Size of event type icon
  animationDuration: number;    // Duration of entrance animation (ms)
  colors: {
    primary: string;
    text: string;
    axis: string;
    glow: string;
  };
}

export interface EventBubble {
  event: HookEvent;
  x: number;                    // Center X position (calculated from timestamp)
  y: number;                    // Center Y position (calculated by layout algorithm)
  width: number;                // Bubble width (based on label length)
  height: number;               // Bubble height (from config)
  color: string;                // Event type color
}

export class SwimLaneRenderer {
  // Visual constants for consistent styling
  private static readonly BUBBLE_BORDER_WIDTH = 1.5;
  private static readonly BUBBLE_SHADOW_COLOR = 'rgba(0, 0, 0, 0.15)';
  private static readonly BUBBLE_SHADOW_BLUR = 4;
  private static readonly BUBBLE_SHADOW_OFFSET_Y = 2;
  private static readonly ICON_PADDING = 8;
  private static readonly LABEL_PADDING = 8;
  private static readonly SESSION_BADGE_PADDING = 8;
  private static readonly SESSION_BADGE_HEIGHT = 16;
  private static readonly SESSION_BADGE_RADIUS = 4;
  private static readonly SESSION_BADGE_RIGHT_MARGIN = 6;
  private static readonly SESSION_BADGE_BACKGROUND = 'rgba(0, 0, 0, 0.3)';
  private static readonly SESSION_BADGE_TEXT_COLOR = 'rgba(255, 255, 255, 0.9)';
  private static readonly GRID_DASH_PATTERN = [4, 4];
  private static readonly GRID_OPACITY = 0.3;
  private static readonly AXIS_OPACITY = 0.5;
  private static readonly AXIS_COLOR = '#444444';
  private static readonly AXIS_LINE_WIDTH = 0.5;
  private static readonly BORDER_BRIGHTNESS_ADJUSTMENT = -30;
  private static readonly ICON_COLOR = '#ffffff';
  private static readonly LABEL_COLOR = '#ffffff';
  private static readonly LABEL_FONT = 'bold 11px system-ui, -apple-system, sans-serif';
  private static readonly SESSION_FONT = 'bold 9px monospace';
  private static readonly TIME_LABEL_FONT = '10px sans-serif';

  private ctx: CanvasRenderingContext2D;
  private dimensions: SwimLaneDimensions;
  private config: SwimLaneConfig;
  private bubbles: EventBubble[] = [];
  private timeRange: { start: number; end: number } | null = null;

  constructor(
    canvas: HTMLCanvasElement,
    dimensions: SwimLaneDimensions,
    config: SwimLaneConfig
  ) {
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Failed to get canvas context');

    this.ctx = ctx;
    this.dimensions = dimensions;
    this.config = config;
    this.setupCanvas(canvas);
  }

  private setupCanvas(canvas: HTMLCanvasElement) {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = this.dimensions.width * dpr;
    canvas.height = this.dimensions.height * dpr;
    canvas.style.width = `${this.dimensions.width}px`;
    canvas.style.height = `${this.dimensions.height}px`;
    this.ctx.scale(dpr, dpr);
  }

  private getChartArea() {
    const { width, height, padding } = this.dimensions;
    return {
      x: padding.left,
      y: padding.top,
      width: width - padding.left - padding.right,
      height: height - padding.top - padding.bottom
    };
  }

  /**
   * Helper: Draw rounded rectangle path
   * Used for event bubble backgrounds
   */
  private roundRect(
    x: number,
    y: number,
    width: number,
    height: number,
    radius: number
  ): void {
    this.ctx.beginPath();
    this.ctx.moveTo(x + radius, y);
    this.ctx.lineTo(x + width - radius, y);
    this.ctx.arcTo(x + width, y, x + width, y + radius, radius);
    this.ctx.lineTo(x + width, y + height - radius);
    this.ctx.arcTo(x + width, y + height, x + width - radius, y + height, radius);
    this.ctx.lineTo(x + radius, y + height);
    this.ctx.arcTo(x, y + height, x, y + height - radius, radius);
    this.ctx.lineTo(x, y + radius);
    this.ctx.arcTo(x, y, x + radius, y, radius);
    this.ctx.closePath();
  }

  /**
   * Convert timestamp to X coordinate within chart area
   * Maps event timestamp to horizontal position based on time range
   */
  private timestampToX(timestamp: number): number {
    if (!this.timeRange) return 0;

    const chartArea = this.getChartArea();
    const timeSpan = this.timeRange.end - this.timeRange.start;

    // Normalize timestamp to 0-1 range
    const normalizedTime = (timestamp - this.timeRange.start) / timeSpan;

    // Map to chart area (right to left - newer events on right)
    return chartArea.x + chartArea.width * normalizedTime;
  }

  /**
   * Layout algorithm: Calculate Y positions to prevent overlapping bubbles
   *
   * Algorithm:
   * 1. Sort events by timestamp (left to right)
   * 2. For each event, find the first available "row" where it doesn't overlap
   * 3. Track occupied X ranges for each row
   * 4. Place bubble in first row with no horizontal overlap
   *
   * This creates a "swim lane" effect with vertical stacking
   */
  private calculateBubbleLayout(
    events: HookEvent[],
    getColorForEvent: (event: HookEvent) => string
  ): EventBubble[] {
    const chartArea = this.getChartArea();
    const bubbles: EventBubble[] = [];

    // Handle edge case: no events
    if (events.length === 0) {
      return bubbles;
    }

    // Handle edge case: single event (center it vertically)
    if (events.length === 1) {
      const event = events[0];
      if (!event.timestamp) return bubbles;

      const centerX = this.timestampToX(event.timestamp);
      const centerY = chartArea.y + chartArea.height / 2;
      const label = this.getEventLabel(event);
      const bubbleWidth = this.calculateBubbleWidth(label);

      bubbles.push({
        event,
        x: centerX,
        y: centerY,
        width: bubbleWidth,
        height: this.config.bubbleHeight,
        color: getColorForEvent(event)
      });

      return bubbles;
    }

    // Track occupied ranges for each row: [{ start: x1, end: x2 }, ...]
    const rows: Array<Array<{ start: number; end: number }>> = [];

    // Sort events by timestamp (oldest first)
    const sortedEvents = [...events].sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));

    sortedEvents.forEach(event => {
      // Skip events without timestamp
      if (!event.timestamp) return;

      // Calculate bubble dimensions
      const centerX = this.timestampToX(event.timestamp);
      const label = this.getEventLabel(event);
      const bubbleWidth = this.calculateBubbleWidth(label);

      const bubbleLeft = centerX - bubbleWidth / 2;
      const bubbleRight = centerX + bubbleWidth / 2;

      // Find first row where this bubble fits
      let rowIndex = 0;
      let foundRow = false;

      while (!foundRow) {
        // Initialize row if needed
        if (!rows[rowIndex]) {
          rows[rowIndex] = [];
        }

        // Check if bubble overlaps with any existing bubble in this row
        const hasOverlap = rows[rowIndex].some(range => {
          // Add spacing to prevent visual overlap
          const spacedLeft = bubbleLeft - this.config.bubbleSpacing;
          const spacedRight = bubbleRight + this.config.bubbleSpacing;

          return !(spacedRight < range.start || spacedLeft > range.end);
        });

        if (!hasOverlap) {
          // Found available row!
          foundRow = true;
          rows[rowIndex].push({ start: bubbleLeft, end: bubbleRight });

          // Calculate Y position based on row index
          const rowHeight = this.config.bubbleHeight + this.config.bubbleSpacing;
          const totalHeight = Math.min(rows.length * rowHeight, chartArea.height);
          const startY = chartArea.y + (chartArea.height - totalHeight) / 2; // Center vertically
          const centerY = startY + rowIndex * rowHeight + this.config.bubbleHeight / 2;

          bubbles.push({
            event,
            x: centerX,
            y: centerY,
            width: bubbleWidth,
            height: this.config.bubbleHeight,
            color: getColorForEvent(event)
          });
        } else {
          // Try next row
          rowIndex++;
        }
      }
    });

    return bubbles;
  }

  /**
   * Calculate bubble width based on content
   * Width now includes: icon + main label + session badge
   */
  private calculateBubbleWidth(label: string): number {
    this.ctx.font = SwimLaneRenderer.LABEL_FONT;
    const labelWidth = this.ctx.measureText(label).width;

    // Session badge width (fixed size for "12345")
    this.ctx.font = SwimLaneRenderer.SESSION_FONT;
    const sessionBadgeWidth = this.ctx.measureText('12345').width + SwimLaneRenderer.SESSION_BADGE_PADDING + 4;

    // Total width: icon + label + session badge + gaps
    const padding = this.config.iconSize + SwimLaneRenderer.ICON_PADDING + SwimLaneRenderer.LABEL_PADDING + 8;
    const totalWidth = labelWidth + sessionBadgeWidth + padding;

    // Clamp to min/max
    return Math.max(
      this.config.bubbleMinWidth,
      Math.min(this.config.bubbleMaxWidth, totalWidth)
    );
  }

  /**
   * Get display label for event
   * Combines event type + tool name (if applicable)
   */
  private getEventLabel(event: HookEvent): string {
    const eventType = event.hook_event_type;

    // For tool events, include tool name
    if ((eventType === 'PreToolUse' || eventType === 'PostToolUse') && event.payload?.tool_name) {
      return `${this.formatEventType(eventType)} • ${event.payload.tool_name}`;
    }

    return this.formatEventType(eventType);
  }

  /**
   * Format event type for display (shorter labels)
   */
  private formatEventType(eventType: string): string {
    const shortNames: Record<string, string> = {
      'PreToolUse': 'Tool',
      'PostToolUse': 'Done',
      'UserPromptSubmit': 'Prompt',
      'SessionStart': 'Start',
      'SessionEnd': 'End',
      'SubagentStop': 'Subagent',
      'PreCompact': 'Compact',
      'Notification': 'Notify',
      'Stop': 'Stop'
    };

    return shortNames[eventType] || eventType;
  }

  /**
   * Set time range for X-axis positioning
   * Events are positioned relative to this time window
   */
  setTimeRange(start: number, end: number): void {
    this.timeRange = { start, end };
  }

  /**
   * Update events and recalculate layout
   */
  setEvents(
    events: HookEvent[],
    getColorForEvent: (event: HookEvent) => string
  ): void {
    this.bubbles = this.calculateBubbleLayout(events, getColorForEvent);
  }

  /**
   * Clear canvas
   */
  clear(): void {
    this.ctx.clearRect(0, 0, this.dimensions.width, this.dimensions.height);
  }

  /**
   * Draw background gradient
   */
  drawBackground(): void {
    const chartArea = this.getChartArea();

    const gradient = this.ctx.createLinearGradient(
      chartArea.x,
      chartArea.y,
      chartArea.x,
      chartArea.y + chartArea.height
    );
    gradient.addColorStop(0, 'rgba(0, 0, 0, 0.02)');
    gradient.addColorStop(1, 'rgba(0, 0, 0, 0.05)');

    this.ctx.fillStyle = gradient;
    this.ctx.fillRect(chartArea.x, chartArea.y, chartArea.width, chartArea.height);
  }

  /**
   * Draw timeline axis
   */
  drawAxes(): void {
    const chartArea = this.getChartArea();

    this.ctx.strokeStyle = SwimLaneRenderer.AXIS_COLOR;
    this.ctx.lineWidth = SwimLaneRenderer.AXIS_LINE_WIDTH;
    this.ctx.globalAlpha = SwimLaneRenderer.AXIS_OPACITY;

    // X-axis (horizontal timeline)
    this.ctx.beginPath();
    this.ctx.moveTo(chartArea.x, chartArea.y + chartArea.height);
    this.ctx.lineTo(chartArea.x + chartArea.width, chartArea.y + chartArea.height);
    this.ctx.stroke();

    this.ctx.globalAlpha = 1.0;
  }

  drawTimeLabels(timeRange: string): void {
    const chartArea = this.getChartArea();
    const labels = this.getTimeLabels(timeRange);
    const spacing = chartArea.width / (labels.length - 1);

    // Draw vertical grid lines with dashed pattern for better distinction
    this.ctx.save();
    this.ctx.strokeStyle = SwimLaneRenderer.AXIS_COLOR;
    this.ctx.lineWidth = SwimLaneRenderer.AXIS_LINE_WIDTH;
    this.ctx.globalAlpha = SwimLaneRenderer.GRID_OPACITY;
    this.ctx.setLineDash(SwimLaneRenderer.GRID_DASH_PATTERN);

    labels.forEach((_, index) => {
      const x = chartArea.x + index * spacing;
      this.ctx.beginPath();
      this.ctx.moveTo(x, chartArea.y);
      this.ctx.lineTo(x, chartArea.y + chartArea.height);
      this.ctx.stroke();
    });

    this.ctx.setLineDash([]); // Reset to solid lines
    this.ctx.restore();

    // Draw text labels
    this.ctx.fillStyle = this.config.colors.text;
    this.ctx.font = SwimLaneRenderer.TIME_LABEL_FONT;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'top';

    labels.forEach((label, index) => {
      const x = chartArea.x + index * spacing;
      const y = chartArea.y + chartArea.height + 5;
      this.ctx.fillText(label, x, y);
    });
  }

  private getTimeLabels(timeRange: string): string[] {
    switch (timeRange) {
      case '1m':
        return ['60s', '45s', '30s', '15s', 'now'];
      case '3m':
        return ['3m', '2m', '1m', 'now'];
      case '5m':
        return ['5m', '4m', '3m', '2m', '1m', 'now'];
      case '10m':
        return ['10m', '8m', '6m', '4m', '2m', 'now'];
      default:
        return [];
    }
  }

  /**
   * Draw all event bubbles
   */
  drawBubbles(): void {
    if (this.bubbles.length === 0) {
      return;
    }

    this.bubbles.forEach(bubble => {
      this.drawEventBubble(bubble);
    });
  }

  /**
   * Draw a single event bubble with enhanced design
   * Layout: [Icon] Label [SessionBadge]
   */
  private drawEventBubble(bubble: EventBubble): void {
    const { x, y, width, height, color, event } = bubble;
    const bubbleLeft = x - width / 2;
    const bubbleTop = y - height / 2;
    const radius = height / 2;

    // Draw bubble shape (rounded corners, solid fill, subtle shadow for depth)
    this.ctx.save();

    // Add subtle drop shadow for depth (without breaking visibility)
    this.ctx.shadowColor = SwimLaneRenderer.BUBBLE_SHADOW_COLOR;
    this.ctx.shadowBlur = SwimLaneRenderer.BUBBLE_SHADOW_BLUR;
    this.ctx.shadowOffsetX = 0;
    this.ctx.shadowOffsetY = SwimLaneRenderer.BUBBLE_SHADOW_OFFSET_Y;

    this.ctx.beginPath();
    this.roundRect(bubbleLeft, bubbleTop, width, height, radius);

    // Use solid color (no gradient - gradients break visibility)
    this.ctx.fillStyle = color;
    this.ctx.fill();

    // Reset shadow for border (prevent double shadow)
    this.ctx.shadowColor = 'transparent';
    this.ctx.shadowBlur = 0;

    // Darker border for definition
    this.ctx.strokeStyle = this.adjustColorBrightness(color, SwimLaneRenderer.BORDER_BRIGHTNESS_ADJUSTMENT);
    this.ctx.lineWidth = SwimLaneRenderer.BUBBLE_BORDER_WIDTH;
    this.ctx.stroke();

    this.ctx.restore();

    // Draw icon (left side)
    const iconX = bubbleLeft + this.config.iconSize / 2 + SwimLaneRenderer.ICON_PADDING;
    const iconY = y;
    this.drawEventIcon(event, iconX, iconY, this.config.iconSize, SwimLaneRenderer.ICON_COLOR);

    // Draw main label (right of icon)
    const label = this.getEventLabel(event);
    const labelX = iconX + this.config.iconSize / 2 + SwimLaneRenderer.LABEL_PADDING;
    this.ctx.fillStyle = SwimLaneRenderer.LABEL_COLOR;
    this.ctx.font = SwimLaneRenderer.LABEL_FONT;
    this.ctx.textAlign = 'left';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(label, labelX, y);

    // Draw session badge (right side)
    const sessionId = event.session_id.slice(0, 5).toUpperCase();

    // Measure session text
    this.ctx.font = SwimLaneRenderer.SESSION_FONT;
    const sessionWidth = this.ctx.measureText(sessionId).width;

    // Session badge dimensions
    const sessionBadgeWidth = sessionWidth + SwimLaneRenderer.SESSION_BADGE_PADDING;
    const sessionBadgeHeight = SwimLaneRenderer.SESSION_BADGE_HEIGHT;
    const sessionBadgeX = bubbleLeft + width - sessionBadgeWidth - SwimLaneRenderer.SESSION_BADGE_RIGHT_MARGIN;
    const sessionBadgeY = y - sessionBadgeHeight / 2;
    const sessionBadgeRadius = SwimLaneRenderer.SESSION_BADGE_RADIUS;

    // Draw session badge background (semi-transparent black for consistent contrast)
    this.ctx.beginPath();
    this.roundRect(sessionBadgeX, sessionBadgeY, sessionBadgeWidth, sessionBadgeHeight, sessionBadgeRadius);
    this.ctx.fillStyle = SwimLaneRenderer.SESSION_BADGE_BACKGROUND;
    this.ctx.fill();

    // Draw session ID text
    this.ctx.fillStyle = SwimLaneRenderer.SESSION_BADGE_TEXT_COLOR;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(sessionId, sessionBadgeX + sessionBadgeWidth / 2, y);
  }

  /**
   * Draw event type icon (re-using Lucide icons from ChartRenderer)
   */
  private drawEventIcon(
    event: HookEvent,
    x: number,
    y: number,
    size: number,
    color: string
  ): void {
    const iconMap: Record<string, string> = {
      PreToolUse: 'wrench',
      PostToolUse: 'check-circle',
      Notification: 'bell',
      Stop: 'stop-circle',
      SubagentStop: 'user-check',
      PreCompact: 'package',
      UserPromptSubmit: 'message-square',
      SessionStart: 'rocket',
      SessionEnd: 'flag'
    };

    const iconName = iconMap[event.hook_event_type];
    if (iconName) {
      this.drawLucideIcon(iconName, x, y, size, color);
    }
  }

  /**
   * Draw Lucide icons using Path2D with exact SVG paths
   * (Copied from ChartRenderer for consistency)
   */
  private drawLucideIcon(
    iconName: string,
    x: number,
    y: number,
    size: number,
    color: string
  ): void {
    this.ctx.save();

    const scale = size / 24;
    this.ctx.translate(x - size / 2, y - size / 2);
    this.ctx.scale(scale, scale);

    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = 2;
    this.ctx.lineCap = 'round';
    this.ctx.lineJoin = 'round';
    this.ctx.fillStyle = 'none';

    switch (iconName) {
      case 'wrench': {
        const p = new Path2D(
          'M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z'
        );
        this.ctx.stroke(p);
        break;
      }
      case 'check-circle': {
        const p1 = new Path2D('M22 11.08V12a10 10 0 1 1-5.93-9.14');
        const p2 = new Path2D('M9 11l3 3L22 4');
        this.ctx.stroke(p1);
        this.ctx.stroke(p2);
        break;
      }
      case 'bell': {
        const p1 = new Path2D('M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9');
        const p2 = new Path2D('M10.3 21a1.94 1.94 0 0 0 3.4 0');
        this.ctx.stroke(p1);
        this.ctx.stroke(p2);
        break;
      }
      case 'stop-circle': {
        this.ctx.beginPath();
        this.ctx.arc(12, 12, 10, 0, Math.PI * 2);
        this.ctx.stroke();
        this.ctx.strokeRect(9, 9, 6, 6);
        break;
      }
      case 'user-check': {
        const p1 = new Path2D('M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2');
        this.ctx.beginPath();
        this.ctx.arc(9, 7, 4, 0, Math.PI * 2);
        this.ctx.stroke();
        this.ctx.stroke(p1);
        const p2 = new Path2D('M16 11l2 2l4-4');
        this.ctx.stroke(p2);
        break;
      }
      case 'package': {
        const p1 = new Path2D('M7.5 4.27l9 5.15');
        const p2 = new Path2D(
          'M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z'
        );
        const p3 = new Path2D('M3.3 7l8.7 5l8.7-5');
        const p4 = new Path2D('M12 22V12');
        this.ctx.stroke(p1);
        this.ctx.stroke(p2);
        this.ctx.stroke(p3);
        this.ctx.stroke(p4);
        break;
      }
      case 'message-square': {
        const p = new Path2D(
          'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'
        );
        this.ctx.stroke(p);
        break;
      }
      case 'rocket': {
        const p1 = new Path2D(
          'M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z'
        );
        const p2 = new Path2D(
          'M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z'
        );
        const p3 = new Path2D(
          'M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0'
        );
        const p4 = new Path2D(
          'M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5'
        );
        this.ctx.stroke(p1);
        this.ctx.stroke(p2);
        this.ctx.stroke(p3);
        this.ctx.stroke(p4);
        break;
      }
      case 'flag': {
        const p1 = new Path2D(
          'M4 15s1-1 4-1s5 2 8 2s4-1 4-1V3s-1 1-4 1s-5-2-8-2s-4 1-4 1z'
        );
        this.ctx.stroke(p1);
        this.ctx.beginPath();
        this.ctx.moveTo(4, 15);
        this.ctx.lineTo(4, 22);
        this.ctx.stroke();
        break;
      }
    }

    this.ctx.restore();
  }

  /**
   * Adjust color brightness for borders/shadows
   */
  private adjustColorBrightness(color: string, amount: number): string {
    if (!color.startsWith('#')) return color;

    const r = Math.max(
      0,
      Math.min(255, parseInt(color.slice(1, 3), 16) + amount)
    );
    const g = Math.max(
      0,
      Math.min(255, parseInt(color.slice(3, 5), 16) + amount)
    );
    const b = Math.max(
      0,
      Math.min(255, parseInt(color.slice(5, 7), 16) + amount)
    );

    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
  }

  /**
   * Render complete swim lane
   */
  render(): void {
    this.clear();
    this.drawBackground();
    this.drawAxes();
    this.drawBubbles();
  }

  /**
   * Resize canvas (update dimensions and redraw)
   */
  resize(dimensions: SwimLaneDimensions): void {
    this.dimensions = dimensions;
    this.setupCanvas(this.ctx.canvas as HTMLCanvasElement);
  }

  /**
   * Get bubble at mouse position (for tooltips/interactions)
   */
  getBubbleAtPosition(x: number, y: number): EventBubble | null {
    // Check bubbles in reverse order (top to bottom in rendering)
    for (let i = this.bubbles.length - 1; i >= 0; i--) {
      const bubble = this.bubbles[i];
      const halfWidth = bubble.width / 2;
      const halfHeight = bubble.height / 2;

      if (
        x >= bubble.x - halfWidth &&
        x <= bubble.x + halfWidth &&
        y >= bubble.y - halfHeight &&
        y <= bubble.y + halfHeight
      ) {
        return bubble;
      }
    }

    return null;
  }
}

/**
 * Factory function to create SwimLaneRenderer instance
 */
export function createSwimLaneRenderer(
  canvas: HTMLCanvasElement,
  dimensions: SwimLaneDimensions,
  config: SwimLaneConfig
): SwimLaneRenderer {
  return new SwimLaneRenderer(canvas, dimensions, config);
}
