import {
    ExceptionFilter,
    Catch,
    ArgumentsHost,
    HttpException,
    HttpStatus,
    Logger,
} from '@nestjs/common';
import { Request, Response } from 'express';

/**
 * Global HTTP Exception Filter
 * 
 * Catches all HttpExceptions and returns a standardized JSON response.
 * Prevents stack traces from leaking to clients in production.
 */
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
    private readonly logger = new Logger(HttpExceptionFilter.name);

    catch(exception: HttpException, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();
        const request = ctx.getRequest<Request>();
        const status = exception.getStatus();

        // Get the exception response (can be string or object)
        const exceptionResponse = exception.getResponse();

        // Extract message from various formats
        let message: string | string[];
        if (typeof exceptionResponse === 'string') {
            message = exceptionResponse;
        } else if (typeof exceptionResponse === 'object') {
            const responseObj = exceptionResponse as Record<string, unknown>;
            message = (responseObj.message as string | string[]) || exception.message;
        } else {
            message = exception.message;
        }

        const errorResponse = {
            statusCode: status,
            timestamp: new Date().toISOString(),
            path: request.url,
            method: request.method,
            message,
        };

        // Log the error for internal monitoring
        this.logger.warn(
            `${request.method} ${request.url} - ${status}: ${JSON.stringify(message)}`,
        );

        response.status(status).json(errorResponse);
    }
}

/**
 * Global All Exceptions Filter
 * 
 * Catches ALL exceptions (including non-HTTP ones) and returns a safe error.
 * Critical for security - prevents internal errors from exposing sensitive data.
 */
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
    private readonly logger = new Logger(AllExceptionsFilter.name);

    catch(exception: unknown, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();
        const request = ctx.getRequest<Request>();

        // Determine if it's an HttpException
        const isHttpException = exception instanceof HttpException;
        const status = isHttpException
            ? exception.getStatus()
            : HttpStatus.INTERNAL_SERVER_ERROR;

        // In production, never expose internal error details
        const isProd = process.env.NODE_ENV === 'production';

        let message: string;
        if (isHttpException) {
            const exceptionResponse = exception.getResponse();
            if (typeof exceptionResponse === 'string') {
                message = exceptionResponse;
            } else if (typeof exceptionResponse === 'object') {
                const responseObj = exceptionResponse as Record<string, unknown>;
                message = (responseObj.message as string) || exception.message;
            } else {
                message = exception.message;
            }
        } else {
            message = isProd
                ? 'Une erreur interne est survenue'
                : (exception as Error).message || 'Unknown error';
        }

        const errorResponse = {
            statusCode: status,
            timestamp: new Date().toISOString(),
            path: request.url,
            method: request.method,
            message,
            // Only include error details in development
            ...(isProd ? {} : { error: (exception as Error).name }),
        };

        // Log full error internally
        this.logger.error(
            `${request.method} ${request.url} - ${status}`,
            exception instanceof Error ? exception.stack : String(exception),
        );

        response.status(status).json(errorResponse);
    }
}
