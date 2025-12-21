# 📱 Mobile Development Guide - Flutter

> **Guía completa para desarrollar OmniMaestro con Flutter**  
> Última actualización: 2025-12-21

---

## 📋 Tabla de Contenidos

1. [Pre-requisitos](#pre-requisitos)
2. [Instalación de Flutter](#instalación-de-flutter)
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
| Flutter SDK | 3.10.0 | 3.16+ | `flutter --version` |
| Dart | 3.0.0 | 3.2+ | `dart --version` |
| Android Studio | 2022.1+ | Latest | Verificar en About |
| Xcode (macOS) | 14.0+ | Latest | `xcode-select -p` |
| JDK | 11 | 17 | `java --version` |

### Espacio en Disco
- Flutter SDK: ~2.5 GB
- Android Studio: ~5 GB
- Android SDK & Emulator: ~10 GB
- Xcode (macOS): ~15 GB

---

## 🚀 Instalación de Flutter

### Windows

```powershell
# Descargar Flutter SDK
# https://docs.flutter.dev/get-started/install/windows

# Descomprimir en C:\src\flutter
# Añadir a PATH: C:\src\flutter\bin

# Verificar instalación
flutter doctor

# Instalar dependencias faltantes
flutter doctor --android-licenses
```

### macOS

```bash
# Opción 1: Con Git
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"

# Opción 2: Con Homebrew
brew install flutter

# Verificar instalación
flutter doctor

# Instalar Xcode
xcode-select --install
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch

# Aceptar licencias
sudo xcodebuild -license
```

### Linux (Ubuntu/Debian)

```bash
# Instalar dependencias del sistema
sudo apt-get update -y
sudo apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    zip \
    libglu1-mesa \
    openjdk-11-jdk

# Descargar e instalar Flutter
cd ~/development
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.16.0-stable.tar.xz
tar xf flutter_linux_3.16.0-stable.tar.xz

# Añadir a PATH (~/.bashrc o ~/.zshrc)
export PATH="$PATH:$HOME/development/flutter/bin"
source ~/.bashrc

# Verificar instalación
flutter doctor
```

---

## 🔧 Configuración de Android

### Instalar Android Studio

1. Descargar de: https://developer.android.com/studio
2. Instalar Android SDK
3. Instalar Android Virtual Device (AVD)

```bash
# Configurar Android SDK
flutter config --android-sdk /path/to/android/sdk

# Aceptar licencias
flutter doctor --android-licenses
```

### Crear Emulador Android

```bash
# Listar AVDs disponibles
flutter emulators

# Crear nuevo emulador
flutter emulators --create --name pixel_7

# Iniciar emulador
flutter emulators --launch pixel_7

# Verificar dispositivos
flutter devices
```

---

## 🍎 Configuración de iOS (solo macOS)

### Configurar Xcode

```bash
# Instalar CocoaPods
sudo gem install cocoapods

# Verificar instalación
pod --version

# Configurar simulador
open -a Simulator

# Listar simuladores disponibles
xcrun simctl list
```

---

## ⚙️ Configuración del Proyecto

### 1. Crear Proyecto Flutter

```bash
# Crear nuevo proyecto
flutter create omnimaestro
cd omnimaestro

# O con configuración específica
flutter create \
    --org com.omnimaestro \
    --description "AI Learning Companion" \
    --platforms android,ios \
    omnimaestro
```

### 2. Estructura del Proyecto

```
omnimaestro/
├── android/               # Código nativo Android
├── ios/                   # Código nativo iOS
├── lib/                   # Código Dart
│   ├── main.dart         # Entry point
│   ├── screens/          # Pantallas
│   ├── widgets/          # Componentes
│   ├── services/         # Servicios (API, etc)
│   ├── models/           # Modelos de datos
│   └── utils/            # Utilidades
├── test/                 # Tests
├── pubspec.yaml          # Dependencias
└── analysis_options.yaml # Linting
```

### 3. Configurar Dependencias (pubspec.yaml)

```yaml
name: omnimaestro
description: AI Learning Companion
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # UI
  cupertino_icons: ^1.0.2
  
  # Camera & Screenshots
  camera: ^0.10.5
  image_picker: ^1.0.4
  screenshot: ^2.1.0
  
  # OCR
  google_ml_kit: ^0.16.0
  
  # HTTP & API
  http: ^1.1.0
  dio: ^5.4.0
  
  # State Management
  provider: ^6.1.1
  # o riverpod: ^2.4.0
  
  # Storage
  shared_preferences: ^2.2.2
  path_provider: ^2.1.1
  sqflite: ^2.3.0
  
  # Permissions
  permission_handler: ^11.1.0
  
  # Utils
  intl: ^0.18.1
  uuid: ^4.2.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
  mockito: ^5.4.4
```

```bash
# Instalar dependencias
flutter pub get
```

### 4. Configurar Permisos

#### Android (android/app/src/main/AndroidManifest.xml)

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Permisos -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" 
                     android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.ACCESS_MEDIA_LOCATION" />
    
    <!-- Features -->
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.camera.autofocus" android:required="false" />
    
    <application
        android:label="OmniMaestro"
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="true">
        <!-- Activities -->
    </application>
</manifest>
```

#### iOS (ios/Runner/Info.plist)

```xml
<dict>
    <!-- Camera Permission -->
    <key>NSCameraUsageDescription</key>
    <string>OmniMaestro needs camera access to analyze screenshots and provide explanations.</string>
    
    <!-- Photo Library Permission -->
    <key>NSPhotoLibraryUsageDescription</key>
    <string>OmniMaestro needs access to your photo library to analyze saved screenshots.</string>
    
    <!-- Microphone Permission -->
    <key>NSMicrophoneUsageDescription</key>
    <string>OmniMaestro needs microphone access for voice commands.</string>
    
    <!-- Other configurations -->
</dict>
```

### 5. Configurar Variables de Entorno

```dart
// lib/config/env.dart
class Env {
  static const String openAiApiKey = String.fromEnvironment(
    'OPENAI_API_KEY',
    defaultValue: '',
  );
  
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );
  
  static const bool enableTelemetry = bool.fromEnvironment(
    'ENABLE_TELEMETRY',
    defaultValue: false,
  );
}
```

```bash
# Ejecutar con variables
flutter run --dart-define=OPENAI_API_KEY=your_key_here
```

---

## 💻 Desarrollo

### Comandos de Desarrollo

```bash
# Modo desarrollo (hot reload)
flutter run

# Modo debug en dispositivo específico
flutter run -d <device_id>

# Modo release
flutter run --release

# Ver logs
flutter logs
```

### Implementar Captura de Pantalla

```dart
// lib/services/screenshot_service.dart
import 'package:camera/camera.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';

class ScreenshotService {
  final ImagePicker _picker = ImagePicker();
  
  Future<bool> requestPermissions() async {
    final status = await Permission.camera.request();
    return status.isGranted;
  }
  
  Future<String?> captureFromCamera() async {
    if (!await requestPermissions()) {
      throw Exception('Camera permission denied');
    }
    
    final XFile? image = await _picker.pickImage(
      source: ImageSource.camera,
      imageQuality: 85,
    );
    
    return image?.path;
  }
  
  Future<String?> pickFromGallery() async {
    final XFile? image = await _picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 85,
    );
    
    return image?.path;
  }
}
```

### Implementar OCR

```dart
// lib/services/ocr_service.dart
import 'dart:io';
import 'package:google_ml_kit/google_ml_kit.dart';

