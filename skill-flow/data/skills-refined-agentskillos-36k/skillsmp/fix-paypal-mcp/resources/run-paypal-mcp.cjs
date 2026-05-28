const { PayPalAgentToolkit } = require('@paypal/agent-toolkit/mcp');
// Pointing to the SDK export which maps to CJS
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

const accessToken = process.env.PAYPAL_ACCESS_TOKEN;
const environment = process.env.PAYPAL_ENVIRONMENT || 'PRODUCTION';

if (!accessToken) {
    console.error("Error: PAYPAL_ACCESS_TOKEN is missing");
    process.exit(1);
}

// Configuration to enable all available tools
const configuration = {
    context: {},
    actions: {
        invoices: { create: true, list: true, get: true, send: true, sendReminder: true, cancel: true, generateQRC: true },
        products: { create: true, list: true, update: true, show: true },
        subscriptionPlans: { create: true, list: true, show: true },
        subscriptions: { create: true, show: true, cancel: true, update: true },
        shipment: { create: true, get: true, update: true },
        orders: { create: true, get: true, capture: true },
        disputes: { list: true, get: true, create: true },
        transactions: { list: true },
        plan: { update: true },
        payments: { createRefund: true, getRefunds: true },
        insights: { get: true }
    }
};

async function main() {
    try {
        const server = new PayPalAgentToolkit({
            accessToken,
            configuration
        });

        // Connect to stdio transport
        const transport = new StdioServerTransport();
        await server.connect(transport);
        console.error("PayPal MCP Server started successfully.");
    } catch (error) {
        console.error("Failed to start server:", error);
        process.exit(1);
    }
}

main();
