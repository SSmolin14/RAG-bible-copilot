import React, { useState } from 'react';
import axios from 'axios';
import { Send, BookOpen, User, Bot } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/ask', {
        question: input
      });
      
      const aiMsg: Message = { 
        role: 'assistant', 
        content: response.data.answer,
        sources: response.data.sources 
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      console.error("API Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      <header className="flex items-center gap-2 mb-6 border-b pb-4">
        <BookOpen className="text-indigo-600" />
        <h1 className="text-2xl font-bold italic">Bible Copilot</h1>
      </header>

      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-4 ${
              msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white border shadow-sm'
            }`}>
              <div className="flex items-center gap-2 mb-1 opacity-70">
                {msg.role === 'user' ? <User size={14}/> : <Bot size={14}/>}
                <span className="text-xs font-semibold uppercase">{msg.role}</span>
              </div>
              <p className="text-sm leading-relaxed">{msg.content}</p>
              {msg.sources && (
                <div className="mt-3 pt-2 border-t border-slate-100 italic text-xs opacity-60">
                  Sources: {msg.sources.join(', ')}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && <div className="text-xs animate-pulse">Scholar is thinking...</div>}
      </div>

      <div className="flex gap-2 bg-white p-2 rounded-full border shadow-lg">
        <input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a question about scripture..."
          className="flex-1 px-4 py-2 outline-none text-sm bg-transparent"
        />
        <button 
          onClick={handleSend}
          className="bg-indigo-600 text-white p-2 rounded-full hover:bg-indigo-700 transition"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}

export default App;