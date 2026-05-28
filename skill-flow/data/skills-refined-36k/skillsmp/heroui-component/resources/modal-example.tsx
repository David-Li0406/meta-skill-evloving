// Example: Modal compound component pattern (HeroUI v3)

import { Modal, Button } from "@heroui/react";

interface ExampleModalProps {
    isOpen: boolean;
    onOpenChange: (open: boolean) => void;
    title: string;
    children: React.ReactNode;
    onConfirm?: () => void;
}

export function ExampleModal({
    isOpen,
    onOpenChange,
    title,
    children,
    onConfirm,
}: ExampleModalProps) {
    const handleConfirm = () => {
        onConfirm?.();
        onOpenChange(false);
    };

    return (
        <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
            <Modal.Backdrop>
                <Modal.Container>
                    <Modal.Dialog>
                        <Modal.CloseTrigger />
                        <Modal.Header>
                            <Modal.Heading>{title}</Modal.Heading>
                        </Modal.Header>
                        <Modal.Body>{children}</Modal.Body>
                        <Modal.Footer>
                            <Button
                                variant="ghost"
                                onPress={() => onOpenChange(false)}
                            >
                                Cancel
                            </Button>
                            <Button variant="primary" onPress={handleConfirm}>
                                Confirm
                            </Button>
                        </Modal.Footer>
                    </Modal.Dialog>
                </Modal.Container>
            </Modal.Backdrop>
        </Modal>
    );
}
