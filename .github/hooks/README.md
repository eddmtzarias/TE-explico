# Git Hooks para OmniMaestro

Este directorio contiene templates de Git hooks que mejoran el flujo de trabajo del proyecto.

## 📋 Hooks Disponibles

### pre-commit.template

Hook que se ejecuta antes de cada commit para:
- ✅ Validar sintaxis de archivos Python
- ✅ Ejecutar linters (si están configurados)
- ✅ Prevenir commit de archivos sensibles (.env)
- ✅ Prevenir eliminación accidental de archivos críticos
- ✅ Advertir sobre archivos muy grandes
- ✅ Sugerir siguiente paso del roadmap

## 🚀 Instalación

### Instalación Manual

```bash
# Desde el directorio raíz del proyecto
cp .github/hooks/pre-commit.template .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Instalación Automática

```bash
# Ejecutar script de instalación (si existe)
./scripts/install_hooks.sh
```

### Desinstalación

```bash
# Remover el hook
rm .git/hooks/pre-commit
```

## 🔧 Personalización

Puedes editar el hook instalado en `.git/hooks/pre-commit` para ajustarlo a tus necesidades:

```bash
# Editar hook instalado
nano .git/hooks/pre-commit
# o
code .git/hooks/pre-commit
```

## ⚠️ Bypass del Hook

Si necesitas hacer un commit sin ejecutar el hook:

```bash
git commit --no-verify -m "tu mensaje"
```

**Nota:** Usa esto solo cuando sea realmente necesario.

## 🧪 Testing del Hook

Para probar el hook sin hacer un commit real:

```bash
# Hacer un commit de prueba
git add .
.git/hooks/pre-commit

# Si sale con código 0, el hook pasó
echo $?
```

## 📝 Notas

- Los hooks no se commitean automáticamente (están en `.git/hooks/`, que está en `.gitignore`)
- Cada desarrollador debe instalar los hooks manualmente
- Los templates están en control de versiones para facilitar la distribución

## 🔗 Recursos

- [Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Pre-commit Framework](https://pre-commit.com/) (alternativa más avanzada)

---

**Última actualización:** 2025-12-21  
**Mantenedor:** @eddmtzarias
