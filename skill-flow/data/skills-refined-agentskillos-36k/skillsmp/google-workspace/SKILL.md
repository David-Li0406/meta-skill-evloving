---
name: google-workspace
description: >
  Google Workspace 통합 스킬. Docs, Sheets, Drive, Gmail, Calendar API 연동.
  OAuth 2.0 인증, 서비스 계정 설정, 데이터 읽기/쓰기 자동화 지원.
  파랑 계열 전문 문서 스타일, 2단계 네이티브 테이블 렌더링 포함.
version: 2.4.0

triggers:
  keywords:
    - "google workspace"
    - "google docs"
    - "google sheets"
    - "google drive"
    - "gmail api"
    - "google calendar"
    - "스프레드시트"
    - "구글 문서"
    - "구글 드라이브"
    - "gdocs"
    - "--gdocs"
    - "prd gdocs"
  file_patterns:
    - "**/credentials.json"
    - "**/token.json"
    - "**/google*.py"
    - "**/sheets*.py"
    - "**/drive*.py"
  context:
    - "Google API 연동"
    - "스프레드시트 데이터 처리"
    - "문서 자동화"
    - "이메일 발송 자동화"
  url_patterns:
    - "drive.google.com"
    - "docs.google.com"
    - "sheets.google.com"

capabilities:
  - setup_google_api
  - oauth_authentication
  - sheets_read_write
  - drive_file_management
  - gmail_send_receive
  - calendar_integration
  - service_account_setup

model_preference: sonnet

auto_trigger: true
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

**서브 레포에서 작업 시 반드시 절대 경로 사용!**

### 인증 방식 선택 가이드

| 작업 | 인증 방식 | 파일 |
|------|----------|------|
| **파일 업로드** | OAuth 2.0 | `desktop_credentials.json` |
| **파일 읽기** | 서비스 계정 또는 OAuth | 둘 다 가능 |
| **스프레드시트 쓰기** | OAuth 2.0 | `desktop_credentials.json` |
| **자동화 (읽기만)** | 서비스 계정 | `service_account_key.json` |

⚠️ **주의**: 서비스 계정은 저장 용량 할당량이 없어 **Drive 업로드 불가**!

### 필수 환경 변수

```bash
# OAuth 2.0 (업로드 필요시 - 권장)
GOOGLE_OAUTH_CREDENTIALS=C:\claude\json\desktop_credentials.json
GOOGLE_OAUTH_TOKEN=C:\claude\json\token.json

# 서비스 계정 (읽기 전용 자동화)
GOOGLE_SERVICE_ACCOUNT_FILE=C:\claude\json\service_account_key.json
GOOGLE_APPLICATION_CREDENTIALS=C:\claude\json\service_account_key.json
```

### 파일 구조

```
C:\claude\
├── json/
│   ├── desktop_credentials.json   # OAuth 클라이언트 ID (업로드용)
│   ├── token.json                 # OAuth 토큰 (자동 생성)
│   └── service_account_key.json   # 서비스 계정 (읽기 전용)
├── wsoptv/                        # 서브 레포
├── db_architecture/               # 서브 레포
└── ...
```

### 공유된 Google Drive 리소스

