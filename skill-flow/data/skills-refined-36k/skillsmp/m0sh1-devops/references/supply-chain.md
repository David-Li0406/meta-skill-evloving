# Supply Chain Rules (m0sh1.cc)

## Table of Contents

1. Pinning Policy
2. Image Rebuilds
3. Scan Exceptions
4. Documentation

## 1. Pinning Policy

- Pin actions and container images by digest where feasible.
- If a tag is used temporarily, document it in `docs/history.md`.

## 2. Image Rebuilds

- Rebuild images to pick up base CVE fixes.
- Do not waive critical findings without a note in `docs/history.md`.

## 3. Scan Exceptions

- Harbor scan exceptions must include rationale and expiry.

## 4. Documentation

- Record temporary tag usage, recovery actions, and exceptions in `docs/history.md`.
