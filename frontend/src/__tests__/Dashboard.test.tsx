import { render, screen } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Dashboard } from '../components/Dashboard'

describe('Dashboard', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  })

  it('renders dashboard header', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <Dashboard />
      </QueryClientProvider>
    )
    
    expect(screen.getByText(/OmniMaestro/i)).toBeInTheDocument()
    expect(screen.getByText(/TOKRAGGCORP Production System/i)).toBeInTheDocument()
  })

  it('renders form inputs', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <Dashboard />
      </QueryClientProvider>
    )
    
    expect(screen.getByLabelText(/Context/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Your Question/i)).toBeInTheDocument()
    expect(screen.getByText(/Get Assistance/i)).toBeInTheDocument()
  })

  it('renders features list', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <Dashboard />
      </QueryClientProvider>
    )
    
    expect(screen.getByText(/Multi-modal input/i)).toBeInTheDocument()
    expect(screen.getByText(/Sub-500ms AI inference/i)).toBeInTheDocument()
  })
})
