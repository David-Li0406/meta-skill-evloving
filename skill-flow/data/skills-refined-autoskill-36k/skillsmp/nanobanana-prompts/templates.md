# NanoBanana プロンプトテンプレート集

## 1. 人物・ポートレート

### ビジネスポートレート
```
Professional corporate headshot of a [gender] executive in their [age]s,
wearing a tailored [color] suit with subtle pinstripes,
confident and approachable expression,
shot with Canon EOS R5, 85mm f/1.4 lens,
soft Rembrandt lighting with fill light,
neutral gray gradient background,
shallow depth of field,
Fortune 500 CEO portrait quality
```

### ファッションポートレート
```
High fashion editorial portrait of a [gender] model,
[specific clothing/outfit description],
dramatic side lighting creating strong shadows,
[hair style and color],
intense gaze, slight head tilt,
shot by Annie Leibovitz style,
Vogue magazine cover worthy,
film grain texture, rich contrast
```

### カジュアルポートレート
```
Candid lifestyle portrait of [subject],
natural golden hour sunlight,
genuine warm smile,
[casual outfit],
outdoor setting with soft bokeh background,
35mm lens perspective,
Instagram influencer aesthetic,
warm color grading
```

---

## 2. 商品・物撮り

### 高級商品
```
Luxury product photography of [product name],
floating on pure white background (#FFFFFF),
soft omnidirectional lighting,
subtle reflection on surface below,
hero angle showing key features,
Hasselblad medium format quality,
Apple product launch aesthetic,
8K ultra high resolution
```

### 食品
```
Appetizing food photography of [dish name],
shot from [angle: 45-degree/overhead/eye-level],
steam rising naturally,
fresh ingredients visible,
rustic wooden surface,
natural window light from left,
shallow depth of field on hero element,
Bon Appétit magazine style
```

### テクノロジー製品
```
Sleek technology product shot of [device],
floating in dramatic dark environment,
subtle blue accent lighting (#0066FF),
reflective surface catching highlights,
showing [key feature],
minimalist composition,
Samsung Galaxy S launch quality,
premium tech aesthetic
```

---

## 3. 風景・環境

### 壮大な自然風景
```
Epic landscape photograph of [location/scene],
shot during [golden hour/blue hour/sunrise],
dramatic cloudscape in the sky,
[foreground element] in lower third,
leading lines drawing eye to [focal point],
shot with Sony A7R V, 16-35mm wide angle,
f/11 for maximum sharpness,
National Geographic cover quality,
vibrant yet natural colors
```

### 都市風景
```
Cinematic cityscape of [city name] at [time],
long exposure light trails from traffic,
modern architecture silhouettes,
[iconic landmark] as focal point,
shot from [high vantage point],
Blade Runner 2049 color grading,
film noir atmosphere,
deep contrast with neon accents
```

### インテリア
```
Architectural interior photograph of [space type],
clean minimalist design,
natural light flooding through large windows,
[design style: Scandinavian/Japanese/Modern],
wide angle showing full space,
perfectly balanced composition,
Architectural Digest feature quality,
f/8 for sharp detail throughout
```

---

## 4. アート・イラスト

### アニメスタイル
```
Anime illustration of [character/scene],
Studio Ghibli inspired art style,
soft pastel color palette,
detailed background with [elements],
emotional lighting,
hand-drawn aesthetic with digital finish,
4K wallpaper quality,
trending on Pixiv
```

### リアリスティックデジタルアート
```
Hyperrealistic digital painting of [subject],
intricate details visible,
dramatic cinematic lighting,
[color mood: warm/cool/vibrant],
concept art for AAA game quality,
4K resolution,
trending on ArtStation,
painted by Greg Rutkowski style
```

### 水彩画風
```
Watercolor painting of [subject],
soft flowing edges with wet-on-wet technique,
[color palette] harmonious colors,
white paper showing through highlights,
loose expressive brushwork,
traditional watercolor texture,
gallery exhibition quality
```

---

## 5. マーケティング・広告

