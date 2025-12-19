# Frontend Applications

## Overview

The `/frontend` directory contains all user-facing applications for the TE-explico system, supporting multiple platforms: Web, Mobile (iOS/Android), and Desktop (Windows/macOS/Linux).

## Structure

```
frontend/
├── web/                 # Web application (React/Next.js)
├── mobile/              # Mobile app (Flutter/React Native)
├── desktop/             # Desktop app (Electron/Tauri)
├── shared/              # Shared UI components and logic
└── README.md
```

## Platform Support

### Web Application
- **Framework**: React 18+ with Next.js
- **Styling**: TailwindCSS
- **State Management**: Redux Toolkit / Zustand
- **Target**: Modern browsers (Chrome, Firefox, Safari, Edge)

### Mobile Application
- **Framework**: Flutter (cross-platform)
- **Platforms**: iOS 13+, Android 8+
- **Features**: Native performance, offline support

### Desktop Application
- **Framework**: Tauri (Rust + Web)
- **Platforms**: Windows 10+, macOS 11+, Linux
- **Features**: System integration, screen capture

## Key Features

### 1. Contextual Overlay System
- Non-intrusive floating assistant
- Screen capture integration
- Real-time context awareness

### 2. Multi-Modal Input
- Text input
- Voice recognition
- Screenshot analysis
- Cursor position tracking

### 3. Adaptive UI
- Responsive design
- Accessibility (WCAG 2.1 AA)
- Dark/Light themes
- Multi-language support

## Development

```bash
# Web
cd web
npm install
npm run dev

# Mobile
cd mobile
flutter pub get
flutter run

# Desktop
cd desktop
npm install
npm run tauri dev
```

## Design System

- **Components**: Storybook for component library
- **Icons**: Heroicons / Material Icons
- **Typography**: Inter, Roboto
- **Accessibility**: ARIA labels, keyboard navigation

## Status

🚧 **Under Construction** - Frontend applications are being developed with focus on multi-platform consistency.
