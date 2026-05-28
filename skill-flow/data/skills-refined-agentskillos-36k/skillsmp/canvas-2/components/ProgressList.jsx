/**
 * ProgressList - Multiple progress bars with labels
 *
 * @prop {Array} items - Progress items: [{label, value, max, current, format}]
 *   - label: Progress bar label
 *   - value: Progress percentage (0-100) OR calculated from current/max
 *   - max: Maximum value (for display, e.g. 100)
 *   - current: Current value (for display, e.g. 75)
 *   - format: Optional format function for display (current, max) => string
 * @prop {string} title - Card title (default: "Progress")
 * @prop {string} description - Card description
 * @prop {boolean} showPercentage - Show percentage on the right (default: false if current/max provided)
 * @prop {string} className - Additional CSS classes
 */
function ProgressList({
  items = [],
  title = "Progress",
  description,
  showPercentage,
  className = ""
}) {
  const content = (
    <div className="space-y-6">
      {items.map((item, index) => {
        // Calculate value from current/max if not provided
        const value = item.value ?? (item.current && item.max ? (item.current / item.max) * 100 : 0)

        // Determine what to show on the right
        const hasCurrentMax = item.current !== undefined && item.max !== undefined
        const displayShowPercentage = showPercentage ?? !hasCurrentMax

        let rightText
        if (item.format) {
          rightText = item.format(item.current, item.max)
        } else if (hasCurrentMax) {
          rightText = `${item.current} / ${item.max}`
        } else if (displayShowPercentage) {
          rightText = `${Math.round(value)}%`
        }

        return (
          <div key={index} className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>{item.label}</span>
              {rightText && <span className="text-gray-500">{rightText}</span>}
            </div>
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-600 rounded-full transition-all duration-300"
                style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
              />
            </div>
          </div>
        )
      })}
    </div>
  )

  if (!title) {
    return <div className={className}>{content}</div>
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>{content}</CardContent>
    </Card>
  )
}
