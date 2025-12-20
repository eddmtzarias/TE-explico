# Deployment Guide - TE-explico

## Prerequisites

- Docker 24.0+
- Docker Compose 2.20+
- Kubernetes 1.27+ (for production)
- kubectl configured
- Node.js 18+ (for local development)
- Python 3.11+ (for AI development)

## Local Development

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/eddmtzarias/TE-explico.git
cd TE-explico
```

2. **Install dependencies**
```bash
npm install
cd frontend && npm install
cd ../backend && npm install
cd ../ai && pip install -r ../requirements.txt
```

3. **Start services with Docker Compose**
```bash
docker-compose up -d
```

4. **Access services**
- Frontend: http://localhost:3000
- Backend API: http://localhost:4000
- AI Service: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

### Development Workflow

**Frontend Development**
```bash
cd frontend
npm run dev
```

**Backend Development**
```bash
cd backend
npm run dev
```

**AI Service Development**
```bash
cd ai
python -m uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Docker Deployment

### Build Images

```bash
# Build all images
docker-compose build

# Or build individually
docker build -f infra/docker/Dockerfile.frontend -t te-explico-frontend:latest ./frontend
docker build -f infra/docker/Dockerfile.backend -t te-explico-backend:latest ./backend
docker build -f infra/docker/Dockerfile.ai -t te-explico-ai:latest ./ai
```

### Run Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Kubernetes Deployment

### Prerequisites

1. **Configure kubectl**
```bash
kubectl config use-context your-cluster
```

2. **Create namespace**
```bash
kubectl create namespace te-explico-production
kubectl config set-context --current --namespace=te-explico-production
```

### Deploy Services

1. **Deploy databases**
```bash
# PostgreSQL
kubectl apply -f infra/kubernetes/postgres-deployment.yaml

# Redis
kubectl apply -f infra/kubernetes/redis-deployment.yaml
```

2. **Deploy application services**
```bash
kubectl apply -f infra/kubernetes/ai-deployment.yaml
kubectl apply -f infra/kubernetes/backend-deployment.yaml
kubectl apply -f infra/kubernetes/frontend-deployment.yaml
```

3. **Deploy monitoring**
```bash
kubectl apply -f infra/kubernetes/monitoring/
```

### Verify Deployment

```bash
# Check pod status
kubectl get pods

# Check services
kubectl get services

# Check logs
kubectl logs -f deployment/te-explico-backend
```

### Scaling

```bash
# Scale backend
kubectl scale deployment te-explico-backend --replicas=5

# Scale AI service
kubectl scale deployment te-explico-ai --replicas=3

# Autoscaling
kubectl autoscale deployment te-explico-backend --cpu-percent=70 --min=3 --max=10
```

## Environment Configuration

### Frontend Environment Variables

Create `.env` file in `frontend/` directory:
```env
VITE_API_URL=http://localhost:4000
```

### Backend Environment Variables

Create `.env` file in `backend/` directory:
```env
NODE_ENV=production
PORT=4000
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
AI_SERVICE_URL=http://ai-service:5000
DATABASE_URL=postgresql://user:password@db:5432/te_explico
REDIS_URL=redis://redis:6379
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRES_IN=24h
RATE_LIMIT_WINDOW=900000
RATE_LIMIT_MAX=100
```

### AI Service Environment Variables

Create `.env` file in `ai/` directory:
```env
MODEL_PATH=distilgpt2
MAX_BATCH_SIZE=32
INFERENCE_TIMEOUT=500
CORS_ORIGINS=http://localhost:4000
```

## SSL/TLS Configuration

### Using Let's Encrypt

1. **Install cert-manager (Kubernetes)**
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

2. **Create issuer**
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

3. **Configure Ingress**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: te-explico-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - yourdomain.com
    secretName: te-explico-tls
  rules:
  - host: yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: te-explico-frontend
            port:
              number: 3000
```

## Database Setup

### PostgreSQL Initialization

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U postgres

# Create database
CREATE DATABASE te_explico;

# Run migrations (add when implemented)
# npm run migrate
```

### Redis Configuration

Redis requires no initial setup but can be configured for persistence:

```yaml
redis:
  command: redis-server --appendonly yes
  volumes:
    - redis-data:/data
```

## Monitoring Setup

### Prometheus

Access Prometheus at http://localhost:9090

Key queries:
```promql
# AI inference latency p95
histogram_quantile(0.95, rate(inference_latency_seconds_bucket[5m]))

# Error rate
rate(inference_requests_total{status="error"}[5m])

# Request throughput
rate(http_requests_total[5m])
```

### Grafana

1. Access Grafana at http://localhost:3001
2. Default credentials: admin/admin
3. Add Prometheus data source: http://prometheus:9090
4. Import dashboards from `infra/monitoring/grafana-dashboards/`

## Backup and Recovery

### Database Backup

```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U postgres te_explico > backup.sql

# Restore
docker-compose exec -T db psql -U postgres te_explico < backup.sql
```

### Configuration Backup

```bash
# Backup Kubernetes configurations
kubectl get all -o yaml > backup-k8s.yaml

# Backup secrets
kubectl get secrets -o yaml > backup-secrets.yaml
```

## Troubleshooting

### Common Issues

**Port already in use**
```bash
# Find and kill process using port
lsof -ti:3000 | xargs kill -9
```

**Docker build fails**
```bash
# Clear Docker cache
docker builder prune -a

# Rebuild without cache
docker-compose build --no-cache
```

**Kubernetes pod not starting**
```bash
# Check pod events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check resource limits
kubectl top pods
```

**AI service out of memory**
```bash
# Increase memory limits in deployment
resources:
  limits:
    memory: "8Gi"
```

## Performance Tuning

### Frontend Optimization
- Enable code splitting
- Optimize images
- Use CDN for static assets
- Enable caching headers

### Backend Optimization
- Connection pooling for database
- Redis caching for frequent queries
- Gzip compression enabled
- Rate limiting to prevent abuse

### AI Service Optimization
- GPU acceleration enabled
- Model quantization (FP16)
- Batch processing
- KV-cache enabled
- Warmup on startup

## Security Checklist

- [ ] Change all default passwords
- [ ] Configure SSL/TLS certificates
- [ ] Set secure JWT secret
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Vulnerability scanning
- [ ] Backup encryption

## Support

For issues or questions:
- Create an issue on GitHub
- Contact: support@tokraggcorp.com
- Documentation: https://docs.te-explico.com

---

**Version**: 1.0  
**Last Updated**: December 2025
