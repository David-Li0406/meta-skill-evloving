---
name: manage_gui_architecture
description: PyQt等のモノリシックなGUIクラスを、データパイプライン・励起・描画のマネージャークラスへ分離・リファクタリングする
---
# Managing GUI Architecture

このスキルは、数百行を超える巨大なメソッド（例：`update_graphs`）を持つGUIクラス（MainWindowなど）を、疎結合で保守性の高いアーキテクチャにリファクタリングするためのガイドラインを提供します。

## Core Architecture Pattern

### 1. Data Pipeline Stages
メインループ（タイマー駆動の `update_graphs` 等）を以下のステージに分割します：
- **Stage 1 (Collect)**: 各種ソース（NDS, Simulation, File）から抽象化された `data_map` (dict[name, TimeSeries]) を収集する。
- **Stage 2 (Excitation)**: `ExcitationManager` を介して信号を生成し、`data_map` に注入（Sum）または追加する。
- **Stage 3 (Processing/Logic)**: 時間クロッピング、平均化の停止判定、統計計算などのビジネスロジックを実行する。
- **Stage 4 (Render)**: `PlotRenderer` を介して解析結果を各プロットパネルに描画する。

### 2. Manager Classes
GUIロジックを詳細な処理から分離するために、以下のマネージャークラスを導入します：

- **ExcitationManager**:
  - UIコントロールからのパラメータ読み取り
  - 波形生成（`SignalGenerator` の呼び出し）
  - データバッファへの信号注入
- **PlotRenderer**:
  - プロットタイプ（Spectrogram vs Series）の判別とディスパッチ
  - 単位変換（dB, Phase, Magnitude）の抽象化
  - 座標変換（Log-Y、相対時間軸）の一括管理
  - ストリーミング中の表示範囲（Range）の安定化

## Instructions for Refactoring

1.  **Skeleton First**: 既存のメソッドから主要なロジックを抽出する前に、まずは `ExcitationManager` や `PlotRenderer` のスケルトンクラスを作成し、`MainWindow.__init__` でインスタンス化する。
2.  **Decouple UI state**: マネージャークラスは `MainWindow` への参照を保持してもよいが、描画や計算の詳細は自分自身で完結させ、`MainWindow` 本体のコード量を削る。
3.  **Pipeline Integration**: 元の一枚岩のメソッドを、定義したヘルパーメソッドを順次呼び出すだけのシンプルな「オーケストレーター」に変える。
4.  **Unit Preservation**: 描画（Renderer）フェーズで物理単位やメタデータが失われないよう、変換ロジックを Renderer 内にカプセル化する。

## Example
MainWindow.py 内の `update_graphs` のリファクタリング例：
```python
def update_graphs(self):
    data_map, times, fs = self._collect_data_map()
    self.excitation_manager.inject_signals(data_map, times, fs)
    self._check_stop_condition(data_map)
    self._render_graphs(data_map, times)
```

このパターンに従うことで、将来的に新しい測定タイプ（Swept Sineなど）を追加する際にも、既存の描画ロジックや励起ロジックを再利用しやすくなります。
