// Example page with AppConfig loading
// This template shows the complete pattern for pages that need configuration

import type { GetServerSideProps } from 'next';
import Head from 'next/head';
import type { ReactElement, ReactNode } from 'react';

import MainContent from '../components/MainContent';
import { useAppConfig } from '../contexts/AppConfigContext';
import { loadAppConfig } from '../lib/config/loader';

// Define prop types (can be empty if no additional props needed)
type PageProps = Record<string, never>;

export default function MyPage(_props: PageProps) {
  // Access configuration via hook
  const appConfig = useAppConfig();

  return (
    <>
      <Head>
        <title>{appConfig.siteName}</title>
        <meta name="description" content={appConfig.siteDescription} />
      </Head>

      <div>
        <h1>My Page</h1>
        <p>Environment: {appConfig.environmentName}</p>
        <p>Base URL: {appConfig.baseUrl}</p>

        {/* Conditional rendering based on config */}
        {appConfig.showPreview && appConfig.previewLink && (
          <a href={appConfig.previewLink}>Preview</a>
        )}

        {/* Use other config values as needed */}
        <a href={appConfig.docsBaseUrl}>Documentation</a>
      </div>
    </>
  );
}

// Optional: Define custom layout (if needed)
MyPage.getLayout = function getLayout(page: ReactElement): ReactNode {
  return <MainContent>{page}</MainContent>;
};

// REQUIRED: getServerSideProps to load configuration
export const getServerSideProps: GetServerSideProps<PageProps> = async () => {
  // Load app configuration from filesystem
  const appConfig = await loadAppConfig();

  return {
    props: {
      appConfig, // Required: _app.tsx extracts this into AppConfigProvider
    },
  };
};
