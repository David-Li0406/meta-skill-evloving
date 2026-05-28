# Shopify Apps

## Patterns


---
  #### **Name**
React Router App Setup
  #### **Description**
Modern Shopify app template with React Router
  #### **When**
Starting a new Shopify app
  #### **Template**
    # Create new Shopify app with CLI
    npm init @shopify/app@latest my-shopify-app
    
    # Project structure
    # my-shopify-app/
    # ├── app/
    # │   ├── routes/
    # │   │   ├── app._index.tsx        # Main app page
    # │   │   ├── app.tsx               # App layout with providers
    # │   │   ├── auth.$.tsx            # Auth callback
    # │   │   └── webhooks.tsx          # Webhook handler
    # │   ├── shopify.server.ts         # Server configuration
    # │   └── root.tsx                  # Root layout
    # ├── extensions/                   # App extensions
    # ├── shopify.app.toml              # App configuration
    # └── package.json
    
    // shopify.app.toml
    name = "my-shopify-app"
    client_id = "your-client-id"
    application_url = "https://your-app.example.com"
    
    [access_scopes]
    scopes = "read_products,write_products,read_orders"
    
    [webhooks]
    api_version = "2024-10"
    
    [webhooks.subscriptions]
    topics = ["orders/create", "products/update"]
    uri = "/webhooks"
    
    [auth]
    redirect_urls = ["https://your-app.example.com/auth/callback"]
    
    // app/shopify.server.ts
    import "@shopify/shopify-app-remix/adapters/node";
    import {
      LATEST_API_VERSION,
      shopifyApp,
      DeliveryMethod,
    } from "@shopify/shopify-app-remix/server";
    import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
    import prisma from "./db.server";
    
    const shopify = shopifyApp({
      apiKey: process.env.SHOPIFY_API_KEY!,
      apiSecretKey: process.env.SHOPIFY_API_SECRET!,
      scopes: process.env.SCOPES?.split(","),
      appUrl: process.env.SHOPIFY_APP_URL!,
      authPathPrefix: "/auth",
      sessionStorage: new PrismaSessionStorage(prisma),
      distribution: AppDistribution.AppStore,
      future: {
        unstable_newEmbeddedAuthStrategy: true,
      },
      ...(process.env.SHOP_CUSTOM_DOMAIN
        ? { customShopDomains: [process.env.SHOP_CUSTOM_DOMAIN] }
        : {}),
    });
    
    export default shopify;
    export const apiVersion = LATEST_API_VERSION;
    export const authenticate = shopify.authenticate;
    export const sessionStorage = shopify.sessionStorage;
    
  #### **Notes**
    - React Router replaced Remix as recommended template (late 2024)
    - unstable_newEmbeddedAuthStrategy enabled by default for new apps
    - Webhooks configured in shopify.app.toml, not code
    - Run 'shopify app deploy' to apply configuration changes

---
  #### **Name**
Embedded App with App Bridge
  #### **Description**
Render app embedded in Shopify Admin
  #### **When**
Building embedded admin app
  #### **Template**
    // app/routes/app.tsx - App layout with providers
    import { Link, Outlet, useLoaderData, useRouteError } from "@remix-run/react";
    import { AppProvider } from "@shopify/shopify-app-remix/react";
    import polarisStyles from "@shopify/polaris/build/esm/styles.css?url";
    
    export const links = () => [{ rel: "stylesheet", href: polarisStyles }];
    
    export async function loader({ request }: LoaderFunctionArgs) {
      await authenticate.admin(request);
      return json({ apiKey: process.env.SHOPIFY_API_KEY! });
    }
    
    export default function App() {
      const { apiKey } = useLoaderData<typeof loader>();
    
      return (
        <AppProvider isEmbeddedApp apiKey={apiKey}>
          <ui-nav-menu>
            <Link to="/app" rel="home">Home</Link>
            <Link to="/app/products">Products</Link>
            <Link to="/app/settings">Settings</Link>
          </ui-nav-menu>
          <Outlet />
        </AppProvider>
      );
    }
    
    export function ErrorBoundary() {
      const error = useRouteError();
      return (
        <AppProvider isEmbeddedApp>
          <Page>
            <Card>
              <Text as="p" variant="bodyMd">
                Something went wrong. Please try again.
              </Text>
            </Card>
          </Page>
        </AppProvider>
      );
    }
    
    // app/routes/app._index.tsx - Main app page
    import {
      Page,
      Layout,
      Card,
      Text,
      BlockStack,
      Button,
    } from "@shopify/polaris";
    import { TitleBar } from "@shopify/app-bridge-react";
    
    export async function loader({ request }: LoaderFunctionArgs) {
      const { admin } = await authenticate.admin(request);
    
      // GraphQL query
      const response = await admin.graphql(`
        query {
          shop {
            name
            email
          }
        }
      `);
    
      const { data } = await response.json();
      return json({ shop: data.shop });
    }
    
    export default function Index() {
      const { shop } = useLoaderData<typeof loader>();
    
      return (
        <Page>
          <TitleBar title="My Shopify App" />
          <Layout>
            <Layout.Section>
              <Card>
                <BlockStack gap="200">
                  <Text as="h2" variant="headingMd">
                    Welcome to {shop.name}!
                  </Text>
                  <Text as="p" variant="bodyMd">
                    Your app is now connected to this store.
                  </Text>
                  <Button variant="primary">
                    Get Started
                  </Button>
                </BlockStack>
              </Card>
            </Layout.Section>
          </Layout>
        </Page>
      );
    }
    
  #### **Notes**
    - App Bridge required for Built for Shopify (July 2025)
    - Polaris components match Shopify Admin design
    - TitleBar and navigation from App Bridge
    - Always authenticate requests with authenticate.admin()

