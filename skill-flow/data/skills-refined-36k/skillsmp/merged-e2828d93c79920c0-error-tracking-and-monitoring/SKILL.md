---
name: error-tracking-and-monitoring
description: Use this skill when you need to implement or improve error tracking and monitoring systems for real-time error detection and resolution.
---

# Error Tracking and Monitoring

You are an error tracking and observability expert specializing in implementing comprehensive error monitoring solutions. Set up error tracking systems, configure alerts, implement structured logging, and ensure teams can quickly identify and resolve production issues.

## Context
The user needs to implement or improve error tracking and monitoring. Focus on real-time error detection, meaningful alerts, error grouping, performance monitoring, and integration with popular error tracking services.

## Requirements
$ARGUMENTS

## Instructions

### 1. Error Tracking Analysis

Analyze current error handling and tracking:

**Error Analysis Script**
```python
import os
import re
import ast
from pathlib import Path
from collections import defaultdict

class ErrorTrackingAnalyzer:
    def analyze_codebase(self, project_path):
        """
        Analyze error handling patterns in codebase
        """
        analysis = {
            'error_handling': self._analyze_error_handling(project_path),
            'logging_usage': self._analyze_logging(project_path),
            'monitoring_setup': self._check_monitoring_setup(project_path),
            'error_patterns': self._identify_error_patterns(project_path),
            'recommendations': []
        }
        
        self._generate_recommendations(analysis)
        return analysis
    
    def _analyze_error_handling(self, project_path):
        """Analyze error handling patterns"""
        patterns = {
            'try_catch_blocks': 0,
            'unhandled_promises': 0,
            'generic_catches': 0,
            'error_types': defaultdict(int),
            'error_reporting': []
        }
        
        for file_path in Path(project_path).rglob('*.{js,ts,py,java,go}'):
            content = file_path.read_text(errors='ignore')
            
            # JavaScript/TypeScript patterns
            if file_path.suffix in ['.js', '.ts']:
                patterns['try_catch_blocks'] += len(re.findall(r'try\s*{', content))
                patterns['generic_catches'] += len(re.findall(r'catch\s*\([^)]*\)\s*{\s*}', content))
                patterns['unhandled_promises'] += len(re.findall(r'\.then\([^)]+\)(?!\.catch)', content))
            
            # Python patterns
            elif file_path.suffix == '.py':
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Try):
                            patterns['try_catch_blocks'] += 1
                            for handler in node.handlers:
                                if handler.type is None:
                                    patterns['generic_catches'] += 1
                except:
                    pass
        
        return patterns
    
    def _analyze_logging(self, project_path):
        """Analyze logging patterns"""
        logging_patterns = {
            'console_logs': 0,
            'structured_logging': False,
            'log_levels_used': set(),
            'logging_frameworks': []
        }
        
        # Check for logging frameworks
        package_files = ['package.json', 'requirements.txt', 'go.mod', 'pom.xml']
        for pkg_file in package_files:
            pkg_path = Path(project_path) / pkg_file
            if pkg_path.exists():
                content = pkg_path.read_text()
                if 'winston' in content or 'bunyan' in content:
                    logging_patterns['logging_frameworks'].append('winston/bunyan')
                if 'pino' in content:
                    logging_patterns['logging_frameworks'].append('pino')
                if 'logging' in content:
                    logging_patterns['logging_frameworks'].append('python-logging')
                if 'logrus' in content or 'zap' in content:
                    logging_patterns['logging_frameworks'].append('logrus/zap')
        
        return logging_patterns
```

### 2. Error Tracking Service Integration

Implement integrations with popular error tracking services:

