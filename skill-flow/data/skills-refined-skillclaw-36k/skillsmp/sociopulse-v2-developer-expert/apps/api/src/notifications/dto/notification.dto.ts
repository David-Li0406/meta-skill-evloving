import { IsString, IsOptional, IsObject, IsNotEmpty } from 'class-validator';

// ============================================
// NOTIFICATION DTOs
// ============================================

export class CreateNotificationDto {
    @IsString()
    @IsNotEmpty()
    type: string;

    @IsString()
    @IsNotEmpty()
    title: string;

    @IsString()
    @IsNotEmpty()
    message: string;

    @IsString()
    @IsOptional()
    link?: string;

    @IsObject()
    @IsOptional()
    metadata?: Record<string, unknown>;
}

export class SendMissionMessageDto {
    @IsString()
    @IsNotEmpty()
    missionId: string;

    @IsString()
    @IsNotEmpty()
    content: string;
}

// ============================================
// SOCKET EVENT PAYLOADS
// ============================================

export interface NotificationPayload {
    id: string;
    type: string;
    title: string;
    message: string;
    link?: string;
    metadata?: Record<string, unknown>;
    createdAt: Date;
}

export interface MissionMessagePayload {
    id: string;
    missionId: string;
    senderId: string;
    senderName: string;
    senderAvatar?: string;
    content: string;
    type: 'TEXT' | 'SYSTEM';
    createdAt: Date;
}

export interface MissionChatStatus {
    isLocked: boolean;
    closesAt?: Date;
    lockMessage?: string;
}

export interface ActiveCountPayload {
    count: number;
}

// ============================================
// NOTIFICATION TYPES
// ============================================

export const NotificationTypes = {
    BRIEFING_READ: 'BRIEFING_READ',
    MISSION_STARTED: 'MISSION_STARTED',
    REPORT_SUBMITTED: 'REPORT_SUBMITTED',
    NEW_CHAT_MESSAGE: 'NEW_CHAT_MESSAGE',
    MISSION_ASSIGNED: 'MISSION_ASSIGNED',
    MISSION_LOCKED: 'MISSION_LOCKED',
} as const;

export type NotificationType = typeof NotificationTypes[keyof typeof NotificationTypes];
