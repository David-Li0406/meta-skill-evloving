import React from 'react';

interface AuthProps {
  children: React.ReactNode;
}

/**
 * Auth component using Clerk
 */
export const Auth: React.FC<AuthProps> = ({ children }) => {
  return (
    <div className="auth-wrapper">
      {children}
    </div>
  );
};

export default Auth;
