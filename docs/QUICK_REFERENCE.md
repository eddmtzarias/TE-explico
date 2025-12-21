# 📖 Quick Reference - OmniMaestro Guide System

> **Referencia rápida de comandos y características del sistema de guía**

---

## 🚀 Comandos Principales

### Ver Estado del Proyecto
```bash
python scripts/project_guide.py status
```
Muestra:
- Progreso general
- Pasos completados
- Próximo paso recomendado
- Advertencias activas
- Bloqueadores

### Ver Siguiente Paso
```bash
# Siguiente paso recomendado
python scripts/project_guide.py next

# Ver paso específico
python scripts/project_guide.py next --step 7
```

### Validar Paso Completado
```bash
# Validar próximo paso
python scripts/project_guide.py validate

# Validar paso específico
python scripts/project_guide.py validate --step 5
```

### Ver Roadmap Completo
```bash
python scripts/project_guide.py roadmap
```

### Cambiar Plataforma Objetivo
```bash
# Ver plataforma actual
python scripts/project_guide.py platform

# Cambiar a desktop
python scripts/project_guide.py platform desktop

# Cambiar a mobile
python scripts/project_guide.py platform mobile

# Cambiar a web
python scripts/project_guide.py platform web
```

### Explicación Profunda
```bash
python scripts/project_guide.py explain 7
```
Muestra:
- Por qué es necesario
- Qué pasa si se salta
- Relación con otros pasos
- Recursos adicionales

---

## 📁 Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| `PROJECT_ROADMAP.md` | Roadmap completo con 50 pasos |
| `PROJECT_DASHBOARD.md` | Dashboard de progreso auto-actualizado |
| `.project_state.json` | Estado persistente del proyecto |
| `docs/PLATFORM_GUIDES/DESKTOP_TAURI.md` | Guía desarrollo Desktop |
| `docs/PLATFORM_GUIDES/MOBILE_FLUTTER.md` | Guía desarrollo Mobile |
| `docs/PLATFORM_GUIDES/WEB_PWA.md` | Guía desarrollo Web |
| `docs/TROUBLESHOOTING.md` | Solución problemas comunes |
| `scripts/project_guide.py` | Script de guía interactivo |
| `.github/hooks/pre-commit.template` | Template de git hook |

---

## 🎨 Niveles de Criticidad

| Símbolo | Nivel | Descripción |
|---------|-------|-------------|
| 🚨 | CRÍTICO | No puede saltarse sin consecuencias graves |
| 🟡 | IMPORTANTE | Recomendado completar, saltear crea deuda técnica |
| 🔵 | OPCIONAL | Mejora la experiencia pero no es obligatorio |

---

## 📊 Fases del Proyecto

| # | Fase | Pasos | Descripción |
|---|------|-------|-------------|
| 0 | Setup Inicial | 1-6 | Configuración básica del proyecto |
| 1 | Core Backend | 7-10 | Sistema AI y OCR |
| 2 | Desktop | 11-18 | Implementación con Tauri |
| 3 | Mobile | 19-26 | Implementación con Flutter |
| 4 | Web | 27-32 | Implementación PWA |
| 5 | Integraciones | 33-36 | Features avanzadas |
| 6 | Testing | 37-43 | QA completo |
| 7 | Deployment | 44-50 | Release y producción |

---

## ⚡ Atajos y Tips

### Workflow Recomendado
```bash
# 1. Ver estado
python scripts/project_guide.py status

# 2. Ver siguiente paso
python scripts/project_guide.py next

# 3. Trabajar en el paso...

# 4. Validar completado
python scripts/project_guide.py validate

# 5. Repetir
```

### Instalar Git Hooks
```bash
./scripts/install_hooks.sh
```

### Actualizar Manualmente el Estado
```bash
# Editar .project_state.json
nano .project_state.json

# O usar Python
python3 -c "
import json
state = json.load(open('.project_state.json'))
state['completed_steps'].append(5)
json.dump(state, open('.project_state.json', 'w'), indent=2)
"
```

### Bypass de Validaciones (usar con cuidado)
```bash
# Marcar paso como completado sin validar
# Editar manualmente .project_state.json

# Bypass git hook
git commit --no-verify -m "mensaje"
```

---

## 🔧 Troubleshooting Rápido

### Script no funciona
```bash
# Dar permisos
chmod +x scripts/project_guide.py

# Usar Python 3
python3 scripts/project_guide.py status
```

### Estado corrupto
```bash
# Regenerar
rm .project_state.json
python3 scripts/project_guide.py status
```

### Dependencias Python
```bash
# El script no requiere dependencias externas
# Solo usa stdlib de Python 3
```

---

## 📚 Recursos Adicionales

### Documentación Completa
- [PROJECT_ROADMAP.md](../PROJECT_ROADMAP.md) - Roadmap detallado
- [PROJECT_DASHBOARD.md](../PROJECT_DASHBOARD.md) - Dashboard de progreso
- [EVOLUTION_LOG.md](../EVOLUTION_LOG.md) - Sistema de mejora continua

### Guías por Plataforma
- [Desktop (Tauri)](PLATFORM_GUIDES/DESKTOP_TAURI.md)
- [Mobile (Flutter)](PLATFORM_GUIDES/MOBILE_FLUTTER.md)
- [Web (PWA)](PLATFORM_GUIDES/WEB_PWA.md)

### Ayuda
- [Troubleshooting](TROUBLESHOOTING.md)
- [Git Hooks README](.github/hooks/README.md)

---

## 🎯 Ejemplos de Uso

### Flujo Completo Desktop MVP

```bash
# 1. Verificar estado inicial
$ python scripts/project_guide.py status
# Progreso: 33%, Fase: Setup, Próximo: Paso 5

# 2. Ver detalles del paso 5
$ python scripts/project_guide.py next
# Configurar variables de entorno - 15 min - CRÍTICO

# 3. Crear .env
$ nano .env  # Añadir API keys

# 4. Validar
$ python scripts/project_guide.py validate --step 5
# ✅ Validación pasó

# 5. Continuar con siguiente paso
$ python scripts/project_guide.py next
# Ahora muestra paso 6 o 7

# 6. Ver roadmap actualizado
$ python scripts/project_guide.py roadmap
# Progreso actualizado: 40%
```

### Cambiar de Plataforma

```bash
# Empezar con Desktop
$ python scripts/project_guide.py platform desktop

# Trabajar hasta Desktop MVP...

# Cambiar a Mobile
$ python scripts/project_guide.py platform mobile
$ python scripts/project_guide.py next
# Ahora muestra pasos de Flutter
```

### Investigar Paso Crítico

```bash
# ¿Por qué necesito Tesseract?
$ python scripts/project_guide.py explain 7

# Muestra:
# - Objetivo del paso
# - Por qué es necesario
# - Qué pasa si se salta
# - Pasos dependientes
# - Recursos
```

---

**Última actualización:** 2025-12-21  
**Mantenedor:** @eddmtzarias  
**Versión:** 1.0.0

---

💡 **Tip:** Guarda este archivo como referencia rápida mientras desarrollas.
