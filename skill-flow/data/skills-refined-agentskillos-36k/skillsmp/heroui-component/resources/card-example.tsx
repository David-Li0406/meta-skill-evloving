// Example: Card compound component pattern (HeroUI v3)

import { Card, Button, Chip } from "@heroui/react";

interface ExampleCardProps {
    title: string;
    description: string;
    status?: "active" | "pending" | "completed";
    onAction?: () => void;
}

export function ExampleCard({
    title,
    description,
    status = "pending",
    onAction,
}: ExampleCardProps) {
    const statusColors = {
        active: "success",
        pending: "warning",
        completed: "default",
    } as const;

    return (
        <Card>
            <Card.Content className="p-6">
                <div className="flex items-start justify-between">
                    <div className="space-y-2">
                        <h3 className="text-lg font-semibold">{title}</h3>
                        <p className="text-default-500">{description}</p>
                    </div>
                    <Chip color={statusColors[status]} size="sm">
                        {status}
                    </Chip>
                </div>

                {onAction && (
                    <div className="mt-4 flex justify-end">
                        <Button onPress={onAction} variant="primary" size="sm">
                            View Details
                        </Button>
                    </div>
                )}
            </Card.Content>
        </Card>
    );
}
