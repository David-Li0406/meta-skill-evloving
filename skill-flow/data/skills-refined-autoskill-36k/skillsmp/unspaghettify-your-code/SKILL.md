---
name: unspaghettify-your-code
description: Essential rules and methods you must follow when refactoring code.
---

**エージェントスキル**: 成熟したコードを3層アーキテクチャにリファクタリングする
## 哲学: いつリファクタリングすべきか

### ❌ リファクタリングすべき**でない**とき

- **新機能の実装中**: まず動かすことが優先
- **要件が不明確**: 何が正解か分からない段階で構造化は無意味
- **プロトタイピング/PoC段階**: 検証が目的、コード品質は二の次
- **1回限りのスクリプト**: 使い捨てコードに投資しない

**原則**: "Premature optimization is the root of all evil" (早すぎる最適化は諸悪の根源)

### ✅ リファクタリングすべきとき

以下の**すべて**を満たす場合:

1. **要件が固まった**: 何を作るべきか明確になった
2. **動作検証済み**: PoC/プロトタイプで動作を確認した
3. **パターンが見えた**: 繰り返しや責務の混在が明確になった
4. **保守が必要**: これから長期的にメンテナンスする
5. **拡張予定**: 類似機能を追加する計画がある

**原則**: "Make it work, make it right, make it fast"

---

## リファクタリング判断基準

### 定量的な基準

| 指標 | しきい値 | アクション |
|------|---------|-----------|
| ファイル行数 | > 500行 | 分割を検討 |
| 関数行数 | > 100行 | 分割を検討 |
| 関数内の責務 | 3つ以上 | 分離を検討 |
| 重複コード | 3箇所以上 | 抽象化を検討 |

### 定性的な基準

- **"ここに何を書けばいいか分からない"** → 責務が不明確
- **"変更の影響範囲が予測できない"** → 結合度が高い
- **"テストが書けない"** → 依存関係が複雑
- **"似たコードを3回書いた"** → 抽象化の機会

---

## 3層アーキテクチャ方針

### 目的

- **関心の分離**: ハードウェア/ビジネスロジック/UIの分離
- **テスタビリティ**: 各層を独立してテスト可能
- **再利用性**: HAL層は他プロジェクトでも利用可能
- **保守性**: 変更の影響範囲を限定

### 層の定義

```
┌─────────────────────────────────────────┐
│  Layer 3: Application Layer             │
│  - main(), CLI parsing, signal handling │
│  - 責務: ライフサイクル管理               │
│  - サイズ: ~100行                        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Layer 2: Pipeline/Business Logic       │
│  - ワークフロー統合、データフロー         │
│  - 責務: 複数のHALを組み合わせた処理      │
│  - サイズ: ~200-300行/ファイル            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Layer 1: Hardware Abstraction (HAL)    │
│  - ハードウェアAPI の薄いラッパー         │
│  - 責務: 単一ハードウェアの操作           │
│  - サイズ: ~200-300行/ファイル            │
└─────────────────────────────────────────┘
```

### 各層の責務

#### Layer 1: HAL (Hardware Abstraction Layer)

**DO (推奨)**:
- ✅ ハードウェアAPIの直接呼び出しをカプセル化
- ✅ エラーハンドリングを統一
- ✅ リソース管理 (create/destroy) を提供
- ✅ ハードウェア固有の設定を隠蔽

**DON'T (禁止)**:
- ❌ ビジネスロジックを含めない
- ❌ 他のHAL層を呼ばない (依存しない)
- ❌ グローバル状態を持たない
- ❌ アプリケーション固有の処理を含めない

**サンプル** (今回の実装):
```c
// vio_lowlevel.h - VIO HAL
int vio_create(vio_context_t *ctx, int camera_index, ...);
int vio_start(vio_context_t *ctx);
int vio_get_frame(vio_context_t *ctx, hbn_vnode_image_t *frame, int timeout_ms);
void vio_destroy(vio_context_t *ctx);
```

#### Layer 2: Pipeline/Business Logic

**DO (推奨)**:
- ✅ 複数のHAL層を組み合わせる
- ✅ データフローを制御
- ✅ ビジネスロジックを実装
- ✅ 状態管理

**DON'T (禁止)**:
- ❌ ハードウェアAPIを直接呼ばない
- ❌ main()を含めない
- ❌ CLI引数解析を含めない

**サンプル** (今回の実装):
```c
// camera_pipeline.h - VIO + Encoder統合
typedef struct {
    vio_context_t vio;           // HAL層を利用
    encoder_context_t encoder;   // HAL層を利用
    SharedFrameBuffer *shm_h264;
    volatile bool *running_flag;
} camera_pipeline_t;

int pipeline_run(camera_pipeline_t *pipeline, volatile bool *running_flag);
```

#### Layer 3: Application Layer

**DO (推奨)**:
- ✅ main()関数
- ✅ CLI引数解析
- ✅ シグナルハンドリング
- ✅ ライフサイクル管理

**DON'T (禁止)**:
- ❌ ビジネスロジックを含めない
- ❌ ハードウェアAPIを直接呼ばない
- ❌ 複雑な処理を含めない (Pipeline層に委譲)

