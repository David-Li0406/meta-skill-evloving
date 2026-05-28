---
name: effect-tracking
description: 28天效果追踪，对比分析皮肤变化，生成改善报告。实现追踪功能时使用此技能。
---

# 效果追踪技能

## 概述
记录用户28天护肤旅程，通过AI对比分析皮肤变化，生成可分享的改善报告。

## 追踪周期设计
```
Day 0 (基准) → Day 7 → Day 14 → Day 21 → Day 28 (结束)
    ↓           ↓        ↓         ↓          ↓
  拍照       拍照     拍照      拍照       拍照
  分析       对比     对比      对比       总结报告
```

## 数据模型
```swift
import SwiftData

@Model
class TrackingSession {
    @Attribute(.unique) var id: UUID
    var startDate: Date
    var endDate: Date?
    var status: TrackingStatus
    var targetProducts: [String]    // 使用的产品ID
    var checkIns: [CheckIn]
    var finalReport: TrackingReport?
    
    init() {
        self.id = UUID()
        self.startDate = Date()
        self.status = .active
        self.checkIns = []
    }
}

enum TrackingStatus: String, Codable {
    case active      // 进行中
    case completed   // 已完成
    case abandoned   // 已放弃
}

@Model
class CheckIn {
    var id: UUID
    var sessionId: UUID
    var day: Int                    // 第几天
    var captureDate: Date
    var photoPath: String           // 本地存储路径
    var analysis: SkinAnalysis?
    var usedProducts: [String]      // 当天使用的产品
    var notes: String?              // 用户备注
    var feeling: Feeling?           // 主观感受
    
    enum Feeling: String, Codable {
        case better, same, worse
    }
}
```

## 对比分析
```swift
struct ComparisonResult {
    let beforeAnalysis: SkinAnalysis
    let afterAnalysis: SkinAnalysis
    let daysPassed: Int
    let changes: [DimensionChange]
    let overallImprovement: Double  // 百分比
    
    struct DimensionChange {
        let dimension: String
        let before: Int
        let after: Int
        let changePercent: Double
        let trend: Trend
    }
    
    enum Trend {
        case improved, stable, worsened
    }
}

class ComparisonEngine {
    func compare(before: SkinAnalysis, after: SkinAnalysis, days: Int) -> ComparisonResult {
        let dimensions = [
            ("spots", before.issues.spots, after.issues.spots),
            ("acne", before.issues.acne, after.issues.acne),
            ("pores", before.issues.pores, after.issues.pores),
            ("wrinkles", before.issues.wrinkles, after.issues.wrinkles),
            ("redness", before.issues.redness, after.issues.redness),
            ("evenness", before.issues.evenness, after.issues.evenness),
            ("texture", before.issues.texture, after.issues.texture)
        ]
        
        let changes = dimensions.map { (name, beforeVal, afterVal) in
            let changePercent = beforeVal > 0 
                ? Double(beforeVal - afterVal) / Double(beforeVal) * 100 
                : 0
            let trend: ComparisonResult.Trend = 
                changePercent > 5 ? .improved :
                changePercent < -5 ? .worsened : .stable
            
            return ComparisonResult.DimensionChange(
                dimension: name,
                before: beforeVal,
                after: afterVal,
                changePercent: changePercent,
                trend: trend
            )
        }
        
        let overallImprovement = Double(after.overallScore - before.overallScore) / 
                                 Double(before.overallScore) * 100
        
        return ComparisonResult(
            beforeAnalysis: before,
            afterAnalysis: after,
            daysPassed: days,
            changes: changes,
            overallImprovement: overallImprovement
        )
    }
}
```

## 最终报告
```swift
struct TrackingReport: Codable {
    let sessionId: UUID
    let duration: Int               // 总天数
    let checkInCount: Int           // 打卡次数
    let completionRate: Double      // 完成率
    
    let beforePhoto: String         // Day 0 照片路径
    let afterPhoto: String          // 最后一天照片路径
    
    let overallImprovement: Double  // 整体改善百分比
    let scoreChange: Int            // 分数变化
    let skinAgeChange: Int          // 皮肤年龄变化
    
    let dimensionChanges: [DimensionSummary]
    let usedProducts: [ProductSummary]
    let aiSummary: String           // AI生成的总结
    let recommendations: [String]   // 后续建议
    
    struct DimensionSummary {
        let dimension: String
        let beforeScore: Int
        let afterScore: Int
        let improvement: Double
        let trend: String           // "↑改善" "→稳定" "↓恶化"
    }
    
    struct ProductSummary {
        let productId: String
        let productName: String
        let usageDays: Int
        let effectiveness: Effectiveness?
    }
    
    enum Effectiveness: String, Codable {
        case effective, neutral, ineffective
    }
}
```

## AI总结生成
```swift
func generateReportSummary(report: TrackingReport) async throws -> String {
    let prompt = """
    作为皮肤护理顾问，请为用户的28天护肤追踪生成总结报告。
    
    数据：
    - 追踪天数：\(report.duration)天
    - 打卡完成率：\(Int(report.completionRate * 100))%
    - 整体改善：\(Int(report.overallImprovement))%
    - 皮肤评分变化：\(report.scoreChange > 0 ? "+" : "")\(report.scoreChange)
    - 皮肤年龄变化：\(report.skinAgeChange > 0 ? "+" : "")\(report.skinAgeChange)岁
    
    各维度变化：
    \(report.dimensionChanges.map { "\($0.dimension): \($0.trend)\(Int($0.improvement))%" }.joined(separator: "\n"))
    
    使用产品：
    \(report.usedProducts.map { "\($0.productName): 使用\($0.usageDays)天" }.joined(separator: "\n"))
    
    请生成：
    1. 一段鼓励性的总结（2-3句话）
    2. 最明显的改善点
    3. 需要继续关注的问题
    4. 后续护肤建议（2-3条）
    
    语气要温暖、专业、鼓励性。
    """
    
    return try await geminiService.generateText(prompt: prompt)
}
```

## 分享卡片生成
```swift
struct ShareCard {
    let beforeImage: UIImage
    let afterImage: UIImage
    let duration: Int
    let improvement: Double
    let highlights: [String]
    
    func render() -> UIImage {
        // 生成可分享的图片卡片
        // 包含before/after对比、改善数据、产品信息
    }
}
```

## 提醒系统
```swift
class TrackingReminder {
    func scheduleReminders(for session: TrackingSession) {
        let checkInDays = [7, 14, 21, 28]
        
        for day in checkInDays {
            let triggerDate = Calendar.current.date(
                byAdding: .day, 
                value: day, 
                to: session.startDate
            )!
            
            let content = UNMutableNotificationContent()
            content.title = "记录你的皮肤变化 📸"
            content.body = "第\(day)天追踪日，来看看你的皮肤改善了多少！"
            content.sound = .default
            
            let trigger = UNCalendarNotificationTrigger(
                dateMatching: Calendar.current.dateComponents([.year, .month, .day, .hour], from: triggerDate),
                repeats: false
            )
            
            let request = UNNotificationRequest(
                identifier: "tracking-\(session.id)-day\(day)",
                content: content,
                trigger: trigger
            )
            
            UNUserNotificationCenter.current().add(request)
        }
    }
}
```

## 验证
- [ ] 追踪数据正确存储
- [ ] 对比分析计算准确
- [ ] 提醒通知按时发送
- [ ] 报告生成完整
- [ ] 分享卡片美观
