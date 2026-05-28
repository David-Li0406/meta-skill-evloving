// Transaction Examples
// This file demonstrates how to use transactions for atomic operations

import { prisma } from "@/lib/db";

// ============================================================================
// EXAMPLE 1: Simple Transaction - All or Nothing
// ============================================================================

async function transferCredits(
	fromUserId: string,
	toUserId: string,
	amount: number,
) {
	return await prisma.$transaction(async (tx) => {
		// 1. Deduct from sender
		const sender = await tx.user.update({
			where: { id: fromUserId },
			data: { credits: { decrement: amount } },
		});

		// 2. Add to receiver
		const receiver = await tx.user.update({
			where: { id: toUserId },
			data: { credits: { increment: amount } },
		});

		// 3. Create transfer record
		const transfer = await tx.transfer.create({
			data: {
				fromUserId,
				toUserId,
				amount,
				status: "COMPLETED",
			},
		});

		return { sender, receiver, transfer };
	});
}

// If any operation fails, all changes are rolled back automatically

// ============================================================================
// EXAMPLE 2: Transaction with Validation
// ============================================================================

async function bookSession(userId: string, sessionId: string) {
	return await prisma.$transaction(async (tx) => {
		// 1. Check session availability
		const session = await tx.session.findUnique({
			where: { id: sessionId },
		});

		if (!session) {
			throw new Error("Session not found");
		}

		if (!session.available) {
			throw new Error("Session no longer available");
		}

		// 2. Mark session as booked
		await tx.session.update({
			where: { id: sessionId },
			data: { available: false },
		});

		// 3. Create booking
		const booking = await tx.booking.create({
			data: {
				userId,
				sessionId,
				status: "CONFIRMED",
				bookedAt: new Date(),
			},
		});

		return booking;
	});
}

// ============================================================================
// EXAMPLE 3: Conditional Transactions
// ============================================================================

async function createCrawlJobWithRetry(
	districtCodes: string[],
	facilityType: string,
) {
	return await prisma.$transaction(async (tx) => {
		// 1. Check if job already exists for today
		const today = new Date();
		today.setHours(0, 0, 0, 0);

		const existingJob = await tx.crawlJob.findFirst({
			where: {
				playDate: today,
				status: { in: ["PENDING", "RUNNING"] },
			},
		});

		if (existingJob) {
			// Return existing job instead of creating duplicate
			return existingJob;
		}

		// 2. Create new crawl job
		const job = await tx.crawlJob.create({
			data: {
				playDate: today,
				districtCodes,
				facilityType,
				status: "PENDING",
			},
		});

		// 3. Initialize scheduled crawl run
		const run = await tx.scheduledCrawlRun.create({
			data: {
				jobId: job.id,
				totalDistricts: districtCodes.length,
				status: "INITIALIZED",
			},
		});

		return { job, run };
	});
}

// ============================================================================
// EXAMPLE 4: Transaction with Rollback Logic
// ============================================================================

async function batchUpdateSessions(
	sessionIds: string[],
	updates: { available: boolean },
) {
	return await prisma.$transaction(async (tx) => {
		const results = [];

		for (const sessionId of sessionIds) {
			try {
				const updated = await tx.session.update({
					where: { id: sessionId },
					data: updates,
				});
				results.push({ success: true, session: updated });
			} catch (error) {
				// Log error but continue with other sessions
				results.push({
					success: false,
					sessionId,
					error: error instanceof Error ? error.message : "Unknown error",
				});
			}
		}

		return results;
	});
}

// ============================================================================
// EXAMPLE 5: Interactive Transaction for Complex Logic
// ============================================================================

async function processBookingWithWaitlist(userId: string, sessionId: string) {
	return await prisma.$transaction(async (tx) => {
		// Step 1: Try to book directly
		const session = await tx.session.findUnique({
			where: { id: sessionId },
			include: {
				bookings: {
					where: { status: "CONFIRMED" },
				},
			},
		});

		if (!session) {
			throw new Error("Session not found");
		}

		const isAvailable =
			session.available && session.bookings.length < session.capacity;

		if (isAvailable) {
			// Direct booking
			const booking = await tx.booking.create({
				data: {
					userId,
					sessionId,
					status: "CONFIRMED",
					bookedAt: new Date(),
				},
			});

			// Update availability
			if (session.bookings.length + 1 >= session.capacity) {
				await tx.session.update({
					where: { id: sessionId },
					data: { available: false },
				});
			}

			return { success: true, booking, waitlisted: false };
		} else {
			// Add to waitlist
			const waitlistEntry = await tx.waitlistEntry.create({
				data: {
					userId,
					sessionId,
					status: "PENDING",
					joinedAt: new Date(),
				},
			});

			return { success: true, waitlistEntry, waitlisted: true };
		}
	});
}

// ============================================================================
// EXAMPLE 6: Transaction with Isolation Level
// ============================================================================

async function safeDecrementCredits(userId: string, amount: number) {
	return await prisma.$transaction(
		async (tx) => {
			const user = await tx.user.findUnique({
				where: { id: userId },
			});

			if (!user || user.credits < amount) {
				throw new Error("Insufficient credits");
			}

			const updated = await tx.user.update({
				where: { id: userId },
				data: { credits: { decrement: amount } },
			});

			return updated;
		},
		{
			maxWait: 5000, // Maximum time to wait for transaction to start
			timeout: 10000, // Maximum time transaction can run
			isolationLevel: prisma.$transaction.IsolationLevel.Serializable,
		},
	);
}

export {
	transferCredits,
	bookSession,
	createCrawlJobWithRetry,
	batchUpdateSessions,
	processBookingWithWaitlist,
	safeDecrementCredits,
};
