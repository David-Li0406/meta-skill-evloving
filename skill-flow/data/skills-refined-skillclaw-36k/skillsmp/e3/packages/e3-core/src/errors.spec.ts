/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for errors.ts - error types and helper functions
 */

import { describe, it } from 'node:test';
import assert from 'node:assert';
import {
  E3Error,
  RepositoryNotFoundError,
  WorkspaceNotFoundError,
  WorkspaceNotDeployedError,
  WorkspaceExistsError,
  WorkspaceLockError,
  type LockHolderInfo,
  PackageNotFoundError,
  PackageInvalidError,
  PackageExistsError,
  DatasetNotFoundError,
  TaskNotFoundError,
  ObjectNotFoundError,
  ObjectCorruptError,
  ExecutionCorruptError,
  DataflowError,
  DataflowAbortedError,
  PermissionDeniedError,
  isNotFoundError,
  isPermissionError,
  isExistsError,
  wrapError,
} from './errors.js';

describe('errors', () => {
  describe('E3Error base class', () => {
    it('sets name to constructor name', () => {
      const err = new E3Error('test message');
      assert.strictEqual(err.name, 'E3Error');
    });

    it('preserves message', () => {
      const err = new E3Error('test message');
      assert.strictEqual(err.message, 'test message');
    });

    it('is instanceof Error', () => {
      const err = new E3Error('test');
      assert.ok(err instanceof Error);
    });
  });

  describe('RepositoryNotFoundError', () => {
    it('includes path in message', () => {
      const err = new RepositoryNotFoundError('/path/to/repo');
      assert.ok(err.message.includes('/path/to/repo'));
      assert.strictEqual(err.path, '/path/to/repo');
    });

    it('is instanceof E3Error', () => {
      const err = new RepositoryNotFoundError('/path');
      assert.ok(err instanceof E3Error);
    });
  });

  describe('WorkspaceNotFoundError', () => {
    it('includes workspace name in message', () => {
      const err = new WorkspaceNotFoundError('myws');
      assert.ok(err.message.includes('myws'));
      assert.strictEqual(err.workspace, 'myws');
    });

    it('sets correct name', () => {
      const err = new WorkspaceNotFoundError('ws');
      assert.strictEqual(err.name, 'WorkspaceNotFoundError');
    });

    it('is instanceof E3Error', () => {
      const err = new WorkspaceNotFoundError('ws');
      assert.ok(err instanceof E3Error);
    });
  });

  describe('WorkspaceNotDeployedError', () => {
    it('includes workspace name in message', () => {
      const err = new WorkspaceNotDeployedError('myws');
      assert.ok(err.message.includes('myws'));
      assert.strictEqual(err.workspace, 'myws');
    });
  });

  describe('WorkspaceExistsError', () => {
    it('includes workspace name in message', () => {
      const err = new WorkspaceExistsError('myws');
      assert.ok(err.message.includes('myws'));
      assert.strictEqual(err.workspace, 'myws');
    });
  });

  describe('WorkspaceLockError', () => {
    it('includes workspace name in message without holder', () => {
      const err = new WorkspaceLockError('myws');
      assert.ok(err.message.includes('myws'));
      assert.ok(err.message.includes('locked'));
      assert.strictEqual(err.workspace, 'myws');
      assert.strictEqual(err.holder, undefined);
    });

    it('includes holder info in message when provided', () => {
      const holder: LockHolderInfo = {
        pid: 12345,
        acquiredAt: '2025-01-15T10:30:00Z',
        bootId: 'abc123',
        command: 'e3 start',
      };
      const err = new WorkspaceLockError('myws', holder);
      assert.ok(err.message.includes('myws'));
      assert.ok(err.message.includes('12345'));
      assert.ok(err.message.includes('2025-01-15T10:30:00Z'));
      assert.strictEqual(err.workspace, 'myws');
      assert.strictEqual(err.holder, holder);
    });

    it('is instanceof E3Error', () => {
      const err = new WorkspaceLockError('ws');
      assert.ok(err instanceof E3Error);
    });
  });

  describe('PackageNotFoundError', () => {
    it('includes name and version in message', () => {
      const err = new PackageNotFoundError('mypkg', '1.0.0');
      assert.ok(err.message.includes('mypkg'));
      assert.ok(err.message.includes('1.0.0'));
      assert.strictEqual(err.packageName, 'mypkg');
      assert.strictEqual(err.version, '1.0.0');
    });

    it('works without version', () => {
      const err = new PackageNotFoundError('mypkg');
      assert.ok(err.message.includes('mypkg'));
      assert.strictEqual(err.version, undefined);
    });
  });

  describe('PackageInvalidError', () => {
    it('includes reason in message', () => {
      const err = new PackageInvalidError('missing manifest');
      assert.ok(err.message.includes('missing manifest'));
      assert.strictEqual(err.reason, 'missing manifest');
    });
  });

  describe('PackageExistsError', () => {
    it('includes name and version', () => {
      const err = new PackageExistsError('pkg', '2.0.0');
      assert.ok(err.message.includes('pkg'));
      assert.ok(err.message.includes('2.0.0'));
    });
  });

  describe('DatasetNotFoundError', () => {
    it('includes workspace and path', () => {
      const err = new DatasetNotFoundError('ws', 'inputs.sales');
      assert.ok(err.message.includes('ws'));
      assert.ok(err.message.includes('inputs.sales'));
      assert.strictEqual(err.workspace, 'ws');
      assert.strictEqual(err.path, 'inputs.sales');
    });
  });

  describe('TaskNotFoundError', () => {
    it('includes task name', () => {
      const err = new TaskNotFoundError('mytask');
      assert.ok(err.message.includes('mytask'));
      assert.strictEqual(err.task, 'mytask');
    });
  });

  describe('ObjectNotFoundError', () => {
    it('shows abbreviated hash', () => {
      const hash = 'abcdef1234567890'.padEnd(64, '0');
      const err = new ObjectNotFoundError(hash);
      assert.ok(err.message.includes('abcdef12'));
      assert.strictEqual(err.hash, hash);
    });
  });

  describe('ObjectCorruptError', () => {
    it('includes hash and reason', () => {
      const hash = 'abcdef1234567890'.padEnd(64, '0');
      const err = new ObjectCorruptError(hash, 'invalid beast2 header');
      assert.ok(err.message.includes('abcdef12'));
      assert.ok(err.message.includes('invalid beast2 header'));
    });
  });

  describe('ExecutionCorruptError', () => {
    it('includes task and inputs hashes', () => {
      const taskHash = 'task'.padEnd(64, '0');
      const inputsHash = 'inputs'.padEnd(64, '0');
      const cause = new Error('decode failed');
      const err = new ExecutionCorruptError(taskHash, inputsHash, cause);
      assert.ok(err.message.includes('task0000'));
      assert.ok(err.message.includes('inputs00'));
      assert.ok(err.message.includes('decode failed'));
    });
  });

  describe('DataflowError', () => {
    it('preserves task results', () => {
      const results = [{ name: 'task1', cached: false, state: 'failed' as const, duration: 100 }];
      const err = new DataflowError('execution failed', results);
      assert.strictEqual(err.taskResults, results);
    });

    it('preserves cause and includes it in message', () => {
      const cause = new Error('root cause');
      const err = new DataflowError('wrapped', undefined, cause);
      assert.strictEqual(err.cause, cause);
      assert.ok(err.message.includes('wrapped'));
      assert.ok(err.message.includes('root cause'));
    });

    it('works without cause', () => {
      const err = new DataflowError('simple message');
      assert.strictEqual(err.message, 'simple message');
    });
  });

  describe('DataflowAbortedError', () => {
    it('has descriptive message', () => {
      const err = new DataflowAbortedError();
      assert.ok(err.message.includes('aborted'));
    });

    it('preserves partial results', () => {
      const results = [
        { name: 'task1', cached: false, state: 'success' as const, duration: 100 },
        { name: 'task2', cached: true, state: 'success' as const, duration: 0 },
      ];
      const err = new DataflowAbortedError(results);
      assert.strictEqual(err.partialResults, results);
    });

    it('works without partial results', () => {
      const err = new DataflowAbortedError();
      assert.strictEqual(err.partialResults, undefined);
    });

    it('is instanceof E3Error', () => {
      const err = new DataflowAbortedError();
      assert.ok(err instanceof E3Error);
    });
  });

  describe('PermissionDeniedError', () => {
    it('includes path', () => {
      const err = new PermissionDeniedError('/protected/file');
      assert.ok(err.message.includes('/protected/file'));
      assert.strictEqual(err.path, '/protected/file');
    });
  });

  describe('isNotFoundError', () => {
    it('returns true for ENOENT', () => {
      const err = new Error('not found') as NodeJS.ErrnoException;
      err.code = 'ENOENT';
      assert.strictEqual(isNotFoundError(err), true);
    });

    it('returns false for other error codes', () => {
      const err = new Error('permission denied') as NodeJS.ErrnoException;
      err.code = 'EACCES';
      assert.strictEqual(isNotFoundError(err), false);
    });

    it('returns false for regular errors', () => {
      assert.strictEqual(isNotFoundError(new Error('test')), false);
    });

    it('returns false for non-errors', () => {
      assert.strictEqual(isNotFoundError('string'), false);
      assert.strictEqual(isNotFoundError(null), false);
      assert.strictEqual(isNotFoundError(undefined), false);
    });
  });

  describe('isPermissionError', () => {
    it('returns true for EACCES', () => {
      const err = new Error('permission denied') as NodeJS.ErrnoException;
      err.code = 'EACCES';
      assert.strictEqual(isPermissionError(err), true);
    });

    it('returns false for other error codes', () => {
      const err = new Error('not found') as NodeJS.ErrnoException;
      err.code = 'ENOENT';
      assert.strictEqual(isPermissionError(err), false);
    });
  });

  describe('isExistsError', () => {
    it('returns true for EEXIST', () => {
      const err = new Error('already exists') as NodeJS.ErrnoException;
      err.code = 'EEXIST';
      assert.strictEqual(isExistsError(err), true);
    });

    it('returns false for other error codes', () => {
      const err = new Error('not found') as NodeJS.ErrnoException;
      err.code = 'ENOENT';
      assert.strictEqual(isExistsError(err), false);
    });
  });

  describe('wrapError', () => {
    it('returns E3Errors unchanged', () => {
      const original = new WorkspaceNotFoundError('ws');
      const wrapped = wrapError(original, 'context');
      assert.strictEqual(wrapped, original);
    });

    it('wraps regular errors with context', () => {
      const original = new Error('something went wrong');
      const wrapped = wrapError(original, 'failed to do thing');
      assert.ok(wrapped instanceof E3Error);
      assert.ok(wrapped.message.includes('failed to do thing'));
      assert.ok(wrapped.message.includes('something went wrong'));
    });

    it('wraps non-errors', () => {
      const wrapped = wrapError('string error', 'context');
      assert.ok(wrapped instanceof E3Error);
      assert.ok(wrapped.message.includes('context'));
      assert.ok(wrapped.message.includes('string error'));
    });
  });
});
