# Drata API Endpoints Reference

## API Versions

- **v1:** `/public/*` - Original API, page-based pagination (`?limit=50&page=1`)
- **v2:** `/public/v2/*` - Newer API, cursor-based pagination (`?cursor=...`)

**Note:** Some v2 endpoints (like `/v2/controls`, `/v2/risks`, `/v2/monitoring-tests`) may return 404. Use v1 alternatives when v2 doesn't work.

---

## v1 Endpoints (Recommended)

### Controls

| Method | Endpoint                                  | Description                                   |
| ------ | ----------------------------------------- | --------------------------------------------- |
| GET    | `/public/controls`                        | List controls (paginated: `?limit=50&page=1`) |
| GET    | `/public/controls/{id}`                   | Get control by ID                             |
| POST   | `/public/controls/{id}/external-evidence` | Upload external evidence                      |

Response fields include:

- `frameworkTags`: ["SOC 2", "ISO 27001:2022"]
- `isReady`: boolean
- `isMonitored`: boolean
- `hasEvidence`: boolean
- `hasOwner`: boolean
- `archivedAt`: timestamp or null

### Personnel

| Method | Endpoint                    | Description                         |
| ------ | --------------------------- | ----------------------------------- |
| GET    | `/public/personnel`         | List personnel with compliance data |
| GET    | `/public/personnel?q=email` | Search by email                     |

Response includes detailed compliance checks for each person.

### Vendors

| Method | Endpoint               | Description      |
| ------ | ---------------------- | ---------------- |
| GET    | `/public/vendors`      | List vendors     |
| GET    | `/public/vendors/{id}` | Get vendor by ID |

### Assets

| Method | Endpoint              | Description                  |
| ------ | --------------------- | ---------------------------- |
| GET    | `/public/assets`      | List assets with device info |
| GET    | `/public/assets/{id}` | Get asset by ID              |

### Users & Documents

| Method | Endpoint                       | Description              |
| ------ | ------------------------------ | ------------------------ |
| GET    | `/public/users/{id}/documents` | List user documents      |
| POST   | `/public/users/{id}/documents` | Upload evidence document |

---

## v2 Endpoints

### Company

| Method | Endpoint             | Description          |
| ------ | -------------------- | -------------------- |
| GET    | `/public/v2/company` | Get company settings |

### Personnel

| Method | Endpoint                    | Description                        |
| ------ | --------------------------- | ---------------------------------- |
| GET    | `/public/v2/personnel`      | List personnel (cursor pagination) |
| GET    | `/public/v2/personnel/{id}` | Get personnel by ID                |
| PATCH  | `/public/v2/personnel/{id}` | Update personnel                   |

**Valid expand values:** `?expand=customFields,complianceChecks,reasonProvider,user`

### Users & Roles

| Method | Endpoint                          | Description                   |
| ------ | --------------------------------- | ----------------------------- |
| GET    | `/public/v2/users`                | List users                    |
| GET    | `/public/v2/users/{id}`           | Get user by ID                |
| POST   | `/public/v2/users/{id}/documents` | Upload document for user      |
| GET    | `/public/v2/users/{id}/documents` | List user documents           |
| GET    | `/public/v2/users/{id}/policies`  | List user's assigned policies |

### Devices

| Method | Endpoint                            | Description            |
| ------ | ----------------------------------- | ---------------------- |
| GET    | `/public/v2/devices`                | List devices           |
| GET    | `/public/v2/devices/{id}`           | Get device by ID       |
| PATCH  | `/public/v2/devices/{id}`           | Update device          |
| POST   | `/public/v2/devices/{id}/documents` | Upload device document |
| GET    | `/public/v2/devices/{id}/documents` | List device documents  |

### Vendors

| Method | Endpoint                                   | Description            |
| ------ | ------------------------------------------ | ---------------------- |
| GET    | `/public/v2/vendors`                       | List vendors           |
| GET    | `/public/v2/vendors/{id}`                  | Get vendor by ID       |
| POST   | `/public/v2/vendors`                       | Create vendor          |
| PATCH  | `/public/v2/vendors/{id}`                  | Update vendor          |
| DELETE | `/public/v2/vendors/{id}`                  | Delete vendor          |
| POST   | `/public/v2/vendors/{id}/documents`        | Upload vendor document |
| GET    | `/public/v2/vendors/{id}/documents`        | List vendor documents  |
| GET    | `/public/v2/vendors/{id}/security-reviews` | List security reviews  |
| POST   | `/public/v2/vendors/{id}/security-reviews` | Create security review |

### Assets

| Method | Endpoint                 | Description     |
| ------ | ------------------------ | --------------- |
| GET    | `/public/v2/assets`      | List assets     |
| GET    | `/public/v2/assets/{id}` | Get asset by ID |
| POST   | `/public/v2/assets`      | Create asset    |
| PATCH  | `/public/v2/assets/{id}` | Update asset    |
| DELETE | `/public/v2/assets/{id}` | Delete asset    |

### Background Checks

| Method | Endpoint                       | Description             |
| ------ | ------------------------------ | ----------------------- |
| GET    | `/public/v2/background-checks` | List background checks  |
| POST   | `/public/v2/background-checks` | Create background check |

### Evidence Library

| Method | Endpoint                           | Description                 |
| ------ | ---------------------------------- | --------------------------- |
| GET    | `/public/v2/evidence-library`      | List evidence library items |
| GET    | `/public/v2/evidence-library/{id}` | Get evidence item           |
| POST   | `/public/v2/evidence-library`      | Upload evidence             |

### Events

| Method | Endpoint            | Description       |
| ------ | ------------------- | ----------------- |
| GET    | `/public/v2/events` | List audit events |

### Custom Connections

| Method | Endpoint                        | Description              |
| ------ | ------------------------------- | ------------------------ |
| GET    | `/public/v2/custom-connections` | List custom connections  |
| POST   | `/public/v2/custom-connections` | Create custom connection |

### Workspaces

| Method | Endpoint                | Description     |
| ------ | ----------------------- | --------------- |
| GET    | `/public/v2/workspaces` | List workspaces |

---

## Query Parameters

### v1 Pagination

| Param   | Description                          |
| ------- | ------------------------------------ |
| `limit` | Items per page (default 50, max 100) |
| `page`  | Page number (1-indexed)              |
| `q`     | Search query (personnel endpoint)    |

### v2 Pagination

| Param    | Description                              |
| -------- | ---------------------------------------- |
| `cursor` | Pagination cursor from previous response |

### Expand Parameter (v2 only)

| Endpoint        | Valid expand values                                          |
| --------------- | ------------------------------------------------------------ |
| `/v2/personnel` | `customFields`, `complianceChecks`, `reasonProvider`, `user` |
| `/v2/vendors`   | `documents`, `securityReviews`                               |

**Note:** Using invalid expand values will return an error message listing valid options.
