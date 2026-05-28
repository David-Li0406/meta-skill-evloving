import { handler } from './index';

const mockEvent = { httpMethod: 'GET', path: '/', headers: {}, queryStringParameters: null, body: null } as never;

const mockContext = { awsRequestId: 'local-test-id', functionName: 'your-lambda-name' } as never;

const invoke = async (): Promise<void> => {
  try {
    const result = await handler(mockEvent, mockContext);

    console.log('response', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('error', error);
  }
};

void invoke();