class OCRService {
  final TextRecognizer _textRecognizer = GoogleMlKit.vision.textRecognizer();
  
  Future<String> extractText(String imagePath) async {
    final inputImage = InputImage.fromFile(File(imagePath));
    final RecognizedText recognizedText = 
        await _textRecognizer.processImage(inputImage);
    
    return recognizedText.text;
  }
  
  void dispose() {
    _textRecognizer.close();
  }
}
```

### Implementar UI Principal

```dart
// lib/screens/home_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('OmniMaestro'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              // Navigate to settings
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton.icon(
              icon: const Icon(Icons.camera_alt),
              label: const Text('Capture Screenshot'),
              onPressed: _captureScreenshot,
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              icon: const Icon(Icons.photo_library),
              label: const Text('Pick from Gallery'),
              onPressed: _pickFromGallery,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _captureScreenshot,
        child: const Icon(Icons.camera),
      ),
    );
  }
  
  Future<void> _captureScreenshot() async {
    // Implementation
  }
  
  Future<void> _pickFromGallery() async {
    // Implementation
  }
}
```

---

## 🧪 Testing

### Tests Unitarios

```dart
// test/services/screenshot_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:omnimaestro/services/screenshot_service.dart';

void main() {
  group('ScreenshotService', () {
    late ScreenshotService service;
    
    setUp(() {
      service = ScreenshotService();
    });
    
    test('should request permissions', () async {
      // Test implementation
    });
  });
}
```

```bash
# Ejecutar tests
flutter test

