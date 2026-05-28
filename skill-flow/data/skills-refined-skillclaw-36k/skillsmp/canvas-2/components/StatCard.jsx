/**
 * StatCard - Single statistic display card
 *
 * @prop {string} title - Stat label (e.g. "Total Revenue")
 * @prop {string} value - Main value to display (e.g. "$45,231")
 * @prop {string} change - Change indicator (e.g. "+20.1%")
 * @prop {"up"|"down"} trend - Trend direction for color (default: inferred from change)
 * @prop {Component} icon - Lucide icon component to display
 * @prop {function} onClick - Click handler (default: emits 'stat-click' with title)
 * @prop {string} description - Additional description text
 * @prop {string} className - Additional CSS classes
 */
function StatCard({
  title,
  value,
  change,
  trend,
  icon: Icon,
  onClick,
  description,
  className = ""
}) {
  // Infer trend from change string if not provided
  const resolvedTrend = trend || (change?.toString().startsWith("-") ? "down" : "up")

  const handleClick = () => {
    if (onClick) {
      onClick({ title, value, change })
    } else {
      window.canvasEmit("stat-click", { title, value, change })
    }
  }

  return (
    <Card
      className={`cursor-pointer hover:shadow-md transition-shadow ${className}`}
      onClick={handleClick}
    >
      <CardContent className="pt-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-500">{title}</p>
            <p className="text-2xl font-bold mt-1">{value}</p>
            {change && (
              <p className={`text-sm mt-1 ${
                resolvedTrend === "up" ? "text-green-600" : "text-red-600"
              }`}>
                {change} {description || "from last period"}
              </p>
            )}
            {!change && description && (
              <p className="text-sm mt-1 text-gray-500">{description}</p>
            )}
          </div>
          {Icon && (
            <div className="p-3 bg-gray-100 rounded-full">
              <Icon className="h-6 w-6 text-gray-600" />
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
