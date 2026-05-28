import type { HookEvent } from './types';
import {
  createTheme,
  updateThemeById,
  getThemeById,
  searchThemes,
  deleteThemeById,
  exportThemeById,
  importTheme,
  getThemeStats
} from './theme';
import { startFileIngestion, getRecentEvents, getFilterOptions, getIngestionHealth } from './file-ingest';
import { logConfiguration, SERVER_PORT } from './config';
import { initDatabase } from './db';

// Store WebSocket clients
const wsClients = new Set<any>();

// Track whether the theme database initialized successfully
let isDatabaseInitialized = false;

// Initialize theme database and log configuration on startup
try {
  initDatabase();
  isDatabaseInitialized = true;
} catch (error: unknown) {
  console.error('❌ Failed to initialize theme database:', error);
}

logConfiguration();

// Start file-based ingestion (reads from ~/.claude/history/raw-outputs/)
// Pass a callback to broadcast new events to connected WebSocket clients
startFileIngestion((events) => {
  console.log(`📡 Broadcasting ${events.length} event(s) to ${wsClients.size} WebSocket client(s)`);

  // Broadcast each event to all connected WebSocket clients
  events.forEach(event => {
    const message = JSON.stringify({ type: 'event', data: event });
    console.log(`   → Event: ${event.source_app} | ${event.hook_event_type}`);

    wsClients.forEach(client => {
      try {
        client.send(message);
      } catch (err) {
        console.log(`   ⚠️  Failed to send to client, removing from list`);
        // Client disconnected, remove from set
        wsClients.delete(client);
      }
    });
  });
});

