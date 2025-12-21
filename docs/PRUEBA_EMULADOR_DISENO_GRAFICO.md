# 🧪 PRUEBA EMULADOR DISEÑO GRÁFICO - PixARR Design

## Descripción General

Este documento describe la prueba completa del emulador de auditoría gráfica PixARR Design. La prueba simula un flujo de trabajo real de creación, modificación, auditoría y respuesta a incidentes en un entorno de diseño gráfico.

---

## Objetivo de la Prueba

Validar que el sistema PixARR Design puede:

1. ✅ Registrar la creación de artefactos visuales
2. ✅ Rastrear modificaciones con versionado
3. ✅ Detectar cambios no autorizados
4. ✅ Aislar archivos comprometidos
5. ✅ Generar reportes de auditoría profesionales
6. ✅ Alertar al supervisor en tiempo real

---

## Flujo de Prueba - 6 Pasos

### Paso 1: Configuración del Agente

**Objetivo:** Activar el agente y establecer el workspace

**Acciones:**
```python
agent = PixARRAgent()
agent.activate()
```

**Resultado Esperado:**
```
✅ Agente PixARR Design activado
   Supervisor: Melampe001
   Workspace: /path/to/TE-explico
```

**Validación:**
- Directorio activo creado
- Logs inicializados
- Supervisor asignado

---

### Paso 2: Generación de Artefacto Visual

**Objetivo:** Crear un nuevo artefacto de diseño y registrarlo en el sistema

**Acciones:**
1. Crear imagen PNG con PIL: `logo_emulador.png`
   - Tamaño: 400x300px
   - Fondo: Azul oscuro
   - Texto: "PixARR Design\nEmulator v1.0"

2. Registrar artefacto:
```python
artifact = agent.create_artifact(
    "designs/active/logo_emulador.png",
    "PixARR Design"
)
```

**Resultado Esperado:**
```
🎨 Imagen creada: logo_emulador.png
✅ Artefacto creado: logo_emulador.png
   Hash: ea7a76d9914b5d3d...
   Creador: PixARR Design
```

**Validación:**
- Archivo existe en `designs/active/`
- Hash SHA-256 calculado
- Metadata inyectada (PNG o .meta)
- Evento registrado en `audit_log.json`

**Estructura del Log:**
```json
{
  "type": "artifact_created",
  "timestamp": "2025-12-21T10:30:00Z",
  "filename": "logo_emulador.png",
  "hash": "ea7a76d9914b5d3d...",
  "creator": "PixARR Design",
  "version": 1,
  "status": "active",
  "supervisor": "Melampe001"
}
```

---

### Paso 3: Edición y Cambios

**Objetivo:** Simular modificación legítima de un artefacto

**Acciones:**
1. Crear versión modificada: `logo_emulador_v2.png`
   - Tamaño: 400x300px
   - Fondo: Navy
   - Texto: "PixARR Design\nEmulator v2.0\n⭐ Actualizado"

2. Registrar modificación:
```python
modification = agent.modify_artifact(
    "designs/active/logo_emulador_v2.png",
    "PixARR Design",
    "Añadir estrella y actualizar versión"
)
```

**Resultado Esperado:**
```
🎨 Imagen creada: logo_emulador_v2.png
✅ Modificación registrada: logo_emulador_v2.png
   Versión: 2
   Modificador: PixARR Design
   Cambio: Añadir estrella y actualizar versión
```

**Validación:**
- Versión incrementada (v1 → v2)
- Nuevo hash calculado
- Hash anterior preservado
- Modificador registrado
- Descripción del cambio almacenada

**Estructura del Log:**
```json
{
  "type": "artifact_modified",
  "timestamp": "2025-12-21T10:35:00Z",
  "filename": "logo_emulador_v2.png",
  "hash": "346d2321031d6351...",
  "modifier": "PixARR Design",
  "description": "Añadir estrella y actualizar versión",
  "previous_hash": "ea7a76d9914b5d3d...",
  "version": 2,
  "supervisor": "Melampe001"
}
```

---

### Paso 4: Auditoría de Integridad

**Objetivo:** Verificar la integridad de todos los archivos monitoreados

**Acciones:**
```python
audit_results = agent.audit_integrity()
```

**Resultado Esperado:**
```
📊 AUDITORÍA DE INTEGRIDAD
   Archivos verificados: 2
   Anomalías detectadas: 0
   ✅ Todos los archivos pasaron la auditoría
```

**Proceso de Auditoría:**
1. Escanear directorio `designs/active/`
2. Para cada archivo:
   - Calcular hash actual
   - Extraer metadata
   - Comparar con hash almacenado
   - Reportar estado
3. Agregar resultados
4. Registrar auditoría

**Estructura del Log:**
```json
{
  "type": "integrity_audit",
  "timestamp": "2025-12-21T10:40:00Z",
  "files_verified": 2,
  "anomalies": 0,
  "details": "Verified 2 files in /path/to/designs/active",
  "supervisor": "Melampe001"
}
```