| 리소스 | 폴더/문서 ID | URL | 용도 |
|--------|-------------|-----|------|
| Google AI Studio | `1JwdlUe_v4Ug-yQ0veXTldFl6C24GH8hW` | [폴더](https://drive.google.com/drive/folders/1JwdlUe_v4Ug-yQ0veXTldFl6C24GH8hW) | 공유 문서/자료 저장소 |
| WSOPTV 와이어프레임 | `1kHuCfqD7PPkybWXRL3pqeNISTPT7LUTB` | [폴더](https://drive.google.com/drive/folders/1kHuCfqD7PPkybWXRL3pqeNISTPT7LUTB) | 홈페이지 와이어프레임 PNG |
| WSOPTV UX 기획서 | `1tghlhpQiWttpB-0CP5c1DiL5BJa4ttWj-2R77xaoVI8` | [문서](https://docs.google.com/document/d/1tghlhpQiWttpB-0CP5c1DiL5BJa4ttWj-2R77xaoVI8/edit) | 사용자 경험 설계 문서 |

**서비스 계정 이메일**: `archive-sync@ggp-academy.iam.gserviceaccount.com`

⚠️ **중요**: 서비스 계정은 스토리지 할당량이 없어 **파일 업로드 불가**!
- 읽기/폴더 생성: 가능
- 파일 업로드: **OAuth 2.0 필요**

## 인증 방식

### 1. OAuth 2.0 (사용자 대신 작업)

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  앱     │────▶│ Google  │────▶│  사용자 │────▶│ 토큰    │
│         │     │ 로그인  │     │  동의   │     │ 발급    │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
```

**용도**: 사용자의 개인 데이터 접근 (내 드라이브, 내 이메일), **파일 업로드**

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/drive']  # 전체 Drive 접근

# 절대 경로 사용 (서브 레포에서도 동작)
CREDENTIALS_FILE = r'C:\claude\json\desktop_credentials.json'
TOKEN_FILE = r'C:\claude\json\token.json'

def get_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds
```

### 2. 서비스 계정 (서버 간 통신)

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  서버   │────▶│ Google  │────▶│ API     │
│         │     │ 인증    │     │ 호출    │
└─────────┘     └─────────┘     └─────────┘
```

**용도**: 자동화 작업, 공유된 리소스 **읽기**

⚠️ **제한 사항**: 서비스 계정은 저장 용량이 없어 **Drive 업로드 불가!**

```python
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# 절대 경로 사용 (서브 레포에서도 동작)
SERVICE_ACCOUNT_FILE = r'C:\claude\json\service_account_key.json'

def get_service_credentials():
    return service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
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

# 사용 예시
# spreadsheet_id: URL에서 /d/ 뒤의 값
# https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit
data = read_sheet('1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms', 'Sheet1!A:E')
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

# 사용 예시
write_sheet(
    spreadsheet_id='your-spreadsheet-id',
    range_name='Sheet1!A1:C3',
    values=[
        ['이름', '나이', '도시'],
        ['홍길동', 30, '서울'],
        ['김철수', 25, '부산']
    ]
)
```

### 스프레드시트 추가 (Append)

```python
def append_sheet(spreadsheet_id: str, range_name: str, values: list):
    """스프레드시트 끝에 데이터 추가"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    body = {'values': values}

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return result.get('updates').get('updatedRows')
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

# 특정 폴더의 스프레드시트만 조회
sheets = list_files(
    folder_id='folder-id',
    mime_type='application/vnd.google-apps.spreadsheet'
)
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

# 사용 예시
result = upload_file('report.pdf', folder_id='target-folder-id')
print(f"업로드 완료: {result['webViewLink']}")
```

### 파일 다운로드

```python
from googleapiclient.http import MediaIoBaseDownload
import io

def download_file(file_id: str, output_path: str):
    """파일 다운로드"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    request = service.files().get_media(fileId=file_id)

    with io.FileIO(output_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"다운로드 진행: {int(status.progress() * 100)}%")
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

# 사용 예시
send_email(
    to='recipient@example.com',
    subject='자동화 알림',
    body='처리가 완료되었습니다.'
)
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

# 최근 안 읽은 메일 조회
unread = list_emails(query='is:unread', max_results=5)
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

# 사용 예시
from datetime import datetime, timedelta

start = datetime(2025, 1, 15, 14, 0)
end = start + timedelta(hours=1)
create_event('팀 미팅', start, end, description='주간 진행 상황 공유')
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
    'heading_primary': '#1A4D8C',   # 진한 파랑 - Title, H1
    'heading_secondary': '#3373B3', # 밝은 파랑 - H2
    'heading_tertiary': '#404040',  # 진한 회색 - H3 이하
    'heading_accent': '#3373B3',    # 밝은 파랑 - 강조/구분선

    # 배경 색상
    'background_gray': '#F2F2F2',   # 연한 회색 - 코드/테이블

    # 테이블
    'table_header_bg': '#E6E6E6',   # 연한 회색 헤더 배경
    'table_header_text': '#404040', # 진한 회색 헤더 텍스트
    'table_border': '#CCCCCC',      # 1pt 회색 테두리
}
```

### 강조 색상 팔레트

| 색상명 | HEX 코드 | 용도 | 하이라이트 배경 |
|--------|----------|------|----------------|
| **Red** | `#DC2626` | 오류, 삭제 | `#FEE2E2` |
| **Orange** | `#D97706` | 경고 | `#FEF3C7` |
| **Yellow** | `#CA8A04` | 주의 | `#FEF9C3` |
| **Green** | `#059669` | 성공, 추가 | `#D1FAE5` |
| **Blue** | `#1A4D8C` | 정보, 기본 강조 | `#DBEAFE` |
| **Purple** | `#7C3AED` | 특수 강조 | `#EDE9FE` |
| **Pink** | `#DB2777` | 중요 표시 | - |

### Callout 박스 스타일

문서 내 중요 정보 강조를 위한 박스 스타일입니다.

| 타입 | 아이콘 | 배경색 | 테두리색 | 용도 |
|------|--------|--------|----------|------|
| **info** | ℹ️ | `#DBEAFE` | `#1A4D8C` | 일반 정보 안내 |
| **warning** | ⚠️ | `#FEF3C7` | `#D97706` | 주의 사항 |
| **success** | ✅ | `#D1FAE5` | `#059669` | 완료, 성공 |
| **danger** | 🚨 | `#FEE2E2` | `#DC2626` | 위험, 오류 |
| **tip** | 💡 | `#FEF9C3` | `#CA8A04` | 팁, 권장 사항 |
| **note** | 📝 | `#F2F2F2` | `#999999` | 일반 메모 |

### 테이블 스타일

| 항목 | 값 |
|------|-----|
| **너비** | 페이지 컨텐츠 영역에 맞춤 (451pt) |
| **헤더 배경** | 연한 회색 `#E6E6E6` |
| **헤더 텍스트** | 진한 회색 `#404040`, Bold |
| **셀 패딩** | 5pt |
| **테두리** | 1pt, 회색 `#CCCCCC` |

### 네이티브 테이블 렌더링 (2단계 방식)

Google Docs API의 인덱스 계산 문제를 해결하기 위해 2단계 방식을 사용합니다.

```
┌─────────────────────────────────────────────────────────────┐
│  네이티브 테이블 2단계 렌더링                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1단계: 테이블 구조 생성                                     │
│     ├── 지금까지의 요청 실행 (batchUpdate)                  │
│     ├── 문서 끝 인덱스 조회                                 │
│     └── insertTable 실행                                    │
│                                                              │
│  2단계: 테이블 내용 삽입                                     │
│     ├── 문서 재조회하여 실제 테이블 구조 확인               │
│     ├── 각 셀의 실제 인덱스 추출                            │
│     ├── 텍스트 삽입 (역순 - 인덱스 시프트 방지)             │
│     └── 헤더 스타일 적용 (Bold, 색상)                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**관련 모듈**:
- `lib/google_docs/table_renderer.py` - 2단계 렌더링 메서드
- `lib/google_docs/converter.py` - 테이블 처리 로직

### 줄바꿈 정책

| 항목 | 정책 |
|------|------|
| **단락 사이** | 줄바꿈 허용 |
| **테이블 앞뒤** | 줄바꿈 제거 (불필요) |
| **헤딩 뒤** | 줄바꿈 제거 |
| **코드 블록 앞뒤** | 줄바꿈 1개만 |

### 금지 사항

| 항목 | 사유 |
|------|------|
| 구분선 (─ 반복) | 시각적 노이즈, H1 하단 구분선으로 대체 |
| **불필요한 빈 줄** | 가독성 저하, 단락 전환 시에만 허용 |
| 150% 이상 줄간격 | 페이지 낭비, 115% 권장 |
| Letter 용지 | A4로 통일 |
| Slate 계열 색상 | 파랑 계열로 통일 |

### 스타일 적용 코드 템플릿

```python
def apply_standard_style(service, doc_id):
    """표준 문서 스타일 적용"""

    # A4 페이지 설정
    requests = [{
        "updateDocumentStyle": {
            "documentStyle": {
                "pageSize": {
                    "width": {"magnitude": 595.28, "unit": "PT"},
                    "height": {"magnitude": 841.89, "unit": "PT"}
                },
                "marginTop": {"magnitude": 72, "unit": "PT"},
                "marginBottom": {"magnitude": 72, "unit": "PT"},
                "marginLeft": {"magnitude": 72, "unit": "PT"},
                "marginRight": {"magnitude": 72, "unit": "PT"},
            },
            "fields": "pageSize,marginTop,marginBottom,marginLeft,marginRight"
        }
    }]

    # 본문 줄간격 설정 (문서 전체)
    doc = service.documents().get(documentId=doc_id).execute()
    end_index = max(el.get("endIndex", 1) for el in doc["body"]["content"])

    requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": 1, "endIndex": end_index - 1},
            "paragraphStyle": {
                "lineSpacing": 115,
                "spaceAbove": {"magnitude": 0, "unit": "PT"},
                "spaceBelow": {"magnitude": 4, "unit": "PT"},
            },
            "fields": "lineSpacing,spaceAbove,spaceBelow"
        }
    })

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()
```

### 헤딩 스타일 적용 코드

```python
def apply_heading_style(service, doc_id, start_idx, end_idx, heading_level):
    """헤딩에 표준 스타일 적용"""

    COLORS = {
        "primary_blue": {"red": 0.10, "green": 0.30, "blue": 0.55},
        "accent_blue": {"red": 0.20, "green": 0.45, "blue": 0.70},
        "dark_gray": {"red": 0.25, "green": 0.25, "blue": 0.25},
    }

    HEADING_STYLES = {
        "TITLE": {"color": "primary_blue", "size": 26},
        "HEADING_1": {"color": "primary_blue", "size": 18, "border": True},
        "HEADING_2": {"color": "accent_blue", "size": 14},
        "HEADING_3": {"color": "dark_gray", "size": 12},
    }

    style = HEADING_STYLES.get(heading_level)
    if not style:
        return

    requests = [{
        "updateTextStyle": {
            "range": {"startIndex": start_idx, "endIndex": end_idx},
            "textStyle": {
                "foregroundColor": {"color": {"rgbColor": COLORS[style["color"]]}},
                "bold": True,
                "fontSize": {"magnitude": style["size"], "unit": "PT"}
            },
            "fields": "foregroundColor,bold,fontSize"
        }
    }]

    # H1에 하단 구분선 추가
    if style.get("border"):
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start_idx, "endIndex": end_idx + 1},
                "paragraphStyle": {
                    "borderBottom": {
                        "color": {"color": {"rgbColor": COLORS["accent_blue"]}},
                        "width": {"magnitude": 1, "unit": "PT"},
                        "padding": {"magnitude": 4, "unit": "PT"},
                        "dashStyle": "SOLID"
                    }
                },
                "fields": "borderBottom"
            }
        })

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()
```

---

## Markdown → Google Docs 변환

### 지원 문법

| 문법 | 예시 | 변환 결과 |
|------|------|----------|
| 제목 | `# H1` ~ `###### H6` | 스타일링된 제목 |
| 볼드 | `**bold**` | **굵은 글씨** |
| 이탤릭 | `*italic*` | *기울임* |
| 코드 | `` `code` `` | 인라인 코드 (배경 `#F2F2F2`) |
| 취소선 | `~~strike~~` | ~~취소선~~ |
| 링크 | `[text](url)` | 파란 밑줄 링크 |
| 불릿 | `- item` | • 불릿 리스트 |
| 번호 | `1. item` | 번호 리스트 |
| 체크박스 | `- [ ]` / `- [x]` | ☐ / ☑ |
| 인용문 | `> quote` | 왼쪽 테두리 + 배경 |
| 코드블록 | ` ``` ` | 언어 표시 + 코드 스타일 |
| 테이블 | `\| a \| b \|` | 네이티브 테이블 |
| 이미지 | `![alt](path)` | Drive 업로드 후 삽입 |
| 수평선 | `---` | H1 하단 구분선 스타일 |

### CLI 변환 도구

```powershell
# 기본 변환
python scripts/prd_to_google_docs.py tasks/prds/PRD-0001-feature.md

