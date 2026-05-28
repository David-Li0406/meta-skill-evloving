/**
 * ActivityFeed - List of recent activities with avatars
 *
 * @prop {Array} items - Activity items: [{id, user, avatar, action, time, ...extra}]
 *   - user: Display name
 *   - avatar: Either initials (e.g. "AJ") or image URL
 *   - action: Action description (e.g. "completed order #1234")
 *   - time: Time string (e.g. "2 min ago")
 * @prop {function} onItemClick - Click handler (default: emits 'activity-click')
 * @prop {string} title - Card title (default: "Recent Activity")
 * @prop {string} description - Card description
 * @prop {string} emptyMessage - Message when no items (default: "No recent activity")
 * @prop {number} maxItems - Maximum items to show
 * @prop {boolean} showViewAll - Show "View All" button (default: true)
 * @prop {function} onViewAll - View All click handler (default: emits 'view-all-activity')
 * @prop {string} className - Additional CSS classes
 */
function ActivityFeed({
  items = [],
  onItemClick,
  title = "Recent Activity",
  description,
  emptyMessage = "No recent activity",
  maxItems,
  showViewAll = true,
  onViewAll,
  className = ""
}) {
  const displayItems = maxItems ? items.slice(0, maxItems) : items

  const handleItemClick = (item) => {
    if (onItemClick) {
      onItemClick(item)
    } else {
      window.canvasEmit("activity-click", item)
    }
  }

  const handleViewAll = () => {
    if (onViewAll) {
      onViewAll()
    } else {
      window.canvasEmit("view-all-activity", {})
    }
  }

  const content = (
    <>
      {displayItems.length === 0 ? (
        <p className="text-center py-8 text-gray-500">{emptyMessage}</p>
      ) : (
        <div className="space-y-4">
          {displayItems.map((item) => (
            <div
              key={item.id}
              className="flex items-center gap-4 cursor-pointer hover:bg-gray-50 p-2 rounded-lg -mx-2"
              onClick={() => handleItemClick(item)}
            >
              <Avatar>
                {item.avatar?.startsWith("http") ? (
                  <AvatarImage src={item.avatar} alt={item.user} />
                ) : null}
                <AvatarFallback>
                  {item.avatar || item.user?.split(" ").map(n => n[0]).join("").slice(0, 2)}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm">
                  <span className="font-medium">{item.user}</span>
                  {" "}{item.action}
                </p>
                <p className="text-xs text-gray-500">{item.time}</p>
              </div>
              <ChevronRight className="h-4 w-4 text-gray-400" />
            </div>
          ))}
        </div>
      )}
      {showViewAll && items.length > 0 && (
        <Button variant="ghost" className="w-full mt-4" onClick={handleViewAll}>
          View All Activity
        </Button>
      )}
    </>
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