**Resultado de Validación:**
```python
{
  "summary": {
    "total_files": 2,
    "valid_files": 2,
    "anomalies": 0,
    "no_metadata": 0
  },
  "results": [
    {
      "filename": "logo_emulador.png",
      "status": "OK",
      "valid": True,
      "current_hash": "ea7a76d9...",
      "stored_hash": "ea7a76d9..."
    },
    {
      "filename": "logo_emulador_v2.png",
      "status": "OK",
      "valid": True,
      "current_hash": "346d2321...",
      "stored_hash": "346d2321..."
    }
  ]
}
```

---

### Paso 5: Detección de Incidentes (Simulada)

**Objetivo:** Detectar y responder a un acceso no autorizado

**Escenario:** Un actor no autorizado (`sim_agenteX`) intenta acceder al archivo

**Acciones:**
```python
agent.detect_unauthorized_access(
    "designs/active/logo_emulador_v2.png",
    "sim_agenteX"
)
```

**Resultado Esperado:**
```
🚨 ALERTA: Acceso no autorizado detectado
   Archivo: logo_emulador_v2.png
   Actor sospechoso: sim_agenteX
   Acción: Movido a cuarentena
   Supervisor notificado: Melampe001

⚠️ ALERTA [HIGH] enviada a tokraagcorp@gmail.com
   Mensaje: ⚠️ ACCESO NO AUTORIZADO detectado en logo_emulador_v2.png
   Timestamp: 2025-12-21T10:45:00Z
```

**Proceso de Respuesta:**
1. Detectar acceso no autorizado
2. Mover archivo a `designs/quarantine/`
3. Registrar incidente en `incident_log.json`
4. Enviar alerta HIGH al supervisor
5. Preservar evidencia para auditoría

**Estructura del Incident Log:**
```json
{
  "type": "unauthorized_access",
  "timestamp": "2025-12-21T10:45:00Z",
  "filename": "logo_emulador_v2.png",
  "suspicious_actor": "sim_agenteX",
  "description": "Acceso no autorizado detectado. Archivo movido a cuarentena.",
  "severity": "HIGH",
  "supervisor": "Melampe001"
}
```

**Validación:**
- Archivo movido a cuarentena ✅
- Incidente registrado ✅
- Alerta enviada ✅
- Evidencia preservada ✅

---

### Paso 6: Documentación y Cierre

**Objetivo:** Generar reporte final de auditoría

**Acciones:**
```python
report_path = agent.generate_report()
```

**Resultado Esperado:**
```
✅ Reporte generado: /path/to/reports/dashboard_20251221_104500.md
```

**Contenido del Reporte:**

#### Header
```markdown
# 🎨 PixARR Design - Reporte de Auditoría

**Fecha de Generación:** 2025-12-21 10:45:00 UTC
**Supervisor:** Melampe001
**Contacto:** tokraagcorp@gmail.com
```

#### Estadísticas
```markdown
## 📊 Estadísticas Generales

| Métrica | Valor |
|---------|-------|
| Total de Artefactos | 1 |
| Artefactos Activos | 1 |
| Archivos en Cuarentena | 1 |
| Modificaciones Totales | 1 |
| Incidentes Detectados | 1 |
```

#### Tabla de Artefactos
```markdown
## 📋 Tabla de Artefactos

| Archivo | Fecha | Cambio | Responsable | Hash | Estado |
|---------|-------|--------|-------------|------|--------|
| logo_emulador.png | 2025-12-21 10:30:00 | Creación | PixARR Design | ea7a76d9... | OK |
| logo_emulador_v2.png | 2025-12-21 10:35:00 | Edición: Añadir estrella | PixARR Design | 346d2321... | OK |
| logo_emulador_v2.png | 2025-12-21 10:45:00 | Incidente: unauthorized_access | sim_agenteX | N/A | ⚠️ ALERTA |
```

#### Incidentes
```markdown
## 🚨 Incidentes de Seguridad

### Incidente #1
- **Tipo:** unauthorized_access
- **Archivo:** logo_emulador_v2.png
- **Actor Sospechoso:** sim_agenteX
- **Severidad:** HIGH
- **Descripción:** Acceso no autorizado detectado. Archivo movido a cuarentena.
- **Timestamp:** 2025-12-21T10:45:00Z
```

#### Alertas
```markdown
## 📧 Alertas Enviadas

### Alerta #1
- **Nivel:** HIGH
- **Mensaje:** ⚠️ ACCESO NO AUTORIZADO detectado en logo_emulador_v2.png
- **Destinatario:** tokraagcorp@gmail.com
- **Timestamp:** 2025-12-21T10:45:00Z
```

---

## Resumen de la Prueba

### Estadísticas Finales
```
📈 ESTADÍSTICAS FINALES:
   - Artefactos monitoreados: 1
   - Incidentes detectados: 1
   - Archivos en cuarentena: 1
   - Auditorías realizadas: 1
```

### Archivos Generados

```
TE-explico/
├── designs/
│   ├── active/
│   │   └── logo_emulador.png          ✅ Activo
│   └── quarantine/
│       └── logo_emulador_v2.png        🔒 En cuarentena
├── logs/
│   ├── audit_log.json                  📝 4 eventos
│   └── incident_log.json               🚨 1 incidente
└── reports/
    └── dashboard_20251221_104500.md    📄 Reporte final
```

