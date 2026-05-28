/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

// =============================================================================
// BufferWriter - Managed Uint8Array with auto-growth
// =============================================================================

export class BufferWriter {
  private buffer: Uint8Array;
  private view: DataView;
  private offset: number = 0;

  constructor(initialCapacity = 16384) { // 16KB default for network payloads
    this.buffer = new Uint8Array(initialCapacity);
    this.view = new DataView(this.buffer.buffer);
  }

  private ensureCapacity(needed: number): void {
    const required = this.offset + needed;
    if (required <= this.buffer.length) {
      return; // sufficient capacity
    }

    // Exponential growth: min 2x, max +1GB per resize
    const doubled = this.buffer.length * 2;
    const maxGrowth = this.buffer.length + 1024 * 1024 * 1024;
    const newSize = Math.max(Math.min(doubled, maxGrowth), required);

    const newBuffer = new Uint8Array(newSize);
    newBuffer.set(this.buffer);
    this.buffer = newBuffer;
    this.view = new DataView(newBuffer.buffer);
  }

  writeUint8(value: number): void {
    this.ensureCapacity(1);
    this.view.setUint8(this.offset, value);
    this.offset += 1;
  }

  writeUint16LE(value: number): void {
    this.ensureCapacity(2);
    this.view.setUint16(this.offset, value, true);
    this.offset += 2;
  }

  writeUint16BE(value: number): void {
    this.ensureCapacity(2);
    this.view.setUint16(this.offset, value, false);
    this.offset += 2;
  }

  writeBytes(bytes: Uint8Array): void {
    this.ensureCapacity(bytes.length);
    this.buffer.set(bytes, this.offset);
    this.offset += bytes.length;
  }

  // ===========================================================================
  // Varint encoding (LEB128 - used by beast2)
  // ===========================================================================

  writeVarint(value: number): void {
    // Unsigned LEB128 encoding for sizes/lengths/tags
    if (value < 0) {
      throw new Error(`writeVarint requires non-negative value, got ${value}`);
    }
    if (!Number.isSafeInteger(value)) {
      throw new Error(`writeVarint requires safe integer, got ${value}`);
    }

    this.ensureCapacity(10); // max 10 bytes for 64-bit value

    // Use BigInt to avoid precision loss with large numbers
    let n = BigInt(value);
    while (n >= 0x80n) {
      this.view.setUint8(this.offset, Number(n & 0x7Fn) | 0x80);
      this.offset += 1;
      n >>= 7n;
    }
    this.view.setUint8(this.offset, Number(n));
    this.offset += 1;
  }

  writeZigzag(value: bigint): void {
    // Zigzag encoding: (n << 1) ^ (n >> 63)
    const zigzagged = (value << 1n) ^ (value >> 63n);

    // Convert to unsigned LEB128
    this.ensureCapacity(10); // max 10 bytes for 64-bit value

    let n = zigzagged;
    while (n >= 0x80n) {
      this.view.setUint8(this.offset, Number(n & 0x7Fn) | 0x80);
      this.offset += 1;
      n >>= 7n;
    }
    this.view.setUint8(this.offset, Number(n));
    this.offset += 1;
  }

  // ===========================================================================
  // Integer encoding - beast v1 (big-endian with sign-bit flip for ordering)
  // ===========================================================================

  writeInt64Twiddled(value: bigint): void {
    this.ensureCapacity(8);
    // Flip sign bit for memcmp ordering (total ordering for all int64 values)
    // Positive values become > 0x8000_0000_0000_0000
    // Negative values become < 0x8000_0000_0000_0000
    // Note: Using -9223372036854775808n (MIN_INT64 = -2^63) which is 0x8000_0000_0000_0000 as signed
    const twiddled = value >= 0n
      ? value + -9223372036854775808n  // Add MIN_INT64 to flip sign bit
      : value - -9223372036854775808n; // Subtract MIN_INT64 (same as add MAX_INT64+1)
    this.view.setBigInt64(this.offset, twiddled, false); // big-endian
    this.offset += 8;
  }

  // ===========================================================================
  // Float encoding - beast2 (little-endian, canonical NaN)
  // ===========================================================================

  writeFloat64LE(value: number): void {
    this.ensureCapacity(8);

    // NaN normalization: always write canonical quiet NaN
    // 0x7FF8000000000000 is the bit pattern (same for big and little-endian)
    // The littleEndian flag controls byte order in memory
    if (Number.isNaN(value)) {
      this.view.setBigUint64(this.offset, 0x7FF8000000000000n, true); // little-endian byte order (Avro-compatible)
    } else {
      this.view.setFloat64(this.offset, value, true); // little-endian (Avro-compatible)
    }
    this.offset += 8;
  }

