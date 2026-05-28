---
name: google-workspace
description: Use this skill for integrating Google Workspace APIs, including Docs, Sheets, Drive, Gmail, and Calendar, with support for OAuth 2.0 authentication and automation of data reading/writing.
---

# Google Workspace Integration Skill

Google Workspace API 통합을 위한 전문 스킬입니다.

## ⚠️ 중요: Google Drive/Docs URL 접근 시

**WebFetch로 Google Drive/Docs URL에 직접 접근 불가!** JavaScript 동적 로딩으로 외부에서 콘텐츠 조회 불가.

```
┌─────────────────────────────────────────────────────────────┐
│  Google URL 접근 방법                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ❌ 불가능:                                                   │
│     WebFetch("https://drive.google.com/drive/folders/...")  │
│     → 빈 페이지 또는 로그인 페이지만 반환                     │
│                                                              │
│  ✅ 정상 방법:                                                │
│     1. 이 스킬의 Python 코드 사용 (API 인증 필요)            │
│     2. 폴더 ID 추출 → list_files() 함수 호출                 │
│                                                              │
│  URL에서 ID 추출:                                            │
│     drive.google.com/drive/folders/{FOLDER_ID}              │
│     docs.google.com/document/d/{DOC_ID}/edit                │
│     docs.google.com/spreadsheets/d/{SHEET_ID}/edit          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### URL → API 변환 예시

| URL 유형 | 예시 URL | 추출 ID | API 호출 |
|----------|----------|---------|----------|
| Drive 폴더 | `drive.google.com/drive/folders/1Jwdl...` | `1Jwdl...` | `list_files(folder_id='1Jwdl...')` |
| Google Doc | `docs.google.com/document/d/1tghl.../edit` | `1tghl...` | Docs API 사용 |
| Spreadsheet | `docs.google.com/spreadsheets/d/1BxiM.../edit` | `1BxiM...` | `read_sheet('1BxiM...', 'Sheet1!A:E')` |

## Quick Start

```bash
# Python 클라이언트 라이브러리 설치
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# 또는 uv 사용
uv add google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## API 설정 흐름

```
┌─────────────────────────────────────────────────────────────┐
│  Google Cloud Console 설정 흐름                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 프로젝트 생성                                            │
│     └── console.cloud.google.com                            │
│                                                              │
│  2. API 활성화                                               │
│     ├── Google Sheets API                                   │
│     ├── Google Drive API                                    │
│     ├── Gmail API                                           │
│     └── Google Calendar API                                 │
│                                                              │
│  3. 인증 정보 생성                                           │
│     ├── OAuth 2.0 클라이언트 ID (사용자 인증용)              │
│     └── 서비스 계정 (서버 간 통신용)                        │
│                                                              │
│  4. credentials.json 다운로드                                │
│     └── 프로젝트 루트에 저장                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 환경 변수 설정

### 이 프로젝트의 인증 파일 위치 (중요!)

```
C:\claude\json\
├── desktop_credentials.json   # OAuth 2.0 클라이언트 (업로드용) ⭐
├── token.json                 # OAuth 토큰 (자동 생성)
└── service_account_key.json   # 서비스 계정 (읽기 전용)
```

### 필수 환경 변수

```bash
# OAuth 2.0 (업로드 필요시 - 권장)
GOOGLE_OAUTH_CREDENTIALS=C:\claude\json\desktop_credentials.json
GOOGLE_OAUTH_TOKEN=C:\claude\json\token.json

# 서비스 계정 (읽기 전용 자동화)
GOOGLE_SERVICE_ACCOUNT_FILE=C:\claude\json\service_account_key.json
GOOGLE_APPLICATION_CREDENTIALS=C:\claude\json\service_account_key.json
```

## Google Sheets 연동

### 스프레드시트 읽기

```python
from googleapiclient.discovery import build

def read_sheet(spreadsheet_id: str, range_name: str):
    """스프레드시트 데이터 읽기"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()

    return result.get('values', [])
```

### 스프레드시트 쓰기

```python
def write_sheet(spreadsheet_id: str, range_name: str, values: list):
    """스프레드시트에 데이터 쓰기"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    body = {'values': values}

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    return result.get('updatedCells')
```

## Google Drive 연동

### 파일 목록 조회

```python
def list_files(folder_id: str = None, mime_type: str = None):
    """드라이브 파일 목록 조회"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    query_parts = []
    if folder_id:
        query_parts.append(f"'{folder_id}' in parents")
    if mime_type:
        query_parts.append(f"mimeType='{mime_type}'")
    query_parts.append("trashed=false")

    query = " and ".join(query_parts)

    results = service.files().list(
        q=query,
        pageSize=100,
        fields="files(id, name, mimeType, modifiedTime)"
    ).execute()

    return results.get('files', [])
```

### 파일 업로드

```python
from googleapiclient.http import MediaFileUpload

def upload_file(file_path: str, folder_id: str = None, mime_type: str = None):
    """파일 업로드"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    return file
```

## Gmail 연동

### 이메일 발송

```python
import base64
from email.mime.text import MIMEText

def send_email(to: str, subject: str, body: str):
    """이메일 발송"""
    creds = get_credentials()  # SCOPES에 gmail.send 포함 필요
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    result = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return result
```

### 이메일 조회

```python
def list_emails(query: str = '', max_results: int = 10):
    """이메일 목록 조회"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()
        emails.append(detail)

    return emails
```

## Google Calendar 연동

### 일정 조회

```python
from datetime import datetime, timedelta

def list_events(calendar_id: str = 'primary', days: int = 7):
    """일정 목록 조회"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])
