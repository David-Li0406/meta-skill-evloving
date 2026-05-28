// 消息类型定义

// 本地后端 → 中转服务器
export interface RegisterMessage {
  type: "register";
  deviceId: string;
  pairCode: string;
}

// 小程序 → 中转服务器
export interface PairMessage {
  type: "pair";
  deviceId: string;
  pairCode: string;
}

// 小程序 → 本地后端（经由中转）
export interface ChatMessage {
  type: "chat";
  requestId: string;
  message: string;
  sessionId?: string; // CC 会话 ID
}

// 本地后端 → 小程序（经由中转）
export interface ChatResponse {
  type: "chat_response";
  requestId: string;
  data: unknown; // SDK Message
}

export interface ChatDone {
  type: "chat_done";
  requestId: string;
  sessionId: string; // 返回 CC 会话 ID 供下次续接
}

export interface ChatError {
  type: "chat_error";
  requestId: string;
  error: string;
}

// 中转服务器 → 客户端
export interface PairSuccess {
  type: "pair_success";
  deviceId: string;
}

export interface DeviceOffline {
  type: "device_offline";
}

// 心跳
export interface Ping {
  type: "ping";
}

export interface Pong {
  type: "pong";
}

export type ClientMessage =
  | RegisterMessage
  | PairMessage
  | ChatMessage
  | Ping;

export type ServerMessage =
  | ChatResponse
  | ChatDone
  | ChatError
  | PairSuccess
  | DeviceOffline
  | Pong;