**サンプル** (今回の実装):
```c
// camera_daemon_main.c
int main(int argc, char *argv[]) {
    // 1. Parse arguments
    // 2. Signal handling
    // 3. Create pipeline (Pipeline層を利用)
    // 4. Start pipeline
    // 5. Run pipeline
    // 6. Cleanup
}
```

---

## 命名規則

### ファイル命名

| 層 | パターン | 例 |
|----|---------|-----|
| HAL | `{hardware}_lowlevel.c/h` | `vio_lowlevel.c`, `encoder_lowlevel.c` |
| Pipeline | `{domain}_pipeline.c/h` | `camera_pipeline.c` |
| Application | `{app}_main.c` | `camera_daemon_main.c` |

### 関数命名

| 層 | パターン | 例 |
|----|---------|-----|
| HAL | `{hardware}_{verb}()` | `vio_create()`, `encoder_encode_frame()` |
| Pipeline | `pipeline_{verb}()` | `pipeline_run()`, `pipeline_create()` |

---

## インフラストラクチャ

### ログライブラリ

**要件**:
- ログレベル (DEBUG, INFO, WARN, ERROR)
- モジュール名表示
- スレッドセーフ
- 組み込みシステムで軽量 (~150行)

**実装**: `logger.c/h`

**使い方**:
```c
#include "logger.h"

// 初期化 (main関数で1回)
log_init(LOG_LEVEL_INFO, stdout, 0);

// 各モジュールで使用
LOG_INFO("VIO", "Pipeline created successfully");
LOG_ERROR("Encoder", "hb_mm_mc_configure failed: %d", ret);
```

**推奨**:
- ✅ `printf`/`fprintf` の代わりにLOG_*マクロを使う
- ✅ モジュール名は固定文字列 (ファイル名由来)
- ✅ エラー時は必ずエラーコードも出力

**禁止**:
- ❌ `printf`でエラーを出力しない (LOG_ERRORを使う)
- ❌ ログレベルを無視しない (DEBUG情報はLOG_DEBUGで)

---

## リファクタリングプロセス

### Phase 1: 分析

1. **既存コードの理解**
   - 責務を列挙 (ハードウェア操作 / ビジネスロジック / UI)
   - 依存関係を図示
   - 重複コードを特定

2. **境界の特定**
   - どこでHAL層とPipeline層を分けるか
   - どのハードウェアをカプセル化するか

### Phase 2: HAL層の抽出

1. **1つのハードウェアに集中**
   - 例: VIO (VIN→ISP→VSE)
   - 例: Encoder (H.264)

2. **最小限のAPIを設計**
   - create/start/process/stop/destroy パターン
   - context構造体でステートを管理

3. **既存コードから抽出**
   - ハードウェアAPIの呼び出しをコピー
   - エラーハンドリングを統一
   - ログ出力を統一

4. **テスト**
   - 元のコードと同じ動作をするか確認

### Phase 3: Pipeline層の抽出

1. **ワークフローを特定**
   - 例: VIO → Encoder → 共有メモリ

2. **HAL層を組み合わせる**
   - 複数のHAL contextを保持
   - データフローを実装

3. **テスト**
   - エンドツーエンドで動作確認

### Phase 4: Application層の簡素化

1. **main()をシンプルに**
   - 引数解析
   - Pipeline層の呼び出し
   - クリーンアップ

2. **テスト**
   - 元の機能と同等か確認
   - パフォーマンス検証 (FPS等)

---

## プロジェクト固有の詳細

### D-Robotics X5 固有

#### ハードウェア制約

| 項目 | 制限 | 対処 |
|------|------|------|
| H.264 Bitrate | <= 700 kbps | デフォルト600kbps推奨 |
| Camera Index | 0 or 1 | Camera 0→MIPI Host 0, Camera 1→MIPI Host 2 |
| bus_select | 常に0 | 両カメラで0を使用 |

#### 重要API

**VIO (Low-level)**:
- `hbn_camera_create()` - カメラ初期化
- `hbn_vnode_open()` - VIN/ISP/VSEノード作成
- `hbn_vflow_bind_vnode()` - パイプライン接続
- `hbn_vnode_getframe()` - フレーム取得

**Encoder (Low-level)**:
- `hb_mm_mc_initialize()` - エンコーダー初期化
- `hb_mm_mc_configure()` - エンコーダー設定
- `hb_mm_mc_start()` - エンコーダー起動
- `hb_mm_mc_queue_input_buffer()` - NV12入力
- `hb_mm_mc_dequeue_output_buffer()` - H.264出力

#### ビルド設定

**必須ライブラリ**:
```makefile
LDLIBS := -lrt -lpthread -lcam -lvpf -lhbmem -lmultimedia
```

**ヘッダーインクルード**:
```c
#include "hb_camera_interface.h"
#include "hb_camera_data_config.h"
#include "hbn_api.h"
#include "hb_media_codec.h"
#include "hb_mem_mgr.h"
```

---

## 成功指標

リファクタリングが成功したかの判断基準:

### 必須条件

