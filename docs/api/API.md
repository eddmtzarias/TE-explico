# API Documentation - TE-explico

## Base URL

- **Development**: `http://localhost:4000`
- **Production**: `https://api.te-explico.com`

## Authentication

Currently, the API is open for development. JWT authentication will be implemented for production.

```http
Authorization: Bearer <token>
```

## Common Headers

```http
Content-Type: application/json
Accept: application/json
```

## Rate Limiting

- **Window**: 15 minutes
- **Max Requests**: 100 per window
- **Headers**:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Time when limit resets

## Endpoints

### Health Check

Check the health status of the backend service.

**Endpoint**: `GET /health`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2025-12-20T04:09:26.511Z",
  "uptime": 3600.5,
  "memory": {
    "rss": 50331648,
    "heapTotal": 20971520,
    "heapUsed": 15728640,
    "external": 1048576
  }
}
```

---

### Get Assistance

Request AI-powered contextual learning assistance.

**Endpoint**: `POST /api/assistance`

**Request Body**:
```json
{
  "context": "I am using Photoshop and looking at the layers panel. There are multiple layers visible.",
  "question": "How do I merge two layers together?"
}
```

**Validation Rules**:
- `context`: Required, string, max 10,000 characters
- `question`: Required, string, max 1,000 characters

**Success Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "answer": "To merge two layers in Photoshop:\n1. Select the layers you want to merge\n2. Right-click and choose 'Merge Layers' or press Ctrl+E (Cmd+E on Mac)\n3. The layers will combine into one",
    "confidence": 0.92,
    "latency_ms": 245.67,
    "model_version": "1.0.0"
  }
}
```

**Error Responses**:

`400 Bad Request` - Validation error
```json
{
  "success": false,
  "errors": [
    {
      "msg": "Context is required",
      "param": "context",
      "location": "body"
    }
  ]
}
```

`429 Too Many Requests` - Rate limit exceeded
```json
{
  "success": false,
  "error": "Too many requests from this IP, please try again later."
}
```

`500 Internal Server Error` - Server error
```json
{
  "success": false,
  "error": "Internal server error"
}
```

`503 Service Unavailable` - AI service not ready
```json
{
  "success": false,
  "error": "AI service error: Model not ready"
}
```

---

### Metrics

Get Prometheus metrics for monitoring.

**Endpoint**: `GET /metrics`

**Response**: `200 OK`
```
# HELP inference_requests_total Total number of inference requests
# TYPE inference_requests_total counter
inference_requests_total{status="success"} 1523
inference_requests_total{status="error"} 12

# HELP assistance_request_duration_seconds Duration of assistance requests in seconds
# TYPE assistance_request_duration_seconds histogram
assistance_request_duration_seconds_bucket{status="success",le="0.1"} 234
assistance_request_duration_seconds_bucket{status="success",le="0.3"} 789
assistance_request_duration_seconds_bucket{status="success",le="0.5"} 1421
...
```

---

## AI Service API

The AI service has its own API for direct access (typically internal use only).

### Base URL

- **Development**: `http://localhost:5000`
- **Production**: `http://ai-service:5000` (internal)

### Health Check

**Endpoint**: `GET /health`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

### Inference

**Endpoint**: `POST /infer`

**Request Body**:
```json
{
  "context": "Using Photoshop layers panel",
  "question": "How to merge layers?"
}
```

**Success Response**: `200 OK`
```json
{
  "answer": "To merge layers in Photoshop...",
  "confidence": 0.92,
  "latency_ms": 245.67,
  "model_version": "1.0.0"
}
```

**Error Responses**:

`503 Service Unavailable` - Model not ready
```json
{
  "detail": "Model not ready"
}
```

`500 Internal Server Error` - Inference failed
```json
{
  "detail": "Inference failed: CUDA out of memory"
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Endpoint doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Service temporarily unavailable |

## Performance Targets

- **API Response Time**: p95 < 1000ms
- **AI Inference Time**: p95 < 500ms
- **Throughput**: 1000+ requests/second
- **Availability**: 99.9% uptime

## Best Practices

### Request Optimization

1. **Keep context concise**: Limit context to relevant information (< 1000 chars recommended)
2. **Be specific**: Clear, focused questions get better answers
3. **Batch requests**: Use multiple requests for different questions rather than combining them
4. **Cache responses**: Cache common questions to reduce API calls

### Error Handling

```javascript
try {
  const response = await fetch('/api/assistance', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ context, question }),
  });

  if (!response.ok) {
    if (response.status === 429) {
      // Handle rate limiting
      console.error('Rate limit exceeded. Please wait.');
    } else if (response.status === 503) {
      // Handle service unavailable
      console.error('Service temporarily unavailable. Please retry.');
    }
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data;
} catch (error) {
  console.error('API request failed:', error);
  throw error;
}
```

### Rate Limiting Strategy

```javascript
// Implement exponential backoff
async function requestWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options);
      
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After') || Math.pow(2, i);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        continue;
      }
      
      return response;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
    }
  }
}
```

## WebSocket Support (Future)

Real-time assistance will be available via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:4000/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'assistance',
    context: 'User context',
    question: 'User question'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Streaming response:', data.chunk);
};
```

## GraphQL Support (Future)

GraphQL endpoint will be available at `/graphql`:

```graphql
mutation GetAssistance($input: AssistanceInput!) {
  assistance(input: $input) {
    answer
    confidence
    latencyMs
    modelVersion
  }
}
```

## OpenAPI Specification

Full OpenAPI 3.0 specification is available at `/api/docs` when the server is running.

---

**API Version**: 1.0  
**Last Updated**: December 2025  
**Support**: api-support@tokraggcorp.com
