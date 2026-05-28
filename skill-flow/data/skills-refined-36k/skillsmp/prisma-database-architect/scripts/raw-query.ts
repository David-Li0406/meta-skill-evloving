/**
 * Raw PostgreSQL Query Execution Script
 *
 * This script allows direct execution of raw SQL queries against the database.
 * It reads the DATABASE_URL from .env or prompts for credentials.
 *
 * Usage:
 *   tsx scripts/raw-query.ts "SELECT * FROM \"Session\" LIMIT 10"
 *   tsx scripts/raw-query.ts --interactive
 */

import { readFileSync } from "fs";
import { resolve } from "path";
import { Pool } from "pg";
import * as readline from "readline";

interface ConnectionConfig {
	host: string;
	port: number;
	database: string;
	user: string;
	password: string;
}

/**
 * Parse DATABASE_URL into connection components
 * Format: postgresql://user:password@host:port/database
 */
function parseDatabaseUrl(url: string): ConnectionConfig | null {
	try {
		const match = url.match(
			/postgresql:\/\/([^:]+):([^@]+)@([^:]+):(\d+)\/(.+)/,
		);
		if (!match) return null;

		return {
			user: match[1],
			password: match[2],
			host: match[3],
			port: parseInt(match[4], 10),
			database: match[5],
		};
	} catch {
		return null;
	}
}

/**
 * Try to read .env file and extract DATABASE_URL
 */
function getDatabaseUrlFromEnv(): string | null {
	try {
		const envPath = resolve(process.cwd(), ".env");
		const envContent = readFileSync(envPath, "utf-8");

		const match = envContent.match(/DATABASE_URL=["']([^"']+)["']/);
		return match ? match[1] : null;
	} catch {
		return null;
	}
}

/**
 * Prompt user for database credentials
 */
async function promptForCredentials(): Promise<ConnectionConfig> {
	console.error("\n🔑 Database Connection Required");
	console.error("Please provide your PostgreSQL credentials:\n");

	const rl = readline.createInterface({
		input: process.stdin,
		output: process.stderr,
	});

	const config: Partial<ConnectionConfig> = {};

	const askQuestion = (prompt: string, echo = true): Promise<string> => {
		return new Promise((resolve) => {
			rl.question(prompt, (answer) => {
				resolve(answer);
			});
		});
	};

	const host = await askQuestion("Host (default: localhost): ");
	config.host = host || "localhost";

	const portStr = await askQuestion("Port (default: 5432): ");
	config.port = parseInt(portStr, 10) || 5432;

	config.database = await askQuestion("Database name: ");
	config.user = await askQuestion("Username: ");

	// For password, we need to handle it differently
	return new Promise((resolve) => {
		rl.question("Password: ", { echo: "*" }, async (password) => {
			config.password = password;
			rl.close();
			resolve(config as ConnectionConfig);
		});
	});
}

/**
 * Run interactive SQL mode
 */
async function runInteractiveMode(pool: Pool): Promise<void> {
	const rl = readline.createInterface({
		input: process.stdin,
		output: process.stderr,
	});

	console.error("📝 Interactive SQL Mode (type \\q to quit)\n");

	const queryLoop = async (): Promise<void> => {
		return new Promise((resolve) => {
			rl.question("sql> ", async (sql: string) => {
				if (sql.trim() === "\\q") {
					rl.close();
					await pool.end();
					resolve();
					return;
				}

				try {
					const start = Date.now();
					const result = await pool.query(sql);
					const duration = Date.now() - start;

					console.error(`\n✅ Query completed in ${duration}ms`);
					console.error(`   Rows: ${result.rowCount}\n`);

					// Output as JSON for easy parsing
					console.log(JSON.stringify(result.rows, null, 2));
					console.error();
				} catch (error: unknown) {
					console.error("❌ Error:", (error as Error).message);
					console.error();
				}

				// Continue loop
				queryLoop().then(() => {});
			});
		});
	};

	await queryLoop();
}

/**
 * Main execution function
 */
async function main(): Promise<void> {
	const query = process.argv[2];
	const interactive = process.argv.includes("--interactive");

	// 1. Try to get DATABASE_URL from .env
	let connectionConfig: ConnectionConfig | null = null;
	const dbUrl = getDatabaseUrlFromEnv();

	if (dbUrl) {
		connectionConfig = parseDatabaseUrl(dbUrl);
		if (connectionConfig) {
			console.error(`✅ Found DATABASE_URL in .env`);
			console.error(`   Host: ${connectionConfig.host}`);
			console.error(`   Database: ${connectionConfig.database}\n`);
		}
	}

	// 2. If no .env or invalid URL, prompt for credentials
	if (!connectionConfig) {
		console.error("⚠️  No valid DATABASE_URL found in .env");
		connectionConfig = await promptForCredentials();
	}

	// 3. Create connection pool
	const pool = new Pool(connectionConfig);

	try {
		// Test connection
		await pool.query("SELECT 1");
		console.error("✅ Connected to database successfully\n");

		// Interactive mode
		if (interactive) {
			await runInteractiveMode(pool);
			return;
		}

		// Single query mode
		if (!query) {
			console.error('Usage: tsx scripts/raw-query.ts "<SQL_QUERY>"');
			console.error("   or: tsx scripts/raw-query.ts --interactive");
			process.exit(1);
		}

		// Execute query
		const start = Date.now();
		const result = await pool.query(query);
		const duration = Date.now() - start;

		console.error(`✅ Query completed in ${duration}ms`);
		console.error(`   Rows returned: ${result.rowCount}\n`);

		// Output as JSON for easy parsing
		console.log(JSON.stringify(result.rows, null, 2));
	} catch (error: unknown) {
		console.error("❌ Database Error:", (error as Error).message);
		process.exit(1);
	} finally {
		if (!interactive) {
			await pool.end();
		}
	}
}

main().catch((error) => {
	console.error("Fatal error:", error);
	process.exit(1);
});