  // ===========================================================================
  // Float encoding - beast v1 (big-endian with bit-twiddling for total ordering)
  // ===========================================================================

  // Preallocated buffers for float bit-twiddling (reused across calls)
  private static _floatBuffer = new Float64Array(1);
  private static _uintBuffer = new BigUint64Array(BufferWriter._floatBuffer.buffer);

  writeFloat64Twiddled(value: number): void {
    this.ensureCapacity(8);

    // Convert to bit pattern using preallocated buffers
    BufferWriter._floatBuffer[0] = value;
    let uint = BufferWriter._uintBuffer[0]!; // Non-null assertion: array access always succeeds for typed arrays

    // Bit-twiddling for total ordering (including NaNs, infinities, signed zeros)
    // This ensures memcmp(encoded_a, encoded_b) matches float comparison
    if (uint < 0x8000_0000_0000_0000n) {
      // Positive float (sign bit = 0) - flip sign bit
      // Maps: 0.0 -> 0x8000..., +inf -> 0xFFF0..., NaN -> 0xFFF8...
      uint = uint ^ 0x8000_0000_0000_0000n;
    } else {
      // Negative float (sign bit = 1) - flip all bits
      // Maps: -0.0 -> 0x7FFF..., -inf -> 0x000F..., -smallest -> 0x7FFF...
      uint = ~uint;
    }

    this.view.setBigUint64(this.offset, uint, false); // big-endian
    this.offset += 8;
  }

  // ===========================================================================
  // String encoding - beast2 (varint-length prefixed)
  // ===========================================================================

  writeStringUtf8Varint(str: string): void {
    // Encode UTF-8 first to know the length
    const maxUtf8Length = str.length * 3; // worst case: 3 bytes per UTF-16 code unit
    this.ensureCapacity(10 + maxUtf8Length); // varint length + string bytes

    // Encode string into a temporary position (after max varint size)
    const tempStringStart = this.offset + 10; // Reserve max varint bytes
    const stringEnd = utf8EncodeInto(str, this.buffer, tempStringStart);
    const utf8ByteLength = stringEnd - tempStringStart;

    // Now write the actual varint length
    this.writeVarint(utf8ByteLength);
    const varintEnd = this.offset;

    // Shift string data to immediately after the varint (if needed)
    if (varintEnd !== tempStringStart) {
      this.buffer.copyWithin(varintEnd, tempStringStart, stringEnd);
    }

    // Update offset to end of string
    this.offset = varintEnd + utf8ByteLength;
  }

  // ===========================================================================
  // String encoding - beast v1 (null-terminated)
  // ===========================================================================

  writeStringUtf8Null(str: string): void {
    const maxUtf8Length = str.length * 3; // worst case: 3 bytes per UTF-16 code unit
    this.ensureCapacity(maxUtf8Length + 1); // +1 for null byte

    this.offset = utf8EncodeInto(str, this.buffer, this.offset);
    this.view.setUint8(this.offset, 0); // null terminator
    this.offset += 1;
  }

  get size(): number {
    return this.offset;
  }

  get currentOffset(): number {
    return this.offset;
  }

  /**
   * Extract the current buffer contents and reset for reuse.
   * Used by streaming encoders to generate chunks.
   */
  pop(): Uint8Array {
    const chunk = this.buffer.subarray(0, this.offset);
    this.offset = 0;
    return chunk;
  }

  toUint8Array(): Uint8Array {
    return this.buffer.subarray(0, this.offset);
  }
}

// =============================================================================
// Stateless read functions
// =============================================================================

// ===========================================================================
// Varint (beast2)
// ===========================================================================

export function readVarint(buffer: Uint8Array, offset: number): [number, number] {
  // Unsigned LEB128 → number for sizes/lengths/tags
  // Use BigInt to avoid precision loss, then convert to number
  let result = 0n;
  let shift = 0n;

  while (true) {
    if (offset >= buffer.length) {
      throw new Error(`Buffer underflow reading varint at offset ${offset}`);
    }

    const byte = buffer[offset++]!;
    result |= BigInt(byte & 0x7F) << shift;

    if ((byte & 0x80) === 0) {
      break; // last byte
    }

    shift += 7n;
    if (shift >= 64n) {
      throw new Error(`Varint too long at offset ${offset - 1}`);
    }
  }

  const numResult = Number(result);
  if (!Number.isSafeInteger(numResult)) {
    throw new Error(`Varint value ${result} exceeds MAX_SAFE_INTEGER`);
  }

  return [numResult, offset];
}

