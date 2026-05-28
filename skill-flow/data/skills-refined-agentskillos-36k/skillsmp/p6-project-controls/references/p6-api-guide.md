# P6 EPPM Web Services API Guide

Guide for integrating with Oracle Primavera P6 EPPM using the Web Services API (REST and SOAP).

## API Overview

P6 EPPM provides two API interfaces:
1. **RESTful API**: Modern, JSON-based (recommended for new integrations)
2. **SOAP API**: XML-based, legacy but more feature-complete

**Base URL Format**:
```
REST: https://{server}:{port}/p6ws/rest/v1/
SOAP: https://{server}:{port}/p6ws/services/
```

## Authentication

### Basic Authentication (Development)
```python
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('username', 'password')
response = requests.get(
    'https://p6server.company.com/p6ws/rest/v1/project',
    auth=auth,
    headers={'Accept': 'application/json'}
)
```

### Session-Based Authentication (Production)
```python
class P6Session:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self._authenticate(username, password)

    def _authenticate(self, username, password):
        """Establish session with P6"""
        login_url = f"{self.base_url}/login"
        response = self.session.post(
            login_url,
            json={'username': username, 'password': password},
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()

    def get(self, endpoint, params=None):
        """Make GET request with session"""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def logout(self):
        """Close P6 session"""
        self.session.post(f"{self.base_url}/logout")
        self.session.close()
```

## Common REST API Endpoints

### Projects

**Get All Projects**:
```http
GET /p6ws/rest/v1/project
```

**Get Specific Project**:
```http
GET /p6ws/rest/v1/project/{projectId}
```

**Response Example**:
```json
{
  "id": "12345",
  "name": "Mine Expansion Project",
  "projectId": "MINE-001",
  "startDate": "2024-01-15T00:00:00",
  "finishDate": "2026-12-31T00:00:00",
  "status": "Active",
  "percentComplete": 34.5
}
```

**Get Projects with Filters**:
```http
GET /p6ws/rest/v1/project?status=Active&fields=id,name,startDate,finishDate
```

### Activities (Tasks)

**Get Activities for a Project**:
```http
GET /p6ws/rest/v1/activity?projectId={projectId}
```

**Get Activity Details**:
```http
GET /p6ws/rest/v1/activity/{activityId}
```

**Response Example**:
```json
{
  "id": "67890",
  "activityId": "A1010",
  "name": "Install Crusher Foundation",
  "projectId": "12345",
  "type": "Task Dependent",
  "status": "In Progress",
  "plannedStartDate": "2024-06-01T08:00:00",
  "plannedFinishDate": "2024-06-15T17:00:00",
  "actualStartDate": "2024-06-03T08:00:00",
  "remainingDuration": 72.0,
  "totalFloat": 5.0,
  "percentComplete": 40.0,
  "isCritical": false
}
```

**Get Critical Activities**:
```http
GET /p6ws/rest/v1/activity?projectId={projectId}&isCritical=true
```

**Get In-Progress Activities**:
```http
GET /p6ws/rest/v1/activity?projectId={projectId}&status=In Progress
```

### Relationships (Activity Dependencies)

**Get Relationships for Activity**:
```http
GET /p6ws/rest/v1/activityPredecessor?activityId={activityId}
```

**Response Example**:
```json
{
  "predecessorId": "67800",
  "successorId": "67890",
  "type": "Finish to Start",
  "lag": 0.0,
  "isDriving": true
}
```

### WBS (Work Breakdown Structure)

**Get WBS for Project**:
```http
GET /p6ws/rest/v1/wbs?projectId={projectId}
```

**Response Example**:
```json
{
  "id": "45678",
  "code": "1.2.3",
  "name": "Crusher Plant",
  "parentId": "45670",
  "projectId": "12345",
  "percentComplete": 28.0
}
```

### Resources

**Get Resources**:
```http
GET /p6ws/rest/v1/resource
```

**Get Resource Assignments**:
```http
GET /p6ws/rest/v1/activityResourceAssignment?activityId={activityId}
```

**Response Example**:
```json
{
  "id": "99001",
  "activityId": "67890",
  "resourceId": "5001",
  "resourceName": "Concrete Crew",
  "budgetedUnits": 160.0,
  "actualUnits": 64.0,
  "remainingUnits": 96.0
}
```

### Baselines

**Get Project Baselines**:
```http
GET /p6ws/rest/v1/baseline?projectId={projectId}
```

