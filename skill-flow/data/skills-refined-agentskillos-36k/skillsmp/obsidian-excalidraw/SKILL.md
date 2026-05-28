---
name: obsidian-excalidraw
description: Generate Excalidraw diagrams from text content for Obsidian. Use when user asks to create diagrams, flowcharts, mind maps, or visual representations in Excalidraw format. Triggers on "Excalidraw", "순서도", "마인드맵", "mindmap", "시각화", "diagram", "플로우차트", "flowchart".
metadata:
  version: 1.1.0
---

# Excalidraw Diagram Generator

Create Excalidraw diagrams from text content, outputting Obsidian-ready `.md` files.

## Workflow

1. Analyze content - identify concepts, relationships, hierarchy
2. Choose diagram type (see below)
3. Generate Excalidraw JSON
4. Generate Obsidian-ready `.md` file with Excalidraw frontmatter
5. **Automatically save to current working directory**
6. Notify user with file path and confirm save successful

## Output Format

**반드시 아래 구조에 따라 출력해야 하며, 수정해서는 안 됩니다:**

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
\`\`\`json
{JSON 完整数据}
\`\`\`
%%
```

**핵심 사항:**
- Frontmatter에는 반드시 `tags: [excalidraw]`가 포함되어야 합니다.
- 경고 메시지는 반드시 포함되어야 합니다.
- JSON은 반드시 `%%` 태그로 감싸야 합니다.
- `excalidraw-plugin: parsed` 이외의 다른 frontmatter 설정은 사용할 수 없습니다.

## Diagram Types & Selection Guide

이해를 돕고 시각적으로 돋보이게 하기 위해 적절한 다이어그램 유형을 선택하세요.

| 유형 | 영문 | 사용 시나리오 | 작성법 |
|---|---|---|---|
| **순서도** | Flowchart | 단계 설명, 워크플로우, 작업 순서 | 화살표로 각 단계를 연결하여 흐름을 명확히 표현 |
| **마인드맵** | Mind Map | 개념 확장, 주제 분류, 영감 포착 | 중심을 핵으로 하여 방사형 구조로 확장 |
| **계층도** | Hierarchy | 조직 구조, 콘텐츠 계층, 시스템 분해 | 위에서 아래로 또는 왼쪽에서 오른쪽으로 계층 노드 구축 |
| **관계도** | Relationship | 요소 간의 영향, 의존, 상호작용 | 도형 간 연결선으로 연관성 표시, 화살표와 설명 추가 |
| **비교도** | Comparison | 두 가지 이상의 방안 또는 관점 대조 분석 | 좌우 2단 또는 표 형식, 비교 차원 명시 |
| **타임라인** | Timeline | 사건 전개, 프로젝트 진행, 모델 진화 | 시간을 축으로 하여 주요 시점과 사건 표시 |
| **매트릭스** | Matrix | 2차원 분류, 우선순위, 포지셔닝 | X축과 Y축 2개 차원 설정, 평면 배치 |
| **자유 형식** | Freeform | 흩어진 내용, 영감 기록, 초기 정보 수집 | 구조 제약 없이 도형과 화살표 자유 배치 |

## Design Rules

### Text & Format
- **모든 텍스트 요소는 반드시** `fontFamily: 5` (Excalifont 손글씨체)를 사용해야 합니다.
- **텍스트 내 큰따옴표 대체 규칙**: `"` 를 `『』` 로 변경
- **텍스트 내 괄호 대체 규칙**: `()` 를 `「」` 로 변경
- **글꼴 크기 규칙**:
  - 제목: 24-28px
  - 부제목: 18-20px
  - 본문/설명: 14-16px
- **줄 높이**: 모든 텍스트는 `lineHeight: 1.25` 사용

### Layout & Design
- **캔버스 범위**: 모든 요소는 0-1200 x 0-800 영역 내에 배치 권장
- **요소 간격**: 적절한 간격을 유지하여 전체 레이아웃을 미려하게 구성
- **명확한 계층**: 색상과 모양을 달리하여 정보의 계층 구분
- **도형 요소**: 사각형, 원형, 화살표 등을 적절히 사용하여 정보 조직

### Color Palette
- **제목 색상**: `#1e40af` (진한 파랑)
- **부제목/연결선**: `#3b82f6` (밝은 파랑)
- **본문 텍스트**: `#374151` (회색)
- **강조/포인트**: `#f59e0b` (금색)
- **기타 배색**: 조화로운 색상 조합 권장, 과도한 색상 사용 지양

참고: [references/excalidraw-schema.md](references/excalidraw-schema.md)

## JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [...],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Element Template

Each element requires these fields:

```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 200, "height": 50,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a1",
  "roundness": {"type": 3},
  "seed": 123456789,
  "version": 1,
  "versionNonce": 987654321,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false
}
```

Text elements add:
```json
{
  "text": "표시 텍스트",
  "rawText": "표시 텍스트",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "표시 텍스트",
  "autoResize": true,
  "lineHeight": 1.25
}
```