export function readZigzag(buffer: Uint8Array, offset: number): [bigint, number] {
  // Zigzag varint → bigint for signed IntegerType values
  let result = 0n;
  let shift = 0n;

  while (true) {
    if (offset >= buffer.length) {
      throw new Error(`Buffer underflow reading zigzag at offset ${offset}`);
    }

    const byte = buffer[offset++]!;
    result |= BigInt(byte & 0x7F) << shift;

    if ((byte & 0x80) === 0) {
      break; // last byte
    }

    shift += 7n;
    if (shift >= 64n) {
      throw new Error(`Zigzag varint too long at offset ${offset - 1}`);
    }
  }

  // Decode zigzag: (n >> 1) ^ -(n & 1)
  const decoded = (result >> 1n) ^ -(result & 1n);
  return [decoded, offset];
}

// ===========================================================================
// Integer - beast v1 (big-endian twiddled)
// ===========================================================================

export function readInt64Twiddled(view: DataView, offset: number): [bigint, number] {
  if (offset + 8 > view.byteLength) {
    throw new Error(`Buffer underflow reading int64 at offset ${offset}`);
  }
  const twiddled = view.getBigInt64(offset, false); // big-endian
  // Undo sign-bit flip (same operation as encoding - XOR is self-inverse)
  // Note: Using -9223372036854775808n (MIN_INT64 = -2^63)
  const value = twiddled >= 0n
    ? twiddled + -9223372036854775808n
    : twiddled - -9223372036854775808n;
  return [value, offset + 8];
}

// ===========================================================================
// Float - beast2 (little-endian with NaN validation)
// ===========================================================================

export function readFloat64LE(view: DataView, offset: number): number {
  if (offset + 8 > view.byteLength) {
    throw new Error(`Buffer underflow reading float64 at offset ${offset}`);
  }

  const bits = view.getBigUint64(offset, true); // little-endian byte order (Avro-compatible)

  // Check for NaN (exponent = all 1s, mantissa != 0)
  // Bit pattern is the same regardless of endianness
  if ((bits & 0x7FF0000000000000n) === 0x7FF0000000000000n &&
      (bits & 0x000FFFFFFFFFFFFFn) !== 0n) {
    // It's a NaN - must be canonical quiet NaN (positive or negative)
    if (bits !== 0x7FF8000000000000n && bits !== 0xFFF8000000000000n) {
      throw new Error(`Non-canonical NaN at offset ${offset}: 0x${bits.toString(16)}`);
    }
  }

  return view.getFloat64(offset, true); // little-endian byte order (Avro-compatible)
}

// ===========================================================================
// Float - beast v1 (big-endian twiddled)
// ===========================================================================

// Preallocated buffers for float bit-twiddling (reused across calls)
const _floatReadUintBuffer = new BigUint64Array(1);
const _floatReadBuffer = new Float64Array(_floatReadUintBuffer.buffer);

export function readFloat64Twiddled(view: DataView, offset: number): number {
  if (offset + 8 > view.byteLength) {
    throw new Error(`Buffer underflow reading float64 at offset ${offset}`);
  }

  let uint = view.getBigUint64(offset, false); // big-endian

  // Undo bit-twiddling for total ordering
  if (uint >= 0x8000_0000_0000_0000n) {
    // Positive float - flip sign bit
    uint = uint ^ 0x8000_0000_0000_0000n;
  } else {
    // Negative float - flip all bits
    uint = ~uint;
  }

  _floatReadUintBuffer[0] = uint;
  return _floatReadBuffer[0]!; // Non-null assertion: array access always succeeds for typed arrays
}

// ===========================================================================
// String - beast2 (varint-length)
// ===========================================================================

export function readStringUtf8Varint(buffer: Uint8Array, offset: number): [string, number] {
  // Read varint length
  const [length, newOffset] = readVarint(buffer, offset);

  if (newOffset + length > buffer.length) {
    throw new Error(`Buffer underflow reading string at offset ${offset}, length ${length}`);
  }

  // Decode UTF-8
  const str = utf8Decode(buffer, newOffset, length);
  return [str, newOffset + length];
}

// ===========================================================================
// String - beast v1 (null-terminated)
// ===========================================================================