**Compare with Baseline**:
```http
GET /p6ws/rest/v1/activity/{activityId}/baseline/{baselineId}
```

## Update Operations

### Update Activity Progress

**PATCH Request**:
```http
PATCH /p6ws/rest/v1/activity/{activityId}
Content-Type: application/json

{
  "actualStartDate": "2024-06-03T08:00:00",
  "percentComplete": 45.0,
  "remainingDuration": 64.0
}
```

**Python Example**:
```python
def update_activity_progress(session, activity_id, actual_start, pct_complete, remaining_duration):
    """Update activity progress"""
    url = f"{session.base_url}/activity/{activity_id}"
    data = {
        'actualStartDate': actual_start,
        'percentComplete': pct_complete,
        'remainingDuration': remaining_duration
    }
    response = session.session.patch(
        url,
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()
    return response.json()
```

### Create New Activity

**POST Request**:
```http
POST /p6ws/rest/v1/activity
Content-Type: application/json

{
  "activityId": "A2050",
  "name": "Install Conveyor Belt",
  "projectId": "12345",
  "wbsId": "45678",
  "type": "Task Dependent",
  "duration": 80.0,
  "plannedStartDate": "2024-07-01T08:00:00"
}
```

### Add Activity Relationship

**POST Request**:
```http
POST /p6ws/rest/v1/activityPredecessor
Content-Type: application/json

{
  "predecessorId": "67890",
  "successorId": "67900",
  "type": "Finish to Start",
  "lag": 8.0
}
```

## Pagination and Filtering

### Pagination

For large datasets, use pagination:
```http
GET /p6ws/rest/v1/activity?projectId={projectId}&limit=100&offset=0
```

**Python Implementation**:
```python
def get_all_activities(session, project_id, page_size=100):
    """Retrieve all activities with pagination"""
    activities = []
    offset = 0

    while True:
        params = {
            'projectId': project_id,
            'limit': page_size,
            'offset': offset
        }
        response = session.get('activity', params=params)

        if not response:
            break

        activities.extend(response)
        offset += page_size

        if len(response) < page_size:
            break  # Last page

    return activities
```

### Field Selection

Request only needed fields to reduce payload:
```http
GET /p6ws/rest/v1/activity?projectId={projectId}&fields=id,activityId,name,status,plannedStartDate,plannedFinishDate,totalFloat
```

### Filtering

**Filter by Status**:
```http
GET /p6ws/rest/v1/activity?projectId={projectId}&status=In Progress
```

**Filter by Date Range**:
```http
GET /p6ws/rest/v1/activity?projectId={projectId}&plannedStartDate=>2024-06-01&plannedStartDate=<2024-06-30
```

**Multiple Filters**:
```http
GET /p6ws/rest/v1/activity?projectId={projectId}&isCritical=true&status=Not Started
```

## Error Handling

### Common HTTP Status Codes

- **200 OK**: Successful GET/PATCH
- **201 Created**: Successful POST
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication failed
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: P6 server error

### Error Response Example
```json
{
  "errorCode": "ACTIVITY_NOT_FOUND",
  "message": "Activity with ID 99999 does not exist",
  "timestamp": "2024-06-15T14:30:00Z"
}
```

### Python Error Handling
```python
import logging

def safe_api_call(session, endpoint, method='get', **kwargs):
    """Make API call with error handling"""
    try:
        if method == 'get':
            response = session.get(endpoint, **kwargs)
        elif method == 'post':
            response = session.session.post(f"{session.base_url}/{endpoint}", **kwargs)
        elif method == 'patch':
            response = session.session.patch(f"{session.base_url}/{endpoint}", **kwargs)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        logging.error(f"Response: {e.response.text}")
        raise
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection error: {e}")
        raise
    except requests.exceptions.Timeout as e:
        logging.error(f"Request timeout: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
```

## Best Practices

### 1. Connection Management

**Use Session Pooling**:
```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_robust_session(base_url, username, password):
    """Create session with retry logic"""
    session = P6Session(base_url, username, password)

    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.session.mount("http://", adapter)
    session.session.mount("https://", adapter)

    return session
```

### 2. Caching

**Cache Reference Data**:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_resource_by_id(session, resource_id):
    """Get resource with caching"""
    return session.get(f'resource/{resource_id}')
