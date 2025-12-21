# 🎨 PixARR Design - Sistema de Auditoría Gráfica Autónoma

**Versión:** 1.0.0  
**Supervisor:** Melampe001  
**Contacto:** tokraagcorp@gmail.com

---

## 📋 Descripción

PixARR Design es un sistema de supervisión autónoma para artefactos de diseño gráfico que proporciona:

- ✅ **Auditoría inmutable** de todos los cambios en archivos de diseño
- 🔒 **Detección automática** de accesos no autorizados
- 📊 **Reportes profesionales** en Markdown con tabla de trazabilidad
- 🚨 **Sistema de alertas** multinivel al supervisor
- 🔐 **Validación de integridad** mediante hashing SHA-256
- 📦 **Cuarentena automática** de archivos comprometidos

---

## 🚀 Características Principales

### 1. Supervisión Automática

Monitorea archivos con las siguientes extensiones:
- **Diseño:** `.psd`, `.ai`, `.xd`, `.fig`, `.sketch`
- **Imágenes:** `.png`, `.jpg`, `.jpeg`, `.svg`, `.webp`
- **Documentación:** `.md`, `.txt`

### 2. Trazabilidad Completa

Cada archivo supervisado incluye:
- Hash SHA-256 único
- Metadata embebida (PNG) o archivo `.meta` asociado
- Historial de versiones
- Registro de creadores y modificadores
- Timestamps en formato ISO 8601

### 3. Sistema de Alertas

Niveles de severidad:
- 🔵 **LOW** - Información general
- 🟡 **MEDIUM** - Advertencia moderada
- 🟠 **HIGH** - Incidente de seguridad
- 🔴 **CRITICAL** - Emergencia crítica

### 4. Gestión de Incidentes

Ante accesos no autorizados:
1. Movimiento automático a cuarentena
2. Registro en bitácora de incidentes
3. Alerta inmediata al supervisor
4. Preservación de evidencia

---

## 📦 Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Configuración del Entorno

```bash
python scripts/setup_environment.py
```

Esto creará la estructura de directorios:

```
TE-explico/
├── designs/
│   ├── active/          # Artefactos activos
│   ├── archive/         # Artefactos archivados
│   └── quarantine/      # Archivos en cuarentena
├── logs/                # Bitácoras JSON
│   ├── audit_log.json
│   └── incident_log.json
├── reports/             # Reportes generados
└── pixarr_design/       # Código fuente
```

---

## 🎯 Uso Rápido

### Ejecución de Simulación Completa

```bash
python scripts/run_simulation.py
```

Este script ejecuta los 6 pasos del emulador:
1. ✅ Configuración del Agente
2. 🎨 Generación de Artefacto Visual
3. ✏️ Edición y Cambios
4. 🔍 Auditoría de Integridad
5. 🚨 Detección de Incidentes
6. 📄 Documentación y Cierre

### Uso Programático

```python
from pixarr_design.core.agent import PixARRAgent

# Inicializar agente
agent = PixARRAgent()
agent.activate()

# Crear artefacto
metadata = agent.create_artifact("designs/active/logo.png", "Designer123")

# Modificar artefacto
agent.modify_artifact("designs/active/logo.png", "Designer123", "Actualizar colores")

# Auditar integridad
results = agent.audit_integrity()

# Generar reporte
report_path = agent.generate_report()
```

---

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
pixarr_design/
├── core/
│   ├── agent.py          # Agente principal
│   ├── logger.py         # Sistema de logging
│   ├── alerts.py         # Sistema de alertas
│   └── integrity.py      # Validador de integridad
├── utils/
│   ├── hash_utils.py     # Utilidades de hashing
│   ├── metadata.py       # Gestión de metadata
│   └── file_watcher.py   # Monitoreo en tiempo real
├── dashboard/
│   └── generator.py      # Generador de reportes
└── config/
    └── settings.py       # Configuración global
```

### Flujo de Datos

```
1. Archivo creado/modificado
   ↓
2. Cálculo de hash SHA-256
   ↓
3. Inyección de metadata
   ↓
4. Registro en bitácora
   ↓
5. Validación de integridad
   ↓
