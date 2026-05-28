// Example component using AppConfig
// This template shows how components access configuration

import { useAppConfig } from '../contexts/AppConfigContext';

type MyComponentProps = {
  // Component-specific props
  title?: string;
};

/**
 * Example component that uses application configuration.
 *
 * This component must be used within a page that implements getServerSideProps
 * with loadAppConfig(), ensuring the AppConfigProvider is available.
 */
export default function MyComponent({ title }: MyComponentProps) {
  // Access configuration via hook
  // This will throw an error if used outside AppConfigProvider
  const config = useAppConfig();

  return (
    <div>
      <h2>{title || 'Welcome'}</h2>

      {/* Use configuration values */}
      <p>Site: {config.siteName}</p>
      <p>Environment: {config.environmentName}</p>

      {/* Conditional rendering based on config */}
      {config.enableAppsMenu && (
        <nav>
          <h3>Applications</h3>
          <ul>
            {config.appLinks.map((link, index) => (
              <li key={index}>
                <a
                  href={link.href}
                  target={link.internal ? undefined : '_blank'}
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      )}

      {/* Use URLs from config */}
      <div>
        <a href={config.docsBaseUrl}>Documentation</a>
        <a href={config.timesSquareUrl}>Times Square</a>
      </div>

      {/* Environment-specific behavior */}
      {config.environmentName === 'development' && (
        <div style={{ background: 'yellow', padding: '1rem' }}>
          Development Mode - {config.baseUrl}
        </div>
      )}
    </div>
  );
}

// Example of a hook that uses config internally
export function useDocsUrl(path: string): string {
  const config = useAppConfig();
  return `${config.docsBaseUrl}${path}`;
}

// Example of a component that conditionally renders based on config
export function PreviewBanner() {
  const config = useAppConfig();

  if (!config.showPreview || !config.previewLink) {
    return null;
  }

  return (
    <div>
      <p>
        Check out what's coming: <a href={config.previewLink}>Preview</a>
      </p>
    </div>
  );
}
