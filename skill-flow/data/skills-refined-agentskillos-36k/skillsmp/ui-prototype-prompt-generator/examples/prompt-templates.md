# Prompt Template Examples

Complete, production-ready prompt templates for common application types across multiple design systems.

---

## Table of Contents

1. [Task Manager - iOS Native](#task-manager)
2. [Enterprise Dashboard - WeChat Work](#enterprise-dashboard)
3. [E-commerce App - Material Design 3](#ecommerce-app)
4. [Admin Panel - Ant Design Mobile](#admin-panel)
5. [Social App - Cross-Platform](#social-app)

---

## Task Manager

**Design System**: iOS Native (Human Interface Guidelines)
**Platform**: iPhone, iPad
**Target Users**: 25-45 professionals managing personal tasks

---

### Project Overview

**App Name**: TaskFlow

**Purpose**: Simple, elegant task management for personal productivity

**Core Value Proposition**: Focus on what matters with minimal friction

**Target Audience**:
- Demographics: 25-45 year old professionals
- Use Case: Personal task management, daily to-do tracking
- Pain Points: Complex task apps with too many features

**Key Features**:
1. Task list with priorities (High, Medium, Low)
2. Calendar view with due dates
3. Categories and custom tags
4. Quick add with Siri shortcuts
5. iCloud sync across devices

---

### Design System Specification

**System**: iOS Human Interface Guidelines (iOS 16+)
**Style**: Large navigation titles, translucent bars, SF Symbols
**Accessibility**: Dynamic Type support, VoiceOver labels, 44pt touch targets

---

### Information Architecture

```
TaskFlow
├── Home (Task List)
│   ├── Today
│   ├── Upcoming
│   └── All
├── Calendar
│   └── Month/Week view
├── Categories
│   ├── Work
│   ├── Personal
│   └── Custom categories
└── Settings
    ├── Notifications
    ├── Default reminder time
    └── iCloud sync
```

---

### Design Tokens

```swift
// Colors
extension UIColor {
    static let primaryAccent = UIColor.systemBlue
    static let priorityHigh = UIColor.systemRed
    static let priorityMedium = UIColor.systemOrange
    static let priorityLow = UIColor.systemGreen
    static let taskCompleted = UIColor.systemGray
}

// Typography
extension UIFont {
    static let taskTitle = UIFont.preferredFont(forTextStyle: .body)      // 17pt
    static let taskSubtitle = UIFont.preferredFont(forTextStyle: .callout) // 16pt
    static let categoryLabel = UIFont.preferredFont(forTextStyle: .subheadline) // 15pt
    static let timestamp = UIFont.preferredFont(forTextStyle: .caption1)  // 12pt
}

// Spacing
let spacingSmall: CGFloat = 8
let spacingMedium: CGFloat = 16
let spacingLarge: CGFloat = 24

// Corner Radius
let cornerRadius: CGFloat = 10
```

---

### Screen Specifications

#### 1. Home Screen (Task List)

**Navigation Bar**:
- Style: Large title
- Title: "Tasks"
- Right button: "+" (SF Symbol: `plus`)
- Background: System default (translucent)

**Search Bar** (UISearchBar):
- Placeholder: "Search tasks"
- Style: `.minimal`
- Cancel button: Appears when focused
- Position: Below navigation bar

**Segmented Control** (UISegmentedControl):
- Segments: "Today" | "Upcoming" | "All"
- Default: "Today"
- Tint color: System blue
- Position: Below search bar
- Height: 32pt
- Margin: 16pt horizontal

**Task List** (UITableView):
- Style: `.insetGrouped`
- Cell type: Custom `TaskCell`
- Swipe actions:
  - Leading: Mark complete (green, SF Symbol: `checkmark.circle.fill`)
  - Trailing: Delete (red, SF Symbol: `trash.fill`)
- Empty state: Illustration + "No tasks yet. Tap + to add one."

**TaskCell Components**:

```swift
// Layout structure
[Checkbox] [Task Content] [Priority Indicator]
           [Due Date]

// Component specs
Checkbox:
  - Type: UIButton with SF Symbol
  - Unchecked: `circle` (24pt, gray)
  - Checked: `checkmark.circle.fill` (24pt, blue)
  - Size: 44x44pt (touch target)

Task Content:
  - Title: UILabel
    - Font: .body (17pt)
    - Color: .label
    - Lines: 0 (unlimited)
  - Due Date: UILabel
    - Font: .caption1 (12pt)
    - Color: .secondaryLabel
    - Format: "Due: Tomorrow at 2:00 PM"

Priority Indicator:
  - Type: Colored dot (UIView)
  - Size: 8x8pt circle
  - Colors:
    - High: .systemRed
    - Medium: .systemOrange
    - Low: .systemGreen
  - Position: Top-right corner

Category Tag:
  - Type: UILabel with rounded background
  - Font: .caption2 (11pt)
  - Padding: 4pt vertical, 8pt horizontal
  - Corner radius: 8pt
  - Background: Category color at 20% opacity
```

**Interaction States**:
- **Default**: Full opacity, white background (light mode)
- **Completed**: 50% opacity, strikethrough text
- **Overdue**: Red due date text, exclamation mark icon
- **Tap**: Navigate to Task Detail screen
- **Swipe Right**: Reveal "Complete" action (green background)
- **Swipe Left**: Reveal "Delete" action (red background)

**Floating Button** (Custom):
- Position: Bottom-right, 16pt from edges
- Size: 56x56pt
- Icon: "+" (SF Symbol: `plus`)
- Background: System blue with blur
- Shadow: 0 2px 8px rgba(0,0,0,0.2)
- Action: Present "Add Task" sheet

---

#### 2. Add/Edit Task Screen (Bottom Sheet)

**Presentation Style**: `.pageSheet` (iOS 15+)
- Corner radius: 10pt (top corners)
- Detents: `.medium()`, `.large()`
- Dimming: 40% black overlay
- Dismissal: Swipe down or tap outside

**Navigation Bar**:
- Left button: "Cancel"
- Title: "New Task" or "Edit Task"
- Right button: "Save" (disabled until title entered)

**Form Fields** (UITableView with static cells):

1. **Task Title** (UITextField):
   - Placeholder: "What needs to be done?"
   - Style: `.roundedRect`
   - Clear button: `.whileEditing`
   - Keyboard: `.default`
   - Return key: `.done`

2. **Due Date** (UIDatePicker):
   - Style: `.inline` (iOS 14+)
   - Mode: `.dateAndTime`
   - Minimum date: Today
   - Initial: Tomorrow at 9:00 AM

3. **Priority** (UISegmentedControl):
   - Segments: "Low" | "Medium" | "High"
   - Tint color: Dynamic based on selection
   - Default: "Medium"

4. **Category** (UIButton with menu):
   - Style: `.plain`
   - Title: Selected category or "None"
   - Menu: List of categories + "Add New..."
   - Icon: SF Symbol matching category

5. **Notes** (UITextView):
   - Placeholder: "Add notes (optional)"
   - Font: `.body`
   - Min height: 88pt (2 lines)
   - Max characters: 500

6. **Reminders** (UISwitch):
   - Label: "Remind me"
   - Default: Off
   - When on: Show time picker below

**Validation**:
- "Save" button disabled if title is empty
- Show error if due date is in the past
- Auto-save as draft on dismiss

---

#### 3. Task Detail Screen

**Navigation Bar**:
- Style: Standard title
- Left button: "< Back"
- Title: Task title (truncated if long)
- Right button: "Edit"

**Content Sections** (UIScrollView):

**Priority Banner** (if High priority):
- Background: System red at 10% opacity
- Icon: SF Symbol `exclamation.triangle.fill`
- Text: "High Priority"
- Height: 44pt
- Position: Top of scroll view

**Task Information**:
- Checkbox: Large (32x32pt)
- Title: `.title3` (20pt bold)
- Due date: `.body` with calendar icon
- Category: Tag with icon
- Priority: Colored indicator

**Notes Section**:
- Header: "Notes"
- Content: UITextView (non-editable)
- Empty state: "No notes"

**Subtasks Section** (if any):
- Header: "Subtasks (2/5 completed)"
- List: Checkboxes + text
- Add button: "+ Add subtask"

**Metadata Section**:
- Created: Timestamp
- Modified: Timestamp
- Completed: Timestamp (if completed)

**Actions** (UIStackView at bottom):
- Complete Button: Full-width, green
- Delete Button: Secondary, red text

---

#### 4. Calendar Screen

**Navigation Bar**:
- Style: Large title
- Title: "Calendar"
- Right button: "Today" (quick jump)

**Calendar View** (FSCalendar or custom):
- Style: Week view (default)
- Toggle: Week | Month
- Dots: Indicate days with tasks
- Color: Priority color of highest priority task
- Selection: Highlights day, shows tasks below

**Task List** (for selected day):
- Grouped by time
- Shows task title, category, priority
- Tap: Navigate to task detail

---

#### 5. Categories Screen

**Navigation Bar**:
- Style: Large title
- Title: "Categories"
- Right button: "Edit"

**Category List** (UITableView):
- Cell type: `.default` with icon
- Icon: SF Symbol (user-selected)
- Title: Category name
- Accessory: Task count badge
- Swipe actions:
  - Edit: Rename, change icon/color
  - Delete: Confirm dialog

**Add Category Button**:
- Style: UIButton with system style
- Title: "+ Add Category"
- Position: Below list

**Default Categories**:
- Work (briefcase, blue)
- Personal (person, green)
- Shopping (cart, orange)
- Health (heart, red)

---

#### 6. Settings Screen

**Navigation Bar**:
- Style: Large title
- Title: "Settings"

**Settings Groups** (UITableView, `.insetGrouped`):

**Notifications**:
- Enable notifications: UISwitch
- Default reminder time: Time picker
- Sound: Selection list

**Appearance**:
- Theme: System | Light | Dark
- Accent color: Color picker

**Data & Sync**:
- iCloud sync: UISwitch with status
- Export data: CSV export
- Clear completed tasks: Destructive action

**About**:
- Version: Display only
- Privacy policy: External link
- Rate app: App Store link

---

### User Flows

#### Flow 1: Add a Task (Quick)

1. User taps "+" button (floating)
2. Bottom sheet slides up (medium detent)
3. User types task title: "Buy groceries"
4. User taps "Save"
5. Sheet dismisses, task appears in list with default settings

**Duration**: ~5 seconds

#### Flow 2: Complete a Task (Swipe)

1. User swipes right on task cell
2. Green "Complete" action reveals
3. User releases swipe
4. Task animates to completed state (strikethrough, fade to 50%)
5. Task moves to bottom of list (completed section)

**Duration**: ~2 seconds

#### Flow 3: Schedule a Task

1. User taps "+" button
2. Bottom sheet appears
3. User types task title
4. User taps "Due Date" field
5. Date picker expands inline
6. User selects date and time
7. User taps "Priority" segment
8. User selects "High"
9. User taps "Category" button
10. Menu appears, user selects "Work"
11. User taps "Save"
12. Task appears in list with priority indicator and category tag

**Duration**: ~30 seconds

---

### Edge Cases

**Empty States**:

1. **No Tasks (First Launch)**:
   - Illustration: Empty checklist graphic
   - Title: "Welcome to TaskFlow"
   - Subtitle: "Tap the + button to add your first task"
   - Primary action: Large "Add Task" button

2. **No Tasks Today**:
   - Illustration: Celebration graphic
   - Title: "All done for today!"
   - Subtitle: "Check upcoming tasks or relax"

3. **No Search Results**:
   - Icon: Magnifying glass
   - Title: "No results found"
   - Subtitle: "Try a different search term"

**Error States**:

1. **Sync Failed**:
   - Banner at top: Red background
   - Icon: Cloud with slash
   - Message: "Sync failed. Tap to retry."
   - Action: Retry button

2. **Network Offline**:
   - Banner: Yellow background
   - Icon: WiFi slash
   - Message: "You're offline. Changes will sync when connected."

3. **Data Load Failed**:
   - Full screen: Error icon
   - Message: "Unable to load tasks"
   - Actions: "Retry" | "Contact Support"

**Loading States**:

1. **Initial Load**:
   - Skeleton screens: Gray placeholder cells
   - Duration: Until data loads

2. **Pull-to-Refresh**:
   - Native UIRefreshControl with spinner
   - Message: "Updating..."

3. **Sync in Progress**:
   - Activity indicator in navigation bar
   - Subtle: Doesn't block interaction

**Validation**:

1. **Empty Task Title**:
   - "Save" button disabled (gray)
   - Border turns red on focus loss
   - Helper text: "Title is required"

2. **Past Due Date**:
   - Alert dialog: "Due date is in the past. Continue?"
   - Actions: "Change Date" | "Save Anyway"

3. **Duplicate Task**:
   - Warning banner: "Similar task exists. Add anyway?"
   - Show similar task with "View" link

---

### Accessibility

**VoiceOver Labels**:
- Checkbox: "Mark as complete" / "Completed"
- Priority dot: "High priority" / "Medium priority" / "Low priority"
- Due date: "Due tomorrow at 2 PM" (natural language)

**Dynamic Type**:
- All text scales with system settings
- Minimum: 12pt
- Maximum: 34pt
- Layout adjusts for larger text

**Color Contrast**:
- Text on background: 7:1 (WCAG AAA)
- Icons: 4.5:1 (WCAG AA)
- Priority indicators visible to colorblind users (shapes + colors)

**Keyboard Navigation** (iPad):
- Tab order: Top to bottom, left to right
- Return key: Move to next field
- Command+N: New task
- Command+F: Search

**Haptic Feedback**:
- Task completed: Success impact (medium)
- Task deleted: Warning impact (heavy)
- Swipe action: Selection feedback (light)

---

### Responsive Behavior

**iPhone SE (Compact Width)**:
- Navigation bar: Standard title (not large)
- Task list: Single column
- Floating button: Smaller (48pt)

**iPhone 14 Pro Max (Regular Width)**:
- Navigation bar: Large title
- Task list: Single column with wider margins
- Floating button: Standard (56pt)

**iPad (Regular Width & Height)**:
- Split view support: Master (task list) + Detail (task detail)
- Multi-column calendar view
- Floating button becomes toolbar button
- Keyboard shortcuts enabled

---

## Enterprise Dashboard

**Design System**: WeChat Work (WeUI)
**Platform**: WeChat Mini Program, Mobile Web (H5)
**Target Users**: Sales managers and executives

---

### Project Overview

**App Name**: SalesView

**Purpose**: Real-time sales data dashboard for enterprise teams

**Core Value Proposition**: Quick insights into sales performance without logging into desktop systems

**Target Audience**:
- Demographics: 30-50 year old sales managers, executives
- Use Case: Monitor team performance, review metrics on-the-go
- Pain Points: Complex desktop BI tools, slow access to data

**Key Features**:
1. Real-time sales metrics (revenue, orders, conversion rate)
2. Team leaderboard and individual performance
3. Trend charts (daily, weekly, monthly)
4. Alert notifications for important thresholds
5. Export reports (Excel, PDF)

---

### Design System Specification

**System**: WeChat Work (WeUI Framework)
**Style**: Flat design, minimal shadows, green primary color
**Accessibility**: Hairline borders, 44px touch targets, clear hierarchy

---

### Information Architecture

```
SalesView
├── Home (Dashboard Overview)
│   ├── Key Metrics (Cards)
│   ├── Trend Chart
│   └── Quick Actions
├── Team (Leaderboard)
│   ├── Top Performers
│   ├── Team Members List
│   └── Comparison View
├── Reports
│   ├── Daily Report
│   ├── Weekly Report
│   └── Custom Date Range
└── Alerts
    ├── Active Alerts
    └── Alert History
```

---

### Design Tokens

```css
/* Colors (WeUI Palette) */
--primary-color: #07C160;        /* WeChat Work Green */
--link-color: #576B95;           /* WeChat Blue */
--text-primary: #000000;
--text-secondary: #888888;
--border-color: #E5E5E5;
--background: #FFFFFF;
--background-secondary: #F7F7F7;
--warn-color: #FA5151;
--success-color: #07C160;

/* Typography */
--font-family: -apple-system-font, "Helvetica Neue", sans-serif;
--font-size-large: 18px;
--font-size-medium: 17px;
--font-size-base: 16px;
--font-size-small: 14px;
--font-size-mini: 13px;

/* Spacing */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 15px;
--spacing-lg: 20px;
--spacing-xl: 30px;

/* Border Radius */
--border-radius-sm: 4px;
--border-radius-md: 8px;
--border-radius-lg: 12px;
```

---

### Screen Specifications

#### 1. Home Screen (Dashboard Overview)

**NavigationBar** (weui-navigation-bar):
- Title: "销售数据"
- Background: #07C160 (green)
- Text color: #FFFFFF
- Height: 44px
- Left button: None (home screen)
- Right button: "设置" (settings icon)

**Key Metrics Section** (Grid of Cards):
- Layout: 2x2 grid with 15px gap
- Card style: `weui-panel`

**Metric Card Structure**:
```html
<div class="weui-panel metric-card">
  <div class="metric-icon">
    <img src="revenue-icon.png" width="32" height="32" />
  </div>
  <div class="metric-value">¥1,234,567</div>
  <div class="metric-label">今日营收</div>
  <div class="metric-change positive">
    <span class="arrow">↑</span>
    <span>+15.8%</span>
  </div>
</div>
```

**Metric Cards** (4 total):

1. **Today's Revenue**:
   - Icon: Money bag (green)
   - Value: ¥1,234,567 (font-size: 24px, bold)
   - Label: "今日营收"
   - Change: +15.8% (green text with ↑ arrow)

2. **Orders Count**:
   - Icon: Shopping bag (blue)
   - Value: 345 (font-size: 24px, bold)
   - Label: "订单数量"
   - Change: +8.2% (green text with ↑ arrow)

3. **Conversion Rate**:
   - Icon: Percentage (orange)
   - Value: 12.5% (font-size: 24px, bold)
   - Label: "转化率"
   - Change: -2.1% (red text with ↓ arrow)

4. **Average Order Value**:
   - Icon: Receipt (purple)
   - Value: ¥3,579 (font-size: 24px, bold)
   - Label: "客单价"
   - Change: +5.3% (green text with ↑ arrow)

**Trend Chart Section** (weui-panel):
- Title: "7日趋势"
- Chart type: Line chart (using ECharts or similar)
- X-axis: Last 7 days (dates)
- Y-axis: Revenue (¥)
- Line color: #07C160 (green)
- Data points: Circles on line
- Grid: Light gray dashed lines
- Height: 200px
- Padding: 15px

**Quick Actions** (weui-grid):
- Layout: 4 columns, single row
- Actions:
  1. "导出报表" (Export icon)
  2. "团队排行" (Trophy icon)
  3. "设置提醒" (Bell icon)
  4. "帮助中心" (Question mark icon)
- Style:
  - Icon size: 28x28px
  - Label font: 13px
  - Touch target: 80x80px

**Tab Bar** (weui-tabbar):
- Position: Fixed bottom
- Height: 50px
- Items (4 total):
  1. "首页" (Home icon) - Active
  2. "团队" (Team icon)
  3. "报表" (Report icon)
  4. "我的" (Profile icon)
- Active indicator: Green icon + text

---

#### 2. Team Screen (Leaderboard)

**NavigationBar**:
- Title: "团队排行"
- Background: #07C160
- Left button: None
- Right button: "筛选" (filter icon)

**Time Filter** (weui-navbar):
- Segments: "今日" | "本周" | "本月"
- Active: Underline with green bar (3px height)
- Default: "今日"

**Top Performers Section**:
- Title: "🏆 Top 3"
- Background: Linear gradient (light gold to white)

**Top 3 Cards** (Custom):

**1st Place Card**:
```html
<div class="weui-media-box top-performer first-place">
  <div class="rank-badge gold">1</div>
  <img class="avatar" src="user1.jpg" width="50" height="50" />
  <div class="info">
    <h4 class="name">张明</h4>
    <p class="title">高级销售经理</p>
    <p class="metrics">
      <span class="revenue">¥458,900</span>
      <span class="orders">156单</span>
    </p>
  </div>
  <div class="trophy">🏆</div>
</div>
```
- Background: #FFF8E1 (light gold)
- Border: 2px solid #FFD700 (gold)
- Height: 80px

**2nd and 3rd Place**:
- Similar structure
- 2nd: Silver badge, #F5F5F5 background, #C0C0C0 border
- 3rd: Bronze badge, #FFF3E0 background, #CD7F32 border

**Team Members List** (weui-cells):
- Cell type: `weui-cell`
- Starting from rank #4

**Member Cell Structure**:
```html
<div class="weui-cell">
  <div class="weui-cell__hd">
    <span class="rank">4</span>
    <img class="avatar" src="user4.jpg" width="40" height="40" />
  </div>
  <div class="weui-cell__bd">
    <p class="name">李华</p>
    <p class="title">销售专员</p>
  </div>
  <div class="weui-cell__ft">
    <p class="revenue">¥234,500</p>
    <p class="orders">98单</p>
  </div>
</div>
```

**Comparison View Toggle** (Floating Button):
- Position: Bottom-right, 16px from edges
- Icon: Bar chart
- Action: Open comparison modal

---

#### 3. Reports Screen

**NavigationBar**:
- Title: "报表中心"
- Left button: None
- Right button: "筛选日期"

**Report Types** (weui-cells):

**Daily Report Cell**:
```html
<div class="weui-cell weui-cell_access">
  <div class="weui-cell__hd">
    <img src="daily-icon.png" width="28" height="28" />
  </div>
  <div class="weui-cell__bd">
    <p>每日报表</p>
    <p class="weui-cell__desc">查看每日销售详情</p>
  </div>
  <div class="weui-cell__ft">
    <span class="date">2024-01-15</span>
  </div>
</div>
```

**Weekly Report Cell**:
- Similar structure
- Icon: Week calendar
- Description: "查看本周销售汇总"

**Custom Report Cell**:
- Icon: Calendar range
- Description: "自定义日期范围"
- Action: Open date picker dialog

**Export Section** (weui-panel):
- Title: "导出选项"
- Buttons:
  - "导出Excel" (green, primary)
  - "导出PDF" (white, bordered)
  - "分享到企业微信" (blue, link style)

---

#### 4. Report Detail Screen

**NavigationBar**:
- Title: "每日报表 - 2024-01-15"
- Left button: "< 返回"
- Right button: "导出"

**Summary Cards** (Similar to Home screen):
- Total Revenue
- Orders
- New Customers
- Returns

**Detailed Data Table** (weui-panel):
- Title: "销售明细"
- Table style: Alternating row colors
- Columns:
  - 时间 (Time)
  - 订单号 (Order ID)
  - 客户 (Customer)
  - 金额 (Amount)
- Scrollable horizontally if needed
- Pagination: "上一页" | "下一页"

**Charts Section**:
- Hourly trend (line chart)
- Product category breakdown (pie chart)
- Payment method distribution (bar chart)

**Action Button** (weui-btn):
- Text: "导出完整报表"
- Style: `weui-btn_primary`
- Width: Full width (minus 30px margins)
- Position: Fixed at bottom (above TabBar)

---

#### 5. Alerts Screen

**NavigationBar**:
- Title: "提醒通知"
- Left button: None
- Right button: "设置"

**Active Alerts Section** (weui-panel):
- Title: "当前提醒"
- Badge: Red dot if any active

**Alert Cell** (weui-media-box):
```html
<div class="weui-media-box alert-cell urgent">
  <div class="alert-icon">
    <img src="alert-icon.png" width="32" height="32" />
  </div>
  <div class="weui-media-box__bd">
    <h4 class="weui-media-box__title">转化率低于目标</h4>
    <p class="weui-media-box__desc">
      当前转化率：10.2%<br/>
      目标转化率：12.0%
    </p>
  </div>
  <div class="weui-media-box__ft">
    <span class="time">2小时前</span>
  </div>
</div>
```

**Alert Types**:
1. **Urgent** (Red):
   - Border-left: 4px solid red
   - Icon: Exclamation mark
   - Example: Revenue below threshold

2. **Warning** (Orange):
   - Border-left: 4px solid orange
   - Icon: Warning triangle
   - Example: Conversion rate declining

3. **Info** (Blue):
   - Border-left: 4px solid blue
   - Icon: Info circle
   - Example: New milestone reached

**Alert History** (weui-cells):
- Title: "历史记录"
- Collapsed by default
- Tap to expand (accordion style)

**Settings Button** (weui-btn):
- Text: "提醒设置"
- Style: `weui-btn_default`
- Action: Open settings dialog

---

### User Flows

#### Flow 1: Check Today's Performance

1. User opens app (Home screen loads)
2. Key metrics animate in (fade + slide up)
3. User scans 4 metric cards (< 5 seconds)
4. User taps "7日趋势" chart to see details
5. Chart expands to full screen modal
6. User swipes to close modal

**Duration**: ~15 seconds

#### Flow 2: View Team Leaderboard

1. User taps "团队" in TabBar
2. Team screen loads with "今日" filter active
3. Top 3 performers display with badges
4. User scrolls down to see full list
5. User taps "本周" filter
6. List refreshes with weekly data
7. User taps member name to see details

**Duration**: ~20 seconds

#### Flow 3: Export Report

1. User taps "报表" in TabBar
2. Report types list displays
3. User taps "每日报表"
4. Report detail screen loads
5. User scrolls to review data
6. User taps "导出完整报表" button
7. Action sheet appears: "Excel | PDF | 取消"
8. User selects "Excel"
9. Toast appears: "导出成功"
10. Share sheet opens (WeChat Work)

**Duration**: ~30 seconds

---

### Edge Cases

**Empty States**:

1. **No Data Available**:
   - Illustration: Empty chart graphic
   - Title: "暂无数据"
   - Subtitle: "今日暂无销售记录"
   - Action: "刷新" button

2. **No Team Members**:
   - Illustration: Team icon
   - Title: "暂无团队成员"
   - Subtitle: "请联系管理员添加"

**Error States**:

1. **Network Error**:
   - Toast: "网络连接失败，请检查网络"
   - Retry button in empty state
   - Cached data shown with timestamp

2. **Data Load Failed**:
   - Full screen error
   - Message: "数据加载失败"
   - Actions: "重试" | "联系客服"

**Loading States**:

1. **Initial Load**:
   - Skeleton screens: Gray placeholders for metrics
   - Duration: Until data loads

2. **Pull-to-Refresh**:
   - WeUI loading icon (spinning)
   - Message: "加载中..."

3. **Chart Loading**:
   - Spinner in chart area
   - Skeleton bars/lines

**Validation**:

1. **Invalid Date Range**:
   - Dialog: "开始日期不能晚于结束日期"
   - Action: "确定" (close dialog)

2. **Export Limit Exceeded**:
   - Toast: "报表数据过大，请缩小日期范围"
   - Suggestion: "建议范围：30天内"

---

### Accessibility

**Touch Targets**:
- Minimum: 44x44px (WeChat standard)
- Buttons: 48px height
- List items: 56px height

**Color Contrast**:
- Text on white: 4.5:1 (WCAG AA)
- Green on white: 3:1 (large text)
- All icons have text labels

**Screen Reader Support**:
- Alt text for all images
- ARIA labels for interactive elements
- Descriptive button text (not just icons)

**Font Scaling**:
- Support WeChat font size settings
- Layout adapts to larger text (line wrapping)

---

### Responsive Behavior

**WeChat Mobile (360px width)**:
- 2-column metric grid
- Full-width chart
- Single-column quick actions

**iPad / Large Screens (768px+)**:
- 4-column metric grid
- Side-by-side charts
- 2-column quick actions
- Larger font sizes (+2px)

---

## E-commerce App

**Design System**: Material Design 3
**Platform**: Android (Kotlin/Jetpack Compose)
**Target Users**: Online shoppers, 18-45 years old

---

### Project Overview

**App Name**: ShopFlow

**Purpose**: Modern e-commerce experience with personalized recommendations

**Core Value Proposition**: Discover products you love with AI-powered recommendations

**Target Audience**:
- Demographics: 18-45 year old online shoppers
- Use Case: Browse, search, and purchase products
- Pain Points: Generic recommendations, cluttered UI, slow checkout

**Key Features**:
1. Product browsing with smart filters
2. AI-powered personalized recommendations
3. Quick checkout (one-click buy)
4. Order tracking with real-time updates
5. Wishlist and product comparisons

---

### Design System Specification

**System**: Material Design 3 (Material You)
**Style**: Dynamic color system, elevation shadows, FAB, ripple effects
**Accessibility**: 48dp touch targets, WCAG AA contrast, TalkBack support

---

### Design Tokens

```kotlin
// Material 3 Color Scheme (Light Theme)
val md_theme_light_primary = Color(0xFF6750A4)
val md_theme_light_onPrimary = Color(0xFFFFFFFF)
val md_theme_light_primaryContainer = Color(0xFFEADDFF)
val md_theme_light_onPrimaryContainer = Color(0xFF21005D)

val md_theme_light_secondary = Color(0xFF625B71)
val md_theme_light_onSecondary = Color(0xFFFFFFFF)
val md_theme_light_secondaryContainer = Color(0xFFE8DEF8)
val md_theme_light_onSecondaryContainer = Color(0xFF1D192B)

val md_theme_light_surface = Color(0xFFFFFBFE)
val md_theme_light_onSurface = Color(0xFF1C1B1F)

val md_theme_light_error = Color(0xFFB3261E)
val md_theme_light_onError = Color(0xFFFFFFFF)

// Typography (Roboto)
val Typography = Typography(
    displayLarge = TextStyle(fontSize = 57.sp, lineHeight = 64.sp, fontFamily = Roboto),
    headlineLarge = TextStyle(fontSize = 32.sp, lineHeight = 40.sp, fontFamily = Roboto),
    titleLarge = TextStyle(fontSize = 22.sp, lineHeight = 28.sp, fontFamily = Roboto),
    bodyLarge = TextStyle(fontSize = 16.sp, lineHeight = 24.sp, fontFamily = Roboto),
    labelLarge = TextStyle(fontSize = 14.sp, lineHeight = 20.sp, fontFamily = Roboto, fontWeight = FontWeight.Medium),
)

// Elevation
val ElevationLevel1 = 1.dp
val ElevationLevel2 = 3.dp
val ElevationLevel3 = 6.dp
val ElevationLevel4 = 8.dp
val ElevationLevel5 = 12.dp

// Shape
val Shapes = Shapes(
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
)

// Spacing
val SpacingSmall = 8.dp
val SpacingMedium = 16.dp
val SpacingLarge = 24.dp
val SpacingXLarge = 32.dp
```

---

### Screen Specifications

#### 1. Home Screen

**Top App Bar** (Material Toolbar):
- Type: Large (collapses on scroll)
- Title: "ShopFlow"
- Height: 64dp (collapsed), 152dp (expanded)
- Background: Surface color
- Elevation: 0dp (default), 4dp (scrolled)
- Actions:
  - Search icon (magnifying glass)
  - Cart icon with badge (item count)

**Search Bar** (Material Search Bar):
- Style: Filled
- Placeholder: "Search products..."
- Leading icon: Magnifying glass
- Trailing icon: Voice search (microphone)
- Corner radius: 28dp (full pill)
- Height: 56dp
- Margin: 16dp horizontal
- Elevation: 1dp

**Category Chips** (Horizontal Scroll):
- Type: Material Chip (Filter)
- Items: "All" | "Electronics" | "Fashion" | "Home" | "Beauty" | "Sports"
- Selected state: Primary color background
- Unselected: Surface variant background
- Height: 32dp
- Spacing: 8dp gap

**Featured Banner** (Carousel):
- Type: ViewPager2 with indicator
- Image height: 200dp
- Corner radius: 16dp
- Indicator: Dots at bottom (8dp diameter)
- Auto-scroll: 5 seconds
- Margin: 16dp horizontal

**Product Grid** (LazyVerticalGrid):
- Columns: 2 (phone), 3 (tablet)
- Gap: 16dp
- Cell type: ProductCard (custom)

**ProductCard Structure**:
```kotlin
@Composable
fun ProductCard(product: Product) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        shape = MaterialTheme.shapes.medium, // 12dp corners
    ) {
        Column {
            // Product Image
            AsyncImage(
                model = product.imageUrl,
                contentDescription = product.name,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(180.dp),
                contentScale = ContentScale.Crop,
            )

            // Favorite Button (Overlay)
            IconButton(
                onClick = { /* Toggle favorite */ },
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(8.dp),
            ) {
                Icon(
                    imageVector = if (product.isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                    contentDescription = "Favorite",
                    tint = if (product.isFavorite) Color.Red else Color.White,
                )
            }

            // Product Info
            Column(modifier = Modifier.padding(12.dp)) {
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
                Spacer(modifier = Modifier.height(4.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Filled.Star,
                        contentDescription = null,
                        tint = Color(0xFFFFC107), // Amber
                        modifier = Modifier.size(16.dp),
                    )
                    Text(
                        text = "${product.rating} (${product.reviewCount})",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = "$${product.price}",
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.primary,
                        fontWeight = FontWeight.Bold,
                    )
                    if (product.discountPercent > 0) {
                        Text(
                            text = "${product.discountPercent}% OFF",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.error,
                            modifier = Modifier
                                .background(
                                    color = MaterialTheme.colorScheme.errorContainer,
                                    shape = RoundedCornerShape(4.dp),
                                )
                                .padding(horizontal = 6.dp, vertical = 2.dp),
                        )
                    }
                }
            }
        }
    }
}
```

**FAB (Floating Action Button)**:
- Type: Extended FAB
- Position: Bottom-right, 16dp from edges
- Icon: Filter (funnel icon)
- Text: "Filters"
- Background: Primary color
- Elevation: 6dp (resting), 12dp (pressed)
- Action: Open filter bottom sheet

**Bottom Navigation Bar**:
- Height: 80dp (with safe area)
- Items (4 total):
  1. Home (house icon) - Active
  2. Categories (grid icon)
  3. Wishlist (heart icon) with badge
  4. Profile (person icon)
- Active indicator: Pill shape background
- Inactive: Icon only

---

#### 2. Product Detail Screen

**Top App Bar**:
- Type: Standard (not large)
- Title: Hidden (transparent background initially)
- Background: Fades in on scroll
- Navigation: Back arrow (left)
- Actions:
  - Share icon
  - Cart icon with badge

**Product Image Gallery** (Pager):
- Height: 400dp
- Full-width images
- Swipe to navigate
- Indicator: Dots at bottom
- Zoom: Pinch to zoom support

**Product Info Section**:

**Title and Price**:
```kotlin
Column(modifier = Modifier.padding(16.dp)) {
    Text(
        text = product.name,
        style = MaterialTheme.typography.headlineMedium,
        fontWeight = FontWeight.Bold,
    )
    Spacer(modifier = Modifier.height(8.dp))
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text(
            text = "$${product.price}",
            style = MaterialTheme.typography.headlineLarge,
            color = MaterialTheme.colorScheme.primary,
            fontWeight = FontWeight.Bold,
        )
        if (product.originalPrice > product.price) {
            Spacer(modifier = Modifier.width(12.dp))
            Text(
                text = "$${product.originalPrice}",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textDecoration = TextDecoration.LineThrough,
            )
        }
    }
}
```

**Rating and Reviews**:
```kotlin
Row(
    modifier = Modifier
        .fillMaxWidth()
        .padding(horizontal = 16.dp)
        .clickable { /* Navigate to reviews */ },
    verticalAlignment = Alignment.CenterVertically,
) {
    repeat(5) { index ->
        Icon(
            imageVector = if (index < product.rating.toInt()) Icons.Filled.Star else Icons.Outlined.Star,
            contentDescription = null,
            tint = Color(0xFFFFC107),
        )
    }
    Spacer(modifier = Modifier.width(8.dp))
    Text(
        text = "${product.rating} (${product.reviewCount} reviews)",
        style = MaterialTheme.typography.bodyLarge,
    )
    Spacer(modifier = Modifier.weight(1f))
    Icon(
        imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
        contentDescription = "View reviews",
    )
}
```

**Color/Size Selection**:
```kotlin
// Color Chips
Text(
    text = "Color",
    style = MaterialTheme.typography.titleMedium,
    modifier = Modifier.padding(start = 16.dp),
)
LazyRow(
    horizontalArrangement = Arrangement.spacedBy(8.dp),
    contentPadding = PaddingValues(horizontal = 16.dp),
) {
    items(product.colors) { color ->
        FilterChip(
            selected = selectedColor == color,
            onClick = { selectedColor = color },
            label = { Text(color.name) },
            leadingIcon = {
                Box(
                    modifier = Modifier
                        .size(16.dp)
                        .background(color.hex, CircleShape),
                )
            },
        )
    }
}

// Size Chips
Text(
    text = "Size",
    style = MaterialTheme.typography.titleMedium,
    modifier = Modifier.padding(start = 16.dp, top = 16.dp),
)
FlowRow(
    modifier = Modifier.padding(horizontal = 16.dp),
    horizontalArrangement = Arrangement.spacedBy(8.dp),
) {
    product.sizes.forEach { size ->
        FilterChip(
            selected = selectedSize == size,
            onClick = { selectedSize = size },
            label = { Text(size) },
        )
    }
}
```

**Description**:
```kotlin
ExpandableText(
    text = product.description,
    style = MaterialTheme.typography.bodyLarge,
    maxLines = 3,
    modifier = Modifier.padding(16.dp),
)
```

**Specifications** (Expandable Card):
```kotlin
Card(
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp),
    elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Row(
            modifier = Modifier.clickable { expanded = !expanded },
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "Specifications",
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.weight(1f),
            )
            Icon(
                imageVector = if (expanded) Icons.Filled.KeyboardArrowUp else Icons.Filled.KeyboardArrowDown,
                contentDescription = if (expanded) "Collapse" else "Expand",
            )
        }
        AnimatedVisibility(visible = expanded) {
            Column {
                Spacer(modifier = Modifier.height(12.dp))
                product.specs.forEach { (key, value) ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                    ) {
                        Text(
                            text = key,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.weight(1f),
                        )
                        Text(
                            text = value,
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Medium,
                        )
                    }
                    if (key != product.specs.keys.last()) {
                        Divider(modifier = Modifier.padding(vertical = 4.dp))
                    }
                }
            }
        }
    }
}
```

**Similar Products** (Horizontal Scroll):
- Title: "You Might Also Like"
- Layout: LazyRow
- Cell: Smaller ProductCard (140dp width)

**Bottom Bar** (Actions):
- Layout: Row with 2 buttons
- Height: 80dp (with padding)
- Background: Surface with elevation
- Buttons:
  1. "Add to Cart" (Outlined button, secondary)
  2. "Buy Now" (Filled button, primary)
- Both buttons: Full height (56dp), equal width

---

#### 3. Cart Screen

**Top App Bar**:
- Title: "Shopping Cart"
- Navigation: Back arrow
- Action: Clear cart icon (trash)

**Cart Items List** (LazyColumn):
- Cell type: CartItemCard

**CartItemCard**:
```kotlin
@Composable
fun CartItemCard(item: CartItem) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Row(modifier = Modifier.padding(12.dp)) {
            // Product Image
            AsyncImage(
                model = item.product.imageUrl,
                contentDescription = item.product.name,
                modifier = Modifier
                    .size(80.dp)
                    .clip(MaterialTheme.shapes.small),
                contentScale = ContentScale.Crop,
            )
            Spacer(modifier = Modifier.width(12.dp))

            // Product Info
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.product.name,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Color: ${item.selectedColor}, Size: ${item.selectedSize}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    // Price
                    Text(
                        text = "$${item.product.price}",
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.primary,
                        fontWeight = FontWeight.Bold,
                    )

                    // Quantity Stepper
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        IconButton(onClick = { /* Decrease quantity */ }) {
                            Icon(Icons.Filled.Remove, contentDescription = "Decrease")
                        }
                        Text(
                            text = "${item.quantity}",
                            style = MaterialTheme.typography.titleMedium,
                            modifier = Modifier.padding(horizontal = 8.dp),
                        )
                        IconButton(onClick = { /* Increase quantity */ }) {
                            Icon(Icons.Filled.Add, contentDescription = "Increase")
                        }
                    }
                }
            }

            // Remove Button
            IconButton(onClick = { /* Remove item */ }) {
                Icon(
                    Icons.Filled.Close,
                    contentDescription = "Remove",
                    tint = MaterialTheme.colorScheme.error,
                )
            }
        }
    }
}
```

**Empty Cart State**:
- Illustration: Shopping cart icon (96dp)
- Title: "Your cart is empty"
- Subtitle: "Add items to get started"
- Action: "Start Shopping" button

**Summary Card** (Fixed at bottom):
```kotlin
Card(
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp),
    elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
) {
    Column(modifier = Modifier.padding(16.dp)) {
        // Subtotal
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Text(
                text = "Subtotal",
                style = MaterialTheme.typography.bodyLarge,
            )
            Text(
                text = "$$subtotal",
                style = MaterialTheme.typography.bodyLarge,
            )
        }
        Spacer(modifier = Modifier.height(4.dp))

        // Shipping
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Text(
                text = "Shipping",
                style = MaterialTheme.typography.bodyLarge,
            )
            Text(
                text = if (shipping == 0.0) "FREE" else "$$shipping",
                style = MaterialTheme.typography.bodyLarge,
                color = if (shipping == 0.0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface,
            )
        }
        Spacer(modifier = Modifier.height(8.dp))
        Divider()
        Spacer(modifier = Modifier.height(8.dp))

        // Total
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "Total",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
            )
            Text(
                text = "$$total",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.Bold,
            )
        }
        Spacer(modifier = Modifier.height(16.dp))

        // Checkout Button
        Button(
            onClick = { /* Navigate to checkout */ },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
        ) {
            Text("Proceed to Checkout")
        }
    }
}
```

---

#### 4. Checkout Screen

**Top App Bar**:
- Title: "Checkout"
- Navigation: Back arrow
- Steps indicator: 1 of 3

**Stepper** (Progress Indicator):
```kotlin
Row(
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp),
    horizontalArrangement = Arrangement.SpaceBetween,
) {
    CheckoutStep(step = 1, label = "Shipping", isActive = true, isCompleted = false)
    Divider(modifier = Modifier.weight(1f))
    CheckoutStep(step = 2, label = "Payment", isActive = false, isCompleted = false)
    Divider(modifier = Modifier.weight(1f))
    CheckoutStep(step = 3, label = "Review", isActive = false, isCompleted = false)
}
```

**Step 1: Shipping Address**:
- Form fields (Material Text Fields):
  - Full Name (outlined)
  - Phone Number (outlined)
  - Street Address (outlined, 2 lines)
  - City, State, ZIP (row of 3 fields)
- Saved addresses list (expandable)
- "Use saved address" chips

**Step 2: Payment Method**:
- Payment options (Radio buttons):
  - Credit/Debit Card (default)
  - PayPal
  - Apple Pay / Google Pay
- Card input fields:
  - Card number (with card icon detection)
  - Expiry date (MM/YY)
  - CVV (password field)
- "Save for future" checkbox

**Step 3: Review Order**:
- Order summary (read-only)
- Shipping address (editable link)
- Payment method (last 4 digits)
- Items list (condensed)
- Total amount

**Action Buttons** (Bottom):
- "Back" (text button, left)
- "Continue" or "Place Order" (filled button, right)

---

### User Flows

#### Flow 1: Browse and Add to Cart

1. User opens app (Home screen)
2. User scrolls through product grid
3. User taps product card
4. Product detail screen opens
5. User selects color and size
6. User taps "Add to Cart"
7. Snackbar appears: "Added to cart" with "View Cart" action
8. User continues browsing

**Duration**: ~30 seconds

#### Flow 2: Quick Checkout

1. User navigates to Cart screen
2. User reviews items
3. User taps "Proceed to Checkout"
4. Checkout screen opens (Step 1)
5. User selects saved address
6. User taps "Continue"
7. Step 2 loads (Payment)
8. User selects Google Pay
9. User taps "Continue"
10. Step 3 loads (Review)
11. User taps "Place Order"
12. Payment sheet appears (Google Pay)
13. User authenticates (fingerprint)
14. Success screen appears with order number

**Duration**: ~45 seconds

---

### Edge Cases

**Empty States**:
1. **No Products**: Illustration + "Check back soon"
2. **Empty Cart**: (See Cart Screen specification)
3. **No Search Results**: "No products found for '[query]'"

**Error States**:
1. **Payment Failed**: Dialog with retry option
2. **Out of Stock**: Disabled "Add to Cart", show "Notify Me" button
3. **Network Error**: Snackbar with retry action

**Loading States**:
1. **Product Grid**: Shimmer effect placeholders
2. **Image Loading**: Placeholder with blur effect
3. **Checkout Processing**: Full-screen progress indicator

---

### Accessibility

- **Touch Targets**: 48x48dp minimum
- **TalkBack**: Content descriptions for all icons and images
- **Color Contrast**: WCAG AA compliant
- **Text Scaling**: Support up to 200% scale

---

## Admin Panel

**Design System**: Ant Design Mobile
**Platform**: Mobile Web (React)

*[Truncated for length - similar detailed specification would continue]*

---

## Social App

**Design System**: Cross-platform (Responsive Web)

*[Truncated for length - similar detailed specification would continue]*

---

For the complete design system specifications, see [../references/design-systems.md](../references/design-systems.md).
