import { Dialog } from "@base-ui/react";
import { XIcon } from "lucide-react";

export function ConfirmDialog() {
	return (
		<Dialog.Root>
			<Dialog.Trigger className="bg-primary text-primary-foreground hover:bg-primary-hover px-4 py-2 rounded-md transition-colors font-medium">
				Delete Account
			</Dialog.Trigger>

			<Dialog.Portal>
				{/* Backdrop: Uses semantic 'fixed' and 'inset-0' plus pure black with opacity for overlay */}
				<Dialog.Backdrop className="fixed inset-0 bg-black/50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />

				{/* Popup: Uses strict semantic colors `bg-card` and `text-card-foreground` */}
				<Dialog.Popup className="fixed left-1/2 top-1/2 w-full max-w-md -translate-x-1/2 -translate-y-1/2 rounded-lg bg-card p-6 text-card-foreground shadow-xl focus:outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]">
					<div className="flex items-center justify-between mb-4">
						<Dialog.Title className="text-lg font-bold text-foreground">
							Confirm Deletion
						</Dialog.Title>
						<Dialog.Close className="text-muted-foreground hover:text-foreground transition-colors">
							<XIcon className="size-5" />
						</Dialog.Close>
					</div>

					<Dialog.Description className="text-sm text-muted-foreground mb-6">
						Are you sure you want to delete your account? This action cannot be
						undone and all your data will be permanently removed.
					</Dialog.Description>

					<div className="flex justify-end gap-3">
						<Dialog.Close className="px-4 py-2 rounded-md bg-secondary text-secondary-foreground hover:bg-secondary-hover transition-colors text-sm font-medium">
							Cancel
						</Dialog.Close>
						<button className="px-4 py-2 rounded-md bg-destructive text-destructive-foreground hover:bg-destructive/90 transition-colors text-sm font-medium">
							Yes, Delete
						</button>
					</div>
				</Dialog.Popup>
			</Dialog.Portal>
		</Dialog.Root>
	);
}
