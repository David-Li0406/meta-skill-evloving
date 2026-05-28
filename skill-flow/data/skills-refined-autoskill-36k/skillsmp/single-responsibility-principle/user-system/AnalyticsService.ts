// AnalyticsService.ts
// SINGLE RESPONSIBILITY: Tracking user analytics events
// REASON TO CHANGE: Analytics requirements or tracking mechanisms change

export interface AnalyticsEvent {
  userId: string;
  eventType: string;
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

export interface AnalyticsStore {
  record(event: AnalyticsEvent): Promise<void>;
  query(userId: string, eventType?: string): Promise<AnalyticsEvent[]>;
}

export class AnalyticsService {
  constructor(private store: AnalyticsStore) {}

  async trackLogin(userId: string, metadata?: { ip?: string; userAgent?: string }): Promise<void> {
    await this.store.record({
      userId,
      eventType: 'login',
      timestamp: new Date(),
      metadata
    });
  }

  async trackPageView(userId: string, page: string, metadata?: Record<string, unknown>): Promise<void> {
    await this.store.record({
      userId,
      eventType: 'page_view',
      timestamp: new Date(),
      metadata: { page, ...metadata }
    });
  }

  async trackEvent(userId: string, eventType: string, metadata?: Record<string, unknown>): Promise<void> {
    await this.store.record({
      userId,
      eventType,
      timestamp: new Date(),
      metadata
    });
  }

  async getLoginHistory(userId: string): Promise<AnalyticsEvent[]> {
    return this.store.query(userId, 'login');
  }

  async getUserEvents(userId: string): Promise<AnalyticsEvent[]> {
    return this.store.query(userId);
  }
}
