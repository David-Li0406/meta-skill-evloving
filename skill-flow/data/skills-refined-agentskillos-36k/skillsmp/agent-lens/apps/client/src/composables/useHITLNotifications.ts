/**
 * HITL Notifications - Agent Lens Edition
 *
 * Enhanced browser notifications for human-in-the-loop requests
 * with urgency indicators and multi-channel support (ready for Phase 4+)
 */

import { ref } from 'vue';
import type { HookEvent } from '../types';

export function useHITLNotifications() {
  const hasPermission = ref(false);
  const notificationsSent = ref(0);

  // Check current permission status
  const checkPermission = () => {
    if (!('Notification' in window)) {
      console.warn('This browser does not support notifications');
      return false;
    }

    if (Notification.permission === 'granted') {
      hasPermission.value = true;
      return true;
    }

    return false;
  };

  // Request notification permission
  const requestPermission = async () => {
    if (!('Notification' in window)) {
      console.warn('This browser does not support notifications');
      return false;
    }

    if (Notification.permission === 'granted') {
      hasPermission.value = true;
      return true;
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission();
      hasPermission.value = permission === 'granted';
      return hasPermission.value;
    }

    return false;
  };

  // Get notification title based on type
  function getNotificationTitle(type: string): string {
    switch (type) {
      case 'permission':
        return '🔐 Permission Required';
      case 'choice':
        return '🎯 Choice Required';
      case 'question':
        return '❓ Agent Question';
      default:
        return '🤖 Agent Needs Input';
    }
  }

  // Get urgency level based on timeout
  function getUrgencyLevel(timeout: number, elapsed: number): 'normal' | 'urgent' | 'critical' {
    const remaining = timeout - elapsed;
    if (remaining < 30) return 'critical';
    if (remaining < 60) return 'urgent';
    return 'normal';
  }

  // Show notification for HITL request
  const notifyHITLRequest = (event: HookEvent, onClickCallback?: () => void) => {
    if (!hasPermission.value || !event.humanInTheLoop) return;

    const hitl = event.humanInTheLoop;
    const title = getNotificationTitle(hitl.type);
    const body = hitl.question.substring(0, 120) + (hitl.question.length > 120 ? '...' : '');

    // Calculate urgency
    const timeout = hitl.timeout || 300;
    const elapsed = 0; // Just sent
    const urgency = getUrgencyLevel(timeout, elapsed);

    const notification = new Notification(title, {
      body,
      icon: '/vite.svg', // TODO: Create custom HITL icon
      badge: '/vite.svg',
      tag: `hitl-${event.event_id}`,
      requireInteraction: urgency !== 'normal', // Don't auto-dismiss urgent/critical
      silent: urgency === 'normal',
      data: {
        eventId: event.event_id,
        urgency,
        type: hitl.type
      }
    });

    notification.onclick = () => {
      window.focus();

      // Call custom callback if provided
      if (onClickCallback) {
        onClickCallback();
      }

      notification.close();
    };

    notificationsSent.value++;
  };

  // Show urgent reminder for expiring request
  const notifyExpiringRequest = (event: HookEvent, secondsRemaining: number) => {
    if (!hasPermission.value || !event.humanInTheLoop) return;

    const notification = new Notification('⚠️ HITL Request Expiring Soon!', {
      body: `${secondsRemaining}s remaining: ${event.humanInTheLoop.question.substring(0, 80)}`,
      icon: '/vite.svg',
      tag: `hitl-expiring-${event.event_id}`,
      requireInteraction: true,
      silent: false,
      vibrate: [200, 100, 200] // Vibrate pattern for mobile
    });

    notification.onclick = () => {
      window.focus();
      notification.close();
    };
  };

  // Initialize on mount (check permission)
  checkPermission();

  return {
    hasPermission,
    notificationsSent,
    checkPermission,
    requestPermission,
    notifyHITLRequest,
    notifyExpiringRequest
  };
}

