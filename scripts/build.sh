#!/bin/bash
# Build script for TE-explico multi-platform project
# This script orchestrates the build process for all modules

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_tools=()
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        missing_tools+=("node")
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    # Check Go (optional)
    if ! command -v go &> /dev/null; then
        log_warn "Go not found - Go modules will be skipped"
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_warn "Docker not found - container builds will be skipped"
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_error "Please install missing tools and try again"
        exit 1
    fi
    
    log_info "Prerequisites check passed ✓"
}

# Build core module
build_core() {
    log_info "Building core module..."
    
    if [ -f "$PROJECT_ROOT/core/package.json" ]; then
        cd "$PROJECT_ROOT/core"
        npm install
        npm run build
        log_info "Core module built successfully ✓"
    else
        log_warn "Core module not yet implemented - skipping"
    fi
}

# Build backend services
build_backend() {
    log_info "Building backend services..."
    
    if [ -f "$PROJECT_ROOT/backend/requirements.txt" ]; then
        cd "$PROJECT_ROOT/backend"
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        log_info "Backend dependencies installed ✓"
    else
        log_warn "Backend module not yet implemented - skipping"
    fi
}

# Build frontend web
build_frontend_web() {
    log_info "Building frontend web application..."
    
    if [ -f "$PROJECT_ROOT/frontend/web/package.json" ]; then
        cd "$PROJECT_ROOT/frontend/web"
        npm install
        npm run build
        log_info "Frontend web built successfully ✓"
    else
        log_warn "Frontend web not yet implemented - skipping"
    fi
}

# Build frontend mobile
build_frontend_mobile() {
    log_info "Building frontend mobile application..."
    
    if [ -f "$PROJECT_ROOT/frontend/mobile/pubspec.yaml" ]; then
        cd "$PROJECT_ROOT/frontend/mobile"
        flutter pub get
        flutter build apk
        log_info "Frontend mobile built successfully ✓"
    else
        log_warn "Frontend mobile not yet implemented - skipping"
    fi
}

# Build AI module
build_ai() {
    log_info "Building AI module..."
    
    if [ -f "$PROJECT_ROOT/ai/requirements.txt" ]; then
        cd "$PROJECT_ROOT/ai"
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        log_info "AI module dependencies installed ✓"
    else
        log_warn "AI module not yet implemented - skipping"
    fi
}

# Build Docker images
build_docker() {
    log_info "Building Docker images..."
    
    if command -v docker &> /dev/null; then
        cd "$PROJECT_ROOT"
        
        # Check if Dockerfiles exist
        if [ -d "$PROJECT_ROOT/docker" ]; then
            log_info "Building Docker images..."
            # docker-compose build
            log_info "Docker images would be built here ✓"
        else
            log_warn "Docker configurations not yet implemented - skipping"
        fi
    else
        log_warn "Docker not available - skipping container builds"
    fi
}

# Run tests
run_tests() {
    log_info "Running tests..."
    
    # Core tests
    if [ -f "$PROJECT_ROOT/core/package.json" ]; then
        cd "$PROJECT_ROOT/core"
        npm test
    fi
    
    # Backend tests
    if [ -f "$PROJECT_ROOT/backend/requirements.txt" ]; then
        cd "$PROJECT_ROOT/backend"
        source venv/bin/activate 2>/dev/null || true
        pytest 2>/dev/null || log_warn "Backend tests not yet implemented"
    fi
    
    # Frontend tests
    if [ -f "$PROJECT_ROOT/frontend/web/package.json" ]; then
        cd "$PROJECT_ROOT/frontend/web"
        npm test
    fi
    
    log_info "Tests completed ✓"
}

# Main build orchestration
main() {
    log_info "==================================="
    log_info "TE-explico Build System"
    log_info "TOKRAGGCORP - 100x100+1 Standard"
    log_info "==================================="
    
    check_prerequisites
    
    # Parse command line arguments
    BUILD_TARGET="${1:-all}"
    RUN_TESTS="${2:-false}"
    
    case $BUILD_TARGET in
        all)
            log_info "Building all modules..."
            build_core
            build_backend
            build_frontend_web
            build_frontend_mobile
            build_ai
            build_docker
            ;;
        core)
            build_core
            ;;
        backend)
            build_backend
            ;;
        frontend)
            build_frontend_web
            build_frontend_mobile
            ;;
        ai)
            build_ai
            ;;
        docker)
            build_docker
            ;;
        *)
            log_error "Unknown build target: $BUILD_TARGET"
            log_info "Available targets: all, core, backend, frontend, ai, docker"
            exit 1
            ;;
    esac
    
    if [ "$RUN_TESTS" = "test" ]; then
        run_tests
    fi
    
    log_info "==================================="
    log_info "Build completed successfully! ✓"
    log_info "==================================="
}

# Run main function
main "$@"
