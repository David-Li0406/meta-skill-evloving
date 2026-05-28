/**
 * DataChart - Flexible chart component supporting multiple chart types
 *
 * @prop {string} type - Chart type: "line", "bar", "area", "pie" (default: "line")
 * @prop {Array} data - Data array, e.g. [{month: "Jan", sales: 100, revenue: 200}]
 * @prop {string} xKey - Key for X-axis values (default: first non-numeric key)
 * @prop {Array} series - Series definitions: [{dataKey, color, label, type}]
 *   If omitted, auto-generates from numeric keys in data
 * @prop {string} title - Card title
 * @prop {string} description - Card description
 * @prop {number} height - Chart height in pixels (default: 300)
 * @prop {function} onClick - Called with {label, values} when chart is clicked
 * @prop {boolean} showLegend - Show legend (default: true)
 * @prop {boolean} showGrid - Show grid lines (default: true)
 * @prop {boolean} showTooltip - Show tooltips (default: true)
 * @prop {function} formatValue - Format Y-axis values, e.g. (v) => `$${v}`
 * @prop {function} formatTooltip - Format tooltip values
 * @prop {string} className - Additional CSS classes
 */
function DataChart({
  type = "line",
  data = [],
  xKey,
  series,
  title,
  description,
  height = 300,
  onClick,
  showLegend = true,
  showGrid = true,
  showTooltip = true,
  formatValue,
  formatTooltip,
  className = ""
}) {
  // Auto-detect xKey if not provided
  const resolvedXKey = xKey || (data[0] ? Object.keys(data[0]).find(k => typeof data[0][k] === "string") : "name")

  // Auto-generate series if not provided
  const resolvedSeries = series || (data[0]
    ? Object.keys(data[0])
        .filter(k => k !== resolvedXKey && typeof data[0][k] === "number")
        .map((key, i) => ({
          dataKey: key,
          color: ["#8884d8", "#82ca9d", "#ffc658", "#ff7300", "#00C49F", "#FFBB28"][i % 6],
          label: key
        }))
    : []
  )

  const handleChartClick = (chartData) => {
    if (onClick && chartData && chartData.activePayload) {
      onClick({
        label: chartData.activeLabel,
        values: chartData.activePayload.map(p => ({
          name: p.name,
          value: p.value
        }))
      })
    }
  }

  const commonAxisProps = {
    stroke: "#888888",
    fontSize: 12
  }

  const tooltipStyle = {
    backgroundColor: "#fff",
    border: "1px solid #e5e7eb",
    borderRadius: "8px"
  }

  const renderChart = () => {
    if (type === "pie") {
      return (
        <PieChart onClick={onClick ? handleChartClick : undefined}>
          {showTooltip && <RechartsTooltip contentStyle={tooltipStyle} formatter={formatTooltip} />}
          {showLegend && <Legend />}
          <Pie
            data={data}
            dataKey={resolvedSeries[0]?.dataKey || "value"}
            nameKey={resolvedXKey}
            cx="50%"
            cy="50%"
            outerRadius={height / 3}
            label
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={resolvedSeries[index % resolvedSeries.length]?.color || "#8884d8"} />
            ))}
          </Pie>
        </PieChart>
      )
    }

    if (type === "bar") {
      return (
        <BarChart data={data} onClick={onClick ? handleChartClick : undefined}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" />}
          <XAxis dataKey={resolvedXKey} {...commonAxisProps} />
          <YAxis {...commonAxisProps} tickFormatter={formatValue} />
          {showTooltip && <RechartsTooltip contentStyle={tooltipStyle} formatter={formatTooltip} />}
          {showLegend && <Legend />}
          {resolvedSeries.map((s, i) => (
            <Bar
              key={s.dataKey}
              dataKey={s.dataKey}
              name={s.label || s.dataKey}
              fill={s.color}
              radius={[4, 4, 0, 0]}
            />
          ))}
        </BarChart>
      )
    }

    if (type === "area") {
      return (
        <AreaChart data={data} onClick={onClick ? handleChartClick : undefined}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" />}
          <XAxis dataKey={resolvedXKey} {...commonAxisProps} />
          <YAxis {...commonAxisProps} tickFormatter={formatValue} />
          {showTooltip && <RechartsTooltip contentStyle={tooltipStyle} formatter={formatTooltip} />}
          {showLegend && <Legend />}
          {resolvedSeries.map((s, i) => (
            <Area
              key={s.dataKey}
              type="monotone"
              dataKey={s.dataKey}
              name={s.label || s.dataKey}
              stroke={s.color}
              fill={s.color}
              fillOpacity={0.6}
              stackId={s.stackId}
            />
          ))}
        </AreaChart>
      )
    }

    // Default: line chart
    return (
      <LineChart data={data} onClick={onClick ? handleChartClick : undefined}>
        {showGrid && <CartesianGrid strokeDasharray="3 3" />}
        <XAxis dataKey={resolvedXKey} {...commonAxisProps} />
        <YAxis {...commonAxisProps} tickFormatter={formatValue} />
        {showTooltip && <RechartsTooltip contentStyle={tooltipStyle} formatter={formatTooltip} />}
        {showLegend && <Legend />}
        {resolvedSeries.map((s, i) => (
          <Line
            key={s.dataKey}
            type={s.type || "monotone"}
            dataKey={s.dataKey}
            name={s.label || s.dataKey}
            stroke={s.color}
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        ))}
      </LineChart>
    )
  }

  const chart = (
    <ResponsiveContainer width="100%" height={height}>
      {renderChart()}
    </ResponsiveContainer>
  )

  if (!title) {
    return <div className={className}>{chart}</div>
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>{chart}</CardContent>
    </Card>
  )
}