---

## Criterios de Éxito

### ✅ Funcionalidad

- [x] Creación de artefactos con hash SHA-256
- [x] Inyección de metadata (PNG embedded)
- [x] Registro de modificaciones con versionado
- [x] Auditoría de integridad automática
- [x] Detección de accesos no autorizados
- [x] Cuarentena automática de archivos
- [x] Generación de reportes profesionales
- [x] Sistema de alertas multinivel

### ✅ Seguridad

- [x] Hashing criptográfico (SHA-256)
- [x] Logs inmutables (append-only)
- [x] Trazabilidad completa
- [x] Preservación de evidencia
- [x] Notificación al supervisor

### ✅ Rendimiento

- [x] Procesamiento en tiempo real
- [x] Lectura eficiente (bloques de 8KB)
- [x] Generación rápida de reportes (< 2s)

### ✅ Usabilidad

- [x] Mensajes claros y formatados
- [x] Reportes en Markdown legibles
- [x] API sencilla y documentada
- [x] Logs en formato JSON estándar

---

## Ejecución de la Prueba

### Comando
```bash
python scripts/run_simulation.py
```

### Salida Completa Esperada

```
======================================================================
🚀 INICIANDO SIMULACIÓN COMPLETA - PIXARR DESIGN EMULATOR
======================================================================

📌 PASO 1: Configuración del Agente
----------------------------------------------------------------------
✅ Agente PixARR Design activado
   Supervisor: Melampe001
   Workspace: /home/runner/work/TE-explico/TE-explico

📌 PASO 2: Generación de Artefacto Visual
----------------------------------------------------------------------
   🎨 Imagen creada: logo_emulador.png
✅ Artefacto creado: logo_emulador.png
   Hash: ea7a76d9914b5d3d...
   Creador: PixARR Design

📌 PASO 3: Edición y Cambios
----------------------------------------------------------------------
   🎨 Imagen creada: logo_emulador_v2.png
✅ Modificación registrada: logo_emulador_v2.png
   Versión: 1
   Modificador: PixARR Design
   Cambio: Añadir estrella y actualizar versión

📌 PASO 4: Auditoría de Integridad
----------------------------------------------------------------------
📊 AUDITORÍA DE INTEGRIDAD
   Archivos verificados: 2
   Anomalías detectadas: 0
   ✅ Todos los archivos pasaron la auditoría

📌 PASO 5: Detección de Incidentes (Simulada)
----------------------------------------------------------------------
🚨 ALERTA: Acceso no autorizado detectado
   Archivo: logo_emulador_v2.png
   Actor sospechoso: sim_agenteX
   Acción: Movido a cuarentena
   Supervisor notificado: Melampe001

⚠️ ALERTA [HIGH] enviada a tokraagcorp@gmail.com
   Mensaje: ⚠️ ACCESO NO AUTORIZADO detectado en logo_emulador_v2.png
   Timestamp: 2025-12-21T10:45:00Z

📌 PASO 6: Documentación y Cierre
----------------------------------------------------------------------
✅ Reporte generado: /path/to/reports/dashboard_20251221_104500.md

======================================================================
✅ SIMULACIÓN COMPLETADA EXITOSAMENTE
======================================================================

📄 Reporte generado: reports/dashboard_20251221_104500.md
📊 Logs disponibles en: logs/
🔒 Archivos en cuarentena: designs/quarantine/
📧 Supervisor notificado: tokraagcorp@gmail.com
======================================================================

📈 ESTADÍSTICAS FINALES:
   - Artefactos monitoreados: 1
   - Incidentes detectados: 1
   - Archivos en cuarentena: 1
   - Auditorías realizadas: 1

✅ Script ejecutado correctamente
```

---

## Validación Post-Prueba

### Verificar Archivos Generados

```bash
# Verificar estructura
ls -la designs/active/
ls -la designs/quarantine/
ls -la logs/
ls -la reports/

# Verificar contenido de logs
cat logs/audit_log.json | python -m json.tool
cat logs/incident_log.json | python -m json.tool

# Visualizar reporte
cat reports/dashboard_*.md
```

### Verificar Metadata

```bash
# Para archivos PNG
python -c "
from PIL import Image
img = Image.open('designs/active/logo_emulador.png')
print(img.info.get('PixARR_Metadata', 'No metadata'))
"

# Para archivos con .meta
cat designs/active/logo_emulador.png.meta
```

---

## Troubleshooting

### Error: "Agent must be activated before use"
**Solución:** Llamar `agent.activate()` antes de cualquier operación

### Error: "File not found"
**Solución:** Verificar que el archivo existe y la ruta es correcta

### Error: "Pillow not installed"
**Solución:** `pip install Pillow`

### Warning: "watchdog not installed"
**Solución:** Opcional. `pip install watchdog` si se requiere monitoreo en tiempo real

---

*Documentación de Prueba - PixARR Design System v1.0*