### SNS広告画像
```
Eye-catching social media ad for [product/service],
bold [primary color] background,
[product/person] as hero element,
clean sans-serif text space reserved on [position],
scroll-stopping composition,
Instagram/Facebook ad optimized,
high contrast for mobile viewing,
brand colors: [HEX codes]
```

### バナー広告
```
Professional web banner for [campaign],
[dimensions: 728x90 / 300x250 / etc],
clear visual hierarchy,
[product/offer] prominently displayed,
brand colors: [primary: #XXX, secondary: #XXX],
clean white space for text overlay,
high CTR optimized design,
A/B test winning aesthetic
```

### LP ヒーローイメージ
```
Landing page hero image for [product/service],
[target audience] engaging with product,
aspirational lifestyle setting,
warm inviting lighting,
space for headline overlay on [left/right],
emotional connection imagery,
conversion-optimized composition,
premium brand aesthetic
```

---

## 6. 画像編集プロンプト

### 背景置換
```
Replace the background with:
- [新しい背景の詳細説明]
- Lighting direction: from [方向]
- Color temperature: [warm/cool/neutral]
- Maintain original subject shadows
- Seamless edge blending
- PRESERVE the original subject exactly
```

### 色調補正
```
Apply color grading:
- Shadows: push toward [color] (#HEX)
- Highlights: push toward [color] (#HEX)
- Overall saturation: [increase/decrease] by [%]
- Contrast: [high/medium/low]
- Style: [cinematic/vintage/modern/film emulation]
```

### オブジェクト追加
```
Add [object] to the image:
- Position: [具体的な位置]
- Size: [relative to existing elements]
- Lighting: match existing scene lighting
- Shadow: cast shadow toward [direction]
- Integration: MUST look naturally part of scene
```

### オブジェクト削除
```
Remove the following from the image:
- [削除対象1]
- [削除対象2]
Fill removed areas with:
- Contextually appropriate background
- Seamless texture matching
- NO visible artifacts or smearing
```

---

## 7. Pro Engineer 画像編集

### フェイススワップ（顔の入れ替え）
```
Using Image 1 as the face reference and Image 2 as the body/scene reference:

FACE EXTRACTION from Image 1:
- Preserve EXACTLY: facial bone structure, eye shape and color, nose profile,
  lip shape, skin tone and texture, any distinctive features (moles, freckles)
- Capture: natural expression lines, facial hair if present

INTEGRATION into Image 2:
- Scale face to match body proportions naturally
- Align: eye line, nose bridge, chin position with neck angle
- Match lighting: direction from [specify], intensity, color temperature
- Blend edges: seamless transition at hairline, jaw, ears
- Adjust: skin tone to match scene lighting conditions

QUALITY REQUIREMENTS:
- NO uncanny valley effect - result must look completely natural
- Preserve both subjects' distinctive characteristics
- Output resolution: match or exceed source images
- NEVER distort facial features or proportions
```

### Identity Locking（キャラクター一貫性）
```
CHARACTER IDENTITY LOCK using [N] reference images:

LOCKED FEATURES (MUST preserve exactly):
- Face: [specific facial feature descriptions from references]
- Hair: [color, style, length, texture, parting]
- Body: [build, height impression, posture tendencies]
- Skin: [tone, any visible marks or features]
- Age: [apparent age range]
- Unique identifiers: [glasses, jewelry, tattoos, etc.]

NEW SCENE GENERATION:
- Location: [detailed environment description]
- Time/Lighting: [time of day, light source, mood]
- Pose: [body position, hand placement, stance]
- Expression: [emotional state, eye direction, mouth]
- Outfit: [clothing appropriate to scene, or specify exact outfit]
- Camera: [angle, distance, lens equivalent]

CONSISTENCY CHECK:
- Character MUST be instantly recognizable across all outputs
- Maintain proportions regardless of pose changes
- Age appearance consistent with references
- Style/aesthetic can vary, identity NEVER varies
```

