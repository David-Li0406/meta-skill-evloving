# Grafix Pattern Recipes（短い型）

コンセプトを「最低限の primitive/effect セット」に落とすためのメモ。
ここにあるのは“型”だけで、作品は **型の組み合わせ + 係数**で作る。

## 1) Grid + Displace

- primitive: `G.grid(...)`
- effect: `E.displace(...)`（微小） + `E.dash(...)`（線密度）

狙い:

- 情報量の多い背景・織物・流体っぽい揺らぎ。

## 2) Polygon / Circle Ring + Rotate

- primitive: `G.polygon(...)`
- effect: `E.rotate(...)` + `E.scale(...)`

狙い:

- 幾何ポスター系。`t` は回転角や半径に割り当てやすい。

## 3) Text + Wobble / Displace

- primitive: `G.text(...)`
- effect: `E.wobble(...)` or `E.displace(...)`

狙い:

- タイポの“崩れ”や“振動”。破綻しやすいので effect は 1 個から。

## 4) Mirror + Repeat

- primitive: 何でも（線・多角形・テキスト）
- effect: `E.mirror(...)` + `E.repeat(...)`

狙い:

- 対称性と規則性。少ない要素で強い見た目になる。

## 5) Fill（面）を使う

- primitive: 閉曲線（`G.polygon(...)`, `G.text(...)` など）
- effect: `E.fill(...)`

狙い:

- “線だけ”から脱却する最短ルート。重い場合は polygon 数を減らす。

## 6) Clip（2入力）で構図を切る

- primitive: A（線群）、B（マスク用の閉曲線）
- effect: `E.clip(...)(A, B)`

狙い:

- コラージュ/版画っぽい切り抜き。multi-input effect はチェーン先頭に置く。

## 7) Subdivide + Relax（有機化）

- primitive: `G.line(...)` / `G.polygon(...)`
- effect: `E.subdivide(...)` + `E.relax(...)`

狙い:

- 角張りを有機化。線が増えやすいので subdivisions は控えめ。

## 8) まず 1 レイヤで成立させる

- layer を増やすのは「1 レイヤで成立」してから。
- 迷ったら:
  - primitive を 1 個減らす
  - effect を 1 個減らす
  - `t` の役割を 1 個に絞る