```

### 일정 생성

```python
def create_event(summary: str, start: datetime, end: datetime,
                 description: str = None, calendar_id: str = 'primary'):
    """일정 생성"""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Seoul'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Seoul'},
    }

    if description:
        event['description'] = description

    result = service.events().insert(
        calendarId=calendar_id,
        body=event
    ).execute()

    return result
```

## 권한 범위 (Scopes)

| 서비스 | Scope | 권한 |
|--------|-------|------|
| Sheets | `spreadsheets.readonly` | 읽기 전용 |
| Sheets | `spreadsheets` | 읽기/쓰기 |
| Drive | `drive.readonly` | 읽기 전용 |
| Drive | `drive.file` | 앱이 생성한 파일만 |
| Drive | `drive` | 전체 접근 |
| Gmail | `gmail.readonly` | 읽기 전용 |
| Gmail | `gmail.send` | 발송만 |
| Gmail | `gmail.modify` | 읽기/쓰기 |
| Calendar | `calendar.readonly` | 읽기 전용 |
| Calendar | `calendar` | 읽기/쓰기 |

**권장**: 필요한 최소 권한만 요청

## 체크리스트

### API 설정

- [ ] Google Cloud Console 프로젝트 생성
- [ ] 필요한 API 활성화 (Sheets, Drive, Gmail, Calendar)
- [ ] OAuth 동의 화면 설정
- [ ] 인증 정보 생성 (OAuth 또는 서비스 계정)
- [ ] credentials.json 다운로드 및 저장

### 코드 설정

- [ ] 클라이언트 라이브러리 설치
- [ ] credentials.json 경로 설정
- [ ] 필요한 Scopes 정의
- [ ] 인증 함수 구현

### 보안

- [ ] credentials.json `.gitignore`에 추가
- [ ] token.json `.gitignore`에 추가
- [ ] 서비스 계정 키 안전하게 보관
- [ ] 최소 권한 원칙 적용

## Anti-Patterns

| 금지 | 이유 | 대안 |
|------|------|------|
| credentials.json 커밋 | 보안 키 노출 | .gitignore 추가 |
| 과도한 권한 요청 | 불필요한 접근 | 최소 Scope만 사용 |
| 토큰 하드코딩 | 유출 위험 | 환경 변수 또는 파일 |
| API 호출 무한 루프 | 할당량 초과 | 에러 핸들링 추가 |
| 동기 호출 남용 | 성능 저하 | 배치 처리 활용 |

## 할당량 관리

```
┌─────────────────────────────────────────────────────────────┐
│  API 할당량 (기본값)                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Sheets API                                                  │
│  ├── 읽기: 300 요청/분/프로젝트                              │
│  └── 쓰기: 300 요청/분/프로젝트                              │
│                                                              │
│  Drive API                                                   │
│  └── 10,000 요청/100초/사용자                                │
│                                                              │
│  Gmail API                                                   │
│  └── 250 요청/초/사용자                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**할당량 초과 방지**:
1. 배치 요청 사용
2. 지수 백오프 재시도
3. 캐싱 적용

---

## Google Docs 문서 스타일 가이드 (파랑 계열 전문 문서)

모든 Google Docs 문서 생성/수정 시 아래 스타일을 적용합니다.

### 페이지 설정

| 항목 | 값 | 비고 |
|------|-----|------|
| **페이지 크기** | A4 (595.28pt x 841.89pt) | 210mm x 297mm |
| **여백** | 72pt (1인치) | 상하좌우 동일 |
| **컨텐츠 너비** | 451.28pt | 595.28 - (72 × 2) |
| **줄간격** | 115% | 본문, 헤딩 동일 적용 |
| **문단 간격** | 상: 0pt, 하: 4pt | 본문 기준, 헤딩은 별도 |

### 타이포그래피 상세

| 요소 | 크기 | 굵기 | 색상 | 여백(상/하) | 비고 |
|------|------|------|------|------------|------|
| **제목 (Title)** | 26pt | Bold (700) | `#1A4D8C` | 12/8pt | 진한 파랑 |
| **H1** | 18pt | Bold (700) | `#1A4D8C` | 18/6pt | 하단 구분선 (1pt, 파랑) |
| **H2** | 14pt | Bold (700) | `#3373B3` | 14/4pt | 밝은 파랑 |
| **H3** | 12pt | Bold (700) | `#404040` | 10/4pt | 진한 회색 |
| **H4** | 11pt | SemiBold (600) | `#404040` | 8/4pt | 진한 회색 |
| **H5** | 11pt | SemiBold (600) | `#404040` | 6/4pt | 진한 회색 |
| **H6** | 10pt | SemiBold (600) | `#666666` | 4/4pt | 중간 회색 |
| **본문** | 11pt | Regular (400) | `#404040` | 0/4pt | - |
| **인라인 코드** | 10.5pt | Regular (400) | `#404040` | - | 배경 `#F2F2F2` |
| **코드 블록** | 10.5pt | Regular (400) | `#404040` | - | 배경 `#F2F2F2`, 패딩 12pt |

### 색상 팔레트 (파랑 계열 전문 문서)

```python
# lib/google_docs/notion_style.py
NOTION_COLORS = {
    # 텍스트 계층
    'text_primary': '#404040',      # 진한 회색 - 본문
    'text_secondary': '#666666',    # 중간 회색 - 메타/캡션
    'text_muted': '#999999',        # 연한 회색 - 힌트 텍스트

    # 제목 색상 (파랑 계열)
    'heading_primary': '#1A4