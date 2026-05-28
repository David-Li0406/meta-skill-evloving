# Commands Reference

Complete reference for all npm scripts in the monorepo.

## Global Commands

### Test
```bash
npm run test
```
Executes tests for:
- Mobile app (Jest)
- API server (pytest)

Runs the test suite to verify functionality across the monorepo.

### Typecheck
```bash
npm run typecheck
```
Performs type checking for:
- Mobile app (TypeScript)
- Web app (TypeScript)
- API server (Python mypy)

Verifies type safety across the monorepo.

### Lint
```bash
npm run lint
```
Executes linting for:
- Mobile app (React Native with ESLint)
- Web app (React with ESLint)
- API server (Python with Ruff)

Checks code style and quality according to project conventions.

## API Server Commands

### API Test
```bash
npm run api:test
```
Executes pytest tests for the FastAPI server to verify functionality and API behavior.

### API Typecheck
```bash
npm run api:typecheck
```
Executes mypy on the FastAPI server to perform Python type checking and ensure type safety.

### API Lint
```bash
npm run api:lint
```
Executes Ruff on the FastAPI server to check code style and quality according to Python conventions.

## Mobile App Commands

### Mobile iOS
```bash
npm run mobile:ios
```
Builds the React Native application and runs it on the iOS simulator.

**Requirements**: Xcode and an iOS simulator must be set up.

### Mobile Android
```bash
npm run mobile:android
```
Builds the React Native application and runs it on an Android emulator or connected Android device.

**Requirements**: Android SDK and emulator must be set up.

### Mobile Test
```bash
npm run mobile:test
```
Executes Jest tests for the React Native mobile application to verify functionality.

### Mobile Typecheck
```bash
npm run mobile:typecheck
```
Performs TypeScript type checking on the React Native mobile application to ensure type safety.

### Mobile Lint
```bash
npm run mobile:lint
```
Executes ESLint on the React Native mobile application to check code style and quality.

## Web App Commands

### Web Dev
```bash
npm run web:dev
```
Launches the React Vite development server with hot module replacement (HMR) for the web application.

**Default URL**: http://localhost:5173

### Web Build
```bash
npm run web:build
```
Builds the React Vite web application for production deployment.

**Output Directory**: `web-app/dist`

Creates optimized bundles ready for deployment.
