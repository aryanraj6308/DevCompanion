import { useState } from 'react';
import { api } from '../../api/client';

export default function RAGExplorer() {
  const [fileContent, setFileContent] = useState('');
  const [filename, setFilename] = useState('');
  const [indexResult, setIndexResult] = useState(null);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [queryLoading, setQueryLoading] = useState(false);
  const [indexLoading, setIndexLoading] = useState(false);

  async function handleIndex() {
    if (!fileContent || !filename) return;
    setIndexLoading(true);
    try {
      const data = await api.rag.index({ content: fileContent, filename });
      setIndexResult(data);
      setFileContent('');
    } catch (err) {
      setIndexResult({ error: err.message });
    }
    setIndexLoading(false);
  }

  async function handleQuery() {
    if (!query) return;
    setQueryLoading(true);
    try {
      const data = await api.rag.query({ query, n_results: 5 });
      setResults(data.results);
    } catch {}
    setQueryLoading(false);
  }

  return (
    <div className="p-6 overflow-y-auto h-full space-y-6">
      <h2 className="text-xl font-bold text-white">RAG Memory System</h2>

      <div className="bg-gray-800 rounded-lg p-4">
        <h3 className="text-white font-semibold mb-3">Index Document</h3>
        <div className="space-y-3">
          <input
            value={filename}
            onChange={(e) => setFilename(e.target.value)}
            placeholder="Filename (e.g. main.py, README.md)"
            className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            value={fileContent}
            onChange={(e) => setFileContent(e.target.value)}
            placeholder="Paste file content here..."
            rows={6}
            className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <button
            onClick={handleIndex}
            disabled={indexLoading || !fileContent || !filename}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg"
          >
            {indexLoading ? 'Indexing...' : 'Index Document'}
          </button>
          {indexResult && (
            <p className="text-sm text-green-400">
              {indexResult.error ? `Error: ${indexResult.error}` : `Indexed ${indexResult.chunk_count} chunks from ${indexResult.filename}`}
            </p>
          )}
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-4">
        <h3 className="text-white font-semibold mb-3">Query Knowledge Base</h3>
        <div className="space-y-3">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleQuery()}
            placeholder="Ask about your project..."
            className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleQuery}
            disabled={queryLoading || !query}
            className="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg"
          >
            {queryLoading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {results.length > 0 && (
          <div className="mt-4 space-y-3">
            {results.map((r, i) => (
              <div key={i} className="bg-gray-900 rounded p-3">
                <p className="text-xs text-gray-400 mb-1">{r.filename} (score: {r.score.toFixed(3)})</p>
                <p className="text-gray-300 text-sm whitespace-pre-wrap">{r.content}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
