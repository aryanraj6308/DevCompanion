const API_BASE = '/api';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export const api = {
  chat: {
    send: (body) => request('/chat', { method: 'POST', body }),
    stream: (body, onChunk, onDone, onError) => {
      const params = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      };
      const controller = new AbortController();
      fetch(`${API_BASE}/chat/stream`, { ...params, signal: controller.signal })
        .then(async (res) => {
          const reader = res.body.getReader();
          const decoder = new TextDecoder();
          let buffer = '';
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6));
                  if (data.error) { onError?.(data.error); return; }
                  if (data.done) { onDone?.(data.session_id); return; }
                  if (data.content) onChunk?.(data.content);
                } catch {}
              }
            }
          }
        })
        .catch((err) => {
          if (err.name !== 'AbortError') onError?.(err.message);
        });
      return () => controller.abort();
    },
    history: (body) => request('/chat/history', { method: 'POST', body }),
    providers: () => request('/chat/providers'),
  },
  projects: {
    list: () => request('/projects'),
    create: (body) => request('/projects', { method: 'POST', body }),
    get: (id) => request(`/projects/${id}`),
    delete: (id) => request(`/projects/${id}`, { method: 'DELETE' }),
    architect: (body) => request('/projects/architect', { method: 'POST', body }),
  },
  rag: {
    index: (body) => request('/rag/index', { method: 'POST', body }),
    query: (body) => request('/rag/query', { method: 'POST', body }),
    stats: () => request('/rag/stats'),
  },
  learn: {
    teach: (body) => request('/learn/teach', { method: 'POST', body }),
    explainError: (body) => request('/learn/explain-error', { method: 'POST', body }),
  },
};
