#!/bin/bash
#
# Script de instalación de Git hooks para OmniMaestro
#
# Uso: ./scripts/install_hooks.sh
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Instalador de Git Hooks para OmniMaestro${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Verificar que estamos en el directorio raíz del proyecto
if [ ! -f "PROJECT_ROADMAP.md" ]; then
    echo -e "${RED}❌ Error: No se encuentra PROJECT_ROADMAP.md${NC}"
    echo -e "${YELLOW}Ejecuta este script desde el directorio raíz del proyecto${NC}"
    exit 1
fi

# Verificar que el template existe
if [ ! -f ".github/hooks/pre-commit.template" ]; then
    echo -e "${RED}❌ Error: No se encuentra el template de pre-commit${NC}"
    exit 1
fi

# Crear directorio de hooks si no existe
mkdir -p .git/hooks

# Copiar el hook
echo -e "${BLUE}📦 Instalando pre-commit hook...${NC}"
cp .github/hooks/pre-commit.template .git/hooks/pre-commit

# Dar permisos de ejecución
chmod +x .git/hooks/pre-commit

# Verificar instalación
if [ -x ".git/hooks/pre-commit" ]; then
    echo -e "${GREEN}✅ Pre-commit hook instalado correctamente${NC}"
    echo ""
    echo -e "${BLUE}📝 Ubicación:${NC} .git/hooks/pre-commit"
    echo -e "${BLUE}🔧 Para editar:${NC} nano .git/hooks/pre-commit"
    echo -e "${BLUE}🗑️  Para desinstalar:${NC} rm .git/hooks/pre-commit"
    echo -e "${BLUE}⚠️  Para bypass:${NC} git commit --no-verify"
    echo ""
    echo -e "${GREEN}🎉 ¡Listo! El hook se ejecutará automáticamente en cada commit${NC}"
else
    echo -e "${RED}❌ Error: No se pudo instalar el hook${NC}"
    exit 1
fi

exit 0
