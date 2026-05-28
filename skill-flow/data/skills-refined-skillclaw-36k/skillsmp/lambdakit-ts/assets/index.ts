import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';

import { Logger } from '@aws-lambda-powertools/logger';
import { injectLambdaContext } from '@aws-lambda-powertools/logger/middleware';
import middy from '@middy/core';

import { greet } from '@functions/greet';

const logger = new Logger({ serviceName: 'your-lambda-name', logLevel: 'INFO' });

const lambdaHandler = async (event: APIGatewayProxyEvent, context: Context): Promise<APIGatewayProxyResult> => {
  logger.debug('Processing request', { event, context });

  try {
    await greet(logger);

    return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) };
  } catch (error) {
    logger.error('error', { error, event });

    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: error instanceof Error ? error.message : 'Unknown error' }),
    };
  }
};

export const handler = middy(lambdaHandler).use(injectLambdaContext(logger));
