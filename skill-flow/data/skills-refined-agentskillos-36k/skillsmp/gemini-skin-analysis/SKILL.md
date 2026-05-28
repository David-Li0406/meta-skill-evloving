---
name: gemini-skin-analysis
description: 使用Gemini Vision API分析皮肤照片，返回结构化分析结果。当需要实现AI皮肤分析功能时自动调用此技能。
---

# Gemini皮肤分析技能

## 概述
调用Gemini 2.0 Flash Vision API分析用户面部照片，返回多维度皮肤评估结果。

## 输入
- `image`: UIImage - 用户面部照片
- `userProfile`: UserProfile? - 用户基础信息（可选）
  - age: Int
  - gender: Gender
  - knownAllergies: [String]

## API配置
```swift
struct GeminiConfig {
    static let model = "gemini-2.0-flash"
    static let baseURL = "https://generativelanguage.googleapis.com/v1beta"
    static let endpoint = "/models/\(model):generateContent"
}
```

## 请求构建
```swift
func buildRequest(image: UIImage, apiKey: String) -> URLRequest {
    let url = URL(string: "\(GeminiConfig.baseURL)\(GeminiConfig.endpoint)?key=\(apiKey)")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let imageData = image.jpegData(compressionQuality: 0.8)!
    let base64Image = imageData.base64EncodedString()
    
    let body: [String: Any] = [
        "contents": [[
            "parts": [
                ["text": promptTemplate],
                ["inline_data": [
                    "mime_type": "image/jpeg",
                    "data": base64Image
                ]]
            ]
        ]],
        "generationConfig": [
            "temperature": 0.1,
            "topP": 0.8,
            "maxOutputTokens": 2048
        ]
    ]
    
    request.httpBody = try? JSONSerialization.data(withJSONObject: body)
    return request
}
```

## Prompt模板
```
你是一位专业皮肤科医生，拥有20年临床经验。请仔细分析这张面部照片。

## 分析要求
请评估以下维度，以JSON格式返回结果：

1. skinType: 肤质类型
   - "dry": 干性（紧绷、脱皮、细纹明显）
   - "oily": 油性（T区泛油、毛孔明显）
   - "combination": 混合性（T区油、两颊干）
   - "sensitive": 敏感性（泛红、易过敏）

2. skinAge: 皮肤表观年龄（数字）

3. overallScore: 综合健康评分（0-100）

4. issues: 问题评分（每项0-10，0为无问题，10为严重）
   - spots: 色斑/色素沉着
   - acne: 痘痘/粉刺
   - pores: 毛孔粗大
   - wrinkles: 皱纹/细纹
   - redness: 红血丝/泛红
   - evenness: 肤色不均
   - texture: 纹理粗糙

5. regions: 区域评分（0-100，100为最佳）
   - tZone: T区（额头+鼻子）
   - leftCheek: 左脸颊
   - rightCheek: 右脸颊
   - eyeArea: 眼周
   - chin: 下巴

6. recommendations: 护肤建议数组（3-5条）

## 输出格式
仅返回JSON对象，不要包含其他文字或markdown代码块标记。
```

## 响应解析
```swift
struct SkinAnalysis: Codable {
    let skinType: SkinType
    let skinAge: Int
    let overallScore: Int
    let issues: IssueScores
    let regions: RegionScores
    let recommendations: [String]
    
    struct IssueScores: Codable {
        let spots: Int
        let acne: Int
        let pores: Int
        let wrinkles: Int
        let redness: Int
        let evenness: Int
        let texture: Int
    }
    
    struct RegionScores: Codable {
        let tZone: Int
        let leftCheek: Int
        let rightCheek: Int
        let eyeArea: Int
        let chin: Int
    }
}

enum SkinType: String, Codable {
    case dry, oily, combination, sensitive
}
```

## 错误处理
```swift
enum AnalysisError: Error {
    case invalidImage
    case networkError(Error)
    case apiError(String)
    case parseError
    case rateLimited
    case unauthorized
}

// 重试策略
func analyzeWithRetry(image: UIImage, maxRetries: Int = 2) async throws -> SkinAnalysis {
    var lastError: Error?
    for attempt in 0..<maxRetries {
        do {
            return try await analyze(image: image)
        } catch AnalysisError.rateLimited {
            try await Task.sleep(nanoseconds: UInt64(pow(2.0, Double(attempt))) * 1_000_000_000)
            lastError = AnalysisError.rateLimited
        } catch {
            lastError = error
            break
        }
    }
    throw lastError ?? AnalysisError.networkError(NSError())
}
```

## 验证
- [ ] API Key正确配置
- [ ] 图片压缩后小于4MB
- [ ] 返回JSON正确解析
- [ ] 错误情况正确处理
- [ ] 超时设置合理（30秒）
