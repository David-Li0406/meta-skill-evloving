import { render, screen } from '@testing-library/react';
import { Auth } from '../Auth';

describe('Auth', () => {
  it('renders children correctly', () => {
    render(
      <Auth>
        <div>Test Content</div>
      </Auth>
    );

    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('applies auth-wrapper class', () => {
    const { container } = render(
      <Auth>
        <div>Test</div>
      </Auth>
    );

    expect(container.querySelector('.auth-wrapper')).toBeInTheDocument();
  });
});