```

### 3. Batch Operations

**Batch Updates**:
```python
def batch_update_activities(session, updates):
    """Update multiple activities in batch"""
    results = []
    for activity_id, data in updates.items():
        try:
            result = safe_api_call(
                session,
                f'activity/{activity_id}',
                method='patch',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            results.append({'activity_id': activity_id, 'success': True})
        except Exception as e:
            results.append({'activity_id': activity_id, 'success': False, 'error': str(e)})
            logging.error(f"Failed to update activity {activity_id}: {e}")

    return results
```

### 4. Rate Limiting

**Respect API Rate Limits**:
```python
import time

class RateLimitedP6Session(P6Session):
    def __init__(self, base_url, username, password, requests_per_second=5):
        super().__init__(base_url, username, password)
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0

    def _wait_if_needed(self):
        """Enforce rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def get(self, endpoint, params=None):
        """Rate-limited GET request"""
        self._wait_if_needed()
        return super().get(endpoint, params)
```

### 5. Data Validation

**Validate Before Update**:
```python
def validate_activity_update(data):
    """Validate activity update data"""
    errors = []

    # Check percent complete range
    if 'percentComplete' in data:
        if not 0 <= data['percentComplete'] <= 100:
            errors.append("Percent complete must be between 0 and 100")

    # Check actual dates
    if 'actualStartDate' in data and 'actualFinishDate' in data:
        from datetime import datetime
        start = datetime.fromisoformat(data['actualStartDate'])
        finish = datetime.fromisoformat(data['actualFinishDate'])
        if finish < start:
            errors.append("Actual finish cannot be before actual start")

    # Check remaining duration
    if 'remainingDuration' in data:
        if data['remainingDuration'] < 0:
            errors.append("Remaining duration cannot be negative")

    return errors
```

## Complete Example: Schedule Health Check

```python
import requests
from requests.auth import HTTPBasicAuth
import logging

class P6HealthChecker:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()

    def check_missing_predecessors(self, project_id):
        """Find activities without predecessors"""
        # Get all activities
        activities = self._get_activities(project_id)

        issues = []
        for activity in activities:
            if activity['type'] != 'Start Milestone':
                # Get predecessors
                preds = self._get_predecessors(activity['id'])
                if not preds:
                    issues.append({
                        'activity_id': activity['activityId'],
                        'name': activity['name'],
                        'issue': 'Missing predecessor'
                    })

        return issues

    def check_critical_path(self, project_id):
        """Analyze critical path"""
        # Get critical activities
        critical = self._get_activities(project_id, {'isCritical': 'true'})

        return {
            'critical_count': len(critical),
            'critical_activities': [
                {
                    'id': a['activityId'],
                    'name': a['name'],
                    'finish': a['plannedFinishDate']
                }
                for a in critical
            ]
        }

    def _get_activities(self, project_id, filters=None):
        """Retrieve activities"""
        params = {'projectId': project_id}
        if filters:
            params.update(filters)

        response = self.session.get(
            f"{self.base_url}/activity",
            auth=self.auth,
            params=params,
            headers={'Accept': 'application/json'}
        )
        response.raise_for_status()
        return response.json()

    def _get_predecessors(self, activity_id):
        """Get activity predecessors"""
        response = self.session.get(
            f"{self.base_url}/activityPredecessor",
            auth=self.auth,
            params={'successorId': activity_id},
            headers={'Accept': 'application/json'}
        )
        response.raise_for_status()
        return response.json()

# Usage
checker = P6HealthChecker(
    'https://p6server.company.com/p6ws/rest/v1',
    'username',
    'password'
)

project_id = '12345'
missing_preds = checker.check_missing_predecessors(project_id)
critical_path = checker.check_critical_path(project_id)

print(f"Found {len(missing_preds)} activities with missing predecessors")
print(f"Critical path has {critical_path['critical_count']} activities")
```

## Resources

**Official Documentation**:
- Oracle P6 EPPM Web Services Reference Guide
- P6 EPPM API Developer's Guide

**Common Issues**:
1. Session timeouts - implement session refresh
2. Large payload responses - use pagination and field selection
3. Concurrent access - implement proper locking mechanisms
4. Date format inconsistencies - always use ISO 8601 format

**Security Considerations**:
- Never hardcode credentials
- Use environment variables or secure vaults
- Implement proper SSL certificate validation
- Log API calls for audit purposes (but not credentials)
- Limit API user permissions to minimum required
