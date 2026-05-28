// NotificationService.ts
// SINGLE RESPONSIBILITY: Sending notifications to users
// REASON TO CHANGE: Notification delivery mechanisms change

export interface Notification {
  userId: string;
  title: string;
  body: string;
}

export interface EmailSender {
  send(to: string, subject: string, body: string): Promise<boolean>;
}

export interface PushSender {
  send(deviceToken: string, title: string, body: string): Promise<boolean>;
}

export interface UserContactRepository {
  getEmail(userId: string): Promise<string | null>;
  getDeviceTokens(userId: string): Promise<string[]>;
}

export class NotificationService {
  constructor(
    private emailSender: EmailSender,
    private pushSender: PushSender,
    private contactRepo: UserContactRepository
  ) {}

  async sendEmail(userId: string, subject: string, body: string): Promise<boolean> {
    const email = await this.contactRepo.getEmail(userId);
    if (!email) return false;

    return this.emailSender.send(email, subject, body);
  }

  async sendPushNotification(userId: string, title: string, body: string): Promise<boolean> {
    const tokens = await this.contactRepo.getDeviceTokens(userId);
    if (tokens.length === 0) return false;

    const results = await Promise.all(
      tokens.map(token => this.pushSender.send(token, title, body))
    );

    const atLeastOneSucceeded = results.some(r => r);
    return atLeastOneSucceeded;
  }

  async sendAll(notification: Notification): Promise<{ email: boolean; push: boolean }> {
    const [email, push] = await Promise.all([
      this.sendEmail(notification.userId, notification.title, notification.body),
      this.sendPushNotification(notification.userId, notification.title, notification.body)
    ]);

    return { email, push };
  }
}
