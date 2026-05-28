/**
 * Better Auth Client Configuration Template
 *
 * Usage:
 * 1. Copy this file to your project (e.g., src/lib/auth-client.ts)
 * 2. Add plugins matching your server configuration
 * 3. Import and use authClient in your components
 */

import { createAuthClient } from "better-auth/client";

// Import plugins matching your server config
// import { twoFactorClient } from "better-auth/client/plugins";
// import { magicLinkClient } from "better-auth/client/plugins";
// import { organizationClient } from "better-auth/client/plugins";
// import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  // Base URL of your auth server
  baseURL: process.env.NEXT_PUBLIC_APP_URL,

  // Plugins (must match server plugins)
  plugins: [
    // Uncomment as needed:

    // twoFactorClient({
    //   onTwoFactorRedirect() {
    //     window.location.href = "/2fa";
    //   },
    // }),

    // magicLinkClient(),

    // organizationClient(),

    // jwtClient(),
  ],

  // Global fetch options
  // fetchOptions: {
  //   onError: async (ctx) => {
  //     if (ctx.response.status === 429) {
  //       console.log("Rate limited");
  //     }
  //   },
  // },
});

// Type exports for convenience
export type Session = typeof authClient.$Infer.Session;
export type User = Session["user"];
