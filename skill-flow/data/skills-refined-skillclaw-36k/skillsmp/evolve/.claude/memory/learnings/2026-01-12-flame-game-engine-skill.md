---
date: "2026-01-12"
tags: [flame, flutter, dart, 2d-games, skill-creation, game-development]
---

# Flame Game Engine Skill 開發

## 背景

用戶需要一個能指導使用 Flame 引擎開發 2D 遊戲的 Skill，涵蓋完整遊戲開發流程，適合各經驗程度的開發者。

## 研究發現

### Flame 引擎核心特點

1. **架構**: 基於 Flutter 的模組化 2D 遊戲引擎
2. **核心系統**:
   - Flame Component System (FCS) - 類似 ECS 的元件架構
   - Game Loop - 內建遊戲循環管理
   - CameraComponent - 攝影機與視口系統
3. **最新版本**: v1.33.0 (2025-10)

### 關鍵概念

| 概念 | 說明 |
|------|------|
| FlameGame | 主遊戲類，管理遊戲循環和元件樹 |
| World | 遊戲世界容器，存放所有遊戲實體 |
| Component | 基礎元件類，支援生命週期 |
| PositionComponent | 有位置/大小的元件 |
| SpriteAnimationComponent | 支援精靈動畫的元件 |
| HasCollisionDetection | 碰撞偵測 mixin |

### Bridge Packages

- `flame_audio`: 音訊播放
- `flame_forge2d`: Box2D 物理引擎
- `flame_tiled`: Tiled 地圖編輯器支援
- `flame_rive` / `flame_lottie`: 動畫支援
- `flame_bloc` / `flame_riverpod`: 狀態管理

### 設計模式

1. **元件生命週期**: onLoad → onMount → update/render → onRemove
2. **碰撞偵測**: CollisionCallbacks mixin + Hitbox
3. **輸入處理**: TapCallbacks, DragCallbacks, KeyboardHandler mixins
4. **攝影機跟隨**: camera.follow() 配合 setBounds()

## Skill 設計決策

### 涵蓋範圍

- 核心架構與設定
- 元件系統（FCS）
- 輸入處理（觸控、鍵盤、搖桿）
- 碰撞偵測
- 攝影機系統
- 精靈動畫
- 效果系統
- 音訊整合
- 遊戲狀態與 Overlay
- 常見設計模式
- 效能優化

### 排除範圍

- 3D 遊戲開發
- 多人連線/後端
- 遊戲上架流程

## 學到的教訓

1. **Context7 很有用**: 能快速獲取最新的程式碼範例和文檔
2. **官方教程結構清晰**: Flame 有 4 個官方教程（Bare Game, Klondike, Ember Quest, Space Shooter）
3. **社群資源**: awesome-flame repo 有大量社群貢獻的範例

## 參考資料

- [Flame Docs](https://docs.flame-engine.org/latest/)
- [Flame GitHub](https://github.com/flame-engine/flame)
- [Awesome Flame](https://github.com/flame-engine/awesome-flame)
