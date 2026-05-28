import { z } from 'zod';

/**
 * API Contract Validator Template (2026)
 * Use this to verify that external API responses match your expected schemas.
 */

const ConfigSchema = z.object({
  endpoint: z.string().url(),
  method: z.enum(['GET', 'POST', 'PUT', 'PATCH', 'DELETE']),
  headers: z.record(z.string()).optional(),
  body: z.any().optional(),
});

export async function validateAPIResponse<T>(
  schema: z.ZodType<T>,
  config: z.infer<typeof ConfigSchema>
): Promise<T> {
  console.log(`🔍 Validating API: ${config.method} ${config.endpoint}`);
  
  const response = await fetch(config.endpoint, {
    method: config.method,
    headers: {
      'Content-Type': 'application/json',
      ...config.headers,
    },
    body: config.body ? JSON.stringify(config.body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  
  const result = schema.safeParse(data);
  if (!result.success) {
    console.error('❌ Schema Validation Failed:', result.error.format());
    throw new Error('API Contract Violation');
  }

  console.log('✅ Validation Successful');
  return result.data;
}

// Example Usage:
/*
const UserSchema = z.object({ id: z.string(), name: z.string() });
validateAPIResponse(UserSchema, { endpoint: 'https://api.example.com/me', method: 'GET' })
  .then(console.log)
  .catch(console.error);
*/
