/**
 * WebSocket 客户端
 * 连接中转服务器，处理消息转发
 */

import WebSocket from "ws";
import { executeChat } from "./cc-bridge.js";
import type {
  ClientMessage,
  ChatMessage,
  ChatResponse,
  ChatDone,
  ChatError,
} from "./types.js";

const RELAY_SERVER = process.env.RELAY_SERVER || "wss://cc-relay.your-domain.workers.dev";
const HEARTBEAT_INTERVAL = 30000; // 30 秒心跳
const RECONNECT_DELAY = 5000; // 5 秒重连

export class WSClient {
  private ws: WebSocket | null = null;
  private deviceId: string;
  private pairCode: string;
  private cwd: string;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private isConnected = false;
  private isPaired = false;

  public onPaired: (() => void) | null = null;
  public onDisconnected: (() => void) | null = null;
  public onError: ((error: string) => void) | null = null;

  constructor(deviceId: string, pairCode: string, cwd: string) {
    this.deviceId = deviceId;
    this.pairCode = pairCode;
    this.cwd = cwd;
  }

  /**
   * 连接到中转服务器
   */
  connect(): void {
    if (this.ws) {
      this.ws.close();
    }

    console.log(`[WS] 连接中转服务器: ${RELAY_SERVER}`);

    this.ws = new WebSocket(RELAY_SERVER);

    this.ws.on("open", () => {
      console.log("[WS] 连接成功");
      this.isConnected = true;

      // 注册设备
      this.send({
        type: "register",
        deviceId: this.deviceId,
        pairCode: this.pairCode,
      });

      // 启动心跳
      this.startHeartbeat();
    });

    this.ws.on("message", (data) => {
      try {
        const msg = JSON.parse(data.toString());
        this.handleMessage(msg);
      } catch (e) {
        console.error("[WS] 解析消息失败:", e);
      }
    });

    this.ws.on("close", () => {
      console.log("[WS] 连接断开");
      this.isConnected = false;
      this.isPaired = false;
      this.stopHeartbeat();
      this.onDisconnected?.();

      // 自动重连
      this.scheduleReconnect();
    });

    this.ws.on("error", (error) => {
      console.error("[WS] 错误:", error.message);
      this.onError?.(error.message);
    });
  }

  /**
   * 处理收到的消息
   */
  private handleMessage(msg: any): void {
    switch (msg.type) {
      case "pair_success":
        console.log("[WS] 配对成功!");
        this.isPaired = true;
        this.onPaired?.();
        break;

      case "chat":
        this.handleChat(msg as ChatMessage);
        break;

      case "pong":
        // 心跳响应，忽略
        break;

      default:
        console.log("[WS] 未知消息类型:", msg.type);
    }
  }

  /**
   * 处理聊天请求
   */
  private async handleChat(msg: ChatMessage): Promise<void> {
    console.log(`[CC] 收到消息: ${msg.message.substring(0, 50)}...`);

    await executeChat({
      message: msg.message,
      sessionId: msg.sessionId,
      cwd: this.cwd,
      onMessage: (data) => {
        const response: ChatResponse = {
          type: "chat_response",
          requestId: msg.requestId,
          data,
        };
        this.send(response);
      },
      onDone: (sessionId) => {
        const done: ChatDone = {
          type: "chat_done",
          requestId: msg.requestId,
          sessionId,
        };
        this.send(done);
        console.log(`[CC] 完成: ${msg.requestId}`);
      },
      onError: (error) => {
        const errMsg: ChatError = {
          type: "chat_error",
          requestId: msg.requestId,
          error,
        };
        this.send(errMsg);
        console.error(`[CC] 错误: ${error}`);
      },
    });
  }

  /**
   * 发送消息
   */
  private send(msg: ClientMessage | ChatResponse | ChatDone | ChatError): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(msg));
    }
  }

  /**
   * 启动心跳
   */
  private startHeartbeat(): void {
    this.stopHeartbeat();
    this.heartbeatTimer = setInterval(() => {
      this.send({ type: "ping" });
    }, HEARTBEAT_INTERVAL);
  }

  /**
   * 停止心跳
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  /**
   * 计划重连
   */
  private scheduleReconnect(): void {
    if (this.reconnectTimer) return;

    console.log(`[WS] ${RECONNECT_DELAY / 1000} 秒后重连...`);
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, RECONNECT_DELAY);
  }

  /**
   * 关闭连接
   */
  close(): void {
    this.stopHeartbeat();
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * 获取状态
   */
  getStatus(): { connected: boolean; paired: boolean } {
    return {
      connected: this.isConnected,
      paired: this.isPaired,
    };
  }
}
