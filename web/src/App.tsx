import { useState, useEffect } from 'react'
import './App.css'
import { motion } from 'framer-motion'

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
    // Check agent status on mount
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
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12 text-center"
        >
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent mb-4">
            TruthGraph
          </h1>
          <p className="text-gray-400 text-xl">The Trust Layer for the AI Era</p>
          <div className="mt-4 flex items-center justify-center gap-4">
            <span className={`px-4 py-2 rounded-full text-sm ${agentStatus === 'running' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-green-500/20 text-green-400'}`}>
              {agentStatus === 'running' ? '🤖 Agent Running...' : '✓ Agent Ready'}
            </span>
          </div>
        </motion.div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Agent Console */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="card"
          >
            <h2 className="text-2xl font-bold text-white mb-6">🧠 Agent Console</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Agent Goal
                </label>
                <textarea
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                  placeholder="e.g., Check if 'The earth is flat' is a hallucination"
                  className="w-full bg-white/5 border border-white/10 rounded-lg p-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  rows={4}
                  disabled={loading}
                />
              </div>

              <button
                onClick={runAgent}
                disabled={loading || !goal.trim()}
                className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Running Agent...
                  </span>
                ) : (
                  '▶ Run Agent'
                )}
              </button>
            </div>

            {/* Result Display */}
            {result && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg"
              >
                <h3 className="text-sm font-semibold text-blue-400 mb-2">Final Result:</h3>
                <p className="text-white">{result}</p>
              </motion.div>
            )}
          </motion.div>

          {/* Agent Thoughts */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="card"
          >
            <h2 className="text-2xl font-bold text-white mb-6">💭 Agent Thoughts</h2>

            <div className="space-y-3 max-h-[500px] overflow-y-auto">
              {history.length === 0 ? (
                <p className="text-gray-500 text-center py-8">
                  Run the agent to see the thought process...
                </p>
              ) : (
                history.map((msg, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className={`p-3 rounded-lg ${msg.role === 'system' ? 'bg-purple-500/10 border-l-4 border-purple-500' :
                        msg.role === 'assistant' ? 'bg-blue-500/10 border-l-4 border-blue-500' :
                          msg.role === 'tool' ? 'bg-green-500/10 border-l-4 border-green-500' :
                            'bg-gray-500/10 border-l-4 border-gray-500'
                      }`}
                  >
                    <div className="text-xs font-semibold text-gray-400 mb-1 uppercase">{msg.role}</div>
                    <div className="text-sm text-gray-200 whitespace-pre-wrap">{msg.content}</div>
                  </motion.div>
                ))
              )}
            </div>
          </motion.div>
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card text-center"
          >
            <div className="text-4xl mb-3">🕸️</div>
            <h3 className="text-lg font-semibold text-white mb-2">Knowledge Layer</h3>
            <p className="text-sm text-gray-400">OriginTrail DKG</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="card text-center"
          >
            <div className="text-4xl mb-3">🛡️</div>
            <h3 className="text-lg font-semibold text-white mb-2">Trust Layer</h3>
            <p className="text-sm text-gray-400">NeuroWeb Parachain</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="card text-center"
          >
            <div className="text-4xl mb-3">💰</div>
            <h3 className="text-lg font-semibold text-white mb-2">x402 Economy</h3>
            <p className="text-sm text-gray-400">Micropayments Ready</p>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default App
