import { Router } from 'express'

const router = Router()

router.get('/', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
  }

  res.json(health)
})

export { router as healthRouter }
