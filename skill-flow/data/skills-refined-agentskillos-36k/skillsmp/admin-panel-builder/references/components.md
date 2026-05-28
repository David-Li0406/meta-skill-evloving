# Admin Component Patterns

## Manager Component Template

Standard pattern for admin data management:

```tsx
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@ui/table";
import { Button } from "@ui/button";
import { Badge } from "@ui/badge";
import { Loader2, Trash2, Edit, Plus } from "lucide-react";

export const FeatureManager = () => {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [editingId, setEditingId] = useState<string | null>(null);

  // Fetch data
  const { data, isLoading, error } = useQuery({
    queryKey: ['feature-data'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('table_name')
        .select('*')
        .order('created_at', { ascending: false });
      if (error) throw error;
      return data;
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const { error } = await supabase.from('table_name').delete().eq('id', id);
      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['feature-data'] });
      toast({ title: "Deleted", description: "Item removed" });
    },
    onError: (error: Error) => {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    },
  });

  if (isLoading) {
    return <div className="flex justify-center p-8"><Loader2 className="animate-spin" /></div>;
  }

  if (error) {
    return <div className="text-destructive">Error: {error.message}</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button onClick={() => setEditingId('new')}>
          <Plus className="h-4 w-4 mr-2" /> Add New
        </Button>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data?.map((item) => (
            <TableRow key={item.id}>
              <TableCell>{item.name}</TableCell>
              <TableCell>
                <Badge variant={item.is_active ? "default" : "secondary"}>
                  {item.is_active ? "Active" : "Inactive"}
                </Badge>
              </TableCell>
              <TableCell className="text-right space-x-2">
                <Button variant="outline" size="sm" onClick={() => setEditingId(item.id)}>
                  <Edit className="h-4 w-4" />
                </Button>
                <Button variant="destructive" size="sm" onClick={() => deleteMutation.mutate(item.id)}>
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
```

## Form Dialog Pattern

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@ui/dialog";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@ui/form";
import { Input } from "@ui/input";
import { Button } from "@ui/button";

const schema = z.object({
  name: z.string().min(1, "Required"),
  value: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

interface EditDialogProps {
  open: boolean;
  onClose: () => void;
  item?: { id: string; name: string; value?: string } | null;
  onSave: (data: FormData) => Promise<void>;
}

export const EditDialog = ({ open, onClose, item, onSave }: EditDialogProps) => {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      name: item?.name || "",
      value: item?.value || "",
    },
  });

  const handleSubmit = async (data: FormData) => {
    await onSave(data);
    onClose();
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{item ? "Edit" : "Add New"}</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl><Input {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={onClose}>Cancel</Button>
              <Button type="submit">Save</Button>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
};
```

## Time Filter Pattern

Common in analytics pages:

```tsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@ui/select";

type TimeFilter = "24h" | "7d" | "30d" | "all";

const [timeFilter, setTimeFilter] = useState<TimeFilter>("7d");

const getTimeFilterDate = (filter: TimeFilter): Date | null => {
  const now = new Date();
  switch (filter) {
    case "24h": return new Date(now.getTime() - 24 * 60 * 60 * 1000);
    case "7d": return new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    case "30d": return new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    default: return null;
  }
};

// In JSX
<Select value={timeFilter} onValueChange={(v) => setTimeFilter(v as TimeFilter)}>
  <SelectTrigger className="w-32">
    <SelectValue />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="24h">24 hours</SelectItem>
    <SelectItem value="7d">7 days</SelectItem>
    <SelectItem value="30d">30 days</SelectItem>
    <SelectItem value="all">All time</SelectItem>
  </SelectContent>
</Select>
```

## Stats Card Pattern

```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@ui/card";

interface StatsCardProps {
  title: string;
  value: number | string;
  description?: string;
  icon?: React.ReactNode;
}

const StatsCard = ({ title, value, description, icon }: StatsCardProps) => (
  <Card>
    <CardHeader className="flex flex-row items-center justify-between pb-2">
      <CardTitle className="text-sm font-medium">{title}</CardTitle>
      {icon}
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
      {description && (
        <p className="text-xs text-muted-foreground">{description}</p>
      )}
    </CardContent>
  </Card>
);

// Usage
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  <StatsCard title="Total Users" value={1234} description="+12% from last month" />
  <StatsCard title="Active" value={987} />
</div>
```

## Confirmation Dialog Pattern

```tsx
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel,
  AlertDialogContent, AlertDialogDescription, AlertDialogFooter,
  AlertDialogHeader, AlertDialogTitle
} from "@ui/alert-dialog";

const [deleteId, setDeleteId] = useState<string | null>(null);

<AlertDialog open={!!deleteId} onOpenChange={() => setDeleteId(null)}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Confirm Delete</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction onClick={() => deleteId && deleteMutation.mutate(deleteId)}>
        Delete
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

## Common Imports for Admin Components

```tsx
// React Query
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

// Supabase
import { supabase } from "@/integrations/supabase/client";

// UI Components
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@ui/card";
import { Button } from "@ui/button";
import { Badge } from "@ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@ui/tabs";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@ui/dialog";
import { Alert, AlertDescription, AlertTitle } from "@ui/alert";
import { Skeleton } from "@ui/skeleton";

// Form
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@ui/form";
import { Input } from "@ui/input";
import { Textarea } from "@ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@ui/select";
import { Switch } from "@ui/switch";

// Icons
import { Loader2, Plus, Edit, Trash2, Check, X, AlertCircle, Search, RefreshCw } from "lucide-react";

// Hooks
import { useToast } from "@/hooks/use-toast";
```
