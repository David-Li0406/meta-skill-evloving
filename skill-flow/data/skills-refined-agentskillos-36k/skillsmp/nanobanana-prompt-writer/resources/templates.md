# Nano Banana プロンプトテンプレート集

用途別のプロンプト骨子（コピペ用）。

---

## A) 写実（フォト）テンプレ

shot type / subject / environment / lighting / mood / lens / texture / aspect を網羅する。

```text
[用途/目的]
A [shot type] of [subject with attributes], in/at [environment, time, season].
Camera: [angle], [lens mm], [aperture/DoF], [focus target].
Lighting: [key light style], [color temperature], [mood words].
Texture/material details: [materials, surfaces].
Composition: [rule of thirds / centered / negative space], [foreground/background elements].
Aspect ratio: [e.g., 16:9].
Constraints: [望ましい状態で制約を書く]
```

### 例（日本語シーン）
```text
映画的なシネマティック写真。
雨上がりの渋谷の路地裏、深夜。30代の日本人男性がネオンの下で佇んでいる。
Camera: medium shot, 35mm lens, f/1.8, shallow DoF focusing on the man's face.
Lighting: neon reflections on wet pavement, cool blue-purple tones, moody and melancholic.
Texture: rain-slicked asphalt, steam rising from a vent, distant blurred signs.
Composition: rule of thirds, subject on left third, negative space on right for atmosphere.
Aspect ratio: 16:9.
Constraints: no text overlays; background stays slightly out of focus; no direct eye contact with camera.
```

---

## B) ステッカー/アイコン（イラスト）テンプレ

線の太さ、塗り、配色、背景（透明/白）を明示。

```text
Create a [style] sticker of [subject].
Linework: [thick/clean outline], Coloring: [cell shading/flat/watercolor], Palette: [vivid/pastel/limited].
Expression/pose: [..].
Background: transparent (or solid white cutout).
Composition: centered, ample padding around the subject.
Aspect ratio: [1:1].
```

### 例
```text
Create a kawaii chibi sticker of a smiling corgi wearing a tiny chef hat.
Linework: thick black outline, Coloring: flat cell shading, Palette: warm pastels (peach, cream, soft brown).
Expression/pose: happy closed-eye smile, holding a tiny whisk.
Background: transparent cutout.
Composition: centered, generous padding around the character for sticker die-cut.
Aspect ratio: 1:1.
```

---

## C) 文字入り（ロゴ/バナー）テンプレ

入れたい文字は **引用符**で明示。ロゴ/文字精度は **Pro** 推奨。

```text
Design a [logo/banner/poster] for [brand/product].
Text to include (exact): "[TEXT HERE]".
Typography: [clean/bold/sans-serif/...], layout: [centered/stacked/left aligned], spacing: [..].
Icon/mark: [describe symbol], integration: [how it combines with text].
Color: [palette], background: [white/transparent/solid].
Constraints: keep text crisp and readable; avoid decorative distortions; ample margin.
Aspect ratio: [1:1 / 16:9 / ...].
```

### 例
```text
Design a minimalist logo for a specialty coffee shop.
Text to include (exact): "The Daily Grind".
Typography: clean sans-serif, all caps, generous letter spacing, layout: horizontal single line.
Icon/mark: a simple geometric coffee cup silhouette to the left of the text.
Color: dark espresso brown text on white background.
Constraints: text must be perfectly legible and undistorted; no decorative flourishes; ample white space around logo.
Aspect ratio: 16:9.
```

### 文字が崩れる場合の2段階アプローチ
1. まず文言のみを生成させる：「Generate the text "The Daily Grind" in clean sans-serif typography on white background」
2. その出力を参照画像として、画像全体を生成：「Using the text from the reference image, create a complete logo with a coffee cup icon」

---

## D) EC/物撮り（商品写真）テンプレ

スタジオライト構成、背景素材、角度、見せたい特徴。