- ✅ **機能等価性**: 元のコードと同じ動作をする
- ✅ **性能維持**: FPS等のパフォーマンスが劣化しない
- ✅ **ビルド成功**: 警告なしでビルドできる

### 推奨条件

- ✅ **ファイルサイズ**: 各ファイルが300行以下
- ✅ **責務明確**: 各ファイルの役割が1文で説明できる
- ✅ **依存最小**: 各層が下の層のみに依存
- ✅ **テスト可能**: 各層を独立してテスト可能
- ✅ **ログ整理**: 統一されたログ出力

---

## チェックリスト

### リファクタリング前

- [ ] 既存コードが動作している
- [ ] 要件が固まっている
- [ ] パフォーマンス目標を達成している
- [ ] 重複/責務混在が明確になっている

### リファクタリング中

- [ ] HAL層が完成し、単体で動作する
- [ ] Pipeline層が完成し、HAL層を使って動作する
- [ ] Application層がシンプルになった
- [ ] ログライブラリを全体に統合した

### リファクタリング後

- [ ] 元のコードと同じ動作をする
- [ ] パフォーマンスが維持されている
- [ ] 警告なしでビルドできる
- [ ] ドキュメントを更新した (architecture_refactor_plan.md等)
- [ ] 制約事項を記録した (ビットレート制限等)

---

## 参考文献

- Martin Fowler - "Refactoring: Improving the Design of Existing Code"
- Robert C. Martin - "Clean Architecture"
- Kent Beck - "Test Driven Development: By Example"

---

## このスキルの使い方

### ユーザーがリファクタリングを依頼する場合

```
User: "camera_daemon_drobotics.c (886行) をリファクタリングしたい"

Agent:
1. まず判断基準を確認します
   - 要件は固まっていますか？
   - 動作検証は済んでいますか？
   - 保守・拡張の予定はありますか？

2. (条件を満たす場合) Phase 1: 分析
   - ファイルを読み、責務を列挙
   - HAL層候補を特定

3. Phase 2-4: 実装
   - HAL層を抽出
   - Pipeline層を作成
   - Application層を簡素化

4. 検証
   - パフォーマンステスト
   - 動作確認
```

### エージェントが自動判断する場合

エージェントは以下の状況で自動的にリファクタリングを提案します:

- ファイルが500行を超え、複数の責務が混在している
- ユーザーが「整理したい」「構造化したい」と発言した
- 類似コードが3箇所以上に出現した

**提案形式**:
```
"このファイルは{行数}行で、{責務1}と{責務2}が混在しています。
3層アーキテクチャにリファクタリングすることで:
- 各ファイルが{予想行数}行程度に収まる
- テスタビリティが向上する
- 保守性が向上する

リファクタリングを実施しますか？"
```

---

## アンチパターン

### ❌ 早すぎるリファクタリング

**NG例**:
```c
// たった50行の単純なスクリプトを3層に分割
// → 過度な複雑化、メンテナンスコストが上がるだけ
```

**正解**: 小さくシンプルなコードはそのまま残す

### ❌ 過度な抽象化

**NG例**:
```c
// 1箇所でしか使わない処理をわざわざ関数化
AbstractFactoryBuilder* builder = createAbstractFactoryBuilder();
// → YAGNI違反
```

**正解**: 3箇所以上で重複してから抽象化を検討

### ❌ 無意味な分割

**NG例**:
```c
// getter/setterだけのファイル
// utils.c に何でも詰め込む
// → 責務が不明確
```

**正解**: 明確な責務を持つ単位で分割

---

## 今回のケーススタディ

### Before (PoC段階)
- `camera_poc_lowlevel.c` - 639行
- VIO操作 + Encoder操作 + メインループが混在
- **目的**: 30fps達成の検証 → ✅ 成功

### 判断
- 要件固定: 2カメラ同時30fps
- 動作検証済み: PoCで達成
- 保守予定: デーモンとして長期運用
- 拡張予定: デコーダー追加など

→ **リファクタリング決定**

### After (リファクタリング後)
- `vio_lowlevel.c/h` - 334行 (HAL)
- `encoder_lowlevel.c/h` - 203行 (HAL)
- `camera_pipeline.c/h` - 217行 (Pipeline)
- `camera_daemon_main.c` - 177行 (Application)
- `logger.c/h` - 106行 (Infrastructure)

**合計**: 1037行 (PoC 639行から400行増)

**トレードオフ**:
- コード量は増えたが、各ファイルの責務が明確に
- テスタビリティ向上 (各層を独立テスト可能)
- 再利用性向上 (HAL層は他プロジェクトでも使用可)
- 保守性向上 (変更の影響範囲が限定)

**結果**:
- 機能等価性: ✅ 同じ動作
- 性能維持: ✅ Camera 0: 29.87 FPS, Camera 1: 30.40 FPS
- ビルド: ✅ 警告なし

---

## まとめ

**リファクタリングの金言**:

> "Make it work, make it right, make it fast"
>
> まず動かせ。次に正しくしろ。最後に速くしろ。

**リファクタリングすべきタイミング**:

> 要件が固まり、動作が確認でき、長期保守が必要になったとき。
> それまでは、汚くても素早く回せ。
