# 🚀 Vercel Deployment Guide for OmniMaestro

## Overview

This guide provides complete instructions for deploying OmniMaestro Web to Vercel.

## Prerequisites

- GitHub account connected to Vercel
- OpenAI API key (`OPENAI_API_KEY`)
- Vercel CLI (optional, for manual deployment)

## Quick Deploy (Recommended)

### Option 1: One-Click Deploy

1. Click the deploy button:
   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/eddmtzarias/TE-explico)

2. Connect your GitHub account if prompted

3. Configure environment variables in Vercel dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key

4. Click "Deploy"

5. Wait 45-90 seconds for deployment to complete

### Option 2: Deploy via GitHub Integration

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import `eddmtzarias/TE-explico` repository
4. Vercel will automatically detect the configuration
5. Add environment variable: `OPENAI_API_KEY`
6. Click "Deploy"

## Manual Deploy (Advanced)

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Navigate to project
cd /path/to/TE-explico

# Deploy to production
vercel --prod

# Set environment variables (if not set via dashboard)
vercel env add OPENAI_API_KEY production
```

## Configuration Files

### `vercel.json`
- Configures Python 3.12 runtime
- Sets function timeout to 10 seconds
- Allocates 1024MB memory per function
- Excludes unnecessary files (tests, desktop, docs)
- Enables CORS headers

### `.vercelignore`
- Additional exclusions for build artifacts
- Prevents deployment of local development files

## API Endpoints

### POST `/api/explain`
Generates pedagogical explanations for text.

**Request:**
```json
{
  "text": "What is a pull request?",
  "context": "Learning GitHub",
  "user_level": "beginner"
}
```

**Response:**
```json
{
  "explanation": "Detailed explanation...",
  "provider": "openai",
  "model": "gpt-4o-mini",
  "status": "success"
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "OmniMaestro API",
  "version": "1.0.0"
}
```

## Testing Your Deployment

### Test Health Endpoint
```bash
curl https://your-deployment.vercel.app/api/health
```

### Test Explain Endpoint
```bash
curl -X POST https://your-deployment.vercel.app/api/explain \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is an API?",
    "user_level": "beginner"
  }'
```

### Test Web Interface
Navigate to: `https://your-deployment.vercel.app/`

## Environment Variables

Required in Vercel Dashboard (Settings → Environment Variables):

| Variable | Value | Environment |
|----------|-------|-------------|
| `OPENAI_API_KEY` | `sk-proj-...` | Production |
| `PYTHON_VERSION` | `3.12` | All |
| `ENVIRONMENT` | `production` | Production |

## Monitoring & Logs

### Access Logs
1. Go to Vercel Dashboard
2. Select your project
3. Navigate to "Functions" tab
4. View real-time logs and metrics

### Performance Metrics
- Cold start time: ~1-2 seconds
- API response time: ~2-4 seconds (including OpenAI)
- Bundle size: ~15-20MB

## Troubleshooting

### Error: "OPENAI_API_KEY not configured"
- Ensure environment variable is set in Vercel Dashboard
- Redeploy after adding environment variables

### Error: "Module not found"
- Check `requirements.txt` includes all dependencies
- Verify Python version is 3.12

### Error: "Function timeout"
- Default timeout is 10 seconds
- Adjust `maxDuration` in `vercel.json` if needed
- Note: Free tier has 10s limit, Pro tier allows 60s

### Bundle Size Too Large
- Check `.vercelignore` is working
- Ensure `excludeFiles` pattern in `vercel.json` is correct
- Remove unnecessary dependencies from `requirements.txt`

## Architecture Differences

| Feature | Desktop | Web (Vercel) |
|---------|---------|--------------|
| **OCR** | ✅ Full Tesseract | ❌ Not available |
| **Screenshots** | ✅ Local capture | ❌ Not available |
| **AI Providers** | ✅ OpenAI + Anthropic | ✅ OpenAI only |
| **Bundle Size** | ~50MB | ~15MB |
| **Offline Mode** | ✅ Yes | ❌ Requires internet |
| **Latency** | <100ms | ~2-4s |

## Security Considerations

- ✅ CORS enabled for web access
- ✅ API key stored as environment variable
- ✅ No sensitive data in client-side code
- ⚠️ Consider rate limiting for production use
- ⚠️ Consider authentication for restricted access

## Cost Estimation

### Vercel (Free Tier)
- 100GB bandwidth/month
- 100 hours function execution/month
- Should be sufficient for small-medium usage

### OpenAI API
- GPT-4o-mini: ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Average explanation: ~$0.001-0.003 per request

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test all endpoints
3. ⏳ Add rate limiting (recommended)
4. ⏳ Add authentication (for production)
5. ⏳ Set up custom domain (optional)
6. ⏳ Configure monitoring alerts (optional)

## Support

For issues or questions:
- GitHub Issues: [eddmtzarias/TE-explico](https://github.com/eddmtzarias/TE-explico/issues)
- Vercel Docs: [vercel.com/docs](https://vercel.com/docs)
- OpenAI API: [platform.openai.com](https://platform.openai.com)
