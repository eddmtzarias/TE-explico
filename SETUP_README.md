# 🚀 OmniMaestro - Setup Autónomo

Sistema de configuración automática completo para OmniMaestro Desktop MVP.

## 📋 Requisitos Previos

- **Python:** 3.8 o superior
- **Sistema Operativo:** Windows 10/11 (optimizado para), Linux, macOS
- **Hardware Target:** 
  - CPU: Intel i5-7300HQ o superior
  - RAM: 8GB (6.5GB usables)
  - Disco: 5GB libres (preferiblemente SSD)

## 🎯 ¿Qué hace este setup?

El sistema de setup autónomo automatiza los siguientes pasos del proyecto:

- ✅ **Paso #5:** Configuración de variables de entorno
- ✅ **Paso #7:** Integración de OCR (Tesseract)
- ✅ **Paso #8:** Integración de IA (OpenAI/Anthropic)
- ✅ **Paso #10:** UI Desktop funcional (Flet)

**Progreso del proyecto:** 6% → 20% (+14%)

## 🏃 Inicio Rápido

### Windows

```bash
# Ejecutar script maestro
cd D:\Proyectos\TE-explico
scripts\RUN_AUTO_SETUP.bat
```

### Linux/macOS

```bash
# 1. Instalar psutil
pip install psutil

# 2. Setup de entorno
python scripts/auto_setup_env.py

# 3. Editar .env con tus API keys
nano .env  # o tu editor favorito

# 4. Setup del core backend
python scripts/auto_core_setup.py
```

## 🔑 Configuración de API Keys

Después del paso 2, **debes** editar el archivo `.env` y agregar al menos una API key:

### OpenAI (Recomendado para MVP)

1. Obtén tu API key en: https://platform.openai.com/api-keys
2. En `.env`, completa:
   ```
   OPENAI_API_KEY=sk-...tu-key-aquí...
   ```

### Anthropic Claude (Alternativa)

1. Obtén tu API key en: https://console.anthropic.com/
2. En `.env`, completa:
   ```
   ANTHROPIC_API_KEY=sk-ant-...tu-key-aquí...
   ```

## 🖥️ Lanzar la Aplicación

Una vez completado el setup:

```bash
# Desde la raíz del proyecto
python omnimastro/desktop/main.py
```

La aplicación abrirá una ventana de 450x700px con:
- ✅ Input field para texto/preguntas
- ✅ Selector de nivel (Principiante/Intermedio/Avanzado)
- ✅ Botón "Explicar" → genera explicaciones con IA
- ⏳ Botón "Capturar Pantalla" (próximamente)

## 📁 Estructura Generada

```
TE-explico/
├── .env                          # Variables de entorno (creado)
├── .resource_log.json            # Log de recursos (auto-generado)
├── data/                         # Database SQLite
├── temp/                         # Archivos temporales
├── .cache/                       # Cache del sistema
├── logs/                         # Logs de aplicación
├── omnimastro/
│   ├── core/
│   │   ├── ai_explainer.py      # Motor de explicaciones (generado)
│   │   ├── ocr_engine.py        # Motor OCR
│   │   └── ai_engine.py         # Motor IA avanzado
│   ├── desktop/
│   │   └── main.py              # UI Desktop con Flet (generado)
│   └── shared/
│       └── config.py            # Configuración mejorada (actualizado)
├── tests/
│   ├── test_config.py           # Tests de configuración
│   ├── test_ai_explainer.py     # Tests de IA
│   └── test_integration.py      # Test de integración completo
└── scripts/
    ├── resource_monitor.py      # Monitor de recursos
    ├── auto_setup_env.py        # Setup de entorno
    ├── auto_core_setup.py       # Setup del core
    └── RUN_AUTO_SETUP.bat       # Script maestro (Windows)
```

## 🧪 Ejecutar Tests

```bash
# Test individual
python tests/test_config.py
python tests/test_ai_explainer.py

# Test de integración completo
python tests/test_integration.py

# Con pytest (si está instalado)
pytest tests/
```

## 🔧 Scripts Individuales

### 1. Monitor de Recursos

```bash
python scripts/resource_monitor.py
```

Muestra estado actual de CPU, RAM y disco.

### 2. Setup de Entorno

```bash
python scripts/auto_setup_env.py
```

Crea `.env` y estructura de directorios.

### 3. Setup del Core

```bash
python scripts/auto_core_setup.py
```

Instala dependencias y genera módulos del sistema.

## 🐛 Solución de Problemas

### Error: "No module named 'psutil'"

```bash
pip install psutil
```

### Error: "Tesseract not found"

**Windows:**
1. Descargar: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar en: `C:\Program Files\Tesseract-OCR\`
3. Actualizar `TESSERACT_PATH` en `.env`

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### Error: "Motor de IA no inicializado"

Verifica que tu archivo `.env` tenga al menos una API key configurada correctamente:

```bash
# Verificar
cat .env | grep API_KEY

# Debe mostrar algo como:
# OPENAI_API_KEY=sk-...
```

### Instalación de dependencias falla

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar manualmente las problemáticas
python -m pip install flet --no-cache-dir
python -m pip install opencv-python-headless --no-cache-dir
```

## 📊 Métricas de Performance

En hardware target (i5-7300HQ + 8GB RAM):

- **Tiempo total:** 60-90 minutos
- **RAM pico:** ~3.5GB (durante instalación)
- **Disco usado:** ~2.5GB (dependencias)
- **CPU promedio:** 40-60%

## 🎨 Decisiones Técnicas

### Flet vs Tauri

**Elegido:** Flet
- ✅ Python puro (sin Rust toolchain)
- ✅ Compilación instantánea
- ✅ Cross-platform sin ajustes
- ✅ Menor consumo de RAM durante desarrollo

### Tesseract vs EasyOCR

**Elegido:** Tesseract
- ✅ Ligero, CPU-only
- ✅ Sin modelos PyTorch pesados
- ✅ Instalación externa (no infla requirements)

### SQLite vs PostgreSQL

**Elegido:** SQLite
- ✅ Zero-config
- ✅ Portátil
- ✅ Suficiente para MVP

## 🔗 Referencias

- **Flet Framework:** https://flet.dev/
- **Tesseract OCR:** https://github.com/tesseract-ocr/tesseract
- **OpenAI API:** https://platform.openai.com/docs
- **Anthropic API:** https://docs.anthropic.com/
- **PROJECT_ROADMAP.md:** Pasos 5-10 del proyecto

## 📝 Notas

- Los archivos `.env`, `.resource_log.json` y `data/*.db` están en `.gitignore` por seguridad
- Todas las operaciones pesadas monitorean recursos automáticamente
- El sistema está optimizado para hardware limitado (i5-7300HQ + 8GB RAM)
- La arquitectura es modular: fácil migrar entre OpenAI ↔ Anthropic

## 🎯 Próximo Paso

**Paso #11:** Captura de pantalla con hotkeys → integrar OCR con UI

---

**Versión:** 0.2.0  
**Estado:** MVP Funcional  
**Progreso:** 20% (10/50 pasos completados)