export function readStringUtf8Null(buffer: Uint8Array, offset: number): [string, number] {
  // Single-pass: decode UTF-8 and find null terminator simultaneously (like ELARACore)
  const codePoints: number[] = [];
  let i = offset;

  while (i < buffer.length) {
    const byte1 = buffer[i++]!;

    if (byte1 === 0) {
      // Null terminator found
      return [String.fromCharCode.apply(String, codePoints), i];
    }

    if ((byte1 & 0x80) === 0) {
      // 1-byte (ASCII)
      codePoints.push(byte1);
    } else if ((byte1 & 0xE0) === 0xC0) {
      // 2-byte
      const byte2 = buffer[i++]! & 0x3F;
      codePoints.push(((byte1 & 0x1F) << 6) | byte2);
    } else if ((byte1 & 0xF0) === 0xE0) {
      // 3-byte
      const byte2 = buffer[i++]! & 0x3F;
      const byte3 = buffer[i++]! & 0x3F;
      codePoints.push(((byte1 & 0x0F) << 12) | (byte2 << 6) | byte3);
    } else if ((byte1 & 0xF8) === 0xF0) {
      // 4-byte
      const byte2 = buffer[i++]! & 0x3F;
      const byte3 = buffer[i++]! & 0x3F;
      const byte4 = buffer[i++]! & 0x3F;
      let codePoint = ((byte1 & 0x07) << 18) | (byte2 << 12) | (byte3 << 6) | byte4;

      // Encode as surrogate pair if needed
      if (codePoint > 0xFFFF) {
        codePoint -= 0x10000;
        codePoints.push(((codePoint >>> 10) & 0x3FF) | 0xD800);
        codePoint = 0xDC00 | (codePoint & 0x3FF);
      }
      codePoints.push(codePoint);
    } else {
      // Invalid UTF-8, skip byte
      codePoints.push(byte1);
    }
  }

  throw new Error(`No null terminator found for string at offset ${offset}`);
}

// =============================================================================
// UTF-8 encoding/decoding (shared by both formats)
// =============================================================================

// Adapted from old implementation, optimized for small strings
export function utf8EncodeInto(str: string, buffer: Uint8Array, offset: number): number {
  let pos = 0;
  const len = str.length;
  let at = offset;

  while (pos < len) {
    let value = str.charCodeAt(pos++);

    // Handle surrogate pairs
    if (value >= 0xD800 && value <= 0xDBFF) {
      // high surrogate
      if (pos < len) {
        const extra = str.charCodeAt(pos);
        if ((extra & 0xFC00) === 0xDC00) {
          ++pos;
          value = ((value & 0x3FF) << 10) + (extra & 0x3FF) + 0x10000;
        }
      }
      if (value >= 0xD800 && value <= 0xDBFF) {
        continue; // drop lone surrogate
      }
    }

    if ((value & 0xFFFFFF80) === 0) {
      // 1-byte (ASCII)
      buffer[at++] = value;
    } else if ((value & 0xFFFFF800) === 0) {
      // 2-byte
      buffer[at++] = ((value >>> 6) & 0x1F) | 0xC0;
      buffer[at++] = (value & 0x3F) | 0x80;
    } else if ((value & 0xFFFF0000) === 0) {
      // 3-byte
      buffer[at++] = ((value >>> 12) & 0x0F) | 0xE0;
      buffer[at++] = ((value >>> 6) & 0x3F) | 0x80;
      buffer[at++] = (value & 0x3F) | 0x80;
    } else if ((value & 0xFFE00000) === 0) {
      // 4-byte
      buffer[at++] = ((value >>> 18) & 0x07) | 0xF0;
      buffer[at++] = ((value >>> 12) & 0x3F) | 0x80;
      buffer[at++] = ((value >>> 6) & 0x3F) | 0x80;
      buffer[at++] = (value & 0x3F) | 0x80;
    } else {
      continue; // out of range
    }
  }

  return at;
}

export function utf8Decode(buffer: Uint8Array, offset: number, length: number): string {
  const end = offset + length;
  const codePoints: number[] = [];

  let i = offset;
  while (i < end) {
    const byte1 = buffer[i++]!;

    if ((byte1 & 0x80) === 0) {
      // 1-byte (ASCII)
      codePoints.push(byte1);
    } else if ((byte1 & 0xE0) === 0xC0) {
      // 2-byte
      const byte2 = buffer[i++]! & 0x3F;
      codePoints.push(((byte1 & 0x1F) << 6) | byte2);
    } else if ((byte1 & 0xF0) === 0xE0) {
      // 3-byte
      const byte2 = buffer[i++]! & 0x3F;
      const byte3 = buffer[i++]! & 0x3F;
      codePoints.push(((byte1 & 0x0F) << 12) | (byte2 << 6) | byte3);
    } else if ((byte1 & 0xF8) === 0xF0) {
      // 4-byte
      const byte2 = buffer[i++]! & 0x3F;
      const byte3 = buffer[i++]! & 0x3F;
      const byte4 = buffer[i++]! & 0x3F;
      let codePoint = ((byte1 & 0x07) << 18) | (byte2 << 12) | (byte3 << 6) | byte4;

      // Encode as surrogate pair if needed
      if (codePoint > 0xFFFF) {
        codePoint -= 0x10000;
        codePoints.push(((codePoint >>> 10) & 0x3FF) | 0xD800);
        codePoint = 0xDC00 | (codePoint & 0x3FF);
      }
      codePoints.push(codePoint);
    } else {
      // Invalid UTF-8, skip byte
      codePoints.push(byte1);
    }
  }

  return String.fromCharCode(...codePoints);
}

