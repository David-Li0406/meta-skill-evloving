import { queryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { createServerFn, useServerFn } from "@tanstack/react-start";
import { z } from "zod";

// 1. Define Server Functions (Business Logic + Security)
const fetchUserProfile = createServerFn()
	.inputValidator((data: unknown) => z.uuid().parse(data)) // Zod 4: top-level z.uuid()
	.handler(async ({ data: userId, context }) => {
		// Simulated DB call - STRICTLY SERVER SIDE
		console.log(`Fetching user ${userId}`);
		return { id: userId, name: "Alice", role: "admin" };
	});

const updateUserProfile = createServerFn({ method: "POST" })
	.inputValidator((data: unknown) =>
		z.object({ userId: z.string(), name: z.string().min(2) }).parse(data),
	)
	.handler(async ({ data }) => {
		// Perform mutation
		return { success: true, updatedName: data.name };
	});

// 2. Define Query Options (Caching & key management)
const userQueryOptions = (userId: string) =>
	queryOptions({
		queryKey: ["users", userId],
		queryFn: () => fetchUserProfile({ data: userId }),
		staleTime: 10 * 1000,
	});

// 3. Define Route (Loader calls Server Function securely)
export const Route = createFileRoute("/users/$userId")({
	// Validate path params
	params: {
		parse: (params) => ({ userId: z.uuid().parse(params.userId) }),
	},
	// Prefetch data on server (SSR) or client (CSR)
	loader: ({ context: { queryClient }, params }) =>
		queryClient.ensureQueryData(userQueryOptions(params.userId)),
	component: UserProfilePage,
});

// 4. Feature Component (Type-safe access)
function UserProfilePage() {
	const { userId } = Route.useParams();
	// 5. Use Suspense Query for data access
	const { data: user } = useSuspenseQuery(userQueryOptions(userId));

	// 6. Use Server Function for mutation
	const updateReq = useServerFn(updateUserProfile);

	return (
		<div className="p-4 space-y-4">
			<h1 className="text-2xl font-bold">User: {user.name}</h1>
			<button
				onClick={() => updateReq({ data: { userId, name: "Bob" } })}
				className="bg-blue-500 text-white px-4 py-2 rounded"
			>
				Update Name
			</button>
		</div>
	);
}
