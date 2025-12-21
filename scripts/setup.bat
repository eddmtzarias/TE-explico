@echo off
REM Setup script para OmniMaestro - Windows

echo.
echo 🚀 Configurando proyecto OmniMaestro...
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Por favor instala Python 3.10+
    echo 📥 Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% encontrado

REM Crear entorno virtual
echo.
echo 📦 Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
echo ⚡ Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo 📦 Actualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar dependencias base
echo 📦 Instalando dependencias base...
pip install --quiet requests beautifulsoup4 pillow python-dotenv

REM Verificar si hay requirements.txt
if exist requirements.txt (
    echo 📦 Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt --quiet
)

REM Crear .env si no existe
if not exist .env (
    echo 📝 Creando archivo .env desde template...
    copy .env.example .env >nul
    echo ⚠️  IMPORTANTE: Edita .env y completa tus API keys
)

REM Crear directorios necesarios
echo 📁 Creando estructura de directorios...
if not exist designs mkdir designs
if not exist screenshots mkdir screenshots
if not exist tutorials mkdir tutorials
if not exist logs mkdir logs
if not exist .metadata mkdir .metadata

REM Verificar instalación de PixARR Design
echo 🔍 Verificando sistema PixARR Design...
python -c "from pixarr_design.core.agent import PixARRAgent" >nul 2>&1
if errorlevel 0 (
    echo ✅ Sistema PixARR Design disponible
) else (
    echo ⚠️  Sistema PixARR Design no encontrado (esto es normal en desarrollo inicial)
)

echo.
echo ✅ ¡Setup completado exitosamente!
echo.
echo 🎯 Próximos pasos:
echo    1. Edita .env con tus configuraciones
echo    2. Activa el entorno: venv\Scripts\activate
echo    3. Ejecuta el proyecto según la plataforma:
echo       - Desktop: python -m omnimastro.desktop
echo       - Mobile: flutter run (en directorio mobile/)
echo       - Web: npm start (en directorio web/)
echo.
echo 📚 Documentación: docs\README.md
echo.
pause