/**
 * StreamBufferReader - Helper for reading bytes from a Web Streams ReadableStream
 * with lookahead support for parsing.
 *
 * Maintains an internal buffer of unconsumed bytes pulled from the underlying stream.
 */
export class StreamBufferReader {
  private reader: ReadableStreamDefaultReader<Uint8Array>;
  private buffer: Uint8Array;
  private bufferOffset: number;
  private done: boolean;
  private totalBytesConsumed: number;

  // Preallocated buffers for efficient primitive decoding (reused across calls)
  private tempBuffer8 = new Uint8Array(8);
  private tempView8 = new DataView(this.tempBuffer8.buffer);
  private floatUintBuffer = new BigUint64Array(1);
  private floatBuffer = new Float64Array(this.floatUintBuffer.buffer);

  constructor(stream: ReadableStream<Uint8Array>) {
    this.reader = stream.getReader();
    this.buffer = new Uint8Array(0);
    this.bufferOffset = 0;
    this.done = false;
    this.totalBytesConsumed = 0;
  }

  /**
   * Get the current position in the stream (total bytes read so far).
   */
  get position(): number {
    return this.totalBytesConsumed + this.bufferOffset;
  }

  /**
   * Ensure we have at least `count` bytes available in the buffer.
   * Pulls from underlying stream as needed.
   */
  private async ensureBytes(count: number): Promise<void> {
    // Keep pulling chunks until we have enough bytes
    while (true) {
      const available = this.buffer.length - this.bufferOffset;
      if (available >= count) {
        return; // Already have enough
      }

      if (this.done) {
        throw new Error(`Unexpected end of stream: needed ${count} bytes, only ${available} available`);
      }

      // Need more bytes - pull from stream
      const { value, done } = await this.reader.read();

      if (done) {
        this.done = true;
        if (this.buffer.length - this.bufferOffset < count) {
          throw new Error(`Unexpected end of stream: needed ${count} bytes, only ${this.buffer.length - this.bufferOffset} available`);
        }
        return;
      }

      if (!value || value.length === 0) {
        // Empty chunk, try again (loop will continue)
        continue;
      }

      // Append new chunk to buffer
      const unconsumed = this.buffer.subarray(this.bufferOffset);
      this.totalBytesConsumed += this.bufferOffset;
      const newBuffer = new Uint8Array(unconsumed.length + value.length);
      newBuffer.set(unconsumed, 0);
      newBuffer.set(value, unconsumed.length);
      this.buffer = newBuffer;
      this.bufferOffset = 0;
      // Loop continues to check if we have enough bytes now
    }
  }

  /**
   * Peek at the next byte without consuming it.
   * Returns null if stream is done.
   * Optimized to avoid promises unless necessary.
   */
  peekByte(): Promise<number | null> | number | null {
    if (this.buffer.length - this.bufferOffset >= 1) {
      return this.buffer[this.bufferOffset]!;
    }
    return this.peekByteAsync();
  }

  private async peekByteAsync(): Promise<number | null> {
    try {
      await this.ensureBytes(1);
      return this.buffer[this.bufferOffset]!;
    } catch {
      return null; // End of stream
    }
  }

  /**
   * Read and consume the next byte.
   * Returns synchronously if data is buffered, otherwise returns a Promise.
   * Throws if stream is done.
   * Optimized to avoid promises unless necessary.
   */
  readByte(): number | Promise<number> {
    // Fast path: if we have buffered data, return it synchronously
    const available = this.buffer.length - this.bufferOffset;
    if (available >= 1) {
      const byte = this.buffer[this.bufferOffset]!;
      this.bufferOffset++;
      return byte;
    }

    // Slow path: need to fetch from stream
    return this.readByteAsync();
  }

  private async readByteAsync(): Promise<number> {
    await this.ensureBytes(1);
    const byte = this.buffer[this.bufferOffset]!;
    this.bufferOffset++;
    return byte;
  }

