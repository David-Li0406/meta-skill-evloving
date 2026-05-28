---
name: grafix-compose
description: 「コンセプト（モチーフ/雰囲気）」を、Grafix の `draw(t)` 実装に落とすための構成決定スキル。primitive/effect の数を絞り、まず静的構図→次に t 変化、の順で破綻しない作品を作る。
---

# Grafix Compose

## 目的

- ユーザーのコンセプトを、実装可能な **構図・レイヤ・op（primitive/effect）** に落とす
- 作品のブレを減らす（少ない要素で成立させる）

## 入力（最小）

- **必須**: モチーフ/雰囲気（1 行）
- 任意: 線の密度、対称/非対称、ノイズ有無、タイポ有無

## 制約（まずはこれで固定）

- まず **静的構図**を完成させる → 次に `t` を使って変化を付ける。
- primitive は最大 3 種、effect は最大 2 種（足りなければ後で増やす）。
- 乱数を使う場合は seed を固定し、`t` 依存の揺らぎは意図して設計する（毎回絵が変わりすぎない）。
- 実装先は `sketch/generated/<slug>.py`、`draw` はモジュールトップレベル関数。

## 作業手順（エージェント向け）

1. モチーフを受け取ったら、まず「構成メモ」を 5 行以内で決める
   - ベース形状（primitive）
   - 変形（effect）
   - レイヤ数（1〜3）
   - `t` の使い方（何が変わるか）
   - 計算量（重くしない）
2. `assets/sketch_template.py` をベースにスケッチを実装する。
3. op の候補が分からない場合だけ `$grafix-api-catalog` を併用して `references/api.md` を参照する。
4. 出力/比較は `$grafix-draw-export` で行う（この skill 単体では export しない）。

## 参照

- テンプレ: `assets/sketch_template.py`
- レシピ集: `assets/pattern_recipes.md`

