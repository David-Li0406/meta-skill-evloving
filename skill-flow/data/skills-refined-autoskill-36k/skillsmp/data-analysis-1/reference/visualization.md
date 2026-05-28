# データ可視化ガイド

## 目次
- グラフの選び方
- matplotlib
- seaborn
- plotly
- ダッシュボード

## グラフの選び方

| 目的 | グラフタイプ |
|------|--------------|
| 時系列の推移 | 折れ線グラフ |
| カテゴリ比較 | 棒グラフ |
| 構成比 | 円グラフ、積み上げ棒 |
| 分布 | ヒストグラム、箱ひげ図 |
| 相関 | 散布図 |
| 地理データ | 地図 |

## matplotlib

### 基本設定

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# 日本語フォント設定
plt.rcParams["font.family"] = "IPAGothic"
# または
mpl.rcParams["font.sans-serif"] = ["Hiragino Sans", "Yu Gothic", "Meiryo"]

# スタイル設定
plt.style.use("seaborn-v0_8-whitegrid")

# サイズ設定
plt.figure(figsize=(10, 6))
```

### 折れ線グラフ

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df["date"], df["sales"], label="売上", marker="o")
ax.plot(df["date"], df["profit"], label="利益", marker="s")

ax.set_xlabel("日付")
ax.set_ylabel("金額")
ax.set_title("売上・利益推移")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("chart.png", dpi=150)
plt.show()
```

### 棒グラフ

```python
fig, ax = plt.subplots(figsize=(10, 6))

categories = df["category"]
values = df["amount"]

bars = ax.bar(categories, values, color="steelblue")

# 値ラベル
for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{value:,.0f}", ha="center", va="bottom")

ax.set_xlabel("カテゴリ")
ax.set_ylabel("金額")
ax.set_title("カテゴリ別売上")

plt.tight_layout()
plt.show()
```

### 複数グラフ

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].plot(df["date"], df["sales"])
axes[0, 0].set_title("売上推移")

axes[0, 1].bar(df["category"], df["count"])
axes[0, 1].set_title("カテゴリ別件数")

axes[1, 0].scatter(df["price"], df["quantity"])
axes[1, 0].set_title("価格vs数量")

axes[1, 1].hist(df["age"], bins=20)
axes[1, 1].set_title("年齢分布")

plt.tight_layout()
plt.show()
```

## seaborn

### 分布

```python
import seaborn as sns

# ヒストグラム + KDE
sns.histplot(data=df, x="amount", kde=True)

# 箱ひげ図
sns.boxplot(data=df, x="category", y="amount")

# バイオリンプロット
sns.violinplot(data=df, x="category", y="amount")
```

### カテゴリ比較

```python
# カウントプロット
sns.countplot(data=df, x="category", hue="status")

# 棒グラフ（集計値）
sns.barplot(data=df, x="category", y="amount", estimator="sum")
```

### 相関・関係

```python
# 散布図
sns.scatterplot(data=df, x="price", y="quantity", hue="category", size="amount")

# 回帰直線付き
sns.regplot(data=df, x="price", y="quantity")

# ペアプロット
sns.pairplot(df[["price", "quantity", "rating"]], hue="category")

# 相関行列ヒートマップ
corr = df[["price", "quantity", "rating", "amount"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
```

### 時系列

```python
# 時系列プロット
sns.lineplot(data=df, x="date", y="amount", hue="category")
```

## plotly

### インタラクティブグラフ

```python
import plotly.express as px
import plotly.graph_objects as go

# 折れ線グラフ
fig = px.line(df, x="date", y="amount", color="category",
              title="カテゴリ別売上推移")
fig.show()

# 棒グラフ
fig = px.bar(df, x="category", y="amount", color="status",
             barmode="group", title="カテゴリ別売上")
fig.show()

# 散布図
fig = px.scatter(df, x="price", y="quantity", 
                 color="category", size="amount",
                 hover_data=["name"])
fig.show()
```

### カスタマイズ

```python
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["date"], y=df["sales"],
    mode="lines+markers",
    name="売上"
))

fig.add_trace(go.Bar(
    x=df["date"], y=df["profit"],
    name="利益",
    yaxis="y2"
))

fig.update_layout(
    title="売上・利益推移",
    xaxis_title="日付",
    yaxis_title="売上",
    yaxis2=dict(title="利益", overlaying="y", side="right"),
    legend=dict(x=0, y=1),
    hovermode="x unified"
)

fig.show()
```

### HTML出力

```python
fig.write_html("chart.html")
fig.write_image("chart.png")  # kaleido必要
```

## ダッシュボード

### Streamlit

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("売上ダッシュボード")

# データ読み込み
df = pd.read_csv("sales.csv")

# フィルター
categories = st.multiselect("カテゴリ", df["category"].unique())
if categories:
    df = df[df["category"].isin(categories)]

# メトリクス
col1, col2, col3 = st.columns(3)
col1.metric("総売上", f"¥{df['amount'].sum():,.0f}")
col2.metric("件数", f"{len(df):,}")
col3.metric("平均", f"¥{df['amount'].mean():,.0f}")

# グラフ
st.subheader("売上推移")
fig = px.line(df.groupby("date")["amount"].sum().reset_index(),
              x="date", y="amount")
st.plotly_chart(fig, use_container_width=True)

# データテーブル
st.subheader("データ")
st.dataframe(df)
```

実行:
```bash
streamlit run app.py
```

### Dash

```python
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv("sales.csv")

app.layout = html.Div([
    html.H1("売上ダッシュボード"),
    dcc.Dropdown(
        id="category-dropdown",
        options=[{"label": c, "value": c} for c in df["category"].unique()],
        multi=True,
        placeholder="カテゴリを選択"
    ),
    dcc.Graph(id="sales-chart")
])

@callback(
    Output("sales-chart", "figure"),
    Input("category-dropdown", "value")
)
def update_chart(categories):
    filtered = df if not categories else df[df["category"].isin(categories)]
    fig = px.line(filtered.groupby("date")["amount"].sum().reset_index(),
                  x="date", y="amount")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
```
