# 🔧 Troubleshooting Guide - OmniMaestro

> **Soluciones a problemas comunes en el desarrollo de OmniMaestro**  
> Última actualización: 2025-12-21

---

## 📋 Tabla de Contenidos

1. [Problemas de Setup General](#problemas-de-setup-general)
2. [Problemas de Desktop (Tauri)](#problemas-de-desktop-tauri)
3. [Problemas de Mobile (Flutter)](#problemas-de-mobile-flutter)
4. [Problemas de Web (PWA)](#problemas-de-web-pwa)
5. [Problemas de Dependencias](#problemas-de-dependencias)
6. [Problemas de Build](#problemas-de-build)
7. [Problemas de Testing](#problemas-de-testing)

---

## 🚀 Problemas de Setup General

### El sistema de guía no funciona

**Síntoma:**
```bash
python scripts/project_guide.py status
# Error: No such file or directory
```

**Solución:**
```bash
# Asegurar que estás en el directorio raíz del proyecto
cd /path/to/TE-explico

# Verificar que el script existe
ls -la scripts/project_guide.py

# Dar permisos de ejecución
chmod +x scripts/project_guide.py

# Ejecutar con Python 3
python3 scripts/project_guide.py status
```

---

### .project_state.json corrupto

**Síntoma:**
```
json.decoder.JSONDecodeError: Expecting value
```

**Solución:**
```bash
# Hacer backup del archivo corrupto
cp .project_state.json .project_state.json.backup

# Regenerar estado inicial
rm .project_state.json
python3 scripts/project_guide.py status

# El script recreará el archivo automáticamente
```

---

### Variables de entorno no se cargan

**Síntoma:**
```
KeyError: 'API_KEY'
```

**Solución:**
```bash
# Crear archivo .env en la raíz del proyecto
cat > .env << 'EOF'
# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Configuration
API_BASE_URL=http://localhost:8000
DEBUG_MODE=false
EOF

# Asegurar que .env está en .gitignore
echo ".env" >> .gitignore

# Verificar que el archivo existe
cat .env
```

---

## 🖥️ Problemas de Desktop (Tauri)

### Rust no encontrado después de instalación

**Síntoma:**
```bash
rustc: command not found
```

**Solución:**
```bash
# Recargar configuración de shell
source $HOME/.cargo/env  # Linux/macOS

# En Windows, reiniciar terminal o ejecutar:
# set PATH=%PATH%;%USERPROFILE%\.cargo\bin

# Verificar instalación
rustc --version
cargo --version
```

---

### WebView2 no encontrado (Windows)

**Síntoma:**
```
Error: WebView2 runtime not found
```

**Solución:**
1. Descargar WebView2 Runtime de: https://developer.microsoft.com/microsoft-edge/webview2/
2. Instalar el runtime
3. Reiniciar terminal
4. Ejecutar `npm run tauri dev` nuevamente

---

### libwebkit2gtk no encontrado (Linux)

**Síntoma:**
```
error: failed to run custom build command for `webkit2gtk-sys`
```

**Solución:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    wget \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev

# Fedora
sudo dnf install webkit2gtk3-devel

# Verificar instalación
dpkg -l | grep libwebkit2gtk  # Debian/Ubuntu
rpm -qa | grep webkit2gtk     # Fedora
```

---

### Tauri build muy lento

**Síntoma:**
El build tarda más de 10 minutos

**Solución:**
```toml
# Añadir a src-tauri/Cargo.toml
[profile.dev]
opt-level = 1  # Optimización básica en desarrollo

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

```bash
# Limpiar caché y rebuill
cd src-tauri
cargo clean
cd ..
npm run tauri build
```

---

## 📱 Problemas de Mobile (Flutter)

### Flutter doctor muestra errores

**Síntoma:**
```bash
flutter doctor
# [✗] Android toolchain - develop for Android devices
```

**Solución:**
```bash
# Aceptar licencias de Android
flutter doctor --android-licenses

# Actualizar Flutter
flutter upgrade

# Ejecutar doctor nuevamente
flutter doctor -v
```

---

### Emulador Android no inicia

**Síntoma:**
```
Error: No connected devices
```

**Solución:**
```bash
# Listar emuladores disponibles
flutter emulators

# Crear nuevo emulador si no existe
flutter emulators --create --name pixel_7

# Iniciar emulador
flutter emulators --launch pixel_7

# Verificar dispositivos
flutter devices
```

---

### Error de permisos en Android

**Síntoma:**
```
SecurityException: Permission denied
```

**Solución:**
1. Verificar que los permisos estén en `AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.INTERNET" />
```

2. Solicitar permisos en runtime:
```dart
import 'package:permission_handler/permission_handler.dart';

await Permission.camera.request();
```

3. En emulador: Settings > Apps > OmniMaestro > Permissions > Enable Camera

---

### CocoaPods error (iOS)

**Síntoma:**
```
CocoaPods not installed or not in valid state
```

**Solución:**
```bash
# Reinstalar CocoaPods
sudo gem install cocoapods

# Limpiar pods
cd ios
rm -rf Pods Podfile.lock
pod deintegrate
pod install
cd ..

# Rebuild
flutter clean
flutter pub get
flutter run
```

---

## 🌐 Problemas de Web (PWA)

### Service Worker no se registra

**Síntoma:**
```
Failed to register service worker
```

**Solución:**
```javascript
// Verificar que el SW existe
ls public/sw.js

// Asegurar que estás en HTTPS o localhost
// Service Workers solo funcionan en contextos seguros

// Verificar configuración en next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development', // ⚠️ Revisar esto
});
```

---

### PWA no es instalable

**Síntoma:**
El navegador no muestra el botón "Instalar"

**Solución:**
```bash
# Checklist de requisitos PWA:
1. manifest.json válido ✓
2. Service Worker registrado ✓
3. HTTPS habilitado (o localhost) ✓
4. Iconos de al menos 192x192 y 512x512 ✓
5. start_url válido ✓
6. display: standalone o fullscreen ✓

# Verificar con Lighthouse
# Chrome DevTools > Lighthouse > PWA
```

---

### Tesseract.js muy lento

**Síntoma:**
OCR tarda más de 10 segundos

**Solución:**
```typescript
// Usar Web Worker
import { createWorker } from 'tesseract.js';

const worker = await createWorker('eng', 1, {
  workerPath: '/worker.js',
  corePath: '/tesseract-core.wasm.js',
  // Optimizaciones
  tessedit_pageseg_mode: '6', // Assume uniform block of text
  tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ',
});

// Procesar imagen reducida
const canvas = document.createElement('canvas');
canvas.width = Math.min(image.width, 1920);
canvas.height = Math.min(image.height, 1080);
// ... reducir resolución antes de OCR
```

---

## 📦 Problemas de Dependencias

### npm install falla

**Síntoma:**
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Solución:**
```bash
# Opción 1: Usar --legacy-peer-deps
npm install --legacy-peer-deps

# Opción 2: Usar --force
npm install --force

# Opción 3: Limpiar caché
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Opción 4: Actualizar npm
npm install -g npm@latest
```

---

### pip install falla

**Síntoma:**
```
ERROR: Could not find a version that satisfies the requirement
```

**Solución:**
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Usar requirements.txt si existe
pip install -r requirements.txt

# Instalar paquete específico
pip install --upgrade <package-name>

# Si persiste, crear virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate  # Windows
pip install <package-name>
```

---

## 🏗️ Problemas de Build

### Build falla con error de memoria

**Síntoma:**
```
FATAL ERROR: Ineffective mark-compacts near heap limit
```

**Solución:**
```bash
# Aumentar límite de memoria de Node.js
export NODE_OPTIONS="--max-old-space-size=4096"

# En Windows
set NODE_OPTIONS=--max-old-space-size=4096

# Build nuevamente
npm run build
```

---

### Build de producción roto pero dev funciona

**Síntoma:**
```
npm run build  # ✗ Falla
npm run dev    # ✓ Funciona
```

**Solución:**
```bash
# Verificar variables de entorno
# Crear .env.production
cat > .env.production << 'EOF'
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.production.com
EOF

# Verificar importaciones dinámicas
# Asegurar que no hay require() dinámicos

# Verificar bundle size
npm run build -- --analyze

# Verificar TypeScript
npm run type-check
```

---

## 🧪 Problemas de Testing

### Tests fallan con "module not found"

**Síntoma:**
```
Cannot find module '@/components/Button'
```

**Solución:**
```javascript
// Configurar jest.config.js o vitest.config.ts
export default {
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  // ...
}
```

---

### Tests de integración muy lentos

**Síntoma:**
Tests tardan más de 1 minuto

**Solución:**
```typescript
// Usar test.concurrent para paralelizar
import { test } from 'vitest';

test.concurrent('test 1', async () => { /* ... */ });
test.concurrent('test 2', async () => { /* ... */ });

// O configurar workers en jest.config.js
module.exports = {
  maxWorkers: 4, // Número de workers paralelos
};
```

---

## 🔍 Diagnóstico General

### Script de diagnóstico completo

```bash
#!/bin/bash
# diagnostics.sh - Ejecutar para verificar el entorno

echo "🔍 Diagnóstico del Entorno OmniMaestro"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo -e "\n📦 Versiones de Herramientas:"
echo "Node.js: $(node --version 2>/dev/null || echo '❌ No instalado')"
echo "npm: $(npm --version 2>/dev/null || echo '❌ No instalado')"
echo "Python: $(python3 --version 2>/dev/null || echo '❌ No instalado')"
echo "Rust: $(rustc --version 2>/dev/null || echo '❌ No instalado')"
echo "Flutter: $(flutter --version 2>/dev/null | head -1 || echo '❌ No instalado')"

echo -e "\n📁 Estructura del Proyecto:"
test -f .project_state.json && echo "✅ .project_state.json" || echo "❌ .project_state.json"
test -f PROJECT_ROADMAP.md && echo "✅ PROJECT_ROADMAP.md" || echo "❌ PROJECT_ROADMAP.md"
test -f .env && echo "✅ .env" || echo "⚠️  .env (crear si necesario)"
test -d scripts && echo "✅ scripts/" || echo "❌ scripts/"
test -d docs/PLATFORM_GUIDES && echo "✅ docs/PLATFORM_GUIDES/" || echo "❌ docs/PLATFORM_GUIDES/"

echo -e "\n🔧 Sistema de Guía:"
python3 scripts/project_guide.py status 2>/dev/null && echo "✅ Funcionando" || echo "❌ Error"

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Diagnóstico completado"
```

---

## 📞 Obtener Ayuda

Si ninguna solución funciona:

1. **Revisar logs completos:**
   ```bash
   # Guardar logs en archivo
   comando_que_falla 2>&1 | tee error.log
   ```

2. **Buscar en Issues del proyecto:**
   - GitHub: https://github.com/eddmtzarias/TE-explico/issues

3. **Consultar documentación oficial:**
   - Tauri: https://tauri.app/
   - Flutter: https://flutter.dev/
   - Next.js: https://nextjs.org/

4. **Crear nuevo Issue:**
   - Incluir: OS, versiones, logs completos, pasos para reproducir

---

**Última actualización:** 2025-12-21  
**Mantenedor:** @eddmtzarias  
**Versión de guía:** 1.0.0
