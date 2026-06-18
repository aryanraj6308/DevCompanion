import { useState } from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import ChatBox from './components/Chat/ChatBox';
import ProjectPlanner from './components/ProjectPlanner/ProjectPlanner';
import RAGExplorer from './components/RAGExplorer/RAGExplorer';
import LearningMode from './components/LearningMode/LearningMode';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [provider, setProvider] = useState('ollama');
  const [model, setModel] = useState('');

  return (
    <div className="flex h-screen bg-gray-950">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        provider={provider}
        setProvider={setProvider}
        model={model}
        setModel={setModel}
      />
      <main className="flex-1 flex flex-col">
        <div className="flex-1">
          {activeTab === 'chat' && <ChatBox provider={provider} model={model} />}
          {activeTab === 'projects' && <ProjectPlanner provider={provider} model={model} />}
          {activeTab === 'rag' && <RAGExplorer />}
          {activeTab === 'learn' && <LearningMode provider={provider} model={model} />}
        </div>
      </main>
    </div>
  );
}
