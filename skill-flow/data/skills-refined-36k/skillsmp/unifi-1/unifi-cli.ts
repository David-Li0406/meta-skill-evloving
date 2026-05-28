#!/usr/bin/env bun
/**
 * UniFi Network CLI v2
 *
 * Direct API implementation for UniFi OS (Cloud Key Gen 2+)
 * Uses native HTTP requests instead of node-unifi library
 */

import { readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

interface Config {
  controller: {
    host: string;
    port: number;
    username: string;
    password: string;
    site: string;
  };
}

class UnifiCLI {
  private config: Config;
  private baseUrl: string;
  private cookie: string | null = null;
  private csrfToken: string | null = null;

  constructor() {
    this.config = this.loadConfig();
    this.baseUrl = `https://${this.config.controller.host}:${this.config.controller.port}`;
  }

  private loadConfig(): Config {
    const configPath = join(homedir(), '.claude', 'skills', 'Unifi', 'config.json');
    try {
      const configData = readFileSync(configPath, 'utf-8');
      return JSON.parse(configData);
    } catch (error) {
      console.error('❌ Error: Unable to load config.json');
      console.error('   Create ~/.claude/skills/Unifi/config.json with your UniFi Controller credentials');
      console.error('   Use config.example.json as a template\n');
      process.exit(1);
    }
  }

  private async request(method: string, path: string, body?: any): Promise<any> {
    const url = `${this.baseUrl}${path}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.cookie) {
      headers['Cookie'] = this.cookie;
    }

    if (this.csrfToken) {
      headers['X-CSRF-Token'] = this.csrfToken;
    }

    try {
      const response = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
        // @ts-ignore - Bun supports this
        tls: { rejectUnauthorized: false }, // Accept self-signed certs
      });

      // Extract cookies from response
      const setCookie = response.headers.get('set-cookie');
      if (setCookie) {
        this.cookie = setCookie.split(';')[0];
      }

      // Extract CSRF token
      const csrfHeader = response.headers.get('x-csrf-token');
      if (csrfHeader) {
        this.csrfToken = csrfHeader;
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error: any) {
      throw new Error(`Request failed: ${error.message}`);
    }
  }

  private async login(): Promise<void> {
    try {
      const result = await this.request('POST', '/api/auth/login', {
        username: this.config.controller.username,
        password: this.config.controller.password,
      });

      if (!result || !result.unique_id) {
        throw new Error('Login failed - invalid response');
      }
    } catch (error: any) {
      console.error('❌ Authentication failed:', error.message);
      console.error('   Check username/password in config.json\n');
      throw error;
    }
  }

  private formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
  }

  private formatUptime(seconds: number): string {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    if (days > 0) return `${days}d ${hours}h`;
    if (hours > 0) return `${hours}h ${minutes}m`;
    return `${minutes}m`;
  }

  async getSiteStatus(): Promise<void> {
    await this.login();

    const sites = await this.request('GET', '/proxy/network/api/self/sites');

    console.log('\n📊 UniFi Site Status\n');
    sites.data.forEach((site: any) => {
      console.log(`Site Name: ${site.desc || site.name}`);
      console.log(`Site ID: ${site.name}`);
      console.log(`Role: ${site.role}`);
      console.log(`Num Devices: ${site.num_adopted || 0}`);
      console.log(`Num Clients: ${site.num_user || 0}\n`);
    });
  }

  async getDevices(): Promise<void> {
    await this.login();

    const result = await this.request(
      'GET',
      `/proxy/network/api/s/${this.config.controller.site}/stat/device`
    );

    const devices = result.data || [];

    console.log('\n🖥️  UniFi Devices\n');
    console.log('─'.repeat(100));
    console.log(
      'NAME'.padEnd(25) +
      'TYPE'.padEnd(15) +
      'MODEL'.padEnd(20) +
      'IP'.padEnd(16) +
      'STATUS'.padEnd(12) +
      'UPTIME'
    );
    console.log('─'.repeat(100));

    devices.forEach((device: any) => {
      const name = (device.name || 'Unnamed').substring(0, 24).padEnd(25);
      const type = (device.type || 'Unknown').substring(0, 14).padEnd(15);
      const model = (device.model || 'Unknown').substring(0, 19).padEnd(20);
      const ip = (device.ip || 'N/A').padEnd(16);
      const status = (device.state === 1 ? '✅ Online' : '❌ Offline').padEnd(12);
      const uptime = device.uptime ? this.formatUptime(device.uptime) : 'N/A';

      console.log(`${name}${type}${model}${ip}${status}${uptime}`);
    });

    console.log('─'.repeat(100));
    console.log(`Total Devices: ${devices.length}\n`);
  }

  async getClients(): Promise<void> {
    await this.login();

    const result = await this.request(
      'GET',
      `/proxy/network/api/s/${this.config.controller.site}/stat/sta`
    );

    const clients = result.data || [];

    console.log('\n👥 Connected Clients\n');
    console.log('─'.repeat(120));
    console.log(
      'HOSTNAME'.padEnd(25) +
      'IP'.padEnd(16) +
      'CONNECTION'.padEnd(15) +
      'NETWORK'.padEnd(20) +
      'TX/RX'.padEnd(25) +
      'UPTIME'
    );
    console.log('─'.repeat(120));

    clients.forEach((client: any) => {
      const hostname = (client.hostname || client.name || 'Unknown').substring(0, 24).padEnd(25);
      const ip = (client.ip || 'N/A').padEnd(16);
      const connection = (client.is_wired ? '🔌 Wired' : '📡 WiFi').padEnd(15);
      const network = (client.essid || 'Wired').substring(0, 19).padEnd(20);
      const tx = this.formatBytes(client.tx_bytes || 0);
      const rx = this.formatBytes(client.rx_bytes || 0);
      const txrx = `↑${tx} ↓${rx}`.padEnd(25);
      const uptime = client.uptime ? this.formatUptime(client.uptime) : 'N/A';

      console.log(`${hostname}${ip}${connection}${network}${txrx}${uptime}`);
    });

    console.log('─'.repeat(120));
    console.log(`Total Clients: ${clients.length}\n`);
  }

  async getHealth(): Promise<void> {
    await this.login();

    const result = await this.request(
      'GET',
      `/proxy/network/api/s/${this.config.controller.site}/stat/device`
    );

    const devices = result.data || [];

    console.log('\n🏥 Device Health\n');
    console.log('─'.repeat(90));
    console.log(
      'NAME'.padEnd(25) +
      'TYPE'.padEnd(15) +
      'CPU'.padEnd(10) +
      'MEMORY'.padEnd(10) +
      'UPTIME'.padEnd(15) +
      'VERSION'
    );
    console.log('─'.repeat(90));

    devices.forEach((device: any) => {
      const name = (device.name || 'Unnamed').substring(0, 24).padEnd(25);
      const type = (device.type || 'Unknown').substring(0, 14).padEnd(15);
      const cpu = device['system-stats']?.cpu ? `${Number(device['system-stats'].cpu).toFixed(1)}%`.padEnd(10) : 'N/A'.padEnd(10);
      const mem = device['system-stats']?.mem ? `${Number(device['system-stats'].mem).toFixed(1)}%`.padEnd(10) : 'N/A'.padEnd(10);
      const uptime = device.uptime ? this.formatUptime(device.uptime).padEnd(15) : 'N/A'.padEnd(15);
      const version = device.version || 'N/A';

      console.log(`${name}${type}${cpu}${mem}${uptime}${version}`);
    });

    console.log('─'.repeat(90));
    console.log(`Total Devices: ${devices.length}\n`);
  }

  async getAlerts(): Promise<void> {
    await this.login();

    const result = await this.request(
      'GET',
      `/proxy/network/api/s/${this.config.controller.site}/stat/alarm?archived=false`
    );

    const alerts = result.data || [];

    console.log('\n🚨 Recent Alerts\n');

    if (alerts.length === 0) {
      console.log('✅ No active alerts\n');
      return;
    }

    console.log('─'.repeat(100));
    console.log(
      'TIME'.padEnd(20) +
      'TYPE'.padEnd(20) +
      'MESSAGE'
    );
    console.log('─'.repeat(100));

    alerts.slice(0, 10).forEach((alert: any) => {
      const time = alert.datetime ? new Date(alert.datetime).toLocaleString() : 'N/A';
      const type = (alert.key || 'Unknown').substring(0, 19).padEnd(20);
      const msg = alert.msg || 'No message';

      console.log(`${time.padEnd(20)}${type}${msg}`);
    });

    console.log('─'.repeat(100));
    console.log(`Total Active Alerts: ${alerts.length}\n`);
  }

  async getWAN(): Promise<void> {
    await this.login();

    const result = await this.request(
      'GET',
      `/proxy/network/api/s/${this.config.controller.site}/stat/health`
    );

    const health = result.data || [];
    const wanHealth = health.find((h: any) => h.subsystem === 'wan');

    console.log('\n🌐 WAN Status\n');

    if (wanHealth) {
      console.log(`Status: ${wanHealth.status || 'Unknown'}`);
      console.log(`WAN IP: ${wanHealth.wan_ip || 'N/A'}`);
      console.log(`Uptime: ${wanHealth.uptime ? this.formatUptime(wanHealth.uptime) : 'N/A'}`);

      if (wanHealth.speedtest_status) {
        console.log(`Download Speed: ${wanHealth.speedtest_status.xput_download?.toFixed(2) || 'N/A'} Mbps`);
        console.log(`Upload Speed: ${wanHealth.speedtest_status.xput_upload?.toFixed(2) || 'N/A'} Mbps`);
        console.log(`Latency: ${wanHealth.speedtest_status.latency || 'N/A'} ms`);
      }
      console.log();
    } else {
      console.log('WAN health information not available\n');
    }
  }

  async getBandwidth(): Promise<void> {
    await this.login();

    const result = await this.request(
      'GET',
      `/proxy/network/api/s/${this.config.controller.site}/stat/sta`
    );

    const clients = result.data || [];

    let totalTx = 0;
    let totalRx = 0;

    clients.forEach((client: any) => {
      totalTx += client.tx_bytes || 0;
      totalRx += client.rx_bytes || 0;
    });

    console.log('\n📊 Bandwidth Usage\n');
    console.log(`Total Upload: ${this.formatBytes(totalTx)}`);
    console.log(`Total Download: ${this.formatBytes(totalRx)}`);
    console.log(`Total Clients: ${clients.length}\n`);

    const sorted = clients.sort((a: any, b: any) => {
      const aTotal = (a.tx_bytes || 0) + (a.rx_bytes || 0);
      const bTotal = (b.tx_bytes || 0) + (b.rx_bytes || 0);
      return bTotal - aTotal;
    });

    console.log('Top 10 Bandwidth Users:\n');
    console.log('─'.repeat(80));
    console.log(
      'HOSTNAME'.padEnd(25) +
      'IP'.padEnd(16) +
      'UPLOAD'.padEnd(15) +
      'DOWNLOAD'
    );
    console.log('─'.repeat(80));

    sorted.slice(0, 10).forEach((client: any) => {
      const hostname = (client.hostname || client.name || 'Unknown').substring(0, 24).padEnd(25);
      const ip = (client.ip || 'N/A').padEnd(16);
      const tx = this.formatBytes(client.tx_bytes || 0).padEnd(15);
      const rx = this.formatBytes(client.rx_bytes || 0);

      console.log(`${hostname}${ip}${tx}${rx}`);
    });

    console.log('─'.repeat(80) + '\n');
  }

  async run(command: string): Promise<void> {
    try {
      switch (command) {
        case 'site-status':
          await this.getSiteStatus();
          break;
        case 'devices':
          await this.getDevices();
          break;
        case 'clients':
          await this.getClients();
          break;
        case 'health':
          await this.getHealth();
          break;
        case 'alerts':
          await this.getAlerts();
          break;
        case 'wan':
          await this.getWAN();
          break;
        case 'bandwidth':
          await this.getBandwidth();
          break;
        default:
          console.log('\n❌ Unknown command:', command);
          this.showHelp();
          process.exit(1);
      }
    } catch (error: any) {
      console.error('\n❌ Error:', error.message);
      process.exit(1);
    }
  }

  showHelp(): void {
    console.log(`
UniFi Network CLI

Usage: bun unifi-cli.ts <command>

Commands:
  site-status    Show overall site status and info
  devices        List all UniFi devices
  clients        List connected clients
  health         Show device health metrics
  alerts         Show recent alerts
  wan            Show WAN connection status
  bandwidth      Show bandwidth usage

Examples:
  bun unifi-cli.ts site-status
  bun unifi-cli.ts clients
  bun unifi-cli.ts health
`);
  }
}

// Main execution
const command = process.argv[2];

if (!command) {
  const cli = new UnifiCLI();
  cli.showHelp();
  process.exit(1);
}

const cli = new UnifiCLI();

(async () => {
  try {
    await cli.run(command);
    process.exit(0);
  } catch (error: any) {
    console.error('Fatal error:', error.message || error);
    process.exit(1);
  }
})();