**Sentry Integration**
```javascript
// sentry-setup.js
import * as Sentry from "@sentry/node";
import { ProfilingIntegration } from "@sentry/profiling-node";

class SentryErrorTracker {
    constructor(config) {
        this.config = config;
        this.initialized = false;
    }
    
    initialize() {
        Sentry.init({
            dsn: this.config.dsn,
            environment: this.config.environment,
            release: this.config.release,
            
            // Performance Monitoring
            tracesSampleRate: this.config.tracesSampleRate || 0.1,
            profilesSampleRate: this.config.profilesSampleRate || 0.1,
            
            // Integrations
            integrations: [
                // HTTP integration
                new Sentry.Integrations.Http({ tracing: true }),
                
                // Express integration
                new Sentry.Integrations.Express({
                    app: this.config.app,
                    router: true,
                    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
                }),
                
                // Database integration
                new Sentry.Integrations.Postgres(),
                new Sentry.Integrations.Mysql(),
                new Sentry.Integrations.Mongo(),
                
                // Profiling
                new ProfilingIntegration(),
                
                // Custom integrations
                ...this.getCustomIntegrations()
            ],
            
            // Filtering
            beforeSend: (event, hint) => {
                // Filter sensitive data
                if (event.request?.cookies) {
                    delete event.request.cookies;
                }
                
                // Filter out specific errors
                if (this.shouldFilterError(event, hint)) {
                    return null;
                }
                
                // Enhance error context
                return this.enhanceErrorEvent(event, hint);
            },
            
            // Breadcrumbs
            beforeBreadcrumb: (breadcrumb, hint) => {
                // Filter sensitive breadcrumbs
                if (breadcrumb.category === 'console' && breadcrumb.level === 'debug') {
                    return null;
                }
                
                return breadcrumb;
            },
            
            // Options
            attachStacktrace: true,
            shutdownTimeout: 5000,
            maxBreadcrumbs: 100,
            debug: this.config.debug || false,
            
            // Tags
            initialScope: {
                tags: {
                    component: this.config.component,
                    version: this.config.version
                },
                user: {
                    id: this.config.userId,
                    segment: this.config.userSegment
                }
            }
        });
        
        this.initialized = true;
        this.setupErrorHandlers();
    }
    
    setupErrorHandlers() {
        // Global error handler
        process.on('uncaughtException', (error) => {
            console.error('Uncaught Exception:', error);
            Sentry.captureException(error, {
                tags: { type: 'uncaught_exception' },
                level: 'fatal'
            });
            
            // Graceful shutdown
            this.gracefulShutdown();
        });
        
        // Promise rejection handler
        process.on('unhandledRejection', (reason, promise) => {
            console.error('Unhandled Rejection:', reason);
            Sentry.captureException(reason, {
                tags: { type: 'unhandled_rejection' },
                extra: { promise: promise.toString() }
            });
        });
    }
    
    enhanceErrorEvent(event, hint) {
        // Add custom context
        event.extra = {
            ...event.extra,
            memory: process.memoryUsage(),
            uptime: process.uptime(),
            nodeVersion: process.version
        };
        
        // Add user context
        if (this.config.getUserContext) {
            event.user = this.config.getUserContext();
        }
        
        // Add custom fingerprinting
        if (hint.originalException) {
            event.fingerprint = this.generateFingerprint(hint.originalException);
        }
        
        return event;
    }
    
    generateFingerprint(error) {
        // Custom fingerprinting logic
        const fingerprint = [];
        
        // Group by error type
        fingerprint.push(error.name || 'Error');
        
        // Group by error location
        if (error.stack) {
            const match = error.stack.match(/at\s+(.+?)\s+\(/);
            if (match) {
                fingerprint.push(match[1]);
            }
        }
        
        // Group by custom properties
        if (error.code) {
            fingerprint.push(error.code);
        }
        
        return fingerprint;
    }
}

// Express middleware
export const sentryMiddleware = {
    requestHandler: Sentry.Handlers.requestHandler(),
    tracingHandler: Sentry.Handlers.tracingHandler(),
    errorHandler: Sentry.Handlers.errorHandler({
        shouldHandleError(error) {
            // Capture 4xx and 5xx errors
            if (error.status >= 400) {
                return true;
            }
            return false;
        }
    })
};
```

**Custom Error Tracking Service**
```typescript
// error-tracker.ts
interface ErrorEvent {
    timestamp: Date;
    level: 'debug' | 'info' | 'warning' | 'error' | 'fatal';
    message: string;
    stack?: string;
    context: {
        user?: any;
        request?: any;
        environment: string;
        release: string;
        tags: Record<string, string>;
        extra: Record<string, any>;
    };
    fingerprint: string[];
}

class ErrorTracker {
    private queue: ErrorEvent[] = [];
    private batchSize = 10;
    private flushInterval = 5000;
    
    constructor(private config: ErrorTrackerConfig) {
        this.startBatchProcessor();
    }
    
    captureException(error: Error, context?: Partial<ErrorEvent['context']>) {
        const event: ErrorEvent = {
            timestamp: new Date(),
            level: 'error',
            message: error.message,
            stack: error.stack,
            context: {
                environment: this.config.environment,
                release: this.config.release,
                tags: {},
                extra: {},
                ...context
            },
            fingerprint: this.generateFingerprint(error)
        };
        
        this.addToQueue(event);
    }
    
    captureMessage(message: string, level: ErrorEvent['level'] = 'info') {
        const event: ErrorEvent = {
            timestamp: new Date(),
            level,
            message,
            context: {
                environment: this.config.environment,
                release: this.config.release,
                tags: {},
                extra: {}
            },
            fingerprint: [message]
        };
        
        this.addToQueue(event);
    }
    
    private addToQueue(event: ErrorEvent) {
        // Apply sampling
        if (Math.random() > this.config.sampleRate) {
            return;
        }
        
        // Filter sensitive data
        event = this.sanitizeEvent(event);
        
        // Add to queue
        this.queue.push(event);
        
        // Flush if queue is full
        if (this.queue.length >= this.batchSize) {
            this.flush();
        }
    }
    
    private sanitizeEvent(event: ErrorEvent): ErrorEvent {
        // Remove sensitive data
        const sensitiveKeys = ['password', 'token', 'secret', 'api_key'];
        
        const sanitize = (obj: any): any => {
            if (!obj || typeof obj !== 'object') return obj;
            
            const cleaned = Array.isArray(obj) ? [] : {};
            
            for (const [key, value] of Object.entries(obj)) {
                if (sensitiveKeys.some(k => key.toLowerCase().includes(k))) {
                    cleaned[key] = '[REDACTED]';
                } else if (typeof value === 'object') {
                    cleaned[key] = sanitize(value);
                } else {
                    cleaned[key] = value;
                }
            }
            
            return cleaned;
        };
        
        return {
            ...event,
            context: sanitize(event.context)
        };
    }
    
    private async flush() {
        if (this.queue.length === 0) return;
        
        const events = this.queue.splice(0, this.batchSize);
        
        try {
            await this.sendEvents(events);
        } catch (error) {
            console.error('Failed to send error events:', error);
            // Re-queue events
            this.queue.unshift(...events);
        }
    }
    
    private async sendEvents(events: ErrorEvent[]) {
        const response = await fetch(this.config.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.config.apiKey}`
            },
            body: JSON.stringify({ events })
        });
        
        if (!response.ok) {
            throw new Error(`Error tracking API returned ${response.status}`);
        }
    }
}
```

### 3. Structured Logging Implementation

Implement comprehensive structured logging:

**Advanced Logger**
```typescript
// structured-logger.ts
import winston from 'winston';
import { ElasticsearchTransport } from 'winston-elasticsearch';

