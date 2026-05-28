---
name: session-mode
description: セッションモード切替 - strict/normal/fast でGuard関手の動作を変更。Serena Memoryで状態永続化。
---

# セッションモード切替スキル

## 概要

Claude Codeの動作モードをセッション単位で切り替える。
モードに応じてGuard関手の挙動、読み込む仕様、確認フローが変化。

---

## モード定義

### strict モード（圏論的制約フル適用）

**Guard関手**:
```
Guard_strict : Action → {Allow, AskUser, Deny}
Guard_strict(a) = AskUser  ⟺ a ∈ Mor(Boundary)  # 常に確認
```

**読み込むファイル**:
- `~/.claude/guidelines/common/session-modes.md`
- `~/.claude/guidelines/common/guardrails.md`

**Boundary射の処理**:
- git commit/push: 必ず確認
- 設定変更: 必ず確認
- npm install: 必ず確認

**ユースケース**: 本番環境作業、重要なリファクタリング

---

### normal モード（デフォルト）

**Guard関手**:
```
Guard_normal : Action → {Allow, AskUser, Deny}
Guard_normal(a) = AskUser  ⟺ a ∈ {git_操作, ファイル削除, 設定変更}
```

**読み込むファイル**:
- CLAUDE.md（8原則）のみ

**Boundary射の処理**:
- git commit/push: 確認
- 設定変更: 確認
- npm install（安全）: 自動許可

**ユースケース**: 通常の開発作業

---

### fast モード（確認最小化）

**Guard関手**:
```
Guard_fast : Action → {Allow, AskUser, Deny}
Guard_fast(a) = Allow  ⟺ a ∈ Mor(Safe) ∪ Mor(SafeBoundary)
```

**SafeBoundary**:
```
SafeBoundary = {
  git commit（ローカル）,
  npm install（安全なライブラリ）,
  format(code)
}
```

**Boundary射の処理**:
- git commit: 自動許可（ローカルのみ）
- git push: 確認
- npm install（安全）: 自動許可

**ユースケース**: プロトタイピング、探索的開発

---

## Guard関手の数学的定義

### モード依存Guard関手

```
Guard_M : Mode × Action → {Allow, AskUser, Deny}

Guard_M(m, a) =
  | Allow   if a ∈ Safe_m
  | AskUser if a ∈ Boundary_m
  | Deny    if a ∈ Forbidden
```

### 各モードの射の分類

```
Safe_strict     = Mor(Safe)
Boundary_strict = Mor(Boundary)

Safe_normal     = Mor(Safe) ∪ {npm_install(safe_lib)}
Boundary_normal = Mor(Boundary) \ {npm_install(safe_lib)}

Safe_fast       = Mor(Safe) ∪ SafeBoundary
Boundary_fast   = Mor(Boundary) \ SafeBoundary
```

### 不変条件

```
∀m ∈ Mode, Forbidden ⊂ Mor(Forbidden)  # Forbiddenは不変
strict ⊑ normal ⊑ fast  # 制約の強さの順序
```

---

## Serena Memory スキーマ

```yaml
memory_key: "session-mode"
schema:
  mode: "strict" | "normal" | "fast"
  activated_at: ISO8601
  previous_mode: "strict" | "normal" | "fast" | null
```

---

## モード遷移図

```
         /mode strict
    ┌──────────────────┐
    │                  ▼
┌───────┐         ┌────────┐
│ fast  │◀───────▶│ strict │
└───────┘         └────────┘
    │                  │
    │   /mode normal   │
    │        │         │
    ▼        ▼         ▼
         ┌────────┐
         │ normal │
         └────────┘
```

---

## 関連コマンド

- `/kenron` - 圏論的思考法ロード（このスキル + guardrails.md を読み込み）

---

## 圏論的解釈

### モード圏の定義

```
Mode圏:
  対象: {strict, normal, fast}
  射: transition : Mode → Mode
  恒等射: id_m : m → m
```

### Guard関手の自然変換

```
η_mode : Guard_normal ⇒ Guard_mode

η_strict : Guard_normal → Guard_strict  （制約強化）
η_fast   : Guard_normal → Guard_fast    （制約緩和）
```
