import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { assistanceService } from '../services/assistanceService'

export function Dashboard() {
  const [input, setInput] = useState('')
  const [context, setContext] = useState('')

  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: () => fetch('/api/health').then(res => res.json()),
    refetchInterval: 30000,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement assistance request
  }

  return (
    <div style={{ padding: '2rem' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1>OmniMaestro™ - Contextual Learning AI</h1>
        <p style={{ color: '#666', marginTop: '0.5rem' }}>
          TOKRAGGCORP Production System
        </p>
        {health && (
          <p style={{ color: health.status === 'healthy' ? 'green' : 'red', fontSize: '0.875rem' }}>
            System Status: {health.status}
          </p>
        )}
      </header>

      <main style={{ maxWidth: '800px' }}>
        <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="context" style={{ display: 'block', marginBottom: '0.5rem' }}>
              Context (Screenshot/Text):
            </label>
            <textarea
              id="context"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Paste text or describe your screen..."
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                minHeight: '100px',
                borderRadius: '4px',
                border: '1px solid #ccc'
              }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="input" style={{ display: 'block', marginBottom: '0.5rem' }}>
              Your Question:
            </label>
            <input
              id="input"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="What do you need help with?"
              style={{ 
                width: '100%', 
                padding: '0.5rem',
                borderRadius: '4px',
                border: '1px solid #ccc'
              }}
            />
          </div>

          <button 
            type="submit" 
            style={{ 
              padding: '0.5rem 1.5rem',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Get Assistance
          </button>
        </form>

        <div style={{ 
          padding: '1rem', 
          backgroundColor: 'white', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ marginBottom: '1rem' }}>Features</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ marginBottom: '0.5rem' }}>✓ Multi-modal input (Visual, Text, Voice)</li>
            <li style={{ marginBottom: '0.5rem' }}>✓ Adaptive pedagogical responses</li>
            <li style={{ marginBottom: '0.5rem' }}>✓ Real-time contextual analysis</li>
            <li style={{ marginBottom: '0.5rem' }}>✓ Cross-platform support</li>
            <li style={{ marginBottom: '0.5rem' }}>✓ Sub-500ms AI inference</li>
          </ul>
        </div>
      </main>
    </div>
  )
}
