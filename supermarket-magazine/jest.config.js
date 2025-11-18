module.exports = {
  testEnvironment: "node",
  setupFilesAfterEnv: ["<rootDir>/setupTests.js"],
  testMatch: ["**/tests/**/*.test.js"],
  collectCoverage: true,
  coverageDirectory: "coverage"
};