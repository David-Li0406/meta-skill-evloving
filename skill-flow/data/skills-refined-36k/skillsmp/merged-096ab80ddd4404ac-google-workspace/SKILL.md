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

## ⚠️ 서브 프로젝트에서 사용 시 (중요!)

**서브 프로젝트에서 `--gdocs` 옵션 사용 시 반드시 절대 경로로 루트 모듈을 호출해야 합니다.**

### 문제 상황

```
┌─────────────────────────────────────────────────────────────┐
│  서브 프로젝트에서 실행 시 문제                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ❌ 실패하는 경우:                                           │
│     cd C:\claude\wsoptv_nbatv_clone                         │
│     python -m lib.google_docs convert docs/PRD.md           │
│     → ModuleNotFoundError: No module named 'lib'            │
│                                                              │
│  ✅ 올바른 방법:                                             │
│     cd C:\claude                                             │
│     python -m lib.google_docs convert C:\claude\wsoptv_nbatv_clone\docs\PRD.md
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 서브 프로젝트 변환 명령

```powershell
# 방법 1: 루트로 이동 후 절대 경로로 파일 지정 (권장)
cd C:\claude && python -m lib.google_docs convert "C:\claude\{서브프로젝트}\docs\파일.md"

# 방법 2: 한 줄 명령
powershell -Command "cd C:\claude; python -m lib.google_docs convert 'C:\claude\wsoptv_nbatv_clone\docs\guides\WSOP-TV-PRD.md'"

# 방법 3: 배치 변환
cd C:\claude && python -m lib.google_docs batch "C:\claude\wsoptv_nbatv_clone\docs\*.md"
```

### 🚨 Claude 강제 실행 규칙 (MANDATORY)

**`--gdocs` 키워드 감지 시 Claude는 다음을 자동으로 수행해야 합니다:**

```
┌─────────────────────────────────────────────────────────────┐
│  --gdocs 자동 처리 워크플로우 (강제)                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 대상 파일 탐색                                           │
│     - PRD, 문서 등 변환할 .md 파일 찾기                      │
│     - 사용자가 지정한 파일 또는 컨텍스트에서 추론            │
│                                                              │
│  2. 절대 경로 변환                                           │
│     - 상대 경로 → 절대 경로 (C:\claude\...)                  │
│                                                              │
│  3. 루트에서 실행 (필수!)                                    │
│     cd C:\claude && python -m lib.google_docs convert "..."  │
│                                                              │
│  4. 결과 URL 반환                                            │
│     - Google Docs URL 출력                                   │
│     - 실패 시 에러 메시지 출력                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**실행 템플릿 (복사-붙여넣기 가능):**

```powershell
# 서브 프로젝트 파일을 Google Docs로 변환
cd C:\claude && python -m lib.google_docs convert "{절대_파일_경로}"

# 예시: wsoptv_ott 프로젝트
cd C:\claude && python -m lib.google_docs convert "C:\claude\wsoptv_ott\docs\prds\PRD-0002-wsoptv-ott-platform-mvp.md"

# 예시: wsoptv_nbatv_clone 프로젝트
cd C:\claude && python -m lib.google_docs convert "C:\claude\wsoptv_nbatv_clone\docs\guides\WSOP-TV-PRD.md"
```

**⚠️ 절대 하지 말아야 할 것:**

| 금지 행동 | 이유 |
|-----------|------|
| ❌ `prd_manager.py` 존재 여부 확인 | 루트 모듈 직접 사용 |
| ❌ `.prd-registry.json` 존재 여부 확인 | 불필요 |
| ❌ 사용자에게 "인프라가 없습니다" 메시지 | 직접 실행하면 됨 |
| ❌ 서브 프로젝트에서 `python -m lib.google_docs` 직접 실행 | 모듈 없음 에러 |

**✅ 항상 해야 할 것:**

| 필수 행동 | 설명 |
|-----------|------|
| ✅ `cd C:\claude &&` 접두사 사용 | 루트에서 모듈 실행 |
| ✅ 절대 경로로 파일 지정 | 상대 경로 해석 오류 방지 |
| ✅ 변환 결과 URL 반환 | 사용자가 바로 접속 가능 |

### 인증 파일 경로 (고정)

서브 프로젝트에서도 **항상 루트의 인증 파일 사용**:

| 파일 | 경로 |
|------|------|
| OAuth 클라이언트 | `C:\claude\json\desktop_credentials.json` |
| OAuth 토큰 | `C:\claude\json\token.json` |
| 서비스 계정 | `C:\claude\json\service_account_key.json` |

⚠️ **주의**: 서브 프로젝트에 `json/` 폴더를 복사하지 마세요! 중복 인증 파일은 혼란을 야기합니다.

---

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