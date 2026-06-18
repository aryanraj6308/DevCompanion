import { useState, useRef, useEffect } from 'react';
import { api } from '../../api/client';

export default function ChatBox({ provider, model }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [tool, setTool] = useState('chat');
  const bottomRef = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const tools = [
    { value: 'chat', label: 'Chat' },
    { value: 'code-gen', label: 'Generate Code' },
    { value: 'code-explain', label: 'Explain Code' },
    { value: 'debug', label: 'Debug' },
  ];

  const toolPrefix = {
    'code-gen': 'Write code for: ',
    'code-explain': 'Explain this code: ',
    'debug': 'Debug this code: ',
  };

  function handleSend() {
    if (!input.trim() || loading) return;
    const msg = toolPrefix[tool] ? `${toolPrefix[tool]}${input}` : input;
    const userMsg = { role: 'user', content: msg };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    const loadingMsg = { role: 'assistant', content: '', loading: true };
    setMessages((prev) => [...prev, loadingMsg]);

    api.chat.stream(
      { message: msg, session_id: sessionId, provider, model, tool },
      (chunk) => {
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          if (last.loading) {
            last.content += chunk;
          }
          return updated;
        });
      },
      (sid) => {
        setSessionId(sid);
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          delete last.loading;
          return updated;
        });
        setLoading(false);
      },
      (err) => {
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = { role: 'assistant', content: `Error: ${err}` };
          return updated;
        });
        setLoading(false);
      },
    );
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  }

  function clearChat() {
    setMessages([]);
    setSessionId(null);
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 p-3 border-b border-gray-700">
        <select
          value={tool}
          onChange={(e) => setTool(e.target.value)}
          className="bg-gray-700 text-white px-3 py-1.5 rounded text-sm"
        >
          {tools.map((t) => (
            <option key={t.value} value={t.value}>{t.label}</option>
          ))}
        </select>
        <button onClick={clearChat} className="ml-auto text-xs text-gray-400 hover:text-white px-2 py-1 rounded border border-gray-600">
          Clear
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <p className="text-xl mb-2">Local AI Engineer</p>
            <p className="text-sm">Ask me anything about code, projects, or programming</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-lg px-4 py-2 whitespace-pre-wrap ${
              msg.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-100'
            }`}>
              {msg.content}
              {msg.loading && <span className="animate-pulse">▊</span>}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="border-t border-gray-700 p-3">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            rows={1}
            className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-2 resize-none outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-medium"
          >
            {loading ? '...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}