---
  #### **Name**
Webhook Handling
  #### **Description**
Secure webhook processing with HMAC verification
  #### **When**
Receiving Shopify webhooks
  #### **Template**
    // app/routes/webhooks.tsx
    import type { ActionFunctionArgs } from "@remix-run/node";
    import { authenticate } from "../shopify.server";
    import db from "../db.server";
    
    export const action = async ({ request }: ActionFunctionArgs) => {
      // Authenticate webhook (verifies HMAC signature)
      const { topic, shop, payload, admin } = await authenticate.webhook(request);
    
      console.log(`Received ${topic} webhook for ${shop}`);
    
      // Process based on topic
      switch (topic) {
        case "ORDERS_CREATE":
          // Queue for async processing
          await queueOrderProcessing(payload);
          break;
    
        case "PRODUCTS_UPDATE":
          await handleProductUpdate(shop, payload);
          break;
    
        case "APP_UNINSTALLED":
          // Clean up shop data
          await db.session.deleteMany({ where: { shop } });
          await db.shopData.delete({ where: { shop } });
          break;
    
        case "CUSTOMERS_DATA_REQUEST":
        case "CUSTOMERS_REDACT":
        case "SHOP_REDACT":
          // GDPR webhooks - mandatory
          await handleGDPRWebhook(topic, payload);
          break;
    
        default:
          console.log(`Unhandled webhook topic: ${topic}`);
      }
    
      // CRITICAL: Return 200 immediately
      // Shopify expects response within 5 seconds
      return new Response(null, { status: 200 });
    };
    
    // Process asynchronously after responding
    async function queueOrderProcessing(payload: any) {
      // Use a job queue (BullMQ, etc.)
      await jobQueue.add("process-order", {
        orderId: payload.id,
        orderData: payload,
      });
    }
    
    async function handleProductUpdate(shop: string, payload: any) {
      // Quick sync operation only
      await db.product.upsert({
        where: { shopifyId: payload.id },
        update: {
          title: payload.title,
          updatedAt: new Date(),
        },
        create: {
          shopifyId: payload.id,
          shop,
          title: payload.title,
        },
      });
    }
    
    async function handleGDPRWebhook(topic: string, payload: any) {
      // GDPR compliance - required for all apps
      switch (topic) {
        case "CUSTOMERS_DATA_REQUEST":
          // Return customer data within 30 days
          break;
        case "CUSTOMERS_REDACT":
          // Delete customer data
          break;
        case "SHOP_REDACT":
          // Delete all shop data (48 hours after uninstall)
          break;
      }
    }
    
  #### **Notes**
    - Respond within 5 seconds or webhook fails
    - Use job queues for heavy processing
    - GDPR webhooks are mandatory for App Store
    - HMAC verification handled by authenticate.webhook()

---
  #### **Name**
GraphQL Admin API
  #### **Description**
Query and mutate shop data with GraphQL
  #### **When**
