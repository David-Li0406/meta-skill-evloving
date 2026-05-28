# 統計分析ガイド

## 目次
- 記述統計
- 相関分析
- 仮説検定
- 回帰分析
- 時系列分析

## 記述統計

### 基本統計量

```python
import pandas as pd
import numpy as np

# 基本統計
df.describe()

# 個別統計量
df["amount"].mean()      # 平均
df["amount"].median()    # 中央値
df["amount"].std()       # 標準偏差
df["amount"].var()       # 分散
df["amount"].min()       # 最小値
df["amount"].max()       # 最大値
df["amount"].quantile([0.25, 0.5, 0.75])  # 四分位数

# 歪度・尖度
df["amount"].skew()      # 歪度
df["amount"].kurtosis()  # 尖度
```

### 度数分布

```python
# 度数
df["category"].value_counts()

# 相対度数
df["category"].value_counts(normalize=True)

# ビニング
pd.cut(df["age"], bins=[0, 18, 30, 50, 100], labels=["未成年", "若年", "中年", "シニア"])

# ヒストグラム用
pd.cut(df["amount"], bins=10).value_counts().sort_index()
```

## 相関分析

### 相関係数

```python
# ピアソン相関係数
df["price"].corr(df["quantity"])

# 相関行列
df[["price", "quantity", "rating"]].corr()

# スピアマン順位相関
df["price"].corr(df["quantity"], method="spearman")
```

### 相関の検定

```python
from scipy import stats

# ピアソン相関の検定
r, p_value = stats.pearsonr(df["price"], df["quantity"])
print(f"相関係数: {r:.3f}, p値: {p_value:.4f}")

# スピアマン相関の検定
r, p_value = stats.spearmanr(df["price"], df["quantity"])
```

## 仮説検定

### t検定

```python
from scipy import stats

# 1標本t検定（母平均との比較）
t_stat, p_value = stats.ttest_1samp(df["score"], popmean=50)
print(f"t統計量: {t_stat:.3f}, p値: {p_value:.4f}")

# 対応のない2標本t検定
group_a = df[df["group"] == "A"]["score"]
group_b = df[df["group"] == "B"]["score"]
t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t統計量: {t_stat:.3f}, p値: {p_value:.4f}")

# 対応のある2標本t検定
t_stat, p_value = stats.ttest_rel(df["before"], df["after"])
```

### カイ二乗検定

```python
from scipy import stats

# クロス集計表
contingency_table = pd.crosstab(df["gender"], df["preference"])

# カイ二乗検定
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
print(f"カイ二乗: {chi2:.3f}, p値: {p_value:.4f}, 自由度: {dof}")
```

### ANOVA（分散分析）

```python
from scipy import stats

# 一元配置分散分析
groups = [df[df["group"] == g]["score"] for g in df["group"].unique()]
f_stat, p_value = stats.f_oneway(*groups)
print(f"F統計量: {f_stat:.3f}, p値: {p_value:.4f}")

# statsmodelsを使用
import statsmodels.api as sm
from statsmodels.formula.api import ols

model = ols("score ~ C(group)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
```

### 効果量

```python
# コーエンのd（2群の差）
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (group1.mean() - group2.mean()) / pooled_std

d = cohens_d(group_a, group_b)
print(f"効果量(d): {d:.3f}")
# 目安: 0.2=小, 0.5=中, 0.8=大
```

## 回帰分析

### 単回帰

```python
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# sklearn
X = df[["price"]].values
y = df["quantity"].values

model = LinearRegression()
model.fit(X, y)

print(f"係数: {model.coef_[0]:.4f}")
print(f"切片: {model.intercept_:.4f}")
print(f"R²: {model.score(X, y):.4f}")

# statsmodels（詳細な統計量）
X_sm = sm.add_constant(df["price"])
model_sm = sm.OLS(df["quantity"], X_sm).fit()
print(model_sm.summary())
```

### 重回帰

```python
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# sklearn
X = df[["price", "rating", "ad_spend"]].values
y = df["sales"].values

model = LinearRegression()
model.fit(X, y)

print("係数:", dict(zip(["price", "rating", "ad_spend"], model.coef_)))
print(f"R²: {model.score(X, y):.4f}")

# statsmodels
X_sm = sm.add_constant(df[["price", "rating", "ad_spend"]])
model_sm = sm.OLS(df["sales"], X_sm).fit()
print(model_sm.summary())
```

### ロジスティック回帰

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

X = df[["age", "income", "score"]].values
y = df["purchase"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

## 時系列分析

### 移動平均

```python
# 単純移動平均
df["ma_7"] = df["sales"].rolling(window=7).mean()
df["ma_30"] = df["sales"].rolling(window=30).mean()

# 指数移動平均
df["ema_7"] = df["sales"].ewm(span=7).mean()
```

### トレンド分解

```python
from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(df["sales"], model="additive", period=7)

# 成分
trend = result.trend
seasonal = result.seasonal
residual = result.resid

# プロット
result.plot()
```

### 自己相関

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 自己相関関数
plot_acf(df["sales"], lags=30)

# 偏自己相関関数
plot_pacf(df["sales"], lags=30)
```

### ARIMA

```python
from statsmodels.tsa.arima.model import ARIMA

# モデル構築
model = ARIMA(df["sales"], order=(1, 1, 1))
result = model.fit()

print(result.summary())

# 予測
forecast = result.forecast(steps=7)
print(forecast)
```

### Prophet

```python
from prophet import Prophet

# データ準備（列名をds, yにする必要あり）
prophet_df = df.rename(columns={"date": "ds", "sales": "y"})

model = Prophet(daily_seasonality=True)
model.fit(prophet_df)

# 予測
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# プロット
model.plot(forecast)
model.plot_components(forecast)
```
