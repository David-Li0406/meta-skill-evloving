import type { Meta, StoryObj } from '@storybook/vue3';
import { expect, within } from '@storybook/test';
import ComponentName from './ComponentName.vue';

const meta = {
  title: 'Category/ComponentName', // e.g., 'Atoms/Button', 'Molecules/FormField'
  component: ComponentName,
  tags: ['autodocs'],
  argTypes: {
    // Add your prop controls and descriptions here
    // Example:
    // label: {
    //   control: 'text',
    //   description: 'Button label text',
    // },
    // variant: {
    //   control: 'select',
    //   options: ['solid', 'outline', 'soft', 'ghost'],
    //   description: 'Button visual style variant',
    // },
  },
} satisfies Meta<typeof ComponentName>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Default component state with minimal props
 *
 * TDD Note: Start with this test ONLY, run it to failure (RED),
 * then implement minimal component code to pass (GREEN).
 */
export const Default: Story = {
  args: {
    // Add minimal props needed for basic rendering
    // Example:
    // label: 'Click me',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Add your test assertions here
    // Example for testing a button:
    // const button = await canvas.findByRole('button', { name: /click me/i });
    // await expect(button).toBeInTheDocument();

    // Example for testing an input:
    // const input = await canvas.findByPlaceholderText(/enter text/i);
    // await expect(input).toBeInTheDocument();
  },
};

/**
 * Add additional stories ONE AT A TIME after Default passes
 *
 * Examples of common story patterns:
 *
 * - WithIcon: Component with an icon
 * - Loading: Component in loading state
 * - Disabled: Component in disabled state
 * - WithError: Component showing error state
 * - Required: Component marked as required
 * - [Variant]: Different visual variants (Outline, Soft, Ghost, etc.)
 */

// Uncomment and customize as you add new tests:

// export const Loading: Story = {
//   args: {
//     label: 'Loading...',
//     loading: true,
//   },
//   play: async ({ canvasElement }) => {
//     const canvas = within(canvasElement);
//     // Test loading indicator appears
//   },
// };

// export const Disabled: Story = {
//   args: {
//     label: 'Disabled',
//     disabled: true,
//   },
//   play: async ({ canvasElement }) => {
//     const canvas = within(canvasElement);
//     // Test disabled state
//   },
// };
