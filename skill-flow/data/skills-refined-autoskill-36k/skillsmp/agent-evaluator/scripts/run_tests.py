#!/usr/bin/env python3
"""Generalized test runner for non-package test files.

Usage:
  run_tests.py [paths_or_globs...]

If no arguments are given, the script will search the current scripts directory
for files matching patterns: "*test*.py" and "*.test.py".

The runner imports each file as a unique module and runs any unittest.TestCase
instances discovered in them, aggregating all into a single test run.
"""
import os
import sys
import glob
import argparse
import importlib.util
import unittest
import hashlib


def discover_files(scripts_dir, patterns):
    files = []
    for pat in patterns:
        path = os.path.join(scripts_dir, pat)
        for f in glob.glob(path):
            if os.path.isfile(f) and f.endswith('.py'):
                files.append(os.path.normpath(f))
    return sorted(set(files))


def load_module_from_path(path):
    key = hashlib.md5(path.encode('utf-8')).hexdigest()[:8]
    mod_name = f'test_module_{key}'
    spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description='Run tests from arbitrary test files')
    parser.add_argument('paths', nargs='*', help='Files or glob patterns to run (relative to scripts dir)')
    args = parser.parse_args(argv)

    if args.paths:
        candidates = []
        for p in args.paths:
            # If path is absolute or exists relative to cwd, use it; else try relative to scripts_dir
            if os.path.isabs(p) and os.path.exists(p):
                candidates.append(os.path.normpath(p))
            else:
                abs_candidate = os.path.join(scripts_dir, p)
                if os.path.exists(abs_candidate):
                    candidates.append(os.path.normpath(abs_candidate))
                else:
                    # Treat as glob relative to scripts_dir
                    for g in glob.glob(os.path.join(scripts_dir, p)):
                        candidates.append(os.path.normpath(g))
        files = sorted(set(candidates))
    else:
        files = discover_files(scripts_dir, ['*test*.py', '*.test.py'])

    if not files:
        print('No test files found.')
        return 2

    loader = unittest.TestLoader()
    full_suite = unittest.TestSuite()

    for f in files:
        try:
            module = load_module_from_path(f)
        except Exception as e:
            print(f'Failed to import {f}: {e}')
            continue

        suite = loader.loadTestsFromModule(module)
        if suite.countTestCases() > 0:
            full_suite.addTests(suite)
        else:
            print(f'No tests discovered in {f}')

    if full_suite.countTestCases() == 0:
        print('No tests to run after discovery.')
        return 3

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(full_suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
