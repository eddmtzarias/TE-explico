import axios from 'axios'
import { config } from '../config/config.js'
import { AppError } from '../middleware/errorHandler.js'

const aiClient = axios.create({
  baseURL: config.aiServiceUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const aiService = {
  async getAssistance(context: string, question: string) {
    try {
      const response = await aiClient.post('/infer', {
        context,
        question,
      })
      
      return response.data
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new AppError(
          `AI service error: ${error.message}`,
          error.response?.status || 500
        )
      }
      throw new AppError('Failed to get AI assistance', 500)
    }
  },
}
