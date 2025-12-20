import { test, expect } from '@playwright/test'

test.describe('Dashboard E2E', () => {
  test('should load dashboard successfully', async ({ page }) => {
    await page.goto('/')
    
    await expect(page.locator('h1')).toContainText('OmniMaestro')
    await expect(page.locator('text=TOKRAGGCORP Production System')).toBeVisible()
  })

  test('should display form inputs', async ({ page }) => {
    await page.goto('/')
    
    const contextInput = page.locator('#context')
    const questionInput = page.locator('#input')
    const submitButton = page.locator('button[type="submit"]')
    
    await expect(contextInput).toBeVisible()
    await expect(questionInput).toBeVisible()
    await expect(submitButton).toBeVisible()
  })

  test('should allow user input', async ({ page }) => {
    await page.goto('/')
    
    await page.fill('#context', 'Test context')
    await page.fill('#input', 'Test question')
    
    const contextValue = await page.inputValue('#context')
    const questionValue = await page.inputValue('#input')
    
    expect(contextValue).toBe('Test context')
    expect(questionValue).toBe('Test question')
  })

  test('should display features list', async ({ page }) => {
    await page.goto('/')
    
    await expect(page.locator('text=Multi-modal input')).toBeVisible()
    await expect(page.locator('text=Sub-500ms AI inference')).toBeVisible()
  })
})
