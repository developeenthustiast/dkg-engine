import { useState, useEffect, useRef } from 'react'
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
  const thoughtsEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .catch(err => console.error('API not reachable:', err))
  }, [])

  useEffect(() => {
    thoughtsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [history])

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
    <div className="min-h-screen relative overflow-hidden bg-[#030014]">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:50px_50px]" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-blue-500/20 rounded-full blur-[120px] opacity-30 pointer-events-none" />
      <div className="absolute bottom-0 right-0 w-[800px] h-[600px] bg-purple-500/10 rounded-full blur-[100px] opacity-20 pointer-events-none" />

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 mb-6 backdrop-blur-sm">
            <span className={`w-2 h-2 rounded-full ${agentStatus === 'running' ? 'bg-amber-400 animate-pulse' : 'bg-emerald-400'}`} />
            <span className="text-xs font-medium text-gray-300 uppercase tracking-wider">
              {agentStatus === 'running' ? 'Agent Active' : 'System Ready'}
            </span>
          </div>

          <h1 className="text-7xl font-bold mb-6 tracking-tight">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-100 to-white">
              TruthGraph
            </span>
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
            The decentralized trust layer for the AI era. Verifiable fact-checking powered by
            <span className="text-blue-400"> OriginTrail DKG</span> and <span className="text-purple-400">NeuroWeb</span>.
          </p>
        </motion.div>

        {/* Main Grid */}
        <div className="grid lg:grid-cols-12 gap-8 mb-20">
          {/* Left Column: Input */}
          <div className="lg:col-span-5 space-y-6">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="glass-card rounded-2xl p-1"
            >
              <div className="bg-[#0a0a0a]/80 backdrop-blur-xl rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-2xl">🎯</span> Agent Objective
                </h2>

                <div className="space-y-4">
                  <textarea
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    placeholder="Enter a claim to verify (e.g., 'Check if the earth is flat')"
                    className="w-full h-40 glass-input rounded-xl p-4 text-lg text-white placeholder-gray-600 resize-none"
                    disabled={loading}
                  />

                  <button
                    onClick={runAgent}
                    disabled={loading || !goal.trim()}
                    className="w-full btn-gradient py-4 rounded-xl font-semibold text-lg flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        Verifying...
                      </>
                    ) : (
                      <>
                        <span>Run Verification</span>
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </motion.div>

            {/* Result Card */}
            <AnimatePresence>
              {result && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="glass-card rounded-2xl p-6 border-l-4 border-l-emerald-500"
                >
                  <h3 className="text-emerald-400 font-semibold mb-2 flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Verification Complete
                  </h3>
                  <p className="text-gray-200 leading-relaxed">{result}</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Right Column: Thoughts */}
          <div className="lg:col-span-7">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="glass-card rounded-2xl h-[600px] flex flex-col overflow-hidden"
            >
              <div className="p-6 border-b border-white/5 bg-white/[0.02]">
                <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                  <span className="text-2xl">🧠</span> Neural Process
                </h2>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {history.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-gray-600 space-y-4">
                    <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center">
                      <svg className="w-8 h-8 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                    </div>
                    <p>Waiting for input...</p>
                  </div>
                ) : (
                  history.map((msg, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className={`p-4 rounded-xl text-sm leading-relaxed border ${msg.role === 'system' ? 'bg-purple-500/5 border-purple-500/20 text-purple-200' :
                          msg.role === 'assistant' ? 'bg-blue-500/5 border-blue-500/20 text-blue-200' :
                            msg.role === 'tool' ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-200' :
                              'bg-gray-500/5 border-gray-500/20 text-gray-300'
                        }`}
                    >
                      <div className="flex items-center gap-2 mb-2 opacity-70 text-xs font-bold uppercase tracking-wider">
                        {msg.role === 'assistant' && '🤖 Agent'}
                        {msg.role === 'system' && '⚙️ System'}
                        {msg.role === 'tool' && '🛠️ Tool Output'}
                        {msg.role === 'user' && '👤 User'}
                      </div>
                      <div className="whitespace-pre-wrap font-mono text-xs opacity-90">
                        {msg.content}
                      </div>
                    </motion.div>
                  ))
                )}
                <div ref={thoughtsEndRef} />
              </div>
            </motion.div>
          </div>
        </div>

        {/* Footer Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="grid md:grid-cols-3 gap-6"
        >
          {[
            { icon: '🕸️', title: 'Knowledge Graph', value: 'OriginTrail DKG', color: 'text-blue-400' },
            { icon: '🛡️', title: 'Trust Layer', value: 'NeuroWeb Chain', color: 'text-purple-400' },
            { icon: '⚡', title: 'Micropayments', value: 'x402 Protocol', color: 'text-emerald-400' },
          ].map((stat, i) => (
            <div key={i} className="glass-card p-6 rounded-xl flex items-center gap-4 hover:bg-white/[0.05] transition-colors cursor-default">
              <div className="text-3xl">{stat.icon}</div>
              <div>
                <div className="text-sm text-gray-500 uppercase tracking-wider font-medium">{stat.title}</div>
                <div className={`text-lg font-bold ${stat.color}`}>{stat.value}</div>
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  )
}

export default App