  /**
   * Read exactly `buffer.length` bytes into the provided buffer.
   * Throws if not enough bytes available.
   * Optimized to avoid promises unless necessary.
   */
  readBytes(buffer: Uint8Array): void | Promise<void> {
    // Fast path: if we have enough buffered data, read synchronously
    if (this.buffer.length - this.bufferOffset >= buffer.length) {
      buffer.set(this.buffer.subarray(this.bufferOffset, this.bufferOffset + buffer.length));
      this.bufferOffset += buffer.length;
      return;
    }

    // Slow path: need to fetch from stream
    return this.readBytesAsync(buffer);
  }

  private async readBytesAsync(buffer: Uint8Array): Promise<void> {
    await this.ensureBytes(buffer.length);
    buffer.set(this.buffer.subarray(this.bufferOffset, this.bufferOffset + buffer.length));
    this.bufferOffset += buffer.length;
  }

  /**
   * Read bytes until the terminator byte is found (exclusive).
   * Returns the bytes read (not including terminator).
   * The terminator byte is consumed.
   * Optimized to avoid promises unless necessary.
   */
  readUntilByte(terminator: number): Uint8Array | Promise<Uint8Array> {
    // Fast path: if we have enough buffered data, read synchronously
    for (let i = this.bufferOffset; i < this.buffer.length; i++) {
      if (this.buffer[i] === terminator) {
        const result = this.buffer.subarray(this.bufferOffset, i);
        this.bufferOffset = i + 1; // consume terminator
        return result;
      }
    }

    // Slow path: need to fetch from stream
    return this.readUntilByteAsync(terminator);
  }

  private async readUntilByteAsync(terminator: number): Promise<Uint8Array> {
    const result: number[] = [];

    while (true) {
      const byte = await this.readByte();
      if (byte === terminator) {
        break;
      }
      result.push(byte);
    }

    return new Uint8Array(result);
  }

  /**
   * Release the underlying reader.
   * Should be called when done reading to release resources.
   */
  async release(): Promise<void> {
    await this.reader.releaseLock();
  }

  // =============================================================================
  // Specialized read methods for Beast v1 format
  // =============================================================================

  /**
   * Read a twiddled big-endian int64 (Beast v1 format).
   * Uses sign-bit flip for total ordering.
   * Optimized to avoid promises unless necessary.
   */
  readInt64Twiddled(): bigint | Promise<bigint> {
    // Fast path: if we have enough buffered data, read synchronously
    if (this.buffer.length - this.bufferOffset >= 8) {
      this.tempBuffer8.set(this.buffer.subarray(this.bufferOffset, this.bufferOffset + 8));
      const twiddled = this.tempView8.getBigInt64(0, false); // big-endian
      this.bufferOffset += 8;
      // Undo sign-bit flip (same operation as encoding - XOR is self-inverse)
      const value = twiddled >= 0n
        ? twiddled + -9223372036854775808n
        : twiddled - -9223372036854775808n;
      return value;
    }

    // Slow path: need to fetch from stream
    return this.readInt64TwiddledAsync();
  }

  private async readInt64TwiddledAsync(): Promise<bigint> {
    await this.readBytes(this.tempBuffer8);
    const twiddled = this.tempView8.getBigInt64(0, false); // big-endian
    // Undo sign-bit flip (same operation as encoding - XOR is self-inverse)
    const value = twiddled >= 0n
      ? twiddled + -9223372036854775808n
      : twiddled - -9223372036854775808n;
    return value;
  }

  /**
   * Read a twiddled big-endian float64 (Beast v1 format).
   * Uses bit-twiddling for total ordering.
   */
  readFloat64Twiddled(): number | Promise<number> {
    // Fast path: if we have enough buffered data, read synchronously
    if (this.buffer.length - this.bufferOffset >= 8) {
      this.tempBuffer8.set(this.buffer.subarray(this.bufferOffset, this.bufferOffset + 8));
      this.bufferOffset += 8;

      let uint = this.tempView8.getBigUint64(0, false); // big-endian

      // Undo bit-twiddling for total ordering
      if (uint >= 0x8000_0000_0000_0000n) {
        // Positive float - flip sign bit
        uint = uint ^ 0x8000_0000_0000_0000n;
      } else {
        // Negative float - flip all bits
        uint = ~uint;
      }

      // Convert to float using preallocated buffers
      this.floatUintBuffer[0] = uint;
      return this.floatBuffer[0]!;
    }

    // Slow path: need to fetch from stream
    return this.readFloat64TwiddledAsync();
  }

