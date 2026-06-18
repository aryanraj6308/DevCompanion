import { useState } from 'react';
import { api } from '../../api/client';

export default function ProjectPlanner({ provider, model }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [techStack, setTechStack] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [saved, setSaved] = useState([]);

  async function handlePlan() {
    if (!name || !description) return;
    setLoading(true);
    try {
      const data = await api.projects.architect({
        project_name: name,
        description,
        tech_stack: techStack.split(',').map((s) => s.trim()).filter(Boolean),
      });
      setResult(data);
    } catch (err) {
      setResult({ plan: `Error: ${err.message}` });
    }
    setLoading(false);
  }

  async function handleSave() {
    try {
      await api.projects.create({
        name,
        description,
        tech_stack: techStack.split(',').map((s) => s.trim()).filter(Boolean),
      });
      loadSaved();
    } catch {}
  }

  async function loadSaved() {
    try {
      const projects = await api.projects.list();
      setSaved(projects);
    } catch {}
  }

  useState(() => { loadSaved(); }, []);

  return (
    <div className="p-6 overflow-y-auto h-full">
      <h2 className="text-xl font-bold text-white mb-4">Project Architect</h2>

      <div className="space-y-3 mb-6">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Project name"
          className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
        />
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Project description"
          rows={3}
          className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />
        <input
          value={techStack}
          onChange={(e) => setTechStack(e.target.value)}
          placeholder="Tech stack (comma-separated, e.g. React, FastAPI, SQLite)"
          className="w-full bg-gray-700 text-white rounded px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
        />
        <div className="flex gap-2">
          <button
            onClick={handlePlan}
            disabled={loading || !name || !description}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-medium"
          >
            {loading ? 'Planning...' : 'Generate Architecture'}
          </button>
          <button
            onClick={handleSave}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm"
          >
            Save
          </button>
        </div>
      </div>

      {result && (
        <div className="space-y-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-white font-semibold mb-2">Architecture Plan</h3>
            <pre className="text-gray-300 text-sm whitespace-pre-wrap">{result.plan}</pre>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-white font-semibold mb-2">Folder Structure</h3>
            <pre className="text-gray-300 text-sm whitespace-pre-wrap">{result.folder_structure}</pre>
          </div>
        </div>
      )}

      {saved.length > 0 && (
        <div className="mt-6">
          <h3 className="text-white font-semibold mb-2">Saved Projects</h3>
          <div className="space-y-2">
            {saved.map((p) => (
              <div key={p.id} className="bg-gray-800 rounded-lg p-3">
                <p className="text-white font-medium">{p.name}</p>
                <p className="text-gray-400 text-xs">{p.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
