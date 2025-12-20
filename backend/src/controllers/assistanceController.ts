import { Request, Response, NextFunction } from 'express'
import { aiService } from '../services/aiService.js'
import { Histogram } from 'prom-client'

const assistanceLatency = new Histogram({
  name: 'assistance_request_duration_seconds',
  help: 'Duration of assistance requests in seconds',
  labelNames: ['status'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1.0, 2.0, 5.0],
})

export const assistanceController = {
  async getAssistance(req: Request, res: Response, next: NextFunction) {
    const timer = assistanceLatency.startTimer()
    
    try {
      const { context, question } = req.body
      
      const response = await aiService.getAssistance(context, question)
      
      timer({ status: 'success' })
      
      res.json({
        success: true,
        data: response,
      })
    } catch (error) {
      timer({ status: 'error' })
      next(error)
    }
  },
}