  private async readFloat64TwiddledAsync(): Promise<number> {
    await this.readBytes(this.tempBuffer8);
    let uint = this.tempView8.getBigUint64(0, false); // big-endian

    // Undo bit-twiddling for total ordering
    if (uint >= 0x8000_0000_0000_0000n) {
      // Positive float - flip sign bit
      uint = uint ^ 0x8000_0000_0000_0000n;
    } else {
      // Negative float - flip all bits
      uint = ~uint;
    }

    // Convert to float using preallocated buffers
    this.floatUintBuffer[0] = uint;
    return this.floatBuffer[0]!;
  }

  /**
   * Read a null-terminated UTF-8 string (Beast v1 format).
   * Decodes UTF-8 while searching for null terminator in single pass.
   * Optimized to avoid promises unless necessary.
   */
  readStringUtf8Null(): string | Promise<string> {
    // Fast path: if we have enough buffered data, read synchronously
    for (let i = this.bufferOffset; i < this.buffer.length; i++) {
      if (this.buffer[i] === 0) {
        // Found null terminator in buffer
        const str = utf8Decode(this.buffer, this.bufferOffset, i - this.bufferOffset);
        this.bufferOffset = i + 1; // consume null terminator
        return str;
      }
    }

    // Slow path: need to fetch from stream
    return this.readStringUtf8NullAsync();
  }

  private async readStringUtf8NullAsync(): Promise<string> {
    const codePoints: number[] = [];

    while (true) {
      const byte1 = await this.readByte();

      if (byte1 === 0) {
        // Null terminator found
        return String.fromCharCode.apply(String, codePoints);
      }

      if ((byte1 & 0x80) === 0) {
        // 1-byte (ASCII)
        codePoints.push(byte1);
      } else if ((byte1 & 0xE0) === 0xC0) {
        // 2-byte
        const byte2 = (await this.readByte()) & 0x3F;
        codePoints.push(((byte1 & 0x1F) << 6) | byte2);
      } else if ((byte1 & 0xF0) === 0xE0) {
        // 3-byte
        const byte2 = (await this.readByte()) & 0x3F;
        const byte3 = (await this.readByte()) & 0x3F;
        codePoints.push(((byte1 & 0x0F) << 12) | (byte2 << 6) | byte3);
      } else if ((byte1 & 0xF8) === 0xF0) {
        // 4-byte
        const byte2 = (await this.readByte()) & 0x3F;
        const byte3 = (await this.readByte()) & 0x3F;
        const byte4 = (await this.readByte()) & 0x3F;
        let codePoint = ((byte1 & 0x07) << 18) | (byte2 << 12) | (byte3 << 6) | byte4;

        // Encode as surrogate pair if needed
        if (codePoint > 0xFFFF) {
          codePoint -= 0x10000;
          codePoints.push(((codePoint >>> 10) & 0x3FF) | 0xD800);
          codePoint = 0xDC00 | (codePoint & 0x3FF);
        }
        codePoints.push(codePoint);
      } else {
        // Invalid UTF-8, skip byte
        codePoints.push(byte1);
      }
    }
  }

  // =============================================================================
  // Specialized read methods for Beast v2 format
  // =============================================================================

  /**
   * Read an unsigned varint (LEB128) - Beast v2 format.
   * Returns a number (safe for lengths/tags up to 2^53-1).
   * Optimized to avoid promises unless necessary.
   */
  readVarint(): number | Promise<number> {
    // Fast path: if we have enough buffered data, read synchronously
    if (this.buffer.length - this.bufferOffset >= 10) {
      const [value, newOffset] = readVarint(this.buffer, this.bufferOffset);
      this.bufferOffset = newOffset;
      return value;
    }

    // Slow path: need to fetch from stream
    return this.readVarintAsync();
  }

  private async readVarintAsync(): Promise<number> {
    let result = 0;
    let shift = 0;

    while (true) {
      const byte = await this.readByte();

      // Use number operations for values that fit in safe integer range
      if (shift < 49) { // 7 * 7 = 49 bits safely fits in number
        result |= (byte & 0x7F) << shift;
      } else {
        // Overflow to BigInt path for large values (rare)
        let bigResult = BigInt(result);
        bigResult |= BigInt(byte & 0x7F) << BigInt(shift);

        if ((byte & 0x80) === 0) {
          return Number(bigResult);
        }

        shift += 7;
        while (true) {
          const nextByte = await this.readByte();
          shift += 7;
          if (shift >= 64) {
            throw new Error(`Varint too long`);
          }
          bigResult |= BigInt(nextByte & 0x7F) << BigInt(shift - 7);
          if ((nextByte & 0x80) === 0) {
            return Number(bigResult);
          }
        }
      }

      if ((byte & 0x80) === 0) {
        break; // last byte
      }

      shift += 7;
    }

    return result;
  }

