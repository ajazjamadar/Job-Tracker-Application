# REST API Documentation

## Overview

The Job Application Tracker provides a REST API for programmatic access to application data. All API endpoints require authentication using Flask-Login session cookies.

## Base URL

```
/api
```

## Authentication

All API endpoints require authentication. You must first log in through the web interface at `/auth/login` to establish a session before making API requests.

## Endpoints

### List Applications

Retrieve all job applications for the authenticated user.

**Endpoint:** `GET /api/applications`

**Authentication:** Required

**Response:**
```json
[
  {
    "id": 1,
    "company": "Tech Corp",
    "position": "Software Engineer",
    "status": "Applied",
    "date_applied": "2025-10-15",
    "follow_up_date": "2025-10-22",
    "notes": "Applied through LinkedIn"
  },
  {
    "id": 2,
    "company": "Startup Inc",
    "position": "Full Stack Developer",
    "status": "Interview",
    "date_applied": "2025-10-10",
    "follow_up_date": null,
    "notes": null
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `302 Found` - Redirect to login (not authenticated)

---

### Create Application

Create a new job application for the authenticated user.

**Endpoint:** `POST /api/applications`

**Authentication:** Required

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "company": "Tech Corp",          // Required
  "position": "Software Engineer", // Optional
  "status": "Applied"              // Optional, defaults to "Applied"
}
```

**Response:**
```json
{
  "id": 3
}
```

**Status Codes:**
- `201 Created` - Application created successfully
- `400 Bad Request` - Missing required field (company)
- `302 Found` - Redirect to login (not authenticated)

**Error Response (400):**
```json
{
  "error": "company required"
}
```

## Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | - | Unique application ID (auto-generated) |
| `company` | string | Yes | Company name |
| `position` | string | No | Job position/title |
| `status` | string | No | Application status (defaults to "Applied") |
| `date_applied` | string (ISO 8601) | No | Date application was submitted |
| `follow_up_date` | string (ISO 8601) | No | Date to follow up |
| `notes` | string | No | Additional notes |

## Valid Status Values

- `Applied`
- `Interview`
- `Offer`
- `Accepted`
- `Rejected`
- `Withdrawn`

## Usage Examples

### Python (requests library)

```python
import requests

# Base URL
base_url = 'http://localhost:5000'

# Login first to establish session
session = requests.Session()
session.post(f'{base_url}/auth/login', data={
    'email': 'user@example.com',
    'password': 'password123'
})

# List all applications
response = session.get(f'{base_url}/api/applications')
applications = response.json()
print(f'Found {len(applications)} applications')

# Create new application
new_app = {
    'company': 'Tech Corp',
    'position': 'Software Engineer',
    'status': 'Applied'
}
response = session.post(f'{base_url}/api/applications', json=new_app)
if response.status_code == 201:
    app_id = response.json()['id']
    print(f'Created application with ID: {app_id}')
```

### JavaScript (fetch API)

```javascript
// Login first
await fetch('/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    email: 'user@example.com',
    password: 'password123'
  }),
  credentials: 'include'  // Important: include cookies
});

// List applications
const response = await fetch('/api/applications', {
  credentials: 'include'  // Important: include cookies
});
const applications = await response.json();
console.log(`Found ${applications.length} applications`);

// Create application
const newApp = {
  company: 'Tech Corp',
  position: 'Software Engineer',
  status: 'Applied'
};

const createResponse = await fetch('/api/applications', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(newApp),
  credentials: 'include'  // Important: include cookies
});

if (createResponse.ok) {
  const data = await createResponse.json();
  console.log(`Created application with ID: ${data.id}`);
}
```

### cURL

```bash
# Login and save cookies
curl -c cookies.txt -X POST http://localhost:5000/auth/login \
  -d "email=user@example.com&password=password123"

# List applications
curl -b cookies.txt http://localhost:5000/api/applications

# Create application
curl -b cookies.txt -X POST http://localhost:5000/api/applications \
  -H "Content-Type: application/json" \
  -d '{"company":"Tech Corp","position":"Software Engineer","status":"Applied"}'
```

## Testing

Run the API test suite:

```bash
python test_api.py
```

This will:
1. Create a test user
2. Authenticate with the API
3. Test GET endpoint
4. Test POST endpoint (valid data)
5. Test POST endpoint (invalid data)
6. Verify data persistence

## Security Notes

- All endpoints require authentication
- Users can only access their own applications
- CSRF protection is disabled for JSON requests
- Session cookies must be included with each request
- API uses the same authentication system as the web interface

## Future Enhancements

Potential additions to the API:

- `GET /api/applications/<id>` - Get single application
- `PUT /api/applications/<id>` - Update application
- `DELETE /api/applications/<id>` - Delete application
- `GET /api/stats` - Get application statistics
- Token-based authentication (JWT)
- API rate limiting
- Pagination support for large datasets
- Filtering and sorting parameters




