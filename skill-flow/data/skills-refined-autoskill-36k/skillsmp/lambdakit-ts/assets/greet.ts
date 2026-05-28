import { Logger } from '@aws-lambda-powertools/logger';

export const greet = async (logger: Logger): Promise<void> => {
  await new Promise((resolve) => setTimeout(resolve, 10));

  logger.info('oh hai!');
};
