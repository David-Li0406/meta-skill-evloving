---
name: nsforge-formula-search
description: 外部公式搜尋。觸發詞：搜尋公式, Wikidata, BioModels, 物理常數, PK模型, 反應動力學。
---

# 外部公式搜尋 Skill

> **⚠️ 搜尋後必須向用戶展示結果！**
> - 搜尋結果用表格形式列出（名稱、公式、來源）
> - 取得詳情後顯示完整 LaTeX 公式
> - 物理常數要顯示數值和單位

## 概述

從外部權威來源（Wikidata、BioModels、SciPy）檢索準確的公式。
**使用直接精確檢索（非 RAG），確保公式正確性。**

## 工具速查

| 工具 | 用途 | 來源 |
|------|------|------|
| `formula_search(query)` | 🔍 統一搜尋 | 全部 |
| `formula_get(id, source)` | 📄 取得詳情 | 指定來源 |
| `formula_categories(source)` | 📂 列出分類 | 指定來源 |
| `formula_pk_models(model_type?)` | 💊 PK 模型 | BioModels |
| `formula_kinetic_laws()` | ⚗️ 反應動力學 | BioModels |
| `formula_constants(category?)` | 🔬 物理常數 | SciPy |

## 來源說明

| 來源 | 內容 | 適用領域 |
|------|------|----------|
| **Wikidata** | P2534 定義公式 | 物理、化學、工程、經濟 |
| **BioModels** | SBML 模型 | 藥動學、藥效學、酵素動力學 |
| **SciPy** | `scipy.constants` | 物理常數、單位換算 |

## 調用範例

### 1. 通用搜尋

```python
# 搜尋雷諾數
formula_search("Reynolds number")

# 搜尋熱力學公式
formula_search("entropy", domain="thermodynamics")

# 限定 Wikidata 來源
formula_search("Arrhenius", source="wikidata")
```

### 2. 藥動學模型（BioModels）

```python
# 列出所有 PK 模型
formula_pk_models()

# 指定模型類型
formula_pk_models(model_type="two_compartment")
# 可選: one_compartment, two_compartment, michaelis_menten
```

### 3. 反應動力學

```python
# 列出所有反應動力學法則
formula_kinetic_laws()
# 包含: Michaelis-Menten, Hill equation, 等
```

### 4. 物理常數

```python
# 列出所有常數
formula_constants()

# 按分類
formula_constants(category="electromagnetic")
# 可選: universal, electromagnetic, atomic, physico-chemical
```

### 5. 取得詳情

```python
# 用 Wikidata Q 號取得
formula_get(id="Q179057", source="wikidata")

# 用 BioModels ID 取得
formula_get(id="BIOMD0000000001", source="biomodels")
```

## 典型工作流

### 推導時搜尋公式

```python
# 1. 搜尋需要的公式
formula_search("Fick first law")

# 2. 取得詳情（含 LaTeX 和 SymPy 格式）
formula_get(id="Q179057", source="wikidata")

# 3. 在推導中使用（從 formula_get 取得的 sympy_str）
derivation_substitute(
    expression="J = -D * grad_C",  # 從公式庫取得
    variable="J",
    value=...,
    description="代入 Fick 第一定律"
)
```

### 藥動學建模

```python
# 1. 查看可用的 PK 模型
formula_pk_models()

# 2. 取得雙隔室模型詳情
formula_get(id="two_compartment", source="biomodels")

# 3. 直接使用返回的 sympy_str 進行推導
```

## 返回格式

```json
{
  "success": true,
  "results": [
    {
      "id": "Q179057",
      "name": "Reynolds number",
      "latex": "Re = \\frac{\\rho v L}{\\mu}",
      "sympy_str": "rho * v * L / mu",
      "variables": {
        "rho": {"description": "密度", "unit": "kg/m³"},
        "v": {"description": "流速", "unit": "m/s"}
      },
      "source": "wikidata",
      "url": "https://www.wikidata.org/wiki/Q179057"
    }
  ],
  "total": 1
}
```

## 注意事項

1. **優先使用 `formula_search`** - 它會自動搜尋最相關的來源
2. **藥學領域自動優先 BioModels** - 設定 `domain="pharmacokinetics"` 時
3. **公式驗證** - 取得公式後建議用 `check_dimensions` 驗證