class StructuredLogger {
    private logger: winston.Logger;
    
    constructor(config: LoggerConfig) {
        this.logger = winston.createLogger({
            level: config.level || 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.errors({ stack: true }),
                winston.format.metadata(),
                winston.format.json()
            ),
            defaultMeta: {
                service: config.service,
                environment: config.environment,
                version: config.version
            },
            transports: this.createTransports(config)
        });
    }
    
    private createTransports(config: LoggerConfig): winston.transport[] {
        const transports: winston.transport[] = [];
        
        // Console transport for development
        if (config.environment === 'development') {
            transports.push(new winston.transports.Console({
                format: winston.format.combine(
                    winston.format.colorize(),
                    winston.format.simple()
                )
            }));
        }
        
        // File transport for all environments
        transports.push(new winston.transports.File({
            filename: 'logs/error.log',
            level: 'error',
            maxsize: 5242880, // 5MB
            maxFiles: 5
        }));
        
        transports.push(new winston.transports.File({
            filename: 'logs/combined.log',
            maxsize: 5242880,
            maxFiles: 5
        }));
        
        // Elasticsearch transport for production
        if (config.elasticsearch) {
            transports.push(new ElasticsearchTransport({
                level: 'info',
                clientOpts: config.elasticsearch,
                index: `logs-${config.service}`,
                transformer: (logData) => {
                    return {
                        '@timestamp': logData.timestamp,
                        severity: logData.level,
                        message: logData.message,
                        fields: {
                            ...logData.metadata,
                            ...logData.defaultMeta
                        }
                    };
                }
            }));
        }
        
        return transports;
    }
    
    // Logging methods with context
    error(message: string, error?: Error, context?: any) {
        this.logger.error(message, {
            error: {
                message: error?.message,
                stack: error?.stack,
                name: error?.name
            },
            ...context
        });
    }
    
    warn(message: string, context?: any) {
        this.logger.warn(message, context);
    }
    
    info(message: string, context?: any) {
        this.logger.info(message, context);
    }
    
    debug(message: string, context?: any) {
        this.logger.debug(message, context);
    }
    
    // Performance logging
    startTimer(label: string): () => void {
        const start = Date.now();
        return () => {
            const duration = Date.now() - start;
            this.info(`Timer ${label}`, { duration, label });
        };
    }
    
    // Audit logging
    audit(action: string, userId: string, details: any) {
        this.info('Audit Event', {
            type: 'audit',
            action,
            userId,
            timestamp: new Date().toISOString(),
            details
        });
    }
}

// Request logging middleware
export function requestLoggingMiddleware(logger: StructuredLogger) {
    return (req: Request, res: Response, next: NextFunction) => {
        const start = Date.now();
        
        // Log request
        logger.info('Incoming request', {
            method: req.method,
            url: req.url,
            ip: req.ip,
            userAgent: req.get('user-agent')
        });
        
        // Log response
        res.on('finish', () => {
            const duration = Date.now() - start;
            logger.info('Request completed', {
                method: req.method,
                url: req.url,
                status: res.statusCode,
                duration,
                contentLength: res.get('content-length')
            });
        });
        
        next();
    };
}
```

### 4. Error Alerting Configuration

Set up intelligent alert