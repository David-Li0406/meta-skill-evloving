# 网页主题参考

## 可用主题

### 1. minimal - Apple 极简风格

**特点**:
- 纯白背景，优雅排版
- SF Pro 字体风格
- 微妙的卡片阴影
- 适合专业阅读和打印

**配色**:
- 背景: #ffffff
- 文字: #1d1d1f
- 强调色: #0071e3
- 次要文字: #86868b

**适用场景**: 正式报告、专业分享、打印输出

---

### 2. pharma-blue - 医药专业蓝

**特点**:
- 渐变蓝色头部
- 卡片式布局
- 专业医学感
- 清晰的信息层次

**配色**:
- 头部渐变: #1a365d → #2b6cb0
- 背景: #f0f4f8
- 卡片: #ffffff
- 强调色: #2b6cb0

**适用场景**: 专业演示、团队分享、医药行业报告

---

### 3. warm - 温暖柔和风格

**特点**:
- 温暖米色背景
- 衬线字体（Georgia）
- 柔和的视觉效果
- 适合长时间阅读

**配色**:
- 背景: #faf8f5
- 文字: #451a03
- 强调色: #d97706
- 卡片: #ffffff

**适用场景**: 个人阅读、邮件订阅、护眼需求

---

## 主题选择建议

| 场景 | 推荐主题 |
|------|----------|
| 正式报告 | minimal |
| 团队分享 | pharma-blue |
| 个人阅读 | warm |
| 打印输出 | minimal |
| 屏幕演示 | pharma-blue |
| 长时间阅读 | warm |

## 使用方法

```bash
# 使用极简主题
python generate_output.py --date today --theme minimal

# 使用医药蓝主题
python generate_output.py --date today --theme pharma-blue

# 使用温暖主题
python generate_output.py --date today --theme warm
```