Interacting with Shopify Admin API
  #### **Template**
    // GraphQL queries with authenticated admin client
    export async function loader({ request }: LoaderFunctionArgs) {
      const { admin } = await authenticate.admin(request);
    
      // Query products with pagination
      const response = await admin.graphql(`
        query GetProducts($first: Int!, $after: String) {
          products(first: $first, after: $after) {
            edges {
              node {
                id
                title
                status
                totalInventory
                priceRangeV2 {
                  minVariantPrice {
                    amount
                    currencyCode
                  }
                }
                images(first: 1) {
                  edges {
                    node {
                      url
                      altText
                    }
                  }
                }
              }
              cursor
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      `, {
        variables: {
          first: 10,
          after: null,
        },
      });
    
      const { data } = await response.json();
      return json({ products: data.products });
    }
    
    // Mutations
    export async function action({ request }: ActionFunctionArgs) {
      const { admin } = await authenticate.admin(request);
      const formData = await request.formData();
      const productId = formData.get("productId");
      const newTitle = formData.get("title");
    
      const response = await admin.graphql(`
        mutation UpdateProduct($input: ProductInput!) {
          productUpdate(input: $input) {
            product {
              id
              title
            }
            userErrors {
              field
              message
            }
          }
        }
      `, {
        variables: {
          input: {
            id: productId,
            title: newTitle,
          },
        },
      });
    
      const { data } = await response.json();
    
      if (data.productUpdate.userErrors.length > 0) {
        return json({
          errors: data.productUpdate.userErrors,
        }, { status: 400 });
      }
    
      return json({ product: data.productUpdate.product });
    }
    
    // Bulk operations for large datasets
    async function bulkUpdateProducts(admin: AdminApiContext) {
      // Create bulk operation
      const response = await admin.graphql(`
        mutation {
          bulkOperationRunMutation(
            mutation: "mutation call($input: ProductInput!) {
              productUpdate(input: $input) { product { id } }
            }",
            stagedUploadPath: "path-to-staged-upload"
          ) {
            bulkOperation {
              id
              status
            }
            userErrors {
              message
            }
          }
        }
      `);
    
      // Poll for completion or use webhook
      // BULK_OPERATIONS_FINISH webhook
    }
    
  #### **Notes**
    - GraphQL required for new public apps (April 2025)
    - Rate limit: 1000 points per 60 seconds
    - Use bulk operations for >250 items
    - Direct API access available from App Bridge

---
  #### **Name**
Billing API Integration
  #### **Description**
Implement subscription billing for your app
  #### **When**
Monetizing Shopify app
  #### **Template**
    // app/routes/app.billing.tsx
    import { json, redirect } from "@remix-run/node";
    import { Page, Card, Button, BlockStack, Text } from "@shopify/polaris";
    import { authenticate } from "../shopify.server";
    
    const PLANS = {
      basic: {
        name: "Basic",
        amount: 9.99,
        currencyCode: "USD",
        interval: "EVERY_30_DAYS",
      },
      pro: {
        name: "Pro",
        amount: 29.99,
        currencyCode: "USD",
        interval: "EVERY_30_DAYS",
      },
    };
    
    export async function loader({ request }: LoaderFunctionArgs) {
      const { admin, billing } = await authenticate.admin(request);
    
      // Check current subscription
      const response = await admin.graphql(`
        query {
          currentAppInstallation {
            activeSubscriptions {
              id
              name
              status
              lineItems {
                plan {
                  pricingDetails {
                    ... on AppRecurringPricing {
                      price {
                        amount
                        currencyCode
                      }
                      interval
                    }
                  }
                }
              }
            }
          }
        }
      `);
    
      const { data } = await response.json();
      return json({
        subscription: data.currentAppInstallation.activeSubscriptions[0],
      });
    }
    
    export async function action({ request }: ActionFunctionArgs) {
      const { admin, session } = await authenticate.admin(request);
      const formData = await request.formData();
      const planKey = formData.get("plan") as keyof typeof PLANS;
      const plan = PLANS[planKey];
    
      // Create subscription charge
      const response = await admin.graphql(`
        mutation CreateSubscription($name: String!, $lineItems: [AppSubscriptionLineItemInput!]!, $returnUrl: URL!, $test: Boolean) {
          appSubscriptionCreate(
            name: $name
            lineItems: $lineItems
            returnUrl: $returnUrl
            test: $test
          ) {
            appSubscription {
              id
              status
            }
            confirmationUrl
            userErrors {
              field
              message
            }
          }
        }
      `, {
        variables: {
          name: plan.name,
          lineItems: [
            {
              plan: {
                appRecurringPricingDetails: {
                  price: {
                    amount: plan.amount,
                    currencyCode: plan.currencyCode,
                  },
                  interval: plan.interval,
                },
              },
            },
          ],
          returnUrl: `https://${session.shop}/admin/apps/${process.env.SHOPIFY_API_KEY}`,
          test: process.env.NODE_ENV !== "production",
        },
      });
    
      const { data } = await response.json();
    
      if (data.appSubscriptionCreate.userErrors.length > 0) {
        return json({
          errors: data.appSubscriptionCreate.userErrors,
        }, { status: 400 });
      }
    
      // Redirect merchant to approve charge
      return redirect(data.appSubscriptionCreate.confirmationUrl);
    }
    
    export default function Billing() {
      const { subscription } = useLoaderData<typeof loader>();
      const submit = useSubmit();
    
      return (
        <Page title="Billing">
          <Card>
            {subscription ? (
              <BlockStack gap="200">
                <Text as="p" variant="bodyMd">
                  Current plan: {subscription.name}
                </Text>
                <Text as="p" variant="bodyMd">
                  Status: {subscription.status}
                </Text>
              </BlockStack>
            ) : (
              <BlockStack gap="400">
                <Text as="h2" variant="headingMd">
                  Choose a Plan
                </Text>
                <Button onClick={() => submit({ plan: "basic" }, { method: "post" })}>
                  Basic - $9.99/month
                </Button>
                <Button onClick={() => submit({ plan: "pro" }, { method: "post" })}>
                  Pro - $29.99/month
                </Button>
              </BlockStack>
            )}
          </Card>
        </Page>
      );
    }
    
  #### **Notes**
    - Use test: true for development stores
    - Merchant must approve subscription
    - One recurring + one usage charge per app max
    - 30-day billing cycle for recurring charges

