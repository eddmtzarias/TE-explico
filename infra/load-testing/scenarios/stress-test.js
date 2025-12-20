import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const aiLatency = new Trend('ai_inference_latency');

// Test configuration for stress testing
export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 200 }, // Ramp up to 200 users
    { duration: '5m', target: 200 }, // Stay at 200 users
    { duration: '2m', target: 300 }, // Ramp up to 300 users
    { duration: '5m', target: 300 }, // Stay at 300 users
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500'], // 95% of requests must complete below 500ms
    'http_req_duration{name:ai_inference}': ['p(95)<500'], // AI inference p95 < 500ms
    'errors': ['rate<0.05'], // Error rate must be below 5%
    'http_req_failed': ['rate<0.05'], // Failed requests must be below 5%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:4000';

export default function () {
  // Test 1: Health check
  const healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health check status is 200': (r) => r.status === 200,
  });

  sleep(1);

  // Test 2: AI Inference request
  const payload = JSON.stringify({
    context: 'I am using Photoshop and trying to understand the layers panel',
    question: 'How do I create a new layer?',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
    tags: { name: 'ai_inference' },
  };

  const inferenceRes = http.post(`${BASE_URL}/api/assistance`, payload, params);
  
  const success = check(inferenceRes, {
    'inference status is 200': (r) => r.status === 200,
    'inference has answer': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.data && body.data.answer;
      } catch {
        return false;
      }
    },
    'inference latency < 500ms': (r) => r.timings.duration < 500,
  });

  // Track metrics
  errorRate.add(!success);
  aiLatency.add(inferenceRes.timings.duration);

  sleep(Math.random() * 3 + 2); // Random sleep between 2-5 seconds
}

export function handleSummary(data) {
  return {
    'load-test-summary.json': JSON.stringify(data, null, 2),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}

function textSummary(data, options) {
  const indent = options.indent || '';
  let summary = '\n';
  
  summary += `${indent}✓ Total requests: ${data.metrics.http_reqs.values.count}\n`;
  summary += `${indent}✓ Failed requests: ${data.metrics.http_req_failed.values.rate * 100}%\n`;
  summary += `${indent}✓ Request duration p95: ${data.metrics.http_req_duration.values['p(95)']}ms\n`;
  summary += `${indent}✓ AI inference p95: ${data.metrics['http_req_duration{name:ai_inference}']?.values['p(95)'] || 'N/A'}ms\n`;
  summary += `${indent}✓ Error rate: ${data.metrics.errors?.values.rate * 100 || 0}%\n`;
  
  return summary;
}
