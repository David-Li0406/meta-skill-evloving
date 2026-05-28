/**
 * DataTable - Searchable, selectable data table with actions
 *
 * @prop {Array} data - Row data array, e.g. [{id: 1, name: "Alice", email: "alice@example.com"}]
 * @prop {Array} columns - Column definitions: [{key, label, render, width}]
 *   - key: Data key to display
 *   - label: Column header text
 *   - render: Optional (value, row) => ReactNode for custom rendering
 *   - width: Optional CSS width
 * @prop {string} title - Card title
 * @prop {string} description - Card description
 * @prop {boolean} searchable - Show search input (default: true)
 * @prop {string} searchPlaceholder - Search input placeholder (default: "Search...")
 * @prop {Array} searchKeys - Keys to search in (default: all string columns)
 * @prop {boolean} selectable - Show checkboxes for row selection (default: false)
 * @prop {function} onSelectionChange - Called with selected row IDs when selection changes
 * @prop {function} onRowClick - Called with row data when row is clicked
 * @prop {Array} actions - Row actions: [{label, icon, onClick, variant}]
 * @prop {ReactNode} headerActions - Custom header actions (buttons, etc.)
 * @prop {string} emptyMessage - Message when no data (default: "No results found")
 * @prop {string} idKey - Key used for row identification (default: "id")
 * @prop {string} className - Additional CSS classes
 */
function DataTable({
  data = [],
  columns = [],
  title,
  description,
  searchable = true,
  searchPlaceholder = "Search...",
  searchKeys,
  selectable = false,
  onSelectionChange,
  onRowClick,
  actions = [],
  headerActions,
  emptyMessage = "No results found",
  idKey = "id",
  className = ""
}) {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedRows, setSelectedRows] = useState([])

  // Auto-detect columns if not provided
  const resolvedColumns = columns.length > 0
    ? columns
    : (data[0]
        ? Object.keys(data[0]).filter(k => k !== idKey).map(key => ({ key, label: key }))
        : []
      )

  // Determine which keys to search
  const resolvedSearchKeys = searchKeys || resolvedColumns.map(c => c.key)

  // Filter data based on search
  const filteredData = data.filter(row => {
    if (!searchQuery) return true
    const query = searchQuery.toLowerCase()
    return resolvedSearchKeys.some(key => {
      const value = row[key]
      return value?.toString().toLowerCase().includes(query)
    })
  })

  const handleRowClick = (row) => {
    if (onRowClick) {
      onRowClick(row)
    } else {
      window.canvasEmit("row-click", row)
    }
  }

  const toggleRowSelection = (id, e) => {
    if (e) e.stopPropagation()
    const newSelection = selectedRows.includes(id)
      ? selectedRows.filter(r => r !== id)
      : [...selectedRows, id]
    setSelectedRows(newSelection)
    onSelectionChange?.(newSelection)
  }

  const toggleSelectAll = () => {
    const allIds = filteredData.map(r => r[idKey])
    const newSelection = selectedRows.length === filteredData.length ? [] : allIds
    setSelectedRows(newSelection)
    onSelectionChange?.(newSelection)
  }

  const handleAction = (action, row, e) => {
    e.stopPropagation()
    if (action.onClick) {
      action.onClick(row)
    } else {
      window.canvasEmit(action.event || action.label.toLowerCase(), row)
    }
  }

  const tableContent = (
    <>
      {(searchable || headerActions || selectable) && (
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            {searchable && (
              <Input
                placeholder={searchPlaceholder}
                className="w-64"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            )}
            {selectable && selectedRows.length > 0 && (
              <span className="px-2 py-1 text-xs bg-gray-100 rounded-full">
                {selectedRows.length} selected
              </span>
            )}
          </div>
          {headerActions}
        </div>
      )}

      <Table>
        <TableHeader>
          <TableRow>
            {selectable && (
              <TableHead className="w-12">
                <input
                  type="checkbox"
                  checked={filteredData.length > 0 && selectedRows.length === filteredData.length}
                  onChange={toggleSelectAll}
                  className="h-4 w-4 rounded border-gray-300"
                />
              </TableHead>
            )}
            {resolvedColumns.map(col => (
              <TableHead key={col.key} style={col.width ? { width: col.width } : undefined}>
                {col.label}
              </TableHead>
            ))}
            {actions.length > 0 && (
              <TableHead className="text-right">Actions</TableHead>
            )}
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredData.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={resolvedColumns.length + (selectable ? 1 : 0) + (actions.length > 0 ? 1 : 0)}
                className="text-center py-8 text-gray-500"
              >
                {emptyMessage}
              </TableCell>
            </TableRow>
          ) : (
            filteredData.map((row) => (
              <TableRow
                key={row[idKey]}
                className={onRowClick ? "cursor-pointer hover:bg-gray-50" : ""}
                onClick={() => onRowClick && handleRowClick(row)}
              >
                {selectable && (
                  <TableCell>
                    <input
                      type="checkbox"
                      checked={selectedRows.includes(row[idKey])}
                      onChange={() => toggleRowSelection(row[idKey])}
                      onClick={(e) => e.stopPropagation()}
                      className="h-4 w-4 rounded border-gray-300"
                    />
                  </TableCell>
                )}
                {resolvedColumns.map(col => (
                  <TableCell key={col.key}>
                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                  </TableCell>
                ))}
                {actions.length > 0 && (
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-1">
                      {actions.map((action, i) => {
                        const Icon = action.icon
                        return (
                          <Button
                            key={i}
                            size="sm"
                            variant={action.variant || "ghost"}
                            onClick={(e) => handleAction(action, row, e)}
                          >
                            {Icon && <Icon className="h-4 w-4" />}
                            {!Icon && action.label}
                          </Button>
                        )
                      })}
                    </div>
                  </TableCell>
                )}
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>

      <div className="mt-4 text-sm text-gray-500">
        Showing {filteredData.length} of {data.length} rows
      </div>
    </>
  )

  if (!title) {
    return <div className={className}>{tableContent}</div>
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>{tableContent}</CardContent>
    </Card>
  )
}
