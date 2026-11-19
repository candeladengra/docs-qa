import { useState, useRef, useEffect, FormEvent } from 'react';
import { ChatMessage } from '../types';
import { documentsApi } from '../services/api';
import './ChatInterface.css';

interface Props {
  hasDocuments: boolean;
}

function ChatInterface({ hasDocuments }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading || !hasDocuments) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await documentsApi.query(input);
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Query failed:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your question. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>Ask Questions</h2>
        {!hasDocuments && (
          <p className="no-docs-warning">Upload and process documents first</p>
        )}
      </div>

      <div className="messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>👋 Welcome!</h3>
            <p>Upload PDFs and ask questions about their content.</p>
            <div className="example-questions">
              <p>Try questions like:</p>
              <ul>
                <li>"What are the main topics covered?"</li>
                <li>"Summarize the key findings"</li>
                <li>"What does the document say about X?"</li>
              </ul>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={`message ${message.role}`}>
              <div className="message-content">
                {message.content}
              </div>
              {message.sources && message.sources.length > 0 && (
                <div className="sources">
                  <div className="sources-header">📎 Sources:</div>
                  {message.sources.map((source, idx) => (
                    <div key={idx} className="source-item">
                      <div className="source-header">
                        <strong>{source.document_name}</strong> - Page {source.page_number}
                      </div>
                      <div className="source-content">
                        {source.content.length > 200
                          ? `${source.content.substring(0, 200)}...`
                          : source.content}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))
        )}
        {loading && (
          <div className="message assistant loading-message">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={hasDocuments ? "Ask a question..." : "Upload documents first..."}
          disabled={loading || !hasDocuments}
          className="message-input"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading || !hasDocuments}
          className="send-button"
        >
          {loading ? '⏳' : '📤'}
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;