# Con cobertura
flutter test --coverage
```

### Tests de Widget

```dart
// test/widgets/home_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:omnimaestro/screens/home_screen.dart';

void main() {
  testWidgets('HomeScreen has capture button', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: HomeScreen()),
    );
    
    expect(find.text('Capture Screenshot'), findsOneWidget);
  });
}
```

### Tests de Integración

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:omnimaestro/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  testWidgets('complete flow test', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();
    
    // Test complete user flow
  });
}
```

```bash
# Ejecutar tests de integración
flutter test integration_test/
```

---

## 📦 Build y Distribución

### Build Android (APK)

```bash
# Debug APK
flutter build apk --debug

# Release APK
flutter build apk --release

# Split APKs por arquitectura (reduce tamaño)
flutter build apk --split-per-abi

# Output:
# build/app/outputs/flutter-apk/app-release.apk
```

### Build Android (App Bundle)

```bash
# Para Google Play Store
flutter build appbundle --release

# Output:
# build/app/outputs/bundle/release/app-release.aab
```

### Build iOS

```bash
# Requiere macOS y Xcode
flutter build ios --release

# O abrir en Xcode
open ios/Runner.xcworkspace

# Archive en Xcode: Product > Archive
```

### Configurar Signing (Android)

```bash
# Generar keystore
keytool -genkey -v -keystore ~/omnimaestro-key.jks \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -alias omnimaestro

# Crear key.properties (android/key.properties)
cat > android/key.properties << 'EOF'
storePassword=<password>
keyPassword=<password>
keyAlias=omnimaestro
storeFile=<path-to-keystore>
EOF
```

```gradle
// android/app/build.gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

---

## 🔧 Problemas Comunes

### Error: "Flutter not found"
```bash
# Solución: Añadir Flutter a PATH
export PATH="$PATH:/path/to/flutter/bin"
```

### Error: "Android licenses not accepted"
```bash
# Solución
flutter doctor --android-licenses
```

### Error: "CocoaPods not installed" (iOS)
```bash
# Solución
sudo gem install cocoapods
cd ios && pod install
```

### Error: "Gradle build failed"
```bash
# Solución: Limpiar caché
flutter clean
flutter pub get
cd android && ./gradlew clean
cd .. && flutter build apk
```

### App crashea al abrir cámara
```dart
// Solución: Verificar permisos en runtime
import 'package:permission_handler/permission_handler.dart';

Future<void> requestCameraPermission() async {
  final status = await Permission.camera.status;
  if (!status.isGranted) {
    await Permission.camera.request();
  }
}
```

---

## ✅ Checklist de Features Móviles

### Funcionalidades Core
- [ ] Captura desde cámara
- [ ] Selección desde galería
- [ ] OCR con Google ML Kit
- [ ] Integración con IA
- [ ] Historial de capturas

### UI/UX Móvil
- [ ] Diseño responsive (phone/tablet)
- [ ] Dark mode / Light mode
- [ ] Gestos táctiles (swipe, pinch)
- [ ] Bottom navigation
- [ ] Loading states

### Permisos
- [ ] Cámara
- [ ] Galería
- [ ] Almacenamiento
- [ ] Notificaciones

### Offline
- [ ] Caché de imágenes
- [ ] SQLite para historial
- [ ] Sincronización cuando online

### Performance
- [ ] Tiempo de captura < 500ms
- [ ] Uso de memoria < 150MB
- [ ] Tamaño de APK < 50MB
- [ ] Inicio de app < 2 segundos

### Distribución
- [ ] Firma de app (Android)
- [ ] Provisioning profile (iOS)
- [ ] Play Store listing
- [ ] App Store listing

---

## 📚 Recursos Adicionales

- [Flutter Documentation](https://docs.flutter.dev/)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)
- [Flutter Samples](https://flutter.github.io/samples/)
- [Pub.dev Packages](https://pub.dev/)

---

**Última actualización:** 2025-12-21  
**Mantenedor:** @eddmtzarias  
**Versión de guía:** 1.0.0
