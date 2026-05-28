# UI Design Patterns for Next.js

## The Perfect KPI Card

This component demonstrates proper visual hierarchy for data.

```tsx
import { ArrowUpRight, ArrowDownRight, DollarSign } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface KpiCardProps {
  title: string
  value: string
  change: string
  trend: "up" | "down" | "neutral"
}

export function KpiCard({ title, value, change, trend }: KpiCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <DollarSign className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className={`text-xs flex items-center mt-1 ${
          trend === "up" ? "text-emerald-500" : 
          trend === "down" ? "text-red-500" : "text-gray-500"
        }`}>
          {trend === "up" ? <ArrowUpRight className="h-3 w-3 mr-1" /> : 
           trend === "down" ? <ArrowDownRight className="h-3 w-3 mr-1" /> : null}
          {change}
        </p>
      </CardContent>
    </Card>
  )
}
```

## Professional Data Table (Clean)

Key characteristics:
1.  **Compact Headers:** `text-xs uppercase text-muted-foreground`
2.  **Right-aligned Numbers:** `text-right`
3.  **Monospace Numbers:** `font-mono` (optional, good for financial data)

```tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const invoices = [
  { invoice: "INV001", status: "Paid", method: "Credit Card", amount: "$250.00" },
  { invoice: "INV002", status: "Pending", method: "PayPal", amount: "$150.00" },
]

export function InvoiceTable() {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">Invoice</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Method</TableHead>
            <TableHead className="text-right">Amount</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {invoices.map((invoice) => (
            <TableRow key={invoice.invoice}>
              <TableCell className="font-medium">{invoice.invoice}</TableCell>
              <TableCell>{invoice.status}</TableCell>
              <TableCell>{invoice.method}</TableCell>
              <TableCell className="text-right font-mono">{invoice.amount}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
```
