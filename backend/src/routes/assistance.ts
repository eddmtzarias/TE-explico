import { Router } from 'express'
import { body, validationResult } from 'express-validator'
import { assistanceController } from '../controllers/assistanceController.js'

const router = Router()

router.post(
  '/',
  [
    body('context').isString().trim().notEmpty().isLength({ max: 10000 }),
    body('question').isString().trim().notEmpty().isLength({ max: 1000 }),
  ],
  async (req, res, next) => {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() })
    }
    return assistanceController.getAssistance(req, res, next)
  }
)

export { router as assistanceRouter }
