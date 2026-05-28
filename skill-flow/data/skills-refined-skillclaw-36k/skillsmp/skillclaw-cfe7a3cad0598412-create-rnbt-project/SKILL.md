---
name: create-rnbt-project
description: Use this skill when you need to create a complete RNBT architecture project, including standard components, a master/page layer, mock server, and dataset configuration.
---

# RNBT 프로젝트 생성

이 스킬은 RNBT 아키텍처 패턴에 맞는 완전한 대시보드 페이지를 생성합니다. Master/Page 레이어, 여러 컴포넌트, Mock 서버, datasetList.json을 포함합니다.

## ⚠️ 작업 전 필수 확인

**코드 작성 전 반드시 다음 파일들을 Read 도구로 읽으세요.**
**이전에 읽었더라도 매번 다시 읽어야 합니다 - 캐싱하거나 생략하지 마세요.**

1. [/RNBT_architecture/README.md](/RNBT_architecture/README.md) - 아키텍처 이해
2. [/.claude/guides/CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) - 코딩 스타일

## 출력 구조

```
Examples/[project_name]/
├── mock_server/                    # Express API 서버
│   ├── server.js
│   └── package.json
│
├── master/page/                    # MASTER 레이어 (앱 전역)
│   ├── page_scripts/
│   │   ├── before_load.js
│   │   ├── loaded.js
│   │   └── before_unload.js
│   ├── page_styles/container.css
│   └── components/
│       ├── Header/
│       └── Sidebar/
│
├── page/                           # PAGE 레이어 (페이지별)
│   ├── page_scripts/
│   │   ├── before_load.js
│   │   ├── loaded.js
│   │   └── before_unload.js
│   ├── page_styles/container.css
│   └── components/
│
├── datasetList.json
├── preview.html
└── README.md
```

## 핵심 원칙

### 1. 역할 분리

```
페이지 = 오케스트레이터
- 데이터 정의 (globalDataMappings)
- Interval 관리 (refreshIntervals)
- 이벤트 핸들러 등록 (eventBusHandlers)

컴포넌트 = 독립적 구독자
- topic 구독 (subscriptions)
- 이벤트 발행 (@eventName)
- 렌더링만 집중
```

### 2. 메서드 분리 (재사용성)

**핵심: 컴포넌트 재사용을 위해 메서드를 철저히 분리한다.**

```javascript
// 고정 (재사용)
function renderChart(config, { response }) {
    const { optionBuilder, ...chartCfg } = config;
    const option = optionBuilder(chartCfg, data);
    this.chartInstance.setOption(option, true);
}

// 가변 (컴포넌트별)
const chartConfig = { optionBuilder: getChartOption };
this.renderChart = renderChart.bind(this, chartConfig);
```

### 3. 이벤트 처리 기준

| 페이지가 알아야 하는가? | 처리 | 예시 |
|----------------------|------|------|
| 아니오 | `_internalHandlers` | Clear, Toggle |
| 예 | `customEvents` + `bindEvents` | 행 선택, 필터 변경 |

### 4. 응답 구조

```javascript
// response 키가 한 번 더 감싸져 있음
function renderData(config, { response }) {
    const { data, meta } = response;
}
```

## 금지 사항

- ❌ 컴포넌트가 직접 fetch (팝업 없이)
- ❌ 생성 후 정리 누락
- ❌ `function(response)` 사용 → `function({ response })` 필수

## Master vs Page 레이어

| 레이어 | 범위 | 용도 | 예시 |
|--------|------|------|------|
| **Master** | 앱 전역 | 공통 UI, 네비게이션 | Header, Sidebar |
| **Page** | 페이지별 | 페이지 고유 콘텐츠 | StatsCards, DataTable, Chart |

### `this` 공유

Master와 Page는 **동일한 `this` 인스턴스를 공유**합니다.

```javascript
// Page loaded.js에서 초기화
this.currentParams = {};

// Master before_load.js에서 접근/수정 가능
this.currentParams.tasks = { ...filters };
```

### ⚠️ 덮어쓰기 방지 (필수)

Master와 Page 모두 같은 변수명을 사용하면 **나중에 실행되는 쪽이 덮어씀**.

```javascript
// ❌ 잘못된 예: Page가 Master의 핸들러를 덮어씀
// Master before_load.js
this.eventBusHandlers = { '@filterApplied': ... };
// Page before_load.js
this.eventBusHandlers = { '@taskClicked': ... };  // Master 핸들러 사라짐!

// ✅ 올바른 예: Object.assign으로 병합
// Page before_load.js
this.eventBusHandlers = Object.assign(this.eventBusHandlers || {}, {
    '@taskClicked': ...
});

// ✅ 올바른 예: spread로 배열 병합
// Page loaded.js
this.globalDataMappings = [
    ...(this.globalDataMappings || []),
    { topic: 'tasks', ... }
];
```

## 관련 자료

| 문서 | 위치 |
|------|------|
| 예제 | [/RNBT_architecture/Examples/SimpleDashboard/](/RNBT_architecture/Examples/SimpleDashboard/) |