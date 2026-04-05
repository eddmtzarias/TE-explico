@echo off
REM ================================================================
REM OmniMaestro - Script Maestro de Setup Automatico
REM Ejecuta todas las fases de configuracion del sistema
REM ================================================================

echo.
echo ================================================================
echo  OMNIMAESTRO - SETUP AUTONOMO COMPLETO
echo ================================================================
echo  Target: i5-7300HQ + 8GB RAM + Windows 10
echo  Progreso esperado: 6%% -^> 20%%
echo ================================================================
echo.

REM Fase 0: Pre-check de Python
echo [FASE 0] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Python no encontrado en PATH
    echo   Instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)
python --version
echo   OK
echo.

REM Fase 1: Instalar psutil si falta (requerido por resource_monitor)
echo [FASE 1] Verificando psutil...
python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo   Instalando psutil...
    python -m pip install psutil --quiet
    if errorlevel 1 (
        echo   ERROR: No se pudo instalar psutil
        pause
        exit /b 1
    )
)
echo   OK
echo.

REM Fase 2: Monitoreo de recursos
echo [FASE 2] Monitoreando recursos del sistema...
python scripts/resource_monitor.py
if errorlevel 1 (
    echo   ADVERTENCIA: Error en monitoreo, continuando...
)
echo.

REM Fase 3: Setup de variables de entorno
echo [FASE 3] Configurando variables de entorno...
python scripts/auto_setup_env.py
if errorlevel 1 (
    echo   ERROR: Fallo en setup de entorno
    pause
    exit /b 1
)
echo.

REM ================================================================
REM PAUSA MANUAL: Usuario debe editar .env con API keys
REM ================================================================
echo ================================================================
echo  PAUSA MANUAL REQUERIDA
echo ================================================================
echo.
echo  Antes de continuar, debes:
echo  1. Abrir el archivo .env en tu editor favorito
echo  2. Completar las API keys:
echo     - OPENAI_API_KEY=sk-...
echo     - ANTHROPIC_API_KEY=sk-ant-...
echo  3. Si usas Windows, verifica TESSERACT_PATH
echo.
echo  Presiona cualquier tecla cuando hayas terminado...
echo ================================================================
pause >nul
echo.

REM Verificar que hay al menos una API key configurada
echo Verificando API keys...
findstr /C:"OPENAI_API_KEY=sk-" .env >nul 2>&1
set OPENAI_FOUND=%errorlevel%
findstr /C:"ANTHROPIC_API_KEY=sk-ant-" .env >nul 2>&1
set ANTHROPIC_FOUND=%errorlevel%

if %OPENAI_FOUND% NEQ 0 if %ANTHROPIC_FOUND% NEQ 0 (
    echo.
    echo   ADVERTENCIA: No se detectaron API keys configuradas
    echo   La funcionalidad de IA NO estara disponible
    echo.
    echo   Presiona Ctrl+C para cancelar y configurar API keys
    echo   o cualquier tecla para continuar sin IA...
    pause >nul
)
echo.

REM Fase 4: Setup del core backend
echo [FASE 4] Configurando core backend...
echo   (Esto puede tomar 5-10 minutos en i5-7300HQ)
echo.
python scripts/auto_core_setup.py
if errorlevel 1 (
    echo   ERROR: Fallo en setup del core
    pause
    exit /b 1
)
echo.

REM ================================================================
REM FINALIZACION
REM ================================================================
echo ================================================================
echo  SETUP COMPLETADO EXITOSAMENTE
echo ================================================================
echo.
echo  Progreso del proyecto: 6%% -^> 20%% (+14%%)
echo.
echo  Pasos completados:
echo    [OK] #5  Variables de entorno
echo    [OK] #7  OCR integrado (Tesseract)
echo    [OK] #8  IA integrada (OpenAI/Anthropic)
echo    [OK] #10 UI Desktop funcional (Flet)
echo.
echo  Para lanzar la aplicacion:
echo    python omnimastro\desktop\main.py
echo.
echo  Para ejecutar tests:
echo    python tests\test_config.py
echo    python tests\test_ai_explainer.py
echo.
echo ================================================================
echo.
pause
