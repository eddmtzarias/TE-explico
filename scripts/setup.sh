#!/bin/bash
# Setup script para OmniMaestro - Linux/macOS

set -e

echo "🚀 Configurando proyecto OmniMaestro..."
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Por favor instala Python 3.10+."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION encontrado"

# Crear entorno virtual
echo ""
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "⚡ Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip --quiet

# Instalar dependencias base
echo "📦 Instalando dependencias base..."
pip install --quiet \
    requests \
    beautifulsoup4 \
    pillow \
    python-dotenv

# Verificar si hay requirements.txt
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt --quiet
fi

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env desde template..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita .env y completa tus API keys"
fi

# Crear directorios necesarios
echo "📁 Creando estructura de directorios..."
mkdir -p designs
mkdir -p screenshots
mkdir -p tutorials
mkdir -p logs
mkdir -p .metadata

# Verificar instalación de PixARR Design
echo "🔍 Verificando sistema PixARR Design..."
if python3 -c "from pixarr_design.core.agent import PixARRAgent" 2>/dev/null; then
    echo "✅ Sistema PixARR Design disponible"
else
    echo "⚠️  Sistema PixARR Design no encontrado (esto es normal en desarrollo inicial)"
fi

echo ""
echo "✅ ¡Setup completado exitosamente!"
echo ""
echo "🎯 Próximos pasos:"
echo "   1. Edita .env con tus configuraciones"
echo "   2. Activa el entorno: source venv/bin/activate"
echo "   3. Ejecuta el proyecto según la plataforma:"
echo "      - Desktop: python -m omnimastro.desktop"
echo "      - Mobile: flutter run (en directorio mobile/)"
echo "      - Web: npm start (en directorio web/)"
echo ""
echo "📚 Documentación: docs/README.md"
echo ""
