---
name: product-recommendation
description: 基于用户皮肤档案和社区数据，生成个性化产品推荐。实现产品推荐功能时使用此技能。
---

# 产品推荐技能

## 概述
结合用户皮肤档案、社区验证数据和AI分析，生成个性化、可信的产品推荐。

## 推荐算法
```swift
class ProductRecommendationEngine {
    
    /// 主推荐函数
    func recommend(
        for user: UserProfile,
        category: ProductCategory? = nil,
        priceRange: PriceRange? = nil,
        limit: Int = 20
    ) async -> [ProductRecommendation] {
        // 1. 获取候选产品
        var candidates = await productDatabase.getProducts(
            category: category,
            priceRange: priceRange
        )
        
        // 2. 排除用户过敏成分
        candidates = filterOutAllergens(candidates, user.allergies)
        
        // 3. 排除用户不喜欢的品牌
        candidates = filterOutBrands(candidates, user.dislikedBrands)
        
        // 4. 计算推荐分数
        let scored = await calculateScores(candidates, for: user)
        
        // 5. 排序并返回
        return scored
            .sorted { $0.score > $1.score }
            .prefix(limit)
            .map { $0 }
    }
    
    private func calculateScores(
        _ products: [Product],
        for user: UserProfile
    ) async -> [ProductRecommendation] {
        // 获取用户的皮肤双胞胎
        let skinTwins = await skinMatcher.findSkinTwins(for: user.fingerprint)
        
        return products.map { product in
            var score: Double = 0
            var reasons: [String] = []
            var warnings: [String] = []
            
            // 权重配置
            let weights = RecommendationWeights()
            
            // 1. 相似用户有效率 (40%)
            let communityScore = calculateCommunityScore(product, skinTwins)
            score += communityScore.value * weights.community
            if let reason = communityScore.reason { reasons.append(reason) }
            
            // 2. 成分适配度 (30%)
            let ingredientScore = calculateIngredientScore(product, user)
            score += ingredientScore.value * weights.ingredient
            if let reason = ingredientScore.reason { reasons.append(reason) }
            if let warning = ingredientScore.warning { warnings.append(warning) }
            
            // 3. 问题针对性 (20%)
            let concernScore = calculateConcernScore(product, user.concerns)
            score += concernScore.value * weights.concern
            if let reason = concernScore.reason { reasons.append(reason) }
            
            // 4. 刺激风险 (-10%)
            let riskScore = calculateRiskScore(product, user)
            score -= riskScore.value * weights.risk
            if let warning = riskScore.warning { warnings.append(warning) }
            
            return ProductRecommendation(
                product: product,
                score: min(1.0, max(0, score)),
                reasons: reasons,
                warnings: warnings.isEmpty ? nil : warnings,
                communityData: communityScore.data
            )
        }
    }
}

struct RecommendationWeights {
    let community: Double = 0.4     // 社区验证
    let ingredient: Double = 0.3    // 成分适配
    let concern: Double = 0.2       // 问题针对
    let risk: Double = 0.1          // 刺激风险
}
```

## 各维度评分详解

### 社区验证分数
```swift
struct CommunityScoreResult {
    let value: Double
    let reason: String?
    let data: CommunityData?
}

struct CommunityData: Codable {
    let effectiveRate: Double       // 有效率
    let sampleSize: Int             // 样本量
    let confidenceInterval: Double  // 置信区间
    let avgImprovementDays: Double  // 平均起效天数
}

func calculateCommunityScore(
    _ product: Product,
    _ skinTwins: [SkinTwin]
) -> CommunityScoreResult {
    let relevantData = skinTwins.compactMap { twin in
        twin.effectiveProducts.first { $0.product.id == product.id }
    }
    
    guard relevantData.count >= 3 else {
        // 样本量不足，返回中性分数
        return CommunityScoreResult(value: 0.5, reason: nil, data: nil)
    }
    
    let totalSimilarity = skinTwins
        .filter { $0.effectiveProducts.contains { $0.product.id == product.id } }
        .reduce(0.0) { $0 + $1.similarity }
    
    let weightedEffectiveness = relevantData.reduce(0.0) { sum, data in
        sum + data.improvementPercent
    } / Double(relevantData.count)
    
    let effectiveRate = Double(relevantData.filter { $0.improvementPercent > 10 }.count) / Double(relevantData.count)
    
    let data = CommunityData(
        effectiveRate: effectiveRate,
        sampleSize: relevantData.count,
        confidenceInterval: calculateCI(relevantData.count),
        avgImprovementDays: relevantData.reduce(0.0) { $0 + Double($1.usageDuration) } / Double(relevantData.count)
    )
    
    let reason = "\(Int(effectiveRate * 100))%相似用户验证有效（\(relevantData.count)人）"
    
    return CommunityScoreResult(
        value: weightedEffectiveness / 100,
        reason: reason,
        data: data
    )
}
```

