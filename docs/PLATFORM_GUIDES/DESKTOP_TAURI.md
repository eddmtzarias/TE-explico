# 🖥️ Desktop Development Guide - Tauri

> **Guía completa para desarrollar OmniMaestro con Tauri**  
> Última actualización: 2025-12-21

---

## 📋 Tabla de Contenidos

1. [Pre-requisitos](#pre-requisitos)
2. [Instalación de Dependencias](#instalación-de-dependencias)
3. [Configuración del Proyecto](#configuración-del-proyecto)
4. [Desarrollo](#desarrollo)
5. [Testing](#testing)
6. [Build y Distribución](#build-y-distribución)
7. [Problemas Comunes](#problemas-comunes)
8. [Checklist de Features](#checklist-de-features)

---

## 📦 Pre-requisitos

### Versiones Requeridas

| Herramienta | Versión Mínima | Recomendada | Validación |
|-------------|----------------|-------------|------------|
| Rust | 1.70.0 | 1.75+ | `rustc --version` |
| Cargo | 1.70.0 | 1.75+ | `cargo --version` |
| Node.js | 18.0.0 | 20.x LTS | `node --version` |
| npm | 9.0.0 | 10.x | `npm --version` |

### Dependencias del Sistema

#### Windows
```powershell
# Instalar Microsoft Visual Studio C++ Build Tools
# Descargar de: https://visualstudio.microsoft.com/downloads/

# Instalar WebView2 (usualmente ya instalado en Windows 10+)
# Descargar de: https://developer.microsoft.com/microsoft-edge/webview2/
```

#### macOS
```bash
# Instalar Xcode Command Line Tools
xcode-select --install

# Verificar instalación
xcode-select -p
```

#### Linux (Ubuntu/Debian)
```bash
# Instalar dependencias del sistema
sudo apt update
sudo apt install libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    wget \
    file \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev

# Verificar instalación
dpkg -l | grep libwebkit2gtk
```

#### Linux (Fedora)
```bash
sudo dnf install webkit2gtk3-devel \
    openssl-devel \
    curl \
    wget \
    file \
    gtk3-devel \
    libappindicator-gtk3-devel \
    librsvg2-devel
```

---

## 🚀 Instalación de Dependencias

### 1. Instalar Rust

```bash
# Unix-like (Linux/macOS)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Windows (PowerShell)
# Descargar e instalar desde: https://rustup.rs/

# Después de instalar, reiniciar terminal y verificar
rustc --version
cargo --version
```

### 2. Configurar Rust

```bash
# Actualizar Rust a la última versión
rustup update

# Añadir target para compilación cruzada (opcional)
# Para Windows desde Linux/macOS
rustup target add x86_64-pc-windows-gnu

# Para macOS desde Linux/Windows
rustup target add x86_64-apple-darwin

# Configurar toolchain por defecto
rustup default stable
```

### 3. Instalar Tauri CLI

```bash
# Opción 1: Via Cargo (recomendado)
cargo install tauri-cli

# Opción 2: Via npm (alternativa)
npm install -g @tauri-apps/cli

# Verificar instalación
cargo tauri --version
```

### 4. Validar Instalación Completa

```bash
# Script de validación completo
echo "🔍 Validando instalación de Tauri..."

echo "✓ Rust:"
rustc --version

echo "✓ Cargo:"
cargo --version

echo "✓ Node.js:"
node --version

echo "✓ npm:"
npm --version

echo "✓ Tauri CLI:"
cargo tauri --version

echo "✅ ¡Todas las dependencias instaladas correctamente!"
```

---

## ⚙️ Configuración del Proyecto

### 1. Inicializar Proyecto Tauri

```bash
# Opción 1: Crear nuevo proyecto Tauri desde cero
npm create tauri-app

# Seguir el wizard interactivo:
# - App name: omnimaestro
# - Window title: OmniMaestro
# - UI template: react-ts (o vue-ts)
# - Package manager: npm

# Opción 2: Añadir Tauri a proyecto existente
npm install --save-dev @tauri-apps/cli
npm install @tauri-apps/api
npx tauri init
```

### 2. Estructura del Proyecto

```
omnimaestro/
├── src/                    # Frontend (React/Vue)
│   ├── App.tsx
│   ├── main.tsx
│   └── components/
├── src-tauri/             # Backend (Rust)
│   ├── Cargo.toml         # Dependencias Rust
│   ├── tauri.conf.json    # Configuración Tauri
│   ├── src/
│   │   ├── main.rs        # Entry point
│   │   └── commands.rs    # Comandos Tauri
│   └── icons/             # Iconos de la app
├── package.json           # Dependencias Node
└── vite.config.ts         # Configuración Vite
```

### 3. Configurar Permisos (tauri.conf.json)

```json
{
  "tauri": {
    "allowlist": {
      "all": false,
      "shell": {
        "all": false,
        "open": true
      },
      "dialog": {
        "all": true,
        "open": true,
        "save": true
      },
      "fs": {
        "all": false,
        "readFile": true,
        "writeFile": true,
        "readDir": true,
        "scope": ["$APPDATA/*", "$RESOURCE/*"]
      },
      "clipboard": {
        "all": true,
        "readText": true,
        "writeText": true
      },
      "notification": {
        "all": true
      },
      "globalShortcut": {
        "all": true
      },
      "window": {
        "all": true,
        "create": true,
        "center": true,
        "requestUserAttention": true,
        "setResizable": true,
        "setTitle": true,
        "maximize": true,
        "unmaximize": true,
        "minimize": true,
        "unminimize": true,
        "show": true,
        "hide": true,
        "close": true,
        "setDecorations": true,
        "setAlwaysOnTop": true,
        "setSize": true,
        "setMinSize": true,
        "setMaxSize": true,
        "setPosition": true,
        "setFullscreen": true,
        "setFocus": true,
        "setIcon": true,
        "setSkipTaskbar": true,
        "startDragging": true,
        "print": true
      }
    },
    "windows": [
      {
        "title": "OmniMaestro",
        "width": 1200,
        "height": 800,
        "resizable": true,
        "fullscreen": false,
        "transparent": false,
        "decorations": true,
        "alwaysOnTop": false
      }
    ],
    "security": {
      "csp": "default-src 'self'; img-src 'self' asset: https://asset.localhost"
    }
  }
}
```

### 4. Configurar Variables de Entorno

```bash
# Crear archivo .env en raíz del proyecto
cat > .env << 'EOF'
# API Keys
VITE_OPENAI_API_KEY=your_openai_api_key_here
VITE_ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Backend URL
VITE_API_BASE_URL=http://localhost:8000

# Feature Flags
VITE_ENABLE_OCR=true
VITE_ENABLE_TELEMETRY=false

# Debug
VITE_DEBUG_MODE=false
EOF

# Añadir a .gitignore
echo ".env" >> .gitignore
```

---

## 💻 Desarrollo

### Comandos de Desarrollo

```bash
# Iniciar modo desarrollo (hot reload)
npm run tauri dev

# O usando cargo directamente
cargo tauri dev

# Modo desarrollo con logs detallados
RUST_LOG=debug npm run tauri dev
```

### Implementar Captura de Pantalla

#### Backend (Rust) - src-tauri/src/screenshot.rs

```rust
use screenshots::Screen;
use tauri::command;

#[command]
pub fn capture_screenshot() -> Result<String, String> {
    let screens = Screen::all().map_err(|e| e.to_string())?;
    
    if let Some(screen) = screens.first() {
        let image = screen.capture().map_err(|e| e.to_string())?;
        
        // Guardar en directorio temporal
        let temp_dir = std::env::temp_dir();
        let file_path = temp_dir.join("omnimaestro_screenshot.png");
        
        image.save(&file_path).map_err(|e| e.to_string())?;
        
        Ok(file_path.to_string_lossy().to_string())
    } else {
        Err("No screens found".to_string())
    }
}
```

#### Añadir dependencia en Cargo.toml

```toml
[dependencies]
tauri = { version = "1.5", features = ["shell-open"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
screenshots = "0.7"
```

#### Frontend (React/TypeScript) - src/hooks/useScreenshot.ts

```typescript
import { invoke } from '@tauri-apps/api/tauri';

export function useScreenshot() {
  const captureScreen = async (): Promise<string> => {
    try {
      const path = await invoke<string>('capture_screenshot');
      return path;
    } catch (error) {
      console.error('Error capturing screenshot:', error);
      throw error;
    }
  };

  return { captureScreen };
}
```

### Implementar Ventana Overlay

```typescript
// src/utils/overlay.ts
import { appWindow, WebviewWindow } from '@tauri-apps/api/window';

export async function createOverlay() {
  const overlay = new WebviewWindow('overlay', {
    url: '/overlay',
    width: 400,
    height: 300,
    decorations: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
  });

  return overlay;
}
```

### Atajos de Teclado Globales

```rust
// src-tauri/src/main.rs
use tauri::{GlobalShortcutManager, Manager};

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let handle = app.handle();
            let mut shortcut_manager = app.global_shortcut_manager();
            
            // Captura de pantalla: Ctrl+Shift+S
            shortcut_manager.register("Ctrl+Shift+S", move || {
                println!("Screenshot shortcut triggered!");
                // Emitir evento para capturar screenshot
            })?;
            
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

## 🧪 Testing

### Tests Unitarios (Rust)

```rust
// src-tauri/src/screenshot.rs
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_capture_screenshot() {
        let result = capture_screenshot();
        assert!(result.is_ok());
    }
}
```

```bash
# Ejecutar tests de Rust
cd src-tauri
cargo test

# Con cobertura
cargo install cargo-tarpaulin
cargo tarpaulin --out Html
```

### Tests de Integración (Frontend)

```typescript
// src/__tests__/screenshot.test.ts
import { describe, it, expect, vi } from 'vitest';
import { useScreenshot } from '../hooks/useScreenshot';

describe('useScreenshot', () => {
  it('should capture screenshot successfully', async () => {
    const { captureScreen } = useScreenshot();
    const path = await captureScreen();
    expect(path).toBeDefined();
  });
});
```

```bash
# Ejecutar tests de frontend
npm run test

# Con cobertura
npm run test:coverage
```

---

## 📦 Build y Distribución

### Build de Desarrollo

```bash
# Build completo (debug)
npm run tauri build -- --debug
```

### Build de Producción

```bash
# Build optimizado
npm run tauri build

# Build para plataforma específica
npm run tauri build -- --target x86_64-pc-windows-msvc  # Windows
npm run tauri build -- --target x86_64-apple-darwin     # macOS
npm run tauri build -- --target x86_64-unknown-linux-gnu # Linux
```

### Ubicación de Binarios

```bash
# Windows
src-tauri/target/release/omnimaestro.exe
src-tauri/target/release/bundle/msi/omnimaestro_1.0.0_x64.msi
src-tauri/target/release/bundle/nsis/omnimaestro_1.0.0_x64-setup.exe

# macOS
src-tauri/target/release/omnimaestro
src-tauri/target/release/bundle/dmg/omnimaestro_1.0.0_x64.dmg
src-tauri/target/release/bundle/macos/omnimaestro.app

# Linux
src-tauri/target/release/omnimaestro
src-tauri/target/release/bundle/deb/omnimaestro_1.0.0_amd64.deb
src-tauri/target/release/bundle/appimage/omnimaestro_1.0.0_amd64.AppImage
```

### Code Signing (Producción)

#### Windows
```bash
# Necesitas un certificado de code signing
# Configurar en tauri.conf.json
{
  "tauri": {
    "bundle": {
      "windows": {
        "certificateThumbprint": "YOUR_THUMBPRINT",
        "timestampUrl": "http://timestamp.digicert.com"
      }
    }
  }
}
```

#### macOS
```bash
# Necesitas Apple Developer ID
# Configurar en tauri.conf.json
{
  "tauri": {
    "bundle": {
      "macOS": {
        "signingIdentity": "Developer ID Application: Your Name",
        "entitlements": "entitlements.plist"
      }
    }
  }
}

# Notarizar app
xcrun notarytool submit omnimaestro.app --apple-id "your@email.com" --password "app-specific-password" --wait
```

---

## 🔧 Problemas Comunes

### Error: "Rust not found"
```bash
# Solución: Asegurar que Rust está en PATH
source $HOME/.cargo/env  # Linux/macOS
# Reiniciar terminal en Windows
```

### Error: "WebView2 not found" (Windows)
```bash
# Solución: Instalar WebView2 Runtime
# Descargar de: https://developer.microsoft.com/microsoft-edge/webview2/
```

### Error: "libwebkit2gtk not found" (Linux)
```bash
# Solución: Instalar dependencias
sudo apt install libwebkit2gtk-4.0-dev
```

### App no se minimiza a system tray
```rust
// Solución: Implementar SystemTray
use tauri::{CustomMenuItem, SystemTray, SystemTrayMenu, SystemTrayEvent};

fn main() {
    let quit = CustomMenuItem::new("quit".to_string(), "Quit");
    let hide = CustomMenuItem::new("hide".to_string(), "Hide");
    let tray_menu = SystemTrayMenu::new()
        .add_item(hide)
        .add_item(quit);
    
    let system_tray = SystemTray::new().with_menu(tray_menu);
    
    tauri::Builder::default()
        .system_tray(system_tray)
        .on_system_tray_event(|app, event| match event {
            SystemTrayEvent::MenuItemClick { id, .. } => {
                match id.as_str() {
                    "quit" => std::process::exit(0),
                    "hide" => {
                        let window = app.get_window("main").unwrap();
                        window.hide().unwrap();
                    }
                    _ => {}
                }
            }
            _ => {}
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Performance Issues
```rust
// Solución: Optimizar build en Cargo.toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
```

---

## ✅ Checklist de Features Desktop

### Funcionalidades Core
- [ ] Captura de pantalla (hotkey global)
- [ ] Análisis de imagen con OCR
- [ ] Integración con IA para explicaciones
- [ ] Modo overlay flotante
- [ ] Sistema de notificaciones

### UI/UX
- [ ] Ventana principal responsive
- [ ] Dark mode / Light mode
- [ ] Configuración persistente
- [ ] Historial de capturas
- [ ] Búsqueda en historial

### Sistema
- [ ] Auto-start en inicio de sistema
- [ ] System tray icon
- [ ] Atajos de teclado configurables
- [ ] Multi-monitor support
- [ ] Actualización automática

### Seguridad
- [ ] Almacenamiento seguro de API keys
- [ ] Encriptación de datos sensibles
- [ ] Permisos mínimos necesarios
- [ ] Validación de inputs

### Performance
- [ ] Tiempo de captura < 200ms
- [ ] Uso de memoria < 200MB
- [ ] Inicio de app < 3 segundos
- [ ] Respuesta UI < 100ms

---

## 📚 Recursos Adicionales

- [Tauri Documentation](https://tauri.app/)
- [Tauri Examples](https://github.com/tauri-apps/tauri/tree/dev/examples)
- [Rust Book](https://doc.rust-lang.org/book/)
- [React TypeScript](https://react-typescript-cheatsheet.netlify.app/)

---

**Última actualización:** 2025-12-21  
**Mantenedor:** @eddmtzarias  
**Versión de guía:** 1.0.0