# 옵션 사용
python scripts/prd_to_google_docs.py --toc tasks/prds/PRD-0001.md   # 목차 포함
python scripts/prd_to_google_docs.py --folder FOLDER_ID file.md     # 특정 폴더
python scripts/prd_to_google_docs.py --no-folder file.md            # 내 드라이브

# 배치 변환
python scripts/prd_to_google_docs.py tasks/prds/*.md
```

---

## HTML 목업 → 이미지 워크플로우

PRD 문서에 다이어그램/UI를 포함하기 위한 워크플로우입니다.

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  HTML 목업      │────▶│  Playwright     │────▶│  Google Docs    │
│  작성           │     │  스크린샷       │     │  이미지 삽입    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
      │                                               ▲
      ▼                                               │
┌─────────────────┐                                   │
│  docs/mockups/  │                                   │
│  feature.html   │─────────────────────────────────►─┘
└─────────────────┘        (자동 처리)
```

### HTML 목업 규격

| 항목 | 값 | 비고 |
|------|-----|------|
| **가로 너비** | 540px | Google Docs 삽입 기준 |
| **최소 폰트** | 16px | 가독성 보장 |
| **캡처 대상** | `#capture-area` | 선택자 지정 |
| **저장 위치** | `docs/mockups/` | 프로젝트별 |

### 캡처 명령

```powershell
# 특정 요소만 캡처 (권장)
npx playwright screenshot docs/mockups/architecture.html docs/images/architecture.png --selector="#capture-area"

# 전체 페이지 캡처
npx playwright screenshot docs/mockups/ui.html docs/images/ui.png --full-page
```

### 템플릿 종류

| 템플릿 | 경로 | 용도 |
|--------|------|------|
| **base** | `lib/google_docs/templates/base.html` | 기본 레이아웃 |
| **architecture** | `lib/google_docs/templates/architecture.html` | 시스템 아키텍처 |
| **flowchart** | `lib/google_docs/templates/flowchart.html` | 프로세스 흐름도 |
| **erd** | `lib/google_docs/templates/erd.html` | 데이터베이스 ERD |
| **ui-mockup** | `lib/google_docs/templates/ui-mockup.html` | UI 목업 |

---

## 이미지 삽입 (ImageInserter)

### 기본 사용법

```python
from lib.google_docs.image_inserter import ImageInserter
from lib.google_docs.auth import get_credentials
from pathlib import Path

creds = get_credentials()
inserter = ImageInserter(creds)

# Drive에 업로드
file_id, image_url = inserter.upload_to_drive(Path('diagram.png'))

# 특정 위치에 삽입
inserter.insert_image_at_position(doc_id, image_url, position=100, width=400)

# 텍스트 다음에 삽입
inserter.insert_image_after_text(doc_id, image_url, "## 아키텍처")

# 제목 다음에 삽입
inserter.insert_image_after_heading(doc_id, image_url, "기술 아키텍처")
```

### 지원 이미지 형식

| 확장자 | MIME Type |
|--------|-----------|
| `.png` | image/png |
| `.jpg`, `.jpeg` | image/jpeg |
| `.gif` | image/gif |
| `.webp` | image/webp |
| `.svg` | image/svg+xml |

---

## 다이어그램 생성기

```python
from lib.google_docs.diagram_generator import DiagramGenerator

generator = DiagramGenerator()

# 아키텍처 다이어그램 생성
html = generator.create_architecture_diagram(
    title="시스템 아키텍처",
    components=[
        {"name": "Frontend", "type": "client"},
        {"name": "API Gateway", "type": "gateway"},
        {"name": "Backend", "type": "server"},
    ]
)

# 파일로 저장
with open("docs/mockups/system-arch.html", "w") as f:
    f.write(html)
```

---

## 연동

| 스킬/에이전트 | 연동 시점 |
|---------------|----------|
| `data-specialist` | 데이터 분석 및 ETL |
| `backend-dev` | API 서버 통합 |
| `python-dev` | Python 자동화 |
| `ai-engineer` | AI 워크플로우 연동 |

## 트러블슈팅

### 인증 오류

```python
# 토큰 삭제 후 재인증
import os
if os.path.exists('credentials/token.json'):
    os.remove('credentials/token.json')
# 다시 get_credentials() 호출
```

### 권한 오류 (403)

```
1. Google Cloud Console에서 API 활성화 확인
2. OAuth 동의 화면에서 Scope 추가
3. 서비스 계정의 경우 파일/폴더 공유 확인
```

### 업로드 실패 - storageQuotaExceeded

**증상**: `Service Accounts do not have storage quota`

**원인**: 서비스 계정은 저장 용량 할당량이 없음

**해결**: OAuth 2.0 인증으로 전환

```python
# 서비스 계정 대신 OAuth 사용
CREDENTIALS_FILE = r'C:\claude\json\desktop_credentials.json'
TOKEN_FILE = r'C:\claude\json\token.json'
```

### 할당량 초과 (429)

```python
import time
from googleapiclient.errors import HttpError

def api_call_with_retry(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except HttpError as e:
            if e.resp.status == 429:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## PRD 관리 시스템 (Google Docs 마스터)

PRD(Product Requirements Document)를 Google Docs로 관리하는 통합 시스템입니다.

### 아키텍처

```
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│   /create prd   │───────▶│   Google Docs   │───────▶│  Local Cache    │
│   (대화형 질문) │        │   (마스터)      │        │  (읽기 전용)    │
└─────────────────┘        └─────────────────┘        └─────────────────┘
                                    │                          │
                                    └──────────┬───────────────┘
                                               ▼
                                    ┌─────────────────┐
                                    │ .prd-registry   │
                                    │    .json        │
                                    └─────────────────┘
```

### 모듈 구조

```
lib/google_docs/                    # 핵심 변환 라이브러리
├── __init__.py
├── auth.py                 # OAuth 2.0 인증 (토큰 관리)
├── converter.py            # Markdown → Google Docs 변환 (2단계 테이블)
├── table_renderer.py       # 네이티브 테이블 렌더링 (2단계 방식)
├── notion_style.py         # 파랑 계열 전문 문서 스타일
├── models.py               # 데이터 모델 (TableData 등)
└── cli.py                  # CLI 인터페이스

src/services/google_docs/           # PRD 관리 서비스
├── __init__.py
├── client.py              # Google Docs API 클라이언트
├── prd_service.py         # PRD CRUD 서비스
├── cache_manager.py       # 로컬 캐시 동기화
├── metadata_manager.py    # .prd-registry.json 관리
└── migration.py           # Markdown → Docs 마이그레이션
```

### 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/create prd [name]` | Google Docs에 PRD 생성 |
| `/create prd [name] --local-only` | 로컬 Markdown만 생성 (호환 모드) |
| `/prd-sync [PRD-ID]` | PRD 동기화 (Docs → 로컬 캐시) |
| `/prd-sync all` | 전체 PRD 동기화 |
| `/prd-sync list` | 등록된 PRD 목록 |
| `/prd-sync stats` | PRD 통계 |

### 사용 예시

#### 네이티브 테이블 포함 문서 생성

```python
from lib.google_docs.converter import create_google_doc

# 마크다운 콘텐츠 (네이티브 테이블 포함)
markdown = '''
# 프로젝트 현황

## 모듈 상태
| 모듈 | 상태 | 담당자 |
|------|------|--------|
| 인증 | 완료 | 김개발 |
| API | 진행중 | 이백엔드 |

## 결론
모든 모듈이 정상 진행 중입니다.
'''

# Google Docs 생성 (네이티브 테이블 자동 적용)
url = create_google_doc(
    title='프로젝트 현황 보고서',
    content=markdown,
    use_native_tables=True  # 기본값
)
print(f'문서 URL: {url}')
```

#### PRD 서비스 사용

```python
from src.services.google_docs import GoogleDocsClient, PRDService

# 클라이언트 생성
client = GoogleDocsClient()

# PRD 서비스 생성
prd_service = PRDService(client=client)

# 새 PRD 생성
metadata = prd_service.create_prd(
    title="User Authentication",
    priority="P1",
    tags=["auth", "security"]
)

print(f"PRD 생성됨: {metadata.prd_id}")
print(f"Google Docs: {metadata.google_doc_url}")
```

### 마이그레이션

```bash
# 기존 Markdown PRD를 Google Docs로 마이그레이션
python scripts/migrate_prds_to_gdocs.py list      # 대상 목록
python scripts/migrate_prds_to_gdocs.py all       # 전체 마이그레이션
python scripts/migrate_prds_to_gdocs.py PRD-0001  # 단일 마이그레이션
```

### 레지스트리 구조

`.prd-registry.json`:

```json
{
  "version": "1.0.0",
  "last_sync": "2025-12-24T10:00:00Z",
  "next_prd_number": 2,
  "prds": {
    "PRD-0001": {
      "google_doc_id": "1abc...",
      "google_doc_url": "https://docs.google.com/document/d/.../edit",
      "title": "포커 핸드 자동 캡처",
      "status": "In Progress",
      "priority": "P0",
      "local_cache": "PRD-0001.cache.md",
      "checklist_path": "docs/checklists/PRD-0001.md"
    }
  }
}
```

### 공유 폴더

- **폴더 ID**: `1JwdlUe_v4Ug-yQ0veXTldFl6C24GH8hW`
- **URL**: [Google AI Studio 폴더](https://drive.google.com/drive/folders/1JwdlUe_v4Ug-yQ0veXTldFl6C24GH8hW)

### 인증 파일

| 파일 | 용도 |
|------|------|
| `C:\claude\json\token_docs.json` | Google Docs OAuth 토큰 |
| `C:\claude\json\desktop_credentials.json` | OAuth 클라이언트 자격증명 |

---

## 변경 로그

### v2.4.0 (2026-01-13)

**Features:**
- Markdown → Google Docs 변환 문법 지원표 추가
- HTML 목업 → 이미지 워크플로우 문서화
- ImageInserter 클래스 상세 사용법 추가
- DiagramGenerator 클래스 문서화
- CLI 변환 도구 옵션 상세화 (--toc, --folder, --no-folder)

**Integration:**
- `automation_feature_table/docs/GOOGLE_DOCS_GUIDE.md` 장점 통합
- 해당 가이드 파일 deprecate (중복 제거)

### v2.3.2 (2026-01-07)

**Documentation:**
- 타이포그래피 상세 표 추가 (H4-H6, 본문, 코드 폰트 크기/굵기/여백)
- 컨텐츠 너비 451.28pt 명시
- 강조 색상 팔레트 7종 문서화 (Red, Orange, Yellow, Green, Blue, Purple, Pink)
- Callout 박스 스타일 6종 정의 (info, warning, success, danger, tip, note)

**Code Consistency:**
- `converter.py`: 코드 배경색 기본값을 스타일 시스템에서 가져오도록 변경
- `table_renderer.py`: 인라인 코드 배경색 `CODE_BG_COLOR` 상수 추가 (#F2F2F2)
- 0.95 → 0.949 (정확한 #F2F2F2 RGB 값) 통일

### v2.3.1 (2026-01-07)

**Bug Fixes:**
- 테이블 테두리 스타일 적용 (SKILL.md 표준: 1pt, #CCCCCC)
- 수평선 스타일 통일 (─ 반복 제거, 하단 구분선 사용)

**Deprecations:**
- `NativeTableRenderer.render()` 메서드 deprecated (v2.4.0에서 제거 예정)
  - 대체: `render_table_structure()` + `render_table_content()`

### v2.3.0 (2026-01-07)

**Features:**
- 2단계 네이티브 테이블 렌더링 구현 (인덱스 계산 문제 해결)
- 파랑 계열 전문 문서 스타일로 통일 (Slate → Blue)
- 테이블 셀 내 마크다운 파싱 (**bold**, *italic*)

**Style Changes:**
- 색상: #1A4D8C (진한 파랑), #3373B3 (밝은 파랑), #404040 (본문)
- 타이포그래피: H1 18pt, H2 14pt, H3 12pt
- 줄간격: 115%

---

## 참조 문서

- [Google Sheets API](https://developers.google.com/sheets/api)
- [Google Drive API](https://developers.google.com/drive/api)
- [Gmail API](https://developers.google.com/gmail/api)
- [Google Calendar API](https://developers.google.com/calendar/api)
- [Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
