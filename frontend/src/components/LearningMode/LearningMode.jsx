import { useState } from 'react';
import { api } from '../../api/client';

export default function LearningMode({ provider, model }) {
  const [topic, setTopic] = useState('');
  const [level, setLevel] = useState('beginner');
  const [errorCode, setErrorCode] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');

  async function handleTeach() {
    if (!topic) return;
    setLoading(true);
    setResult('');
    try {
      const data = await api.learn.teach({ message: topic, level, provider, model });
      setResult(data.reply);
    } catch (err) {
      setResult(`Error: ${err.message}`);
    }
    setLoading(false);
  }

  async function handleErrorExplain() {
    if (!errorMsg) return;
    setLoading(true);
    setResult('');
    try {
      const data = await api.learn.explainError({ error: errorMsg, code_context: errorCode, provider, model });
      setResult(data.reply);
    } catch (err) {
      setResult(`Error: ${err.message}`);
    }
    setLoading(false);
  }

  return (
    <div className="p-6 overflow-y-auto h-full space-y-6">
      <h2 className="text-xl font-bold text-white">Learning Mode</h2>

      <div className="bg-gray-800 rounded-lg p-4">
        <h3 className="text-white font-semibold mb-3">Learn a Concept</h3>
        <div className="space-y-3">
          <input
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleTeach()}
            placeholder="What do you want to learn? (e.g. React hooks, SQL joins)"
            className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={level}
            onChange={(e) => setLevel(e.target.value)}
            className="bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <button
            onClick={handleTeach}
            disabled={loading || !topic}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg"
          >
            {loading ? 'Teaching...' : 'Teach Me'}
          </button>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-4">
        <h3 className="text-white font-semibold mb-3">Explain Error</h3>
        <div className="space-y-3">
          <textarea
            value={errorMsg}
            onChange={(e) => setErrorMsg(e.target.value)}
            placeholder="Paste the error message here..."
            rows={2}
            className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <textarea
            value={errorCode}
            onChange={(e) => setErrorCode(e.target.value)}
            placeholder="Paste related code (optional)..."
            rows={4}
            className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <button
            onClick={handleErrorExplain}
            disabled={loading || !errorMsg}
            className="bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg"
          >
            Explain Error
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="text-white font-semibold mb-2">Response</h3>
          <div className="text-gray-300 text-sm whitespace-pre-wrap">{result}</div>
        </div>
      )}
    </div>
  );
}