See [references/excalidraw-schema.md](references/excalidraw-schema.md) for all element types.

---

## Additional Technical Requirements

### Text Elements 처리
- `## Text Elements` 부분은 Markdown에서 **반드시 비워두고**, `%%` 만 구분자로 사용
- Obsidian ExcaliDraw 플러그인이 JSON 데이터에 따라 **텍스트 요소를 자동 완성함**
- 모든 텍스트 내용을 수동으로 나열할 필요 없음

### 좌표 및 레이아웃
- **좌표계**: 좌측 상단을 원점 (0,0)으로 함
- **권장 범위**: 모든 요소는 0-1200 x 0-800 픽셀 범위 내
- **요소 ID**: 각 요소는 고유한 `id` 필요 (문자열 가능, 예: 'title', 'box1' 등)
- **Index 필드**: 영문자와 숫자 조합 권장 (a1, a2, a3...)

### Required Fields for All Elements
```json
{
  "id": "unique-identifier",
  "type": "rectangle|text|arrow|ellipse|diamond",
  "x": 100, "y": 100,
  "width": 200, "height": 50,
  "angle": 0,
  "strokeColor": "#color-hex",
  "backgroundColor": "transparent|#color-hex",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid|dashed",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a1",
  "roundness": {"type": 3},
  "seed": 123456789,
  "version": 1,
  "versionNonce": 987654321,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false
}
```

### Text-Specific Properties
텍스트 요소 (type: "text") 추가 속성:
```json
{
  "text": "표시 텍스트",
  "rawText": "표시 텍스트",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "표시 텍스트",
  "autoResize": true,
  "lineHeight": 1.25
}
```

### appState 配置
```json
"appState": {
  "gridSize": null,
  "viewBackgroundColor": "#ffffff"
}
```

### files 字段
```json
"files": {}
```

## Implementation Notes

### Auto-save & File Generation Workflow

Excalidraw 다이어그램 생성 시, **반드시 다음 단계를 자동으로 수행해야 합니다**:

#### 1. 적절한 다이어그램 유형 선택
- 사용자가 제공한 콘텐츠 특성에 따라, 위 'Diagram Types & Selection Guide' 표 참고
- 콘텐츠의 핵심 요구사항을 분석하여 가장 적절한 시각화 형태 선택

#### 2. 의미 있는 파일명 생성
- 형식: `[주제].[유형].md`
- 예: `콘텐츠제작프로세스.flowchart.md`, `Axton비즈니스모델.relationship.md`
- 명확성을 높이기 위해 한국어 사용 권장

#### 3. Write 도구를 사용하여 파일 자동 저장
- **저장 위치**: 현재 작업 디렉토리 (환경 변수 자동 감지)
- **전체 경로**: `{current_directory}/[filename].md`
- 이를 통해 하드코딩된 경로 없이 유연한 이동 가능

#### 4. Markdown 구조의 완전한 정확성 보장
**반드시 다음 형식으로 생성해야 함 (수정 불가):**

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
\`\`\`json
{完整的 JSON 数据}
\`\`\`
%%
```

#### 5. JSON 데이터 요구사항
- ✅ 완전한 Excalidraw JSON 구조 포함
- ✅ 모든 텍스트 요소에 `fontFamily: 5` 사용
- ✅ 텍스트 내 `"` 를 `『』` 로 변경
- ✅ 텍스트 내 `()` 를 `「」` 로 변경
- ✅ JSON 형식은 유효해야 하며 구문 검사 통과 필수
- ✅ 모든 요소에 고유 `id` 부여
- ✅ `appState` 및 `files: {}` 필드 포함

#### 6. 사용자 피드백 및 확인
사용자에게 보고:
- ✅ 다이어그램 생성 완료
- 📍 정확한 저장 위치
- 📖 Obsidian에서 확인하는 방법
- 🎨 다이어그램 디자인 선택 설명 (어떤 유형을 선택했는지, 그 이유는 무엇인지)
- ❓ 조정이나 수정이 필요한지 여부

### Example Output Message
```
✅ Excalidraw 다이어그램이 자동 생성되었습니다!

📍 저장 위치:
Axton_2026비즈니스모델.relationship.md

🎨 다이어그램 선택 설명:
세 가지 제품 라인 간의 전환 관계를 표현하기 위해 '관계도'를 선택했으며, 화살표를 사용하여 사용자의 업그레이드 경로와 이들이 어떻게 완전한 비즈니스 순환 고리를 구성하는지 보여주었습니다.

📖 사용 방법:
1. Obsidian에서 이 파일 열기
2. 우측 상단 'MORE OPTIONS' 메뉴 클릭
3. 'Switch to EXCALIDRAW VIEW' 선택
4. 시각화된 비즈니스 모델 전경 확인

수정이 필요하신가요? 레이아웃 변경, 세부 사항 추가 또는 색상 조정 등 무엇이든 말씀해 주세요!
```