  /**
   * Read a zigzag-encoded signed integer (varint) - Beast v2 format.
   * Returns a bigint.
   * Optimized to avoid promises unless necessary.
   */
  readZigzag(): bigint | Promise<bigint> {
    // Fast path: if we have enough buffered data, read synchronously
    if (this.buffer.length - this.bufferOffset >= 10) {
      const [value, newOffset] = readZigzag(this.buffer, this.bufferOffset);
      this.bufferOffset = newOffset;
      return value;
    }

    // Slow path: need to fetch from stream
    return this.readZigzagAsync();
  }

  private async readZigzagAsync(): Promise<bigint> {
    let result = 0n;
    let shift = 0n;

    while (true) {
      const byte = await this.readByte();

      result |= BigInt(byte & 0x7F) << shift;

      if ((byte & 0x80) === 0) {
        break; // last byte
      }

      shift += 7n;
      if (shift >= 64n) {
        throw new Error(`Zigzag varint too long`);
      }
    }

    // Decode zigzag: (n >> 1) ^ -(n & 1)
    const decoded = (result >> 1n) ^ -(result & 1n);
    return decoded;
  }

  /**
   * Read a little-endian float64 - Beast v2 format.
   * Validates NaN values are canonical.
   * Optimized to avoid promises unless necessary.
   */
  readFloat64LE(): number | Promise<number> {
    // Fast path: if we have enough buffered data, read synchronously
    if (this.buffer.length - this.bufferOffset >= 8) {
      this.tempBuffer8.set(this.buffer.subarray(this.bufferOffset, this.bufferOffset + 8));
      this.bufferOffset += 8;

      const bits = this.tempView8.getBigUint64(0, true); // little-endian

      // Check for NaN (exponent = all 1s, mantissa != 0)
      if ((bits & 0x7FF0000000000000n) === 0x7FF0000000000000n &&
          (bits & 0x000FFFFFFFFFFFFFn) !== 0n) {
        // It's a NaN - must be canonical quiet NaN (positive or negative)
        if (bits !== 0x7FF8000000000000n && bits !== 0xFFF8000000000000n) {
          throw new Error(`Non-canonical NaN`);
        }
      }

      return this.tempView8.getFloat64(0, true); // little-endian
    }

    // Slow path: need to fetch from stream
    return this.readFloat64LEAsync();
  }

  private async readFloat64LEAsync(): Promise<number> {
    await this.readBytes(this.tempBuffer8);
    const bits = this.tempView8.getBigUint64(0, true); // little-endian

    // Check for NaN (exponent = all 1s, mantissa != 0)
    if ((bits & 0x7FF0000000000000n) === 0x7FF0000000000000n &&
        (bits & 0x000FFFFFFFFFFFFFn) !== 0n) {
      // It's a NaN - must be canonical quiet NaN (positive or negative)
      if (bits !== 0x7FF8000000000000n && bits !== 0xFFF8000000000000n) {
        throw new Error(`Non-canonical NaN`);
      }
    }

    return this.tempView8.getFloat64(0, true); // little-endian
  }

  /**
   * Read a varint-length-prefixed UTF-8 string - Beast v2 format.
   */
  readStringUtf8Varint(): string | Promise<string> {
    if (this.buffer.length - this.bufferOffset >= 10) {
      // Fast path: if we have enough buffered data, read synchronously
      const [length, newOffset] = readVarint(this.buffer, this.bufferOffset);
      this.bufferOffset = newOffset;

      if (this.buffer.length - this.bufferOffset >= length) {
        const str = utf8Decode(this.buffer, this.bufferOffset, length);
        this.bufferOffset += length;
        return str;
      } else {
        return this.readStringUtf8SizedAsync(length);
      }
    }

    // Slow path: need to fetch from stream
    return this.readStringUtf8VarintAsync();
  }

  private async readStringUtf8VarintAsync(): Promise<string> {
    const length = await this.readVarint();

    if (length === 0) {
      return "";
    }

    // Read the string bytes
    const bytes = new Uint8Array(length);
    await this.readBytes(bytes);

    // Decode UTF-8
    const decoder = new TextDecoder('utf-8', { fatal: true });
    return decoder.decode(bytes);
  }

  private async readStringUtf8SizedAsync(length: number): Promise<string> {
    if (length === 0) {
      return "";
    }

    // Read the string bytes
    const bytes = new Uint8Array(length);
    await this.readBytes(bytes);

    // Decode UTF-8
    const decoder = new TextDecoder('utf-8', { fatal: true });
    return decoder.decode(bytes);
  }
}
