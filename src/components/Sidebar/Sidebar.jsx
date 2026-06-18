import { useState, useEffect } from 'react';
import { api } from '../../api/client';

export default function Sidebar({ activeTab, setActiveTab, provider, setProvider, model, setModel }) {
  const [providers, setProviders] = useState([]);
  const [ragStats, setRagStats] = useState(null);

  useEffect(() => {
    api.chat.providers().then((d) => setProviders(d.providers)).catch(() => {});
    api.rag.stats().then(setRagStats).catch(() => {});
  }, []);

  const tabs = [
    { id: 'chat', label: 'Chat', icon: '💬' },
    { id: 'projects', label: 'Projects', icon: '📋' },
    { id: 'rag', label: 'RAG Explorer', icon: '📚' },
    { id: 'learn', label: 'Learning', icon: '🎓' },
  ];

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      <div className="p-4 border-b border-gray-700">
        <h1 className="text-lg font-bold">AI Engineer</h1>
        <p className="text-xs text-gray-400 mt-1">Local AI Dev Assistant</p>
      </div>

      <nav className="flex-1 p-2 space-y-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 text-sm transition-colors ${
              activeTab === tab.id ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800'
            }`}
          >
            <span>{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </nav>

      <div className="p-3 border-t border-gray-700 space-y-3">
        <div>
          <label className="text-xs text-gray-400 block mb-1">Provider</label>
          <select
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
            className="w-full bg-gray-800 text-white text-sm rounded px-2 py-1.5 border border-gray-600"
          >
            {providers.map((p) => (
              <option key={p.name} value={p.name} disabled={!p.available}>
                {p.name} {!p.available ? '(no key)' : ''}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="text-xs text-gray-400 block mb-1">Model</label>
          <input
            value={model}
            onChange={(e) => setModel(e.target.value)}
            placeholder="qwen2.5:7b"
            className="w-full bg-gray-800 text-white text-sm rounded px-2 py-1.5 border border-gray-600"
          />
        </div>
        {ragStats && (
          <div className="text-xs text-gray-400">
            RAG: {ragStats.total_chunks} chunks indexed
          </div>
        )}
      </div>
    </div>
  );
}
