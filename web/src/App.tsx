import { useState, useEffect } from 'react'
import './App.css'
import { motion, AnimatePresence } from 'framer-motion'

const API_URL = 'http://localhost:8000'

interface AgentMessage {
  role: string
  content: string
}

function App() {
  const [goal, setGoal] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<string>('')
  const [history, setHistory] = useState<AgentMessage[]>([])
  const [agentStatus, setAgentStatus] = useState<'idle' | 'running'>('idle')

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then(res => res.json())
      .then(data => console.log('API Status:', data))
      .catch(err => console.error('API not reachable:', err))
  }, [])

  const runAgent = async () => {
    if (!goal.trim()) return

    setLoading(true)
    setResult('')
    setHistory([])
    setAgentStatus('running')

    try {
      const response = await fetch(`${API_URL}/agent/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal, max_steps: 10 })
      })

      if (!response.ok) throw new Error('Failed to run agent')

      const data = await response.json()
      setResult(data.result)
      setHistory(data.history)
      setAgentStatus('idle')
    } catch (error) {
      console.error('Agent error:', error)
      setResult('Error: Could not connect to backend API. Make sure the FastAPI server is running on port 8000.')
      setAgentStatus('idle')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      {/* Hero Section */}
      <div className="hero-section">
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="hero-content"
        >
          <div className="logo-container">
            <div className="logo-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <path d="M24 4L40 14V34L24 44L8 34V14Z" stroke="url(#grad1)" strokeWidth="2" fill="none" />
                <defs>
                  <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#3B82F6" />
                    <stop offset="100%" stopColor="#8B5CF6" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <h1 className="hero-title">TruthGraph</h1>
          </div>
          <p className="hero-subtitle">The Trust Layer for the AI Era</p>
          <div className="status-badge">
            <span className={`status-dot ${agentStatus === 'running' ? 'running' : 'idle'}`}></span>
            {agentStatus === 'running' ? 'Agent Running' : 'Ready'}
          </div>
        </motion.div>
      </div>

      {/* Main Content */}
      <div className="container">
        <div className="content-grid">
          {/* Left Column - Agent Console */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="console-card"
          >
            <div className="card-header">
              <h2>🧠 Agent Console</h2>
              <p>Enter your verification goal</p>
            </div>

            <div className="input-group">
              <label>What would you like to verify?</label>
              <textarea
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                placeholder="Example: Check if 'The earth is flat' is a hallucination"
                disabled={loading}
                rows={5}
                className="input-field"
              />
            </div>

            <button
              onClick={runAgent}
              disabled={loading || !goal.trim()}
              className="btn-primary"
            >
              {loading ? (
                <>
                  <svg className="spinner" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Running...
                </>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  Run Agent
                </>
              )}
            </button>

            {result && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="result-box"
              >
                <div className="result-header">✓ Final Result</div>
                <p>{result}</p>
              </motion.div>
            )}
          </motion.div>

          {/* Right Column - Agent Thoughts */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="thoughts-card"
          >
            <div className="card-header">
              <h2>💭 Agent Reasoning</h2>
              <p>Live thought process</p>
            </div>

            <div className="thoughts-container">
              <AnimatePresence>
                {history.length === 0 ? (
                  <div className="empty-state">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    </svg>
                    <p>Run the agent to see its reasoning...</p>
                  </div>
                ) : (
                  history.map((msg, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className={`thought-item ${msg.role}`}
                    >
                      <div className="thought-role">{msg.role}</div>
                      <div className="thought-content">{msg.content}</div>
                    </motion.div>
                  ))
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </div>

        {/* Feature Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="features-grid"
        >
          <div className="feature-card">
            <div className="feature-icon">🕸️</div>
            <h3>Knowledge Layer</h3>
            <p>OriginTrail DKG for decentralized storage</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🛡️</div>
            <h3>Trust Layer</h3>
            <p>NeuroWeb blockchain verification</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💰</div>
            <h3>x402 Economy</h3>
            <p>Autonomous micropayments</p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default App
