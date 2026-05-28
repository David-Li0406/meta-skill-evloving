import { useActionState } from "react";

// import { updateSettings } from './actions' // server action

// Mock Server Action
async function updateSettings(prevState: any, formData: FormData) {
	"use server";
	await new Promise((r) => setTimeout(r, 1000));
	const name = formData.get("name");
	if (!name || name.toString().length < 3) {
		return { error: "Name must be at least 3 chars", success: false };
	}
	return { error: null, success: true, message: "Saved!" };
}

export function SettingsForm() {
	// 1. React 19 useActionState: Manages pending/error/result states auto-magically
	const [state, formAction, isPending] = useActionState(updateSettings, {
		error: null,
		success: false,
	});

	return (
		<div className="max-w-md mx-auto p-6 bg-surface-100 rounded-lg shadow-md">
			<h2 className="text-xl font-bold mb-4 text-copy-900">Settings</h2>

			<form action={formAction} className="space-y-4">
				<div>
					<label
						htmlFor="name"
						className="block text-sm font-medium text-copy-700"
					>
						Display Name
					</label>
					<input
						type="text"
						name="name"
						id="name"
						defaultValue=""
						disabled={isPending}
						// Tailwind v4: No config needed, using atomic classes
						className="mt-1 block w-full rounded-md border-gray-300 shadow-sm 
                       focus:border-primary-500 focus:ring-primary-500 
                       disabled:opacity-50 disabled:cursor-not-allowed
                       transition-all duration-200"
					/>
				</div>

				{/* Error State */}
				{state.error && (
					<p className="text-red-500 text-sm animate-pulse" role="alert">
						{state.error}
					</p>
				)}

				{/* Success State */}
				{state.success && (
					<p className="text-green-600 text-sm">{state?.message}</p>
				)}

				<button
					type="submit"
					disabled={isPending}
					className="w-full flex justify-center py-2 px-4 border border-transparent 
                     rounded-md shadow-sm text-sm font-medium text-white 
                     bg-indigo-600 hover:bg-indigo-700 focus:outline-none 
                     focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
                     data-[loading=true]:bg-indigo-400"
					data-loading={isPending}
				>
					{isPending ? "Saving..." : "Save Changes"}
				</button>
			</form>
		</div>
	);
}
