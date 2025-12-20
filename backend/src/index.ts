import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import compression from 'compression'
import morgan from 'morgan'
import { config } from './config/config.js'
import { errorHandler } from './middleware/errorHandler.js'
import { rateLimiter } from './middleware/rateLimiter.js'
import { securityMiddleware } from './middleware/security.js'
import { healthRouter } from './routes/health.js'
import { assistanceRouter } from './routes/assistance.js'
import { metricsRouter } from './routes/metrics.js'

const app = express()

// Security middleware
app.use(helmet())
app.use(securityMiddleware)
app.use(cors({
  origin: config.corsOrigins,
  credentials: true,
}))

// Performance middleware
app.use(compression())
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }))

// Logging
if (config.nodeEnv !== 'test') {
  app.use(morgan('combined'))
}

// Rate limiting
app.use(rateLimiter)

// Routes
app.use('/health', healthRouter)
app.use('/api/assistance', assistanceRouter)
app.use('/metrics', metricsRouter)

// Error handling
app.use(errorHandler)

const server = app.listen(config.port, () => {
  console.log(`🚀 Server running on port ${config.port}`)
  console.log(`📊 Metrics available at http://localhost:${config.port}/metrics`)
})

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server...')
  server.close(() => {
    console.log('Server closed')
    process.exit(0)
  })
})

export { app }
