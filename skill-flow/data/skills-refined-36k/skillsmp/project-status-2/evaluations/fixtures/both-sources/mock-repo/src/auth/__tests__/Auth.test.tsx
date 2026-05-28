import { render, screen } from '@testing-library/react';
import { Auth } from '../Auth';

describe('Auth', () => {
  it('renders children', () => {
    render(<Auth><span>Test</span></Auth>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
});