// Create Bun server with HTTP and WebSocket support
const server = Bun.serve({
  port: SERVER_PORT,

  async fetch(req: Request) {
    const url = new URL(req.url);

    // Handle CORS
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle preflight
    if (req.method === 'OPTIONS') {
      return new Response(null, { headers });
    }

    // GET /health - Basic server and ingestion health
    if (url.pathname === '/health' && req.method === 'GET') {
      const ingestion = getIngestionHealth();
      const health = {
        status: isDatabaseInitialized ? 'ok' : 'degraded',
        db: {
          initialized: isDatabaseInitialized,
        },
        ingestion,
        websocketClients: wsClients.size,
      };

      return new Response(JSON.stringify(health), {
        headers: { ...headers, 'Content-Type': 'application/json' }
      });
    }

    // GET /events/filter-options - Get available filter options
    if (url.pathname === '/events/filter-options' && req.method === 'GET') {
      const options = getFilterOptions();
      return new Response(JSON.stringify(options), {
        headers: { ...headers, 'Content-Type': 'application/json' }
      });
    }

    // GET /events/recent - Get recent events
    if (url.pathname === '/events/recent' && req.method === 'GET') {
      const limit = parseInt(url.searchParams.get('limit') || '100');
      const events = getRecentEvents(limit);
      return new Response(JSON.stringify(events), {
        headers: { ...headers, 'Content-Type': 'application/json' }
      });
    }

    // Theme API endpoints

    // GET /api/themes/stats - Get theme statistics (must be checked before generic /api/themes/:id)
    if (url.pathname === '/api/themes/stats' && req.method === 'GET') {
      const result = await getThemeStats();
      return new Response(JSON.stringify(result), {
        headers: { ...headers, 'Content-Type': 'application/json' }
      });
    }

    // GET /api/themes/:id/export - Export a theme (more specific than /api/themes/:id)
    if (req.method === 'GET') {
      const exportMatch = url.pathname.match(/^\/api\/themes\/([^\/]+)\/export$/);
      if (exportMatch) {
        const id = exportMatch[1];

        const result = await exportThemeById(id);
        if (!result.success) {
          const status = result.error?.includes('not found') ? 404 : 400;
          return new Response(JSON.stringify(result), {
            status,
            headers: { ...headers, 'Content-Type': 'application/json' }
          });
        }

        return new Response(JSON.stringify(result.data), {
          headers: {
            ...headers,
            'Content-Type': 'application/json',
            'Content-Disposition': `attachment; filename="${result.data.theme.name}.json"`
          }
        });
      }
    }

    // POST /api/themes/import - Import a theme
    if (url.pathname === '/api/themes/import' && req.method === 'POST') {
      try {
        const importData = await req.json();
        const authorId = url.searchParams.get('authorId');

        const result = await importTheme(importData, authorId || undefined);

        const status = result.success ? 201 : 400;
        return new Response(JSON.stringify(result), {
          status,
          headers: { ...headers, 'Content-Type': 'application/json' }
        });
      } catch (error) {
        console.error('Error importing theme:', error);
        return new Response(JSON.stringify({
          success: false,
          error: 'Invalid import data'
        }), {
          status: 400,
          headers: { ...headers, 'Content-Type': 'application/json' }
        });
      }
    }

    // POST /api/themes - Create a new theme
    if (url.pathname === '/api/themes' && req.method === 'POST') {
      try {
        const themeData = await req.json();
        const result = await createTheme(themeData);

        const status = result.success ? 201 : 400;
        return new Response(JSON.stringify(result), {
          status,
          headers: { ...headers, 'Content-Type': 'application/json' }
        });
      } catch (error) {
        console.error('Error creating theme:', error);
        return new Response(JSON.stringify({
          success: false,
          error: 'Invalid request body'
        }), {
          status: 400,
          headers: { ...headers, 'Content-Type': 'application/json' }
        });
      }
    }

    // GET /api/themes - Search themes
    if (url.pathname === '/api/themes' && req.method === 'GET') {
      const query = {
        query: url.searchParams.get('query') || undefined,
        isPublic: url.searchParams.get('isPublic') ? url.searchParams.get('isPublic') === 'true' : undefined,
        authorId: url.searchParams.get('authorId') || undefined,
        sortBy: url.searchParams.get('sortBy') as any || undefined,
        sortOrder: url.searchParams.get('sortOrder') as any || undefined,
        limit: url.searchParams.get('limit') ? parseInt(url.searchParams.get('limit')!) : undefined,
        offset: url.searchParams.get('offset') ? parseInt(url.searchParams.get('offset')!) : undefined,
      };

      const result = await searchThemes(query);
      return new Response(JSON.stringify(result), {
        headers: { ...headers, 'Content-Type': 'application/json' }
      });
    }

    // GET /api/themes/:id - Get a specific theme
    if (req.method === 'GET') {
      const match = url.pathname.match(/^\/api\/themes\/([^\/]+)$/);
      if (match) {
        const id = match[1];

        const result = await getThemeById(id);
        const status = result.success ? 200 : 404;
        return new Response(JSON.stringify(result), {
          status,
          headers: { ...headers, 'Content-Type': 'application/json' }
        });
      }
    }

    // PUT /api/themes/:id - Update a theme
    if (req.method === 'PUT') {
      const match = url.pathname.match(/^\/api\/themes\/([^\/]+)$/);
      if (match) {
        const id = match[1];

        try {
          const updates = await req.json();
          const result = await updateThemeById(id, updates);

          const status = result.success ? 200 : 400;
          return new Response(JSON.stringify(result), {
            status,
            headers: { ...headers, 'Content-Type': 'application/json' }
          });
        } catch (error) {
          console.error('Error updating theme:', error);
          return new Response(JSON.stringify({
            success: false,
            error: 'Invalid request body'
          }), {
            status: 400,
            headers: { ...headers, 'Content-Type': 'application/json' }
          });
        }
      }
    }

    // DELETE /api/themes/:id - Delete a theme
    if (req.method === 'DELETE') {
      const match = url.pathname.match(/^\/api\/themes\/([^\/]+)$/);
      if (match) {
        const id = match[1];

        const authorId = url.searchParams.get('authorId');
        const result = await deleteThemeById(id, authorId || undefined);

        const status = result.success ? 200 : (result.error?.includes('not found') ? 404 : 403);
        return new Response(JSON.stringify(result), {
          status,
          headers: { ...headers, 'Content-Type': 'application/json' }
        });
      }
    }

    // WebSocket upgrade
    if (url.pathname === '/stream') {
      const success = server.upgrade(req);
      if (success) {
        return undefined;
      }
    }

    // Default response
    return new Response('Multi-Agent Observability Server', {
      headers: { ...headers, 'Content-Type': 'text/plain' }
    });
  },

  websocket: {
    open(ws) {
      console.log(`🔌 WebSocket client connected (total clients: ${wsClients.size + 1})`);
      wsClients.add(ws);

      // Send recent events on connection
      const events = getRecentEvents(50);
      console.log(`   → Sending ${events.length} initial events to new client`);
      ws.send(JSON.stringify({ type: 'initial', data: events }));
    },

    message(ws, message) {
      // Handle any client messages if needed
      console.log('Received message:', message);
    },

    close(ws) {
      wsClients.delete(ws);
      console.log(`🔌 WebSocket client disconnected (remaining clients: ${wsClients.size})`);
    }
  }
});

console.log(`🚀 Server running on http://localhost:${server.port}`);
console.log(`📊 WebSocket endpoint: ws://localhost:${server.port}/stream`);
console.log(`� REST events endpoints:`);
console.log(`   • GET http://localhost:${server.port}/events/recent`);
console.log(`   • GET http://localhost:${server.port}/events/filter-options`);