# API Integration Command Templates

This file contains templates and patterns for creating slash commands that integrate with APIs, implement components using curl examples, and handle data fetching workflows.

## 1. REST API Component Generator

### Basic CRUD Component Template

````markdown
---
description: Generate React component from REST API curl examples
argument-hint: [component-name] [api-endpoints-json]
allowed-tools: Read, Write, WebFetch, Bash
---

# REST API Component Generator

Creating component: $1
Using APIs: $2

## API Analysis Process

1. Parse the provided JSON configuration:

```json
{
  "endpoints": [
    {
      "name": "getItems",
      "method": "GET",
      "url": "/api/items",
      "response": "itemsResponse"
    },
    {
      "name": "createItem",
      "method": "POST",
      "url": "/api/items",
      "request": "createItemRequest",
      "response": "itemResponse"
    }
  ]
}
```
````

2. Generate TypeScript interfaces from response structures
3. Create API service functions
4. Build React component with state management
5. Add loading, error, and success states

## Generated Component Structure

```tsx
// src/components/$1/$1.tsx
import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/Button";

interface Item {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
}

interface ApiResponse {
  data: Item[];
  total: number;
  page: number;
}

export const $1: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auto-generated API calls
  const fetchItems = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/items");
      if (!response.ok) throw new Error("Failed to fetch items");
      const data: ApiResponse = await response.json();
      setItems(data.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  // Render component based on API requirements
  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">$1</h2>

      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">
          Error: {error}
        </div>
      )}

      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="space-y-2">
          {items.map((item) => (
            <div key={item.id} className="border p-3 rounded">
              <h3 className="font-semibold">{item.name}</h3>
              {item.description && (
                <p className="text-gray-600">{item.description}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default $1;
```

````

## 2. GraphQL Component Generator

### GraphQL Query Component
```markdown
---
description: Create React component for GraphQL operations
argument-hint: [component-name] [graphql-schema-url]
allowed-tools: WebFetch, Write, Read
---

# GraphQL Component Generator

Component: $1
Schema: $2

## GraphQL Integration Process

1. Fetch GraphQL schema: $2
2. Parse types and queries
3. Generate React Query hooks
4. Create component with GraphQL operations
5. Add optimistic updates if needed

## Generated GraphQL Service

```tsx
// src/services/$1Service.ts
import { gql } from '@apollo/client';
import { useQuery, useMutation } from '@apollo/client';

const GET_ITEMS_QUERY = gql`
  query GetItems {
    items {
      id
      name
      description
      createdAt
    }
  }
`;

const CREATE_ITEM_MUTATION = gql`
  mutation CreateItem($input: CreateItemInput!) {
    createItem(input: $input) {
      id
      name
      description
      createdAt
    }
  }
`;

export const useItems = () => {
  const { data, loading, error } = useQuery(GET_ITEMS_QUERY);
  return { items: data?.items || [], loading, error };
};

export const useCreateItem = () => {
  const [createItem, { loading, error }] = useMutation(CREATE_ITEM_MUTATION);

  return {
    createItem: async (input: CreateItemInput) => {
      const result = await createItem({
        variables: { input },
        update: (cache, { data }) => {
          // Update cache
        }
      });
      return result.data?.createItem;
    },
    loading,
    error
  };
};
````

````

## 3. WebSocket Component Template

### Real-time Data Component
```markdown
---
description: Create component with WebSocket integration for real-time updates
argument-hint: [component-name] [websocket-url] [message-format]
allowed-tools: Write, Read, Bash
---

# WebSocket Component Generator

Component: $1
WebSocket URL: $2
Message Format: $3

## WebSocket Integration Pattern

```tsx
// src/components/$1/$1.tsx
import React, { useState, useEffect, useRef } from 'react';

interface WebSocketMessage {
  type: string;
  payload: any;
  timestamp: number;
}