### 成分适配分数
```swift
func calculateIngredientScore(
    _ product: Product,
    _ user: UserProfile
) -> (value: Double, reason: String?, warning: String?) {
    var score: Double = 0.5 // 基准分
    var reason: String?
    var warning: String?
    
    // 检查有益成分
    let beneficialIngredients = product.ingredients.filter { ingredient in
        isIngredientBeneficial(ingredient, for: user.skinType, concerns: user.concerns)
    }
    
    if !beneficialIngredients.isEmpty {
        score += 0.3 * min(1.0, Double(beneficialIngredients.count) / 3)
        reason = "含有\(beneficialIngredients.prefix(2).map(\.name).joined(separator: "、"))"
    }
    
    // 检查风险成分
    let riskyIngredients = product.ingredients.filter { ingredient in
        isIngredientRisky(ingredient, for: user.skinType)
    }
    
    if !riskyIngredients.isEmpty {
        score -= 0.2 * min(1.0, Double(riskyIngredients.count) / 2)
        warning = "含\(riskyIngredients.first!.name)，\(user.skinType.rawValue)肤质需注意"
    }
    
    return (max(0, min(1, score)), reason, warning)
}
```

## 推荐结果模型
```swift
struct ProductRecommendation: Identifiable {
    let id = UUID()
    let product: Product
    let score: Double               // 0-1
    let reasons: [String]           // 推荐理由
    let warnings: [String]?         // 风险提示
    let communityData: CommunityData?
    
    /// 是否有足够的社区数据支撑
    var hasCommunityValidation: Bool {
        guard let data = communityData else { return false }
        return data.sampleSize >= 10
    }
    
    /// 推荐强度标签
    var strengthLabel: String {
        switch score {
        case 0.8...: return "强烈推荐"
        case 0.6..<0.8: return "推荐"
        case 0.4..<0.6: return "可考虑"
        default: return "谨慎选择"
        }
    }
}
```

## 透明度展示
```swift
struct RecommendationTransparency: View {
    let recommendation: ProductRecommendation
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // 推荐分数可视化
            ScoreBar(score: recommendation.score)
            
            // 推荐理由
            ForEach(recommendation.reasons, id: \.self) { reason in
                Label(reason, systemImage: "checkmark.circle.fill")
                    .foregroundColor(.green)
            }
            
            // 风险提示
            if let warnings = recommendation.warnings {
                ForEach(warnings, id: \.self) { warning in
                    Label(warning, systemImage: "exclamationmark.triangle.fill")
                        .foregroundColor(.orange)
                }
            }
            
            // 社区数据
            if let data = recommendation.communityData {
                CommunityDataView(data: data)
            } else {
                Text("暂无社区验证数据，推荐基于AI分析")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            // 商业披露
            if recommendation.product.isSponsored {
                Label("品牌合作", systemImage: "info.circle")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }
}

struct CommunityDataView: View {
    let data: CommunityData
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("社区验证数据")
                .font(.caption)
                .fontWeight(.medium)
            
            HStack {
                StatItem(label: "有效率", value: "\(Int(data.effectiveRate * 100))%")
                StatItem(label: "样本量", value: "\(data.sampleSize)人")
                StatItem(label: "平均起效", value: "\(Int(data.avgImprovementDays))天")
            }
            
            Text("95%置信区间")
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color.secondary.opacity(0.1))
        .cornerRadius(8)
    }
}
```

## 商业化隔离
```swift
/// 推荐排序与商业化完全隔离
/// 商业合作只影响展示位置，不影响推荐分数

struct RecommendationPresenter {
    func present(
        recommendations: [ProductRecommendation],
        sponsoredProducts: [Product]
    ) -> [DisplayItem] {
        var items: [DisplayItem] = []
        
        // 推荐产品按分数排序（不受商业影响）
        let sortedRecommendations = recommendations
            .sorted { $0.score > $1.score }
            .enumerated()
            .map { DisplayItem.recommendation($0.element, rank: $0.offset + 1) }
        
        items.append(contentsOf: sortedRecommendations)
        
        // 商业产品单独展示区域（明确标注）
        if !sponsoredProducts.isEmpty {
            items.append(.sponsoredSection(sponsoredProducts))
        }
        
        return items
    }
}

enum DisplayItem {
    case recommendation(ProductRecommendation, rank: Int)
    case sponsoredSection([Product])
}
```

## 验证
- [ ] 推荐分数计算准确
- [ ] 排序不受商业影响
- [ ] 透明度展示完整
- [ ] 社区数据正确统计
- [ ] 用户过滤正确应用
