# pandas 操作ガイド

## 目次
- データ読み込み
- データ選択・フィルタ
- データ変換
- 集計・グループ化
- 結合・マージ
- 欠損値処理

## データ読み込み

```python
import pandas as pd

# CSV
df = pd.read_csv("data.csv", encoding="utf-8")

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# JSON
df = pd.read_json("data.json")

# SQL
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@localhost/db")
df = pd.read_sql("SELECT * FROM users", engine)

# オプション指定
df = pd.read_csv(
    "data.csv",
    encoding="utf-8",
    dtype={"id": str, "amount": float},  # 型指定
    parse_dates=["created_at"],           # 日付パース
    na_values=["", "N/A", "null"],        # NA値
    usecols=["id", "name", "amount"],     # 読み込む列
    nrows=1000                            # 行数制限
)
```

## データ選択・フィルタ

### 列選択

```python
# 単一列
df["name"]

# 複数列
df[["name", "age"]]

# 条件で選択
df.loc[:, df.columns.str.startswith("user_")]
```

### 行選択

```python
# インデックス指定
df.loc[0]           # ラベル
df.iloc[0]          # 位置

# スライス
df.loc[0:10]        # ラベル
df.iloc[0:10]       # 位置

# 条件フィルタ
df[df["age"] >= 18]
df[df["status"] == "active"]
df[df["name"].str.contains("田")]

# 複数条件
df[(df["age"] >= 18) & (df["status"] == "active")]
df[(df["category"] == "A") | (df["category"] == "B")]
df[df["category"].isin(["A", "B", "C"])]

# 欠損値フィルタ
df[df["email"].notna()]
df[df["phone"].isna()]
```

### query メソッド

```python
df.query("age >= 18 and status == 'active'")
df.query("category in ['A', 'B']")

# 変数を使用
min_age = 20
df.query("age >= @min_age")
```

## データ変換

### 列の追加・変更

```python
# 新しい列
df["full_name"] = df["last_name"] + " " + df["first_name"]
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 30, 50, 100], labels=["未成年", "若年", "中年", "シニア"])

# 条件付き
df["is_adult"] = df["age"].apply(lambda x: x >= 18)
df["category"] = df["amount"].apply(lambda x: "high" if x > 10000 else "low")

# 複数条件
df["grade"] = np.select(
    [df["score"] >= 90, df["score"] >= 70, df["score"] >= 50],
    ["A", "B", "C"],
    default="D"
)
```

### 型変換

```python
# 数値
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# 日付
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

# 文字列
df["id"] = df["id"].astype(str)

# カテゴリ
df["status"] = df["status"].astype("category")
```

### 文字列操作

```python
# 大文字・小文字
df["name_upper"] = df["name"].str.upper()
df["name_lower"] = df["name"].str.lower()

# 分割・結合
df["domain"] = df["email"].str.split("@").str[1]
df["full_name"] = df["first"].str.cat(df["last"], sep=" ")

# 置換
df["phone"] = df["phone"].str.replace("-", "")

# 抽出
df["year"] = df["date_str"].str.extract(r"(\d{4})")
```

## 集計・グループ化

### 基本集計

```python
df["amount"].sum()
df["amount"].mean()
df["amount"].median()
df["amount"].std()
df["amount"].min()
df["amount"].max()
df["amount"].count()
df["amount"].nunique()

# 複数統計
df["amount"].agg(["sum", "mean", "count"])
```

### グループ集計

```python
# 単一列でグループ化
df.groupby("category")["amount"].sum()

# 複数列でグループ化
df.groupby(["category", "region"])["amount"].sum()

# 複数集計
df.groupby("category").agg({
    "amount": ["sum", "mean", "count"],
    "quantity": "sum"
})

# 名前付き集計
df.groupby("category").agg(
    total_amount=("amount", "sum"),
    avg_amount=("amount", "mean"),
    order_count=("id", "count")
)
```

### ピボットテーブル

```python
pd.pivot_table(
    df,
    values="amount",
    index="category",
    columns="month",
    aggfunc="sum",
    fill_value=0
)
```

### クロス集計

```python
pd.crosstab(df["category"], df["status"], margins=True)
```

## 結合・マージ

```python
# 内部結合
pd.merge(df1, df2, on="id")

# 左結合
pd.merge(df1, df2, on="id", how="left")

# 複数キーで結合
pd.merge(df1, df2, on=["user_id", "date"])

# 異なる列名で結合
pd.merge(df1, df2, left_on="user_id", right_on="id")

# 縦方向に連結
pd.concat([df1, df2], ignore_index=True)

# 横方向に連結
pd.concat([df1, df2], axis=1)
```

## 欠損値処理

```python
# 欠損値確認
df.isnull().sum()
df.info()

# 削除
df.dropna()                    # 欠損がある行を削除
df.dropna(subset=["name"])     # 特定列の欠損で削除
df.dropna(thresh=3)            # 3つ以上の値がある行のみ

# 補完
df["age"].fillna(0)                    # 固定値
df["age"].fillna(df["age"].mean())     # 平均値
df["age"].fillna(method="ffill")       # 前の値
df["age"].fillna(method="bfill")       # 後の値

# 補間
df["value"].interpolate()              # 線形補間
```

## 出力

```python
# CSV
df.to_csv("output.csv", index=False, encoding="utf-8-sig")

# Excel
df.to_excel("output.xlsx", index=False, sheet_name="Data")

# 複数シート
with pd.ExcelWriter("output.xlsx") as writer:
    df1.to_excel(writer, sheet_name="Data1", index=False)
    df2.to_excel(writer, sheet_name="Data2", index=False)
```
