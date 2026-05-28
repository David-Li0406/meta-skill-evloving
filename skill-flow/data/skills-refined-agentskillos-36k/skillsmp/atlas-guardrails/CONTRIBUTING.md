# Contributing to Atlas Guardrails

Thank you for your interest in contributing!

## Development Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/atlas.git
    cd atlas
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Build**:
    ```bash
    npm run build
    ```

4.  **Run Tests**:
    ```bash
    npm test
    ```

## Code Quality

*   **Linting**: We use ESLint. Run `npm run lint` to check for issues.
*   **Formatting**: We use Prettier. Run `npm run format` to fix style.
*   **Tests**: Please ensure all new features are covered by tests. We aim for >80% coverage.

## Pull Request Process

1.  Fork the repo and create your branch from `main`.
2.  Add tests for your changes.
3.  Ensure `npm test` passes.
4.  Ensure `npm run lint` passes.
5.  Submit the PR!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
