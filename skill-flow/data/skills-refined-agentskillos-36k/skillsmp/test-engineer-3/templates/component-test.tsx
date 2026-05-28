// =============================================================================
// Component Test Template - Faiston NEXO
// =============================================================================
// Usage: Copy and adapt for testing React components
// Framework: Vitest + React Testing Library
// =============================================================================

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";

// Import the component to test
// import { ComponentName } from "./ComponentName";

// =============================================================================
// Test Setup
// =============================================================================

// Create test query client with retry disabled
const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

// Wrapper with all providers
const AllProviders = ({ children }: { children: React.ReactNode }) => {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{children}</MemoryRouter>
    </QueryClientProvider>
  );
};

// Custom render with providers
const renderWithProviders = (ui: React.ReactElement) => {
  return render(ui, { wrapper: AllProviders });
};

// =============================================================================
// Tests
// =============================================================================

describe("ComponentName", () => {
  // Default props - adapt to your component
  const defaultProps = {
    title: "Test Title",
    onClick: vi.fn(),
    isLoading: false,
  };

  // Reset mocks between tests
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // ---------------------------------------------------------------------------
  // Rendering Tests
  // ---------------------------------------------------------------------------

  describe("rendering", () => {
    it("should render with correct content", () => {
      renderWithProviders(<div {...defaultProps} />);

      expect(screen.getByText("Test Title")).toBeInTheDocument();
    });

    it("should render loading state", () => {
      renderWithProviders(<div {...defaultProps} isLoading />);

      expect(screen.getByRole("status")).toBeInTheDocument();
    });

    it("should render empty state when no data", () => {
      renderWithProviders(<div {...defaultProps} items={[]} />);

      expect(screen.getByText(/no items/i)).toBeInTheDocument();
    });
  });

  // ---------------------------------------------------------------------------
  // Interaction Tests
  // ---------------------------------------------------------------------------

  describe("interactions", () => {
    it("should call onClick when button clicked", async () => {
      const user = userEvent.setup();
      renderWithProviders(<div {...defaultProps} />);

      await user.click(screen.getByRole("button"));

      expect(defaultProps.onClick).toHaveBeenCalledTimes(1);
    });

    it("should update input value on type", async () => {
      const user = userEvent.setup();
      renderWithProviders(<div {...defaultProps} />);

      const input = screen.getByRole("textbox");
      await user.type(input, "Hello");

      expect(input).toHaveValue("Hello");
    });

    it("should toggle state on checkbox click", async () => {
      const user = userEvent.setup();
      renderWithProviders(<div {...defaultProps} />);

      const checkbox = screen.getByRole("checkbox");
      await user.click(checkbox);

      expect(checkbox).toBeChecked();
    });
  });

  // ---------------------------------------------------------------------------
  // Async Tests
  // ---------------------------------------------------------------------------

  describe("async behavior", () => {
    it("should load data and display it", async () => {
      renderWithProviders(<div {...defaultProps} />);

      // Wait for loading to complete
      await waitFor(() => {
        expect(screen.getByText("Loaded Data")).toBeInTheDocument();
      });
    });

    it("should show error state on API failure", async () => {
      // Override MSW handler in test
      // server.use(http.get("/api/data", () => HttpResponse.error()));

      renderWithProviders(<div {...defaultProps} />);

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument();
      });
    });
  });

  // ---------------------------------------------------------------------------
  // Accessibility Tests
  // ---------------------------------------------------------------------------

  describe("accessibility", () => {
    it("should have no accessibility violations", async () => {
      const { container } = renderWithProviders(<div {...defaultProps} />);

      // Requires jest-axe: import { axe, toHaveNoViolations } from "jest-axe"
      // expect.extend(toHaveNoViolations);
      // const results = await axe(container);
      // expect(results).toHaveNoViolations();
    });

    it("should be keyboard navigable", async () => {
      const user = userEvent.setup();
      renderWithProviders(<div {...defaultProps} />);

      await user.tab();
      expect(screen.getByRole("button")).toHaveFocus();

      await user.keyboard("{Enter}");
      expect(defaultProps.onClick).toHaveBeenCalled();
    });
  });

  // ---------------------------------------------------------------------------
  // Edge Cases
  // ---------------------------------------------------------------------------

  describe("edge cases", () => {
    it("should handle empty string", () => {
      renderWithProviders(<div {...defaultProps} title="" />);
      // Assert appropriate behavior
    });

    it("should handle very long content", () => {
      const longTitle = "A".repeat(1000);
      renderWithProviders(<div {...defaultProps} title={longTitle} />);
      // Assert truncation or overflow handling
    });

    it("should handle special characters", () => {
      renderWithProviders(<div {...defaultProps} title="<script>alert('xss')</script>" />);
      // Assert proper escaping
    });
  });
});
