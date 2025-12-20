# Quick Start Guide - TE-explico

Get up and running with TE-explico in under 5 minutes!

## Prerequisites

- **Docker Desktop** 24.0+ ([Download](https://www.docker.com/products/docker-desktop))
- **Git** ([Download](https://git-scm.com/downloads))

That's it! Docker will handle everything else.

## 1. Clone the Repository

```bash
git clone https://github.com/eddmtzarias/TE-explico.git
cd TE-explico
```

## 2. Start All Services

```bash
docker-compose up -d
```

This will:
- Build and start all services (Frontend, Backend, AI, Databases)
- Set up monitoring (Prometheus, Grafana)
- Configure networking between services

**First-time build**: ~5-10 minutes (downloads dependencies)  
**Subsequent starts**: ~30 seconds

## 3. Verify Services

Check that all services are running:

```bash
docker-compose ps
```

You should see all services with status "Up".

## 4. Access the Application

Open your browser and visit:

### Main Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:4000/health
- **AI Service**: http://localhost:5000/health

### Monitoring
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

## 5. Try It Out!

1. Go to http://localhost:3000
2. In the context box, enter: `I'm using Photoshop and looking at the layers panel`
3. In the question box, enter: `How do I merge two layers?`
4. Click "Get Assistance"

You should receive an AI-powered response explaining how to merge layers!

## 6. View Logs

To see what's happening behind the scenes:

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f ai-service
```

## 7. Stop Services

When you're done:

```bash
docker-compose down
```

To also remove data:

```bash
docker-compose down -v
```

## Troubleshooting

### Port Already in Use

If you get port conflicts, stop the conflicting service or edit `docker-compose.yml` to use different ports.

### Services Won't Start

```bash
# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### AI Service Takes Too Long

The AI service needs to download models on first start. This is normal and can take 2-3 minutes.

### Can't Connect to Services

Wait 30 seconds after running `docker-compose up -d` for all services to fully start.

## Development Mode

For active development with hot reload:

### 1. Install Dependencies

```bash
# Root
npm install

# Frontend
cd frontend && npm install

# Backend
cd backend && npm install

# AI (requires Python 3.11+)
cd ai && pip install -r ../requirements.txt
```

### 2. Start Services

```bash
# Frontend (hot reload)
cd frontend && npm run dev

# Backend (hot reload)
cd backend && npm run dev

# AI Service (hot reload)
cd ai && python -m uvicorn main:app --reload
```

### 3. Run Tests

```bash
# All tests
npm test

# Frontend only
cd frontend && npm test

# Backend only
cd backend && npm test

# AI only
cd ai && pytest
```

## Configuration

### Environment Variables

Copy example files and customize:

```bash
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
cp ai/.env.example ai/.env
```

Edit the files to match your environment.

## Next Steps

- 📚 Read the [Architecture Documentation](docs/architecture/ARCHITECTURE.md)
- 🔌 Explore the [API Documentation](docs/api/API.md)
- 🚀 Check the [Deployment Guide](docs/deployment/DEPLOYMENT.md)
- 🔒 Review [Security Policy](SECURITY.md)
- 🤝 See [Contributing Guidelines](CONTRIBUTING.md)

## Need Help?

- 📖 Check the [full README](README.md)
- 🐛 Report issues on [GitHub](https://github.com/eddmtzarias/TE-explico/issues)
- 📧 Email: support@tokraggcorp.com

---

**🎉 You're all set!** Start building with OmniMaestro™
