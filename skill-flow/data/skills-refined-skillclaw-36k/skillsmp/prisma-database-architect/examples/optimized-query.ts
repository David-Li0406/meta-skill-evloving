// Optimized Query Examples
// This file demonstrates best practices for performant Prisma queries

import { prisma } from "@/lib/db";

// ============================================================================
// EXAMPLE 1: Select Only Needed Fields (Select Objects Pattern)
// ============================================================================

// ❌ BAD: Fetches all fields (over-fetching)
const usersBad = await prisma.user.findMany({
	where: { isActive: true },
});

// ✅ GOOD: Fetches only required fields
const usersGood = await prisma.user.findMany({
	where: { isActive: true },
	select: {
		id: true,
		name: true,
		email: true, // Only fetch strictly needed fields
	},
});

// ============================================================================
// EXAMPLE 2: Avoid N+1 Queries with relationLoadStrategy
// ============================================================================

// ❌ BAD: N+1 query issue (separate query for each post's comments)
const postsBad = await prisma.post.findMany({
	include: {
		comments: true, // This can cause N+1 queries
	},
});

// ✅ GOOD: Use join strategy (Prisma v5.10+)
const postsGood = await prisma.post.findMany({
	relationLoadStrategy: "join", // Fetch relations at DB level
	include: {
		comments: {
			take: 5, // Limit related records
		},
	},
});

// ============================================================================
// EXAMPLE 3: Efficient Counting
// ============================================================================

// ❌ BAD: Fetches all records just to count
const countBad = await prisma.session.findMany();
const total = countBad.length;

// ✅ GOOD: Use count() directly
const totalGood = await prisma.session.count();

// ✅ EVEN BETTER: Count with filtering
const availableCount = await prisma.session.count({
	where: {
		available: true,
		date: {
			gte: new Date(),
		},
	},
});

// ============================================================================
// EXAMPLE 4: Pagination and Ordering
// ============================================================================

const paginatedSessions = await prisma.session.findMany({
	where: {
		date: {
			gte: new Date(),
		},
	},
	select: {
		id: true,
		date: true,
		startTime: true,
		available: true,
		facility: {
			select: {
				name: true,
				district: {
					select: {
						name: true,
					},
				},
			},
		},
	},
	orderBy: {
		date: "asc",
	},
	take: 20, // Limit results
	skip: 0, // Offset for pagination
});

// ============================================================================
// EXAMPLE 5: Batch Operations with createMany
// ============================================================================

// ❌ BAD: Individual inserts in a loop
for (const session of sessions) {
	await prisma.session.create({ data: session });
}

// ✅ GOOD: Batch insert
await prisma.session.createMany({
	data: sessions,
	skipDuplicates: true, // Skip if unique constraint violated
});

// ============================================================================
// EXAMPLE 6: Upsert for Idempotent Operations
// ============================================================================

const session = await prisma.session.upsert({
	where: {
		// Unique constraint
		venueId_facilityCode_date_startTime: {
			venueId: "fac-123",
			facilityCode: "TENC",
			date: new Date("2025-01-15"),
			startTime: "09:00",
		},
	},
	update: {
		available: true, // Update if exists
	},
	create: {
		venueId: "fac-123",
		facilityCode: "TENC",
		date: new Date("2025-01-15"),
		startTime: "09:00",
		available: true, // Create if doesn't exist
	},
});

// ============================================================================
// EXAMPLE 7: Complex Filtering with Indexes
// ============================================================================

// Assumes @@index([date, available]) on Session model
const availableSessions = await prisma.session.findMany({
	where: {
		AND: [
			{ date: { gte: new Date() } },
			{ available: true },
			{ facility: { district: { code: "KC" } } },
		],
	},
	select: {
		id: true,
		date: true,
		startTime: true,
		facility: {
			select: {
				name: true,
				district: {
					select: {
						name: true,
					},
				},
			},
		},
	},
});

export {
	usersGood,
	postsGood,
	availableCount,
	paginatedSessions,
	session,
	availableSessions,
};
