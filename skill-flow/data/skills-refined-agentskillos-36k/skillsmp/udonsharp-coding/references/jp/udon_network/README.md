# Udon ネットワーク同期（分割版）

このフォルダは、段階的に学べるよう `udon_network.md` を再編成した分割版ドキュメントです。最小限の実装情報に素早くアクセスできる構成を優先しています。元の [udon_network.md](../udon_network.md) は保持されています。

## 学習順（最短→発展）

1. 最短実装（必須）: [01_basics_minimum.md](01_basics_minimum.md)
2. 実装章（実践）: [02_implementation.md](02_implementation.md)
3. 補足（同期オプション/コールバック）: [03_sync_options.md](03_sync_options.md)
4. 参照（同期可能な型）: [04_synced_types.md](04_synced_types.md)
5. 最適化（設計指針）: [05_design_tips.md](05_design_tips.md)

## 目的別ショートカット

- とにかく動くものを作る: [01_basics_minimum.md](01_basics_minimum.md)
- オーナー移譲や同期フックを使いたい: [02_implementation.md](02_implementation.md)
- 補間や `FieldChangeCallback` を確認したい: [03_sync_options.md](03_sync_options.md)
- 同期可能な型を一覧で確認したい: [04_synced_types.md](04_synced_types.md)
- 同期負荷を減らす設計を考えたい: [05_design_tips.md](05_design_tips.md)