### 衣装統一（Outfit Consistency）
```
OUTFIT CONSISTENCY across multiple images:

REFERENCE OUTFIT (from Image [N]):
- Garment type: [specific item descriptions]
- Color: [exact colors with HEX codes if precise match needed]
- Fabric: [material, texture, sheen level]
- Fit: [loose/tailored/tight, silhouette shape]
- Details: [buttons, zippers, patterns, logos, stitching]
- Accessories: [jewelry, belt, bag, shoes - each described]

APPLICATION RULES:
- Maintain EXACT color matching across different lighting conditions
- Preserve fabric behavior: wrinkles appropriate to pose, drape based on movement
- Scale consistently with body proportions
- Adapt naturally to: sitting, standing, walking, various arm positions
- Keep all details visible and consistent

FOR EACH OUTPUT IMAGE:
- Verify: same outfit recognizable immediately
- Allow: natural variations from pose/lighting only
- NEVER: change colors, add/remove details, alter fit
```

### 背景変更（Advanced）
```
SUBJECT EXTRACTION AND RECOMPOSITION:

PRESERVE FROM ORIGINAL:
- Subject: [person/object] with ALL original details
- Original lighting direction on subject: from [direction]
- Edge details: hair strands, fabric edges, transparent elements
- Shadows: original shadow shape for reference

NEW ENVIRONMENT:
- Setting: [detailed description of new background]
- Atmosphere: [mood, time of day, weather if outdoor]
- Depth: [foreground elements, middle ground, background layers]

INTEGRATION REQUIREMENTS:
- Relight subject to match new environment:
  * New key light: from [direction], [color temperature]
  * Fill light: [intensity relative to key]
  * Rim/back light: [if environment suggests]
- Cast NEW shadow: direction and softness matching new light
- Color grade subject: match new environment's color palette
- Add environmental interaction: [reflections, atmospheric haze, etc.]
- Scale subject appropriately to new scene

SEAMLESS BLEND CHECKLIST:
- NO visible cutout edges
- Lighting 100% consistent
- Color temperature unified
- Atmospheric perspective applied
- Ground contact realistic
```

### スタイル変換（Style Transfer）
```
STYLE TRANSFORMATION:

SOURCE: Original image with [describe key elements to preserve]

TARGET STYLE: [specific art style]
- Art movement/genre: [e.g., Impressionism, Art Nouveau, Ukiyo-e]
- Reference artists: [1-3 specific artists for style reference]
- Medium simulation: [oil paint, watercolor, pencil, digital, etc.]

STYLE ELEMENTS TO APPLY:
- Brushwork/linework: [characteristic strokes, line quality]
- Color palette: [typical colors, saturation, contrast]
- Texture: [canvas, paper, digital smoothness]
- Composition adjustments: [if style typically uses specific compositions]
- Detail level: [highly detailed vs. impressionistic]

PRESERVATION REQUIREMENTS:
- Subject identity: MUST remain recognizable
- Core composition: maintain unless style demands change
- Emotional tone: [preserve or adapt to style]

OUTPUT:
- Resolution: [specify]
- Aspect ratio: [if style-specific]
- Authenticity: Should look like genuine [style] artwork, not a filter
```

---

## 8. 特殊効果

### ダブルエクスポージャー
```
Double exposure effect combining:
- Primary subject: [subject 1]
- Overlay: [subject 2 / texture / scene]
- Blending: [silhouette filled / overlapping]
- Color scheme: [monochrome / selective color]
- Artistic, conceptual aesthetic
- Professional album cover quality
```

### レトロ・ヴィンテージ
```
Vintage [decade: 70s/80s/90s] aesthetic:
- Film grain texture
- [Kodak Portra / Fuji Velvia] color emulation
- Slight color fade on edges
- Light leak effects
- Analog photography imperfections
- Nostalgic warm tones
```

### 未来的・サイバーパンク
```
Cyberpunk futuristic scene of [subject],
neon lights in [colors: magenta, cyan, purple],
rain-slicked streets reflecting lights,
holographic advertisements,
dystopian urban environment,
Blade Runner + Ghost in the Shell aesthetic,
dramatic contrast,
4K cinematic quality
```