```text
Commercial product photo for [EC use].
Product: [exact product + material + color + key features].
Setup: studio background [white/gradient], surface [marble/wood/acrylic], clean reflections.
Camera: [angle], [lens], sharp focus on [feature].
Lighting: [softbox key + fill + rim], realistic shadows.
Composition: centered with [negative space] for text if needed.
Aspect ratio: [4:5 / 1:1 / ...].
Constraints: no extra props unless specified; no text unless specified.
```

### 例
```text
Commercial product photo for e-commerce listing.
Product: matte black wireless earbuds in charging case, premium plastic finish, subtle LED indicator.
Setup: pure white seamless background, product on white acrylic surface with soft reflection.
Camera: 45-degree elevated angle, 85mm macro lens, tack sharp focus on the earbuds.
Lighting: large softbox key light from upper left, fill from right, subtle rim light for separation.
Composition: centered, generous negative space on top and right for text overlay.
Aspect ratio: 4:5.
Constraints: no props; no visible text; product is the sole focus; clean professional look.
```

---

## E) ミニマル・余白（サムネ/ポスター下地）テンプレ

"テキスト用ネガティブスペース" を明示。

```text
Minimalist composition intended as a thumbnail/poster base.
Main subject: [..] placed on [left/right/center], leaving large negative space on [top/right/...].
Background: simple, clean, low-detail.
Lighting/mood: [..].
Aspect ratio: [16:9 / ...].
Constraints: preserve empty space; avoid clutter; keep background uniform.
```

### 例
```text
Minimalist composition for YouTube thumbnail base.
Main subject: a person's silhouette looking at a glowing laptop screen, placed on the left third.
Negative space: large empty area on the right two-thirds for title text overlay.
Background: deep navy blue gradient, subtle ambient glow from the laptop.
Mood: contemplative, late-night coding vibe.
Aspect ratio: 16:9.
Constraints: no text in image; keep right side completely clean; subject should not extend past center line.
```

---

## F) 差分編集（元画像あり）テンプレ

元画像 + 追加/削除/変更 を明確化。権利がある画像のみ入力。

```text
Keep everything the same as the input image except:
- Change: [...]
- Add: [...]
- Remove: [...]
Maintain consistent lighting, perspective, and style with the original.
```

### 例
```text
Keep everything the same as the input image except:
- Change: the person's shirt color from blue to red
- Add: a subtle warm sunset glow in the background
- Remove: the coffee cup on the table
Maintain consistent lighting, perspective, and overall mood with the original.
```

---

## G) 参照画像で同一性/レイアウト固定テンプレ

「Image 1 と同じ顔を維持」など明示。Pro推奨。

```text
Use the provided reference images.
Identity: keep the face/character identity consistent with Image 1.
Layout: follow Image 2's composition/grid placement exactly.
Style: match Image 3's rendering style and color palette.
Now generate: [new scene description...]
Constraints: preserve identity + layout; only change [explicit changes].
```

### 例
```text
Use the provided reference images.
Identity: keep the woman's face and features identical to Image 1.
Pose reference: follow the body pose and hand position from Image 2.
Style: match the soft watercolor illustration style from Image 3.
Now generate: the same woman sitting at a café table, holding a book, looking out a rainy window.
Constraints: face must be recognizably the same person; maintain the watercolor aesthetic; only change the setting and activity.
```

---

## 差分プロンプト例（詰め用）

80%当たりが出た後の微修正用テンプレ：

### 光だけ変更
```text
Keep everything exactly the same. Only change the lighting to [golden hour sunset / harsh midday sun / soft overcast / neon night].
```

### 服/衣装だけ変更
```text
Keep the same person, pose, background, and lighting. Only change the outfit to [white t-shirt / formal suit / casual hoodie].
```

### 背景だけ変更
```text
Keep the subject and lighting identical. Replace the background with [solid white / gradient blue / outdoor park scene].
```

### 表情だけ変更
```text
Keep everything the same. Change only the facial expression to [confident smile / serious contemplation / surprised].
```

### 色温度/ムードだけ変更
```text
Keep the composition and subject identical. Shift the color temperature to [warmer/cooler] and mood to [more dramatic / more cheerful].
```
