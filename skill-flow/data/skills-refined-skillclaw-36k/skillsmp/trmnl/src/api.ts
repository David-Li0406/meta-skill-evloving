const BASE_URL = "https://usetrmnl.com";

export class TRMNLClient {
  private apiKey: string;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${BASE_URL}${endpoint}`;
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
      ...((options.headers as Record<string, string>) || {}),
    };

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`TRMNL API error ${response.status}: ${text}`);
    }

    return response.json() as Promise<T>;
  }

  // Device endpoints
  async listDevices(): Promise<DevicesResponse> {
    return this.request<DevicesResponse>("/api/devices");
  }

  async getDevice(id: number): Promise<DeviceResponse> {
    return this.request<DeviceResponse>(`/api/devices/${id}`);
  }

  async updateDevice(
    id: number,
    updates: DeviceUpdate
  ): Promise<DeviceResponse> {
    return this.request<DeviceResponse>(`/api/devices/${id}`, {
      method: "PATCH",
      body: JSON.stringify(updates),
    });
  }

  // Display endpoints (uses device API key via Access-Token)
  async getCurrentScreen(deviceApiKey: string): Promise<CurrentScreenResponse> {
    const response = await fetch(`${BASE_URL}/api/display/current`, {
      headers: {
        "access-token": deviceApiKey,
      },
    });
    if (!response.ok) {
      throw new Error(`TRMNL API error ${response.status}`);
    }
    return response.json() as Promise<CurrentScreenResponse>;
  }

  async advanceScreen(deviceApiKey: string): Promise<DisplayResponse> {
    const response = await fetch(`${BASE_URL}/api/display`, {
      headers: {
        "access-token": deviceApiKey,
      },
    });
    if (!response.ok) {
      throw new Error(`TRMNL API error ${response.status}`);
    }
    return response.json() as Promise<DisplayResponse>;
  }

  // Playlist endpoints
  async listPlaylistItems(): Promise<PlaylistResponse> {
    return this.request<PlaylistResponse>("/api/playlists/items");
  }

  async updatePlaylistItem(
    id: number,
    visible: boolean
  ): Promise<PlaylistItemResponse> {
    return this.request<PlaylistItemResponse>(`/api/playlists/items/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ visible }),
    });
  }

  // Plugin settings endpoints
  async listPluginSettings(pluginId?: number): Promise<PluginSettingsResponse> {
    const query = pluginId ? `?plugin_id=${pluginId}` : "";
    return this.request<PluginSettingsResponse>(`/api/plugin_settings${query}`);
  }

  async createPluginSetting(
    name: string,
    pluginId: number
  ): Promise<PluginSettingResponse> {
    return this.request<PluginSettingResponse>("/api/plugin_settings", {
      method: "POST",
      body: JSON.stringify({ name, plugin_id: pluginId }),
    });
  }

  async deletePluginSetting(id: number): Promise<void> {
    await this.request<void>(`/api/plugin_settings/${id}`, {
      method: "DELETE",
    });
  }

  async getPluginData(id: number): Promise<PluginDataResponse> {
    return this.request<PluginDataResponse>(`/api/plugin_settings/${id}/data`);
  }

  async updatePluginData(
    id: number,
    mergeVariables: Record<string, unknown>
  ): Promise<PluginDataResponse> {
    return this.request<PluginDataResponse>(`/api/plugin_settings/${id}/data`, {
      method: "POST",
      body: JSON.stringify({ merge_variables: mergeVariables }),
    });
  }

  // Webhook endpoints (for private plugins)
  async pushWebhookContent(
    uuid: string,
    mergeVariables: Record<string, unknown>,
    mergeStrategy?: "deep_merge" | "stream",
    streamLimit?: number
  ): Promise<WebhookResponse> {
    const body: Record<string, unknown> = { merge_variables: mergeVariables };
    if (mergeStrategy) body.merge_strategy = mergeStrategy;
    if (streamLimit) body.stream_limit = streamLimit;

    const response = await fetch(`${BASE_URL}/api/custom_plugins/${uuid}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      throw new Error(`TRMNL API error ${response.status}`);
    }
    return response.json() as Promise<WebhookResponse>;
  }

  async getWebhookContent(uuid: string): Promise<WebhookResponse> {
    const response = await fetch(`${BASE_URL}/api/custom_plugins/${uuid}`);
    if (!response.ok) {
      throw new Error(`TRMNL API error ${response.status}`);
    }
    return response.json() as Promise<WebhookResponse>;
  }

  // User endpoint
  async getAccount(): Promise<AccountResponse> {
    return this.request<AccountResponse>("/api/me");
  }

  // Public endpoints
  async listCategories(): Promise<CategoriesResponse> {
    const response = await fetch(`${BASE_URL}/api/categories`);
    return response.json() as Promise<CategoriesResponse>;
  }

  async listModels(): Promise<ModelsResponse> {
    const response = await fetch(`${BASE_URL}/api/models`);
    return response.json() as Promise<ModelsResponse>;
  }

  async listPalettes(): Promise<PalettesResponse> {
    const response = await fetch(`${BASE_URL}/api/palettes`);
    return response.json() as Promise<PalettesResponse>;
  }
}

// Type definitions
export interface Device {
  id: number;
  name: string;
  friendly_id: string;
  mac_address: string;
  battery_voltage: number;
  rssi: number;
  api_key?: string;
}

export interface DevicesResponse {
  data: Device[];
}

export interface DeviceResponse {
  data: Device;
}

export interface DeviceUpdate {
  sleep_mode_enabled?: boolean;
  sleep_start_time?: string;
  sleep_end_time?: string;
}

export interface CurrentScreenResponse {
  status: number;
  refresh_rate: number;
  image_url: string;
  filename: string;
  rendered_at: string | null;
}

export interface DisplayResponse {
  status: number;
  image_url: string;
  image_name: string;
  update_firmware: boolean;
  firmware_url?: string;
  refresh_rate: number;
  reset_firmware: boolean;
}

export interface PlaylistItem {
  id: number;
  name: string;
  visible: boolean;
  position: number;
}

export interface PlaylistResponse {
  data: PlaylistItem[];
}

export interface PlaylistItemResponse {
  data: PlaylistItem;
}

export interface PluginSetting {
  id: number;
  name: string;
  plugin_id: number;
  uuid: string;
}

export interface PluginSettingsResponse {
  data: PluginSetting[];
}

export interface PluginSettingResponse {
  data: PluginSetting;
}

export interface PluginDataResponse {
  data: Record<string, unknown>;
}

export interface WebhookResponse {
  status: number;
  message?: string;
}

export interface AccountResponse {
  id: number;
  name: string;
  email: string;
  timezone: string;
  api_key: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface CategoriesResponse {
  data: Category[];
}

export interface Model {
  id: number;
  name: string;
  width: number;
  height: number;
  colors: number;
  bit_depth: number;
  rotation: number;
  mime_type: string;
}

export interface ModelsResponse {
  data: Model[];
}

export interface Palette {
  id: number;
  name: string;
  colors: string[];
}

export interface PalettesResponse {
  data: Palette[];
}
