# 🌐 Web Development Guide - Progressive Web App (PWA)

> **Guía completa para desarrollar OmniMaestro como PWA**  
> Última actualización: 2025-12-21

---

## 📋 Tabla de Contenidos

1. [Pre-requisitos](#pre-requisitos)
2. [Setup del Proyecto](#setup-del-proyecto)
3. [Configuración PWA](#configuración-pwa)
4. [Desarrollo](#desarrollo)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Problemas Comunes](#problemas-comunes)
8. [Checklist de Features](#checklist-de-features)

---

## 📦 Pre-requisitos

### Versiones Requeridas

| Herramienta | Versión Mínima | Recomendada | Validación |
|-------------|----------------|-------------|------------|
| Node.js | 18.0.0 | 20.x LTS | `node --version` |
| npm | 9.0.0 | 10.x | `npm --version` |
| Git | 2.30+ | Latest | `git --version` |

---

## 🚀 Setup del Proyecto

### Opción 1: Next.js (Recomendado)

```bash
# Crear proyecto Next.js con TypeScript
npx create-next-app@latest omnimaestro --typescript --tailwind --app --eslint

cd omnimaestro
```

### Opción 2: React + Vite

```bash
# Crear proyecto con Vite
npm create vite@latest omnimaestro -- --template react-ts

cd omnimaestro
npm install
```

### Estructura del Proyecto (Next.js)

```
omnimaestro/
├── app/                   # App Router (Next.js 13+)
│   ├── layout.tsx        # Layout principal
│   ├── page.tsx          # Página principal
│   ├── api/              # API routes
│   └── components/       # Componentes
├── public/               # Assets estáticos
│   ├── manifest.json    # PWA manifest
│   ├── sw.js           # Service Worker
│   └── icons/          # Iconos PWA
├── lib/                 # Utilidades
├── hooks/               # Custom hooks
├── styles/              # Estilos
├── next.config.js       # Configuración Next.js
└── package.json
```

---

## ⚙️ Configuración PWA

### 1. Instalar Dependencias PWA

```bash
# Para Next.js
npm install next-pwa
npm install --save-dev @types/serviceworker

# Dependencias adicionales
npm install react-camera-pro
npm install tesseract.js
npm install axios
```

### 2. Configurar next.config.js

```javascript
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
  buildExcludes: [/middleware-manifest\.json$/],
  runtimeCaching: [
    {
      urlPattern: /^https:\/\/api\.openai\.com\/.*/i,
      handler: 'NetworkFirst',
      options: {
        cacheName: 'openai-cache',
        expiration: {
          maxEntries: 50,
          maxAgeSeconds: 60 * 60 * 24 * 7, // 7 días
        },
      },
    },
    {
      urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/i,
      handler: 'CacheFirst',
      options: {
        cacheName: 'images-cache',
        expiration: {
          maxEntries: 100,
          maxAgeSeconds: 60 * 60 * 24 * 30, // 30 días
        },
      },
    },
  ],
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
};

module.exports = withPWA(nextConfig);
```

### 3. Crear Manifest.json

```json
{
  "name": "OmniMaestro - AI Learning Companion",
  "short_name": "OmniMaestro",
  "description": "AI-powered learning companion that analyzes screenshots and provides adaptive explanations",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2563eb",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/desktop-1.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    },
    {
      "src": "/screenshots/mobile-1.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ],
  "categories": ["education", "productivity", "utilities"],
  "shortcuts": [
    {
      "name": "Capture Screenshot",
      "short_name": "Capture",
      "description": "Take a screenshot to analyze",
      "url": "/capture",
      "icons": [
        {
          "src": "/icons/capture-icon.png",
          "sizes": "96x96"
        }
      ]
    }
  ],
  "share_target": {
    "action": "/share",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "title": "title",
      "text": "text",
      "url": "url",
      "files": [
        {
          "name": "image",
          "accept": ["image/*"]
        }
      ]
    }
  }
}
```

### 4. Añadir Manifest al Layout

```tsx
// app/layout.tsx
import type { Metadata, Viewport } from 'next'

export const metadata: Metadata = {
  title: 'OmniMaestro - AI Learning Companion',
  description: 'AI-powered learning companion',
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'OmniMaestro',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#2563eb',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/icons/icon-192x192.png" />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

---

## 💻 Desarrollo

### Implementar Captura de Pantalla

```typescript
// lib/capture.ts
export async function captureScreen(): Promise<Blob | null> {
  try {
    // Usar Screen Capture API (requiere HTTPS)
    const stream = await navigator.mediaDevices.getDisplayMedia({
      video: { mediaSource: 'screen' } as any,
    });
    
    const video = document.createElement('video');
    video.srcObject = stream;
    video.play();
    
    // Esperar a que el video esté listo
    await new Promise(resolve => {
      video.onloadedmetadata = resolve;
    });
    
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    ctx?.drawImage(video, 0, 0);
    
    // Detener stream
    stream.getTracks().forEach(track => track.stop());
    
    return new Promise(resolve => {
      canvas.toBlob(blob => resolve(blob), 'image/png');
    });
  } catch (error) {
    console.error('Error capturing screen:', error);
    return null;
  }
}
```

### Implementar OCR (Tesseract.js)

```typescript
// lib/ocr.ts
import { createWorker } from 'tesseract.js';

export class OCRService {
  private worker: Tesseract.Worker | null = null;

  async initialize() {
    this.worker = await createWorker('eng');
  }

  async extractText(imageBlob: Blob): Promise<string> {
    if (!this.worker) {
      await this.initialize();
    }

    const { data } = await this.worker!.recognize(imageBlob);
    return data.text;
  }

  async terminate() {
    if (this.worker) {
      await this.worker.terminate();
    }
  }
}
```

### Implementar Upload de Imagen

```typescript
// components/ImageUpload.tsx
'use client';

import { useState } from 'react';

export function ImageUpload() {
  const [image, setImage] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="file-input"
      />
      {image && (
        <img src={image} alt="Preview" className="max-w-md rounded-lg" />
      )}
    </div>
  );
}
```

### Implementar Offline Storage

```typescript
// lib/storage.ts
import { openDB, DBSchema, IDBPDatabase } from 'idb';

interface OmniMaestroDB extends DBSchema {
  screenshots: {
    key: string;
    value: {
      id: string;
      image: Blob;
      text: string;
      explanation: string;
      timestamp: number;
    };
  };
}

export class StorageService {
  private db: IDBPDatabase<OmniMaestroDB> | null = null;

  async initialize() {
    this.db = await openDB<OmniMaestroDB>('omnimaestro-db', 1, {
      upgrade(db) {
        db.createObjectStore('screenshots', { keyPath: 'id' });
      },
    });
  }

  async saveScreenshot(data: {
    image: Blob;
    text: string;
    explanation: string;
  }) {
    if (!this.db) await this.initialize();
    
    const id = crypto.randomUUID();
    await this.db!.put('screenshots', {
      id,
      ...data,
      timestamp: Date.now(),
    });
    
    return id;
  }

  async getScreenshot(id: string) {
    if (!this.db) await this.initialize();
    return this.db!.get('screenshots', id);
  }

  async getAllScreenshots() {
    if (!this.db) await this.initialize();
    return this.db!.getAll('screenshots');
  }
}
```

### Componente Principal

```tsx
// app/page.tsx
'use client';

import { useState } from 'react';
import { captureScreen } from '@/lib/capture';
import { OCRService } from '@/lib/ocr';

export default function Home() {
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<string>('');

  const handleCapture = async () => {
    setAnalyzing(true);
    try {
      const blob = await captureScreen();
      if (!blob) throw new Error('Failed to capture screen');

      const ocr = new OCRService();
      await ocr.initialize();
      const text = await ocr.extractText(blob);
      await ocr.terminate();

      setResult(text);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">OmniMaestro</h1>
        
        <button
          onClick={handleCapture}
          disabled={analyzing}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg"
        >
          {analyzing ? 'Analyzing...' : 'Capture Screenshot'}
        </button>

        {result && (
          <div className="mt-8 p-6 bg-gray-100 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">Extracted Text:</h2>
            <p className="whitespace-pre-wrap">{result}</p>
          </div>
        )}
      </div>
    </main>
  );
}
```

---

## 🧪 Testing

### Setup Testing

```bash
# Instalar dependencias de testing
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
npm install --save-dev @testing-library/user-event
```

### Tests Unitarios

```typescript
// __tests__/capture.test.ts
import { captureScreen } from '@/lib/capture';

describe('Capture Service', () => {
  it('should capture screen', async () => {
    // Mock getDisplayMedia
    global.navigator.mediaDevices = {
      getDisplayMedia: jest.fn().mockResolvedValue({
        getTracks: () => [],
      }),
    } as any;

    const result = await captureScreen();
    expect(result).toBeDefined();
  });
});
```

### Tests E2E (Playwright)

```bash
# Instalar Playwright
npm install --save-dev @playwright/test

# Inicializar
npx playwright install
```

```typescript
// e2e/capture.spec.ts
import { test, expect } from '@playwright/test';

test('should capture and analyze screenshot', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  await page.click('text=Capture Screenshot');
  
  await expect(page.locator('text=Analyzing...')).toBeVisible();
  await expect(page.locator('text=Extracted Text:')).toBeVisible({ timeout: 10000 });
});
```

---

## 🚀 Deployment

### Vercel (Recomendado)

```bash
# Instalar Vercel CLI
npm install -g vercel

# Desplegar
vercel

# Producción
vercel --prod
```

### Netlify

```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Desplegar
netlify deploy --prod --dir=.next
```

### Variables de Entorno

```bash
# .env.local (no commitear)
NEXT_PUBLIC_API_URL=https://api.omnimaestro.com
OPENAI_API_KEY=sk-...
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

### Configurar en Vercel

1. Ir a Project Settings > Environment Variables
2. Añadir todas las variables de `.env.local`
3. Redeploy

---

## 🔧 Problemas Comunes

### Error: "Service Worker not registering"
```javascript
// Solución: Verificar next.config.js
// Asegurar que disable: false en producción
```

### Error: "Screen Capture API not working"
```
Solución: La API requiere HTTPS
- En desarrollo: usar localhost (permitido sin HTTPS)
- En producción: usar dominio con SSL
```

### Error: "PWA not installable"
```
Solución: Verificar checklist:
1. manifest.json válido
2. Service Worker registrado
3. HTTPS habilitado
4. Iconos de tamaños correctos
```

### Error: "Tesseract.js slow"
```typescript
// Solución: Usar Web Worker
import { createWorker } from 'tesseract.js';

const worker = await createWorker('eng', 1, {
  workerPath: '/worker.js',
  corePath: '/tesseract-core.wasm.js',
});
```

---

## ✅ Checklist de Features PWA

### PWA Básico
- [ ] manifest.json configurado
- [ ] Service Worker funcionando
- [ ] Iconos de múltiples tamaños
- [ ] HTTPS habilitado
- [ ] Instalable en dispositivos

### Capacidades Offline
- [ ] Caché de assets estáticos
- [ ] IndexedDB para datos
- [ ] Sincronización en background
- [ ] Notificaciones offline

### UI/UX Web
- [ ] Responsive design (móvil/tablet/desktop)
- [ ] Dark mode
- [ ] Loading states
- [ ] Error boundaries
- [ ] Skeleton loaders

### Performance
- [ ] Lighthouse score > 90
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s
- [ ] Bundle size optimizado

### SEO
- [ ] Meta tags configurados
- [ ] Open Graph tags
- [ ] Twitter Cards
- [ ] Sitemap.xml
- [ ] robots.txt

---

## 📚 Recursos Adicionales

- [Next.js Documentation](https://nextjs.org/docs)
- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Vercel Deployment](https://vercel.com/docs)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)

---

**Última actualización:** 2025-12-21  
**Mantenedor:** @eddmtzarias  
**Versión de guía:** 1.0.0
