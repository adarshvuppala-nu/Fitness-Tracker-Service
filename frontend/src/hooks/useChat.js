import { useState, useCallback } from 'react';
import { chatWithAgent, clearMemory } from '../services/api';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (userMessage, options = {}) => {
    setIsLoading(true);
    setError(null);

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: userMessage,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);

    try {
      const response = await chatWithAgent(userMessage, options);

      const assistantMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        tools_used: response.tools_used || [],
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMsg]);
      return response;
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to send message');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearChat = useCallback(async () => {
    try {
      await clearMemory();
      setMessages([]);
      setError(null);
    } catch (err) {
      setError('Failed to clear chat history');
    }
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearChat,
  };
};
