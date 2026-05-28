/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { encodeBeast2For, decodeBeast2For, variant } from '@elaraai/east';
import type { EastType, ValueTypeOf } from '@elaraai/east';
import type { Context } from 'hono';
import { ResponseType, type Error } from './types.js';

/**
 * Decode BEAST2 request body from Hono context.
 */
export async function decodeBody<T extends EastType>(
  c: Context,
  type: T
): Promise<ValueTypeOf<T>> {
  const contentType = c.req.header('content-type');
  if (contentType !== 'application/beast2') {
    throw new Error(`Expected Content-Type: application/beast2, got ${contentType}`);
  }

  // TODO should we use use streaming decoder here?
  const buffer = await c.req.arrayBuffer();
  const decode = decodeBeast2For(type);
  return decode(new Uint8Array(buffer));
}

/**
 * Decode raw BEAST2 bytes (for handlers that receive body directly).
 */
export function decodeBeast2<T extends EastType>(
  data: Uint8Array,
  type: T
): ValueTypeOf<T> {
  const decode = decodeBeast2For(type);
  return decode(data);
}

/**
 * Send BEAST2 success response.
 *
 * Returns a web Response object that can be used by both Hono routes and Lambda handlers.
 */
export function sendSuccess<T extends EastType>(
  type: T,
  value: ValueTypeOf<T>
): Response {
  const responseType = ResponseType(type);
  const encode = encodeBeast2For(responseType); // TODO should we use streaming encoder here?
  const body = encode(variant('success', value) as ValueTypeOf<typeof responseType>);

  return new Response(body, {
    status: 200,
    headers: {
      'Content-Type': 'application/beast2',
    },
  });
}

/**
 * Send BEAST2 error response.
 *
 * Returns a web Response object that can be used by both Hono routes and Lambda handlers.
 */
export function sendError<T extends EastType>(
  type: T,
  error: Error
): Response {
  const responseType = ResponseType(type);
  const encode = encodeBeast2For(responseType);
  const body = encode(variant('error', error) as ValueTypeOf<typeof responseType>);

  return new Response(body, {
    status: 200,
    headers: {
      'Content-Type': 'application/beast2',
    },
  });
}

/**
 * Send BEAST2 success response with custom HTTP status.
 */
export function sendSuccessWithStatus<T extends EastType>(
  type: T,
  value: ValueTypeOf<T>,
  status: number
): Response {
  const responseType = ResponseType(type);
  const encode = encodeBeast2For(responseType); // TODO should we use streaming encoder here?
  const body = encode(variant('success', value) as ValueTypeOf<typeof responseType>);

  return new Response(body, {
    status,
    headers: {
      'Content-Type': 'application/beast2',
    },
  });
}
