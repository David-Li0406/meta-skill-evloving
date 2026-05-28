---
name: event-storm
description: |
  이벤트 스토밍 다이어그램을 대화형으로 생성하는 스킬. 사용자와의 질문-응답을 통해
  Domain Event, Command, System, Actor, Policy 등의 구성요소를 점진적으로 도출하고
  Mermaid flowchart (.md 파일)과 PNG 이미지를 생성한다.

  When to use: 도메인 프로세스 분석, 소프트웨어 설계, 비즈니스 플로우 시각화 시 사용.
---

# Event Storm

이벤트 스토밍 다이어그램을 대화형으로 생성하는 스킬입니다.

## 사용 시점

**이 스킬을 사용하는 경우:**
- 도메인 프로세스를 시각화하고 싶을 때
- 시스템 간 이벤트 흐름을 분석할 때
- 비즈니스 요구사항을 이벤트 중심으로 정리할 때
- `/event-storm` 명령어 실행 시

**사용하지 않는 경우:**
- 단순 플로우차트가 필요한 경우
- 이미 완성된 다이어그램을 편집하는 경우
- 시퀀스 다이어그램이 더 적합한 경우

## 구성요소 요약

| 구성요소 | Mermaid 노드 | 색상 | 설명 |
|---------|-------------|------|------|
| Actor/Agent | `{{"고객"}}` (hexagon) | 노란색 | 행위자, 관련 인물/팀 |
| Command | `["주문 생성"]` (rectangle) | 파란색 | 결정/액션/의도 |
| System | `(["주문 시스템"])` (stadium) | 분홍색 | IT 시스템 |
| Domain Event | `(("주문 접수됨"))` (circle) | 주황색 | 도메인 이벤트 (과거형) |
| Policy | `{{"결제 정책"}}` (diamond) | 보라색 | 반응 규칙 (Whenever...) |
| Query Model | `[/"재고 현황"/]` (parallelogram) | 연두색 | 정보/읽기 모델 |
| Constraint | `[["재고 확인"]]` (subroutine) | 노란색 | 제약조건 |
| Hotspot | `(((("미정"))))` (double circle) | 빨간색 | 논쟁점/불확실성 |

> 상세 스펙은 `references/component-spec.md` 참조

## 대화형 워크플로우

### Phase 1: 컨텍스트 파악

사용자에게 다음 질문을 순차적으로 한다:

**Q1. 이벤트 스토밍 유형**
```
어떤 유형의 이벤트 스토밍을 진행하시겠습니까?

1. Process Modelling - 비즈니스 프로세스 분석
2. Software Design - 소프트웨어 설계
```

**Q2. 도메인/프로세스명**
```
분석할 도메인 또는 프로세스의 이름을 알려주세요.
예: "주문 처리", "회원 가입", "결제 시스템"
```

**Q3. 초기 Domain Event 나열**
```
이 프로세스에서 발생하는 주요 이벤트를 나열해주세요.
이벤트는 과거형으로 작성합니다.

예시:
- 주문이 접수됨
- 결제가 완료됨
- 상품이 배송됨
```

### Phase 2: 구성요소 도출 (반복)

각 Domain Event에 대해 다음 질문을 반복한다:

```
[이벤트: {event_name}]

1. 어떤 System이 이 이벤트를 발생시키나요?
2. 어떤 Command가 System을 호출하나요?
3. 누가(Actor) 이 Command를 실행하나요?
4. 이 이벤트 후 어떤 Policy가 반응하나요? (선택)
5. Actor가 결정에 필요한 정보(Query Model)는? (선택)
6. 제약조건(Constraint)이 있나요? (선택)
7. 불확실한 점(Hotspot)이 있나요? (선택)
```

**진행 중 표시:**
```
진행률: [██████░░░░] 3/5 이벤트 완료

수집된 구성요소:
- Domain Events: 5
- Actors: 2
- Commands: 4
- Systems: 3
- Policies: 1
```

### Phase 3: 연결 관계 확인

수집된 구성요소 간의 연결 관계를 확인한다:

```
다음 연결 관계가 맞는지 확인해주세요:

1. [고객] --Decides to--> [주문 생성]
2. [주문 생성] --Invoked On--> [주문 시스템]
3. [주문 시스템] --Produces--> [주문 접수됨]
4. [주문 접수됨] --Activates--> [재고 확인 정책]

수정이 필요한 항목이 있으면 번호와 함께 알려주세요.
```

### Phase 4: 다이어그램 생성

**Step 1: JSON 데이터 생성**

수집된 정보를 JSON 형식으로 정리:

```json
{
  "title": "주문 처리 프로세스",
  "type": "process_modelling",
  "components": [...],
  "connections": [...]
}
```

**Step 2: Mermaid 다이어그램 생성**

```bash
# JSON을 스크립트에 전달하여 Mermaid 파일 생성
echo '<JSON_DATA>' | python3 ~/.claude/skills/event-storm/scripts/generate_mermaid.py

# PNG 이미지도 함께 생성
echo '<JSON_DATA>' | python3 ~/.claude/skills/event-storm/scripts/generate_mermaid.py --png

# 출력 파일:
# - {title}.md (Mermaid 코드가 포함된 Markdown)
# - {title}.png (PNG 이미지, --png 옵션 사용 시)
```

**Step 3: 결과 안내**

```
다이어그램이 생성되었습니다!

파일 위치:
- Markdown: ./주문_처리_프로세스.md
- PNG 이미지: ./주문_처리_프로세스.png (--png 옵션 사용 시)

Mermaid 다이어그램은 GitHub, VSCode, Obsidian 등에서 바로 렌더링됩니다.
```

## 스크립트 사용법

### generate_mermaid.py

```bash
# 도움말
python3 ~/.claude/skills/event-storm/scripts/generate_mermaid.py --help

# stdin으로 JSON 입력
echo '{"title": "test", ...}' | python3 ~/.claude/skills/event-storm/scripts/generate_mermaid.py

# 파일에서 JSON 입력
python3 ~/.claude/skills/event-storm/scripts/generate_mermaid.py < input.json

# PNG 이미지도 생성 (mermaid-cli 필요)
echo '...' | python3 ~/.claude/skills/event-storm/scripts/generate_mermaid.py --png

# 출력 디렉토리 지정
echo '...' | python3 ~/.claude/skills/event-storm/scripts/generate_mermaid.py --output-dir ./diagrams
```

### PNG 생성 (수동)

```bash
# mermaid-cli를 사용한 PNG 변환
npx -p @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.png
```

## 에러 처리

- **구성요소 누락**: 필수 구성요소(Event, System, Command, Actor)가 하나라도 없으면 다시 질문
- **순환 의존성 감지**: Policy → Command → System → Event → Policy 순환 시 경고
- **JSON 파싱 오류**: 스크립트 입력 JSON 형식 오류 시 상세 에러 메시지 출력

## 참고사항

- Nushell 문법 사용 (`;` 구분자)
- 이벤트 이름은 항상 과거형으로 작성
- Mermaid 노드 형태와 색상은 `references/component-spec.md` 참조