---
  #### **Name**
App Extension Development
  #### **Description**
Extend Shopify checkout, admin, or storefront
  #### **When**
Building app extensions
  #### **Template**
    # shopify.extension.toml (in extensions/my-extension/)
    api_version = "2024-10"
    
    [[extensions]]
    type = "ui_extension"
    name = "Product Customizer"
    handle = "product-customizer"
    
    [[extensions.targeting]]
    target = "admin.product-details.block.render"
    module = "./src/AdminBlock.tsx"
    
    [extensions.capabilities]
    api_access = true
    
    [extensions.settings]
    [[extensions.settings.fields]]
    key = "show_preview"
    type = "boolean"
    name = "Show Preview"
    
    // extensions/my-extension/src/AdminBlock.tsx
    import {
      reactExtension,
      useApi,
      useSettings,
      BlockStack,
      Text,
      Button,
      InlineStack,
    } from "@shopify/ui-extensions-react/admin";
    
    export default reactExtension(
      "admin.product-details.block.render",
      () => <ProductCustomizer />
    );
    
    function ProductCustomizer() {
      const { data, extension } = useApi<"admin.product-details.block.render">();
      const settings = useSettings();
    
      const productId = data?.selected?.[0]?.id;
    
      const handleCustomize = async () => {
        // API calls from extension
        const result = await fetch("/api/customize", {
          method: "POST",
          body: JSON.stringify({ productId }),
        });
      };
    
      return (
        <BlockStack gap="base">
          <Text fontWeight="bold">Product Customizer</Text>
          <Text>
            Customize product: {productId}
          </Text>
          {settings.show_preview && (
            <Text size="small">Preview enabled</Text>
          )}
          <InlineStack gap="base">
            <Button onPress={handleCustomize}>
              Apply Customization
            </Button>
          </InlineStack>
        </BlockStack>
      );
    }
    
    // Checkout UI Extension
    // [[extensions.targeting]]
    // target = "purchase.checkout.block.render"
    
    // extensions/checkout-ext/src/Checkout.tsx
    import {
      reactExtension,
      Banner,
      useCartLines,
      useTotalAmount,
    } from "@shopify/ui-extensions-react/checkout";
    
    export default reactExtension(
      "purchase.checkout.block.render",
      () => <CheckoutBanner />
    );
    
    function CheckoutBanner() {
      const cartLines = useCartLines();
      const total = useTotalAmount();
    
      if (total.amount > 100) {
        return (
          <Banner status="success">
            You qualify for free shipping!
          </Banner>
        );
      }
    
      return null;
    }
    
  #### **Notes**
    - Extensions run in sandboxed iframe
    - Use @shopify/ui-extensions-react for React
    - Limited APIs compared to full app
    - Deploy with 'shopify app deploy'

## Anti-Patterns


---
  #### **Name**
REST API for New Apps
  #### **Description**
REST API deprecated, GraphQL required for new public apps (April 2025)
  #### **Instead**
Use GraphQL Admin API

---
  #### **Name**
Webhook Processing Before Response
  #### **Description**
Processing webhooks before responding causes timeout
  #### **Instead**
Respond immediately, process asynchronously

---
  #### **Name**
Polling Instead of Webhooks
  #### **Description**
Wastes rate limits, slower than event-driven
  #### **Instead**
Use webhooks for event notifications

---
  #### **Name**
Duplicate Webhook Definitions
  #### **Description**
Defining webhooks in both TOML and code causes conflicts
  #### **Instead**
Define webhooks in shopify.app.toml only

---
  #### **Name**
Ignoring Rate Limits
  #### **Description**
Not handling 429 responses causes app failures
  #### **Instead**
Implement exponential backoff and request queuing