// @ts-nocheck
/**
 * This is an EXAMPLE TEMPLATE for the AI Agent. 
 * Do not import this file into the main application.
 */
import { v } from "convex/values";
import { mutation } from "../../../../../convex/_generated/server"; // Template path
import { getDescopeUserId } from "../../../../../convex/authUtils"; // Template path

/**
 * Standard mutation pattern for FlyerBoard:
 * 1. Auth check
 * 2. Resource existence check (if applicable)
 * 3. Ownership check (if applicable)
 * 4. Soft delete logic
 */
export const updateResource = mutation({
    args: {
        id: v.id("resources"),
        data: v.string(),
    },
    handler: async (ctx, args) => {
        // 1. Auth check
        const userId = await getDescopeUserId(ctx);
        if (!userId) throw new Error("Must be logged in");

        // 2. Resource existence check
        const resource = await ctx.db.get(args.id);
        if (!resource || resource.isDeleted) {
            throw new Error("Resource not found");
        }

        // 3. Ownership check
        if (resource.userId !== userId) {
            throw new Error("Unauthorized");
        }

        // 4. Perform update
        await ctx.db.patch(args.id, {
            content: args.data,
            updatedAt: Date.now(),
        });

        return { success: true };
    },
});
