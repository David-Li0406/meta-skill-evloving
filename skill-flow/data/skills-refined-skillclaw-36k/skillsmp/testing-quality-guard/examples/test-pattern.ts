import { describe, expect, it, vi } from "vitest";

// 1. The Code Under Test
export function calculateDiscount(price: number, code?: string) {
	if (code === "SUMMER") return price * 0.9;
	return price;
}

// Private helper (not exported)
function _validatePrice(price: number) {
	return price >= 0;
}

// 2. In-Source Testing for Private Helpers
// This block is stripped in production builds
if (import.meta.vitest) {
	const { it, expect } = import.meta.vitest;
	it("_validatePrice rejects negative numbers", () => {
		expect(_validatePrice(-10)).toBe(false);
		expect(_validatePrice(10)).toBe(true);
	});
}

// 3. Standard Test Suite (would normally be in .test.ts)
describe("calculateDiscount", () => {
	it("applies 10% discount for SUMMER code", () => {
		expect(calculateDiscount(100, "SUMMER")).toBe(90);
	});

	it("ignores invalid codes", () => {
		expect(calculateDiscount(100, "INVALID")).toBe(100);
	});
});

// 4. Mocking Example
// Imagine this imports a DB function
const db = {
	getUser: async (id: string) => ({ id, name: "Real" }),
};

describe("Mocking", () => {
	it("mocks db calls", async () => {
		const spy = vi
			.spyOn(db, "getUser")
			.mockResolvedValue({ id: "1", name: "Mocked" });

		const user = await db.getUser("1");

		expect(user.name).toBe("Mocked");
		expect(spy).toHaveBeenCalledWith("1");
	});
});