export const $1: React.FC = () => {
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [connected, setConnected] = useState(false);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Establish WebSocket connection
    ws.current = new WebSocket('$2');

    ws.current.onopen = () => {
      setConnected(true);
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        setMessages(prev => [...prev, message]);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    ws.current.onclose = () => {
      setConnected(false);
      console.log('WebSocket disconnected');
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const sendMessage = (message: any) => {
    if (ws.current && connected) {
      ws.current.send(JSON.stringify(message));
    }
  };

  return (
    <div className="p-4">
      <div className="mb-4">
        Status: {connected ?
          <span className="text-green-600">Connected</span> :
          <span className="text-red-600">Disconnected</span>
        }
      </div>

      <div className="space-y-2">
        {messages.map((msg, index) => (
          <div key={index} className="border p-2 rounded">
            <small className="text-gray-500">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </small>
            <pre className="text-sm">{JSON.stringify(msg.payload, null, 2)}</pre>
          </div>
        ))}
      </div>
    </div>
  );
};
````

````

## 4. Multi-API Integration Template

### Data Aggregation Component
```markdown
---
description: Create component that aggregates data from multiple APIs
argument-hint: [component-name] [apis-config-json]
allowed-tools: Read, Write, WebFetch, Bash
---

# Multi-API Component Generator

Component: $1
APIs Configuration: $2

## Multi-API Integration Pattern

1. Parse API configuration JSON
2. Generate TypeScript interfaces for each API
3. Create data aggregation logic
4. Handle concurrent API calls
5. Implement error boundaries

## Configuration Example
```json
{
  "apis": [
    {
      "name": "users",
      "url": "https://jsonplaceholder.typicode.com/users",
      "transform": "mapUserResponse",
      "cache": true
    },
    {
      "name": "posts",
      "url": "https://jsonplaceholder.typicode.com/posts",
      "transform": "mapPostResponse",
      "cache": false
    },
    {
      "name": "comments",
      "url": "https://jsonplaceholder.typicode.com/comments",
      "dependencies": ["posts"],
      "transform": "mapCommentsResponse"
    }
  ],
  "aggregations": [
    {
      "name": "userWithPosts",
      "sources": ["users", "posts"],
      "merge": "mergeUserAndPosts"
    }
  ]
}
````

## Generated Component

```tsx
// src/components/$1/$1.tsx
import React, { useState, useEffect } from "react";

interface User {
  id: number;
  name: string;
  email: string;
}

interface Post {
  id: number;
  userId: number;
  title: string;
  body: string;
}

interface UserWithPosts extends User {
  posts: Post[];
}

export const $1: React.FC = () => {
  const [data, setData] = useState<UserWithPosts[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch all APIs concurrently
        const [usersRes, postsRes] = await Promise.all([
          fetch("https://jsonplaceholder.typicode.com/users"),
          fetch("https://jsonplaceholder.typicode.com/posts"),
        ]);

        if (!usersRes.ok || !postsRes.ok) {
          throw new Error("Failed to fetch data");
        }

        const users: User[] = await usersRes.json();
        const posts: Post[] = await postsRes.json();

        // Aggregate data
        const userWithPosts: UserWithPosts[] = users.map((user) => ({
          ...user,
          posts: posts.filter((post) => post.userId === user.id),
        }));

        setData(userWithPosts);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">$1</h1>

      {loading && <div>Loading aggregated data...</div>}
      {error && <div className="text-red-600">Error: {error}</div>}

      <div className="space-y-4">
        {data.map((user) => (
          <div key={user.id} className="border rounded p-4">
            <h2 className="text-lg font-semibold">{user.name}</h2>
            <p className="text-gray-600">{user.email}</p>

            <div className="mt-2">
              <h3 className="font-medium">Posts ({user.posts.length})</h3>
              <div className="ml-4 space-y-1">
                {user.posts.map((post) => (
                  <div key={post.id} className="text-sm">
                    <span className="font-medium">{post.title}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

````

## 5. File Upload API Integration

### File Upload Component
```markdown
---
description: Create component with file upload to API endpoint
argument-hint: [component-name] [upload-endpoint] [file-types]
allowed-tools: Write, Read, Bash
---

# File Upload Component Generator

Component: $1
Upload Endpoint: $2
Allowed File Types: $3

## File Upload Pattern

```tsx
// src/components/$1/$1.tsx
import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/Button';

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  url: string;
  uploadedAt: string;
}

export const $1: React.FC = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFiles = async (fileList: FileList) => {
    const validFiles = Array.from(fileList).filter(file =>
      $3 ? file.type.match($3) : true
    );

    for (const file of validFiles) {
      await uploadFile(file);
    }
  };

  const uploadFile = async (file: File) => {
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('$2', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const uploadedFile: UploadedFile = await response.json();
      setFiles(prev => [...prev, uploadedFile]);
    } catch (error) {
      console.error('Upload error:', error);
      // Handle error display
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">$1</h2>

      {/* Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center ${
          dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={$3}
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
          className="hidden"
        />

        <Button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Choose Files or Drag & Drop'}
        </Button>

        <p className="mt-2 text-sm text-gray-600">
          Supported formats: $3 || 'All files'
        </p>
      </div>

      {/* File List */}
      <div className="mt-4 space-y-2">
        {files.map(file => (
          <div key={file.id} className="flex items-center justify-between border p-3 rounded">
            <div>
              <span className="font-medium">{file.name}</span>
              <span className="text-sm text-gray-500 ml-2">
                ({(file.size / 1024 / 1024).toFixed(2)} MB)
              </span>
            </div>
            <a
              href={file.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              View
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};
````

```

## Best Practices for API Integration Commands

1. **Type Safety**: Always generate TypeScript interfaces from API responses
2. **Error Handling**: Implement comprehensive error boundaries
3. **Loading States**: Show loading indicators during API calls
4. **Caching**: Implement caching strategies for repeated requests
5. **Retry Logic**: Add retry mechanisms for failed requests
6. **Debouncing**: Debounce search/filter API calls
7. **Pagination**: Handle paginated responses efficiently
8. **Authentication**: Securely handle API keys and tokens
9. **Rate Limiting**: Respect API rate limits
10. **Data Transformation**: Transform API responses to component-friendly formats
```
