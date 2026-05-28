/** @type {import('jest').Config} */
module.exports = {
  testEnvironment: 'jsdom',
  testMatch: ['**/tests/unit/**/*.test.[jt]s', '**/tests/validate-story/**/*.test.[jt]s', '**/tests/replay/**/*.spec.[jt]s', '**/tests/integration/**/*.test.[jt]s'],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
};