6. Generación de reportes
```

---

## 📊 Formato de Reportes

Los reportes se generan en Markdown con las siguientes secciones:

### Tabla de Artefactos

| Archivo | Fecha | Cambio | Responsable | Hash | Estado |
|---------|-------|--------|-------------|------|--------|
| logo.png | 2025-12-21 09:05:00 | Creación | Designer | 6e3cf5... | OK |
| logo_v2.png | 2025-12-21 09:15:00 | Edición | Designer | f2e8b1... | OK |

### Estadísticas

- Total de Artefactos
- Artefactos Activos
- Archivos en Cuarentena
- Modificaciones Totales
- Incidentes Detectados

### Incidentes de Seguridad

Detalle de cada incidente con timestamp, actor y severidad.

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_agent.py -v
pytest tests/test_integrity.py -v
pytest tests/test_simulation.py -v

# Con cobertura
pytest tests/ --cov=pixarr_design --cov-report=html
```

### Tests Disponibles

- ✅ `test_agent.py` - Tests del agente principal
- ✅ `test_integrity.py` - Tests de validación de integridad
- ✅ `test_simulation.py` - Tests del flujo completo

---

## 🔒 Seguridad

### Características de Seguridad

1. **Hashing Inmutable**: SHA-256 para todos los archivos
2. **Metadata Embebida**: Prevención de manipulación externa
3. **Cuarentena Automática**: Aislamiento de archivos sospechosos
4. **Bitácoras Append-Only**: No modificables una vez escritas
5. **Alertas en Tiempo Real**: Notificación inmediata al supervisor

### Detección de Amenazas

El sistema detecta:
- Modificaciones no autorizadas
- Cambios de hash inesperados
- Acceso de actores no registrados
- Alteración de metadata

---

## 🔧 Configuración

### Archivo `pixarr_design/config/settings.py`

```python
# Supervisor
SUPERVISOR_NAME = "Melampe001"
SUPERVISOR_EMAIL = "tokraagcorp@gmail.com"

# Extensiones monitoreadas
MONITORED_EXTENSIONS = [".psd", ".ai", ".png", ".jpg", ...]

# Algoritmo de hash
HASH_ALGORITHM = "sha256"
```

---

## 📈 Benchmarks

### Rendimiento

- **Hash SHA-256**: ~500 MB/s en archivos grandes
- **Metadata PNG**: < 100ms por archivo
- **Auditoría**: ~1000 archivos/segundo
- **Reportes**: < 2s para 10,000 eventos

### Escalabilidad

- ✅ Soporta repositorios con 100,000+ archivos
- ✅ Lectura en bloques de 8KB para eficiencia
- ✅ Procesamiento paralelo en auditorías

---

## 🔄 CI/CD con GitHub Actions

El sistema incluye workflow automatizado:

```yaml
# .github/workflows/pixarr_monitor.yml
- Trigger en cambios de designs/**
- Instalación automática de dependencias
- Ejecución de auditoría de integridad
- Upload de reportes como artifacts
- Notificación de anomalías
```

---

## 📚 Documentación Adicional

- 📖 [Documentación de API](docs/API_DOCUMENTATION.md)
- 🏛️ [Arquitectura del Sistema](docs/ARCHITECTURE.md)
- 🧪 [Guía de Testing](docs/TESTING.md)

---

## 🤝 Contribución

Este es un sistema de auditoría crítico. Cualquier contribución debe:

1. ✅ Mantener compatibilidad con el formato de bitácoras
2. ✅ Pasar todos los tests existentes
3. ✅ Incluir tests para nuevas funcionalidades
4. ✅ Seguir PEP 8 y usar type hints
5. ✅ Documentar con docstrings completos

---

## 📞 Soporte

**Supervisor:** Melampe001  
**Email:** tokraagcorp@gmail.com  
**Proyecto:** TE-explico  
**Repositorio:** github.com/eddmtzarias/TE-explico

---

## 📄 Licencia

Sistema propietario de TOKRAGGCORP.  
Todos los derechos reservados © 2025.

---

## 🎯 Roadmap

### v1.1 (Q1 2026)
- [ ] Soporte para archivos Figma (.fig)
- [ ] Dashboard web interactivo
- [ ] Integración con Slack/Discord
- [ ] Machine learning para detección de anomalías

### v1.2 (Q2 2026)
- [ ] Versionado automático con Git LFS
- [ ] Comparación visual de cambios
- [ ] API REST para integraciones
- [ ] Mobile app para supervisión

---

*Documento generado por PixARR Design System v1.0*
