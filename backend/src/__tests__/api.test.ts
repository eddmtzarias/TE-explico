import request from 'supertest'
import { app } from '../index.js'

describe('Health Endpoint', () => {
  it('should return health status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200)
    
    expect(response.body).toHaveProperty('status', 'healthy')
    expect(response.body).toHaveProperty('timestamp')
    expect(response.body).toHaveProperty('uptime')
  })
})

describe('Assistance Endpoint', () => {
  it('should validate required fields', async () => {
    const response = await request(app)
      .post('/api/assistance')
      .send({})
      .expect(400)
    
    expect(response.body).toHaveProperty('errors')
  })

  it('should validate context length', async () => {
    const response = await request(app)
      .post('/api/assistance')
      .send({
        context: 'a'.repeat(10001),
        question: 'test',
      })
      .expect(400)
  })

  it('should validate question length', async () => {
    const response = await request(app)
      .post('/api/assistance')
      .send({
        context: 'test',
        question: 'a'.repeat(1001),
      })
      .expect(400)
  })
})

describe('Security Headers', () => {
  it('should include security headers', async () => {
    const response = await request(app).get('/health')
    
    expect(response.headers).toHaveProperty('x-content-type-options', 'nosniff')
    expect(response.headers).toHaveProperty('x-frame-options', 'DENY')
    expect(response.headers).toHaveProperty('x-xss-protection')
  })
})
