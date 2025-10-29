import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Trash2, Bot, User, Sparkles, Target, TrendingUp, ThumbsUp, ThumbsDown } from 'lucide-react';
import { useChat } from '../hooks/useChat';
import toast from 'react-hot-toast';

const QUICK_ACTIONS = [
  {
    icon: Target,
    label: 'Create a workout plan',
    message: 'Create a personalized workout plan for weight loss',
  },
  {
    icon: TrendingUp,
    label: 'Track my progress',
    message: 'Show me my workout statistics and progress',
  },
  {
    icon: Sparkles,
    label: 'Nutrition advice',
    message: 'Give me nutrition tips for muscle building',
  },
];

export const Chat = () => {
  const [input, setInput] = useState('');
  const [feedback, setFeedback] = useState({});
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (error) {
      toast.error(error);
    }
  }, [error]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const message = input.trim();
    setInput('');

    try {
      await sendMessage(message);
    } catch (err) {
      console.error('Send message error:', err);
    }
  };

  const handleQuickAction = async (message) => {
    if (isLoading) return;
    try {
      await sendMessage(message);
    } catch (err) {
      console.error('Quick action error:', err);
    }
  };

  const handleClear = async () => {
    if (window.confirm('Clear chat history?')) {
      await clearChat();
      toast.success('Chat cleared');
    }
  };

  const handleFeedback = (messageId, type) => {
    setFeedback((prev) => ({
      ...prev,
      [messageId]: type,
    }));
    toast.success(`Feedback recorded: ${type === 'positive' ? 'Helpful' : 'Not helpful'}`);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-180px)] bg-white dark:bg-gray-800 rounded-lg shadow-lg">
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-2">
          <Bot className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            AI Assistant
          </h2>
        </div>
        <button
          onClick={handleClear}
          className="p-2 text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 transition-colors"
          title="Clear chat"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center px-4">
            <div className="relative mb-6">
              <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-purple-500 rounded-full blur-2xl opacity-20 animate-pulse-slow"></div>
              <Bot className="w-20 h-20 text-primary-600 dark:text-primary-400 relative" />
            </div>

            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Welcome to FitBot AI
            </h2>
            <p className="text-gray-600 dark:text-gray-300 text-sm mb-6 max-w-md">
              Your intelligent fitness companion. I can help you with workouts, nutrition, goal tracking, and personalized fitness advice.
            </p>

            <div className="w-full max-w-2xl space-y-3">
              <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide font-semibold mb-3">
                Quick Actions
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {QUICK_ACTIONS.map((action, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickAction(action.message)}
                    disabled={isLoading}
                    className="group flex flex-col items-center p-4 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 hover:from-primary-50 hover:to-primary-100 dark:hover:from-primary-900 dark:hover:to-primary-800 rounded-xl border border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-600 transition-all duration-200 hover:shadow-lg hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <action.icon className="w-8 h-8 text-primary-600 dark:text-primary-400 mb-2 group-hover:scale-110 transition-transform" />
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-200 text-center">
                      {action.label}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-8 text-xs text-gray-400 dark:text-gray-500">
              Powered by OpenAI GPT-4o-mini with RAG
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`flex items-start space-x-2 max-w-[80%] ${
                msg.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
              }`}
            >
              <div
                className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  msg.role === 'user'
                    ? 'bg-primary-600 dark:bg-primary-500'
                    : 'bg-gray-200 dark:bg-gray-700'
                }`}
              >
                {msg.role === 'user' ? (
                  <User className="w-5 h-5 text-white" />
                ) : (
                  <Bot className="w-5 h-5 text-gray-700 dark:text-gray-300" />
                )}
              </div>

              <div className="flex flex-col">
                <div
                  className={`p-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-primary-600 text-white dark:bg-primary-500'
                      : 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>

                  {msg.tools_used && msg.tools_used.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-gray-300 dark:border-gray-600">
                      <p className="text-xs opacity-75">
                        Tools: {msg.tools_used.map((t) => t.tool).join(', ')}
                      </p>
                    </div>
                  )}
                </div>

                {msg.role === 'assistant' && (
                  <div className="flex gap-2 mt-2">
                    <button
                      onClick={() => handleFeedback(msg.id, 'positive')}
                      className={`p-1.5 rounded-lg transition-colors ${
                        feedback[msg.id] === 'positive'
                          ? 'bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 hover:bg-green-50 dark:hover:bg-green-900/50'
                      }`}
                      title="Helpful"
                    >
                      <ThumbsUp className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => handleFeedback(msg.id, 'negative')}
                      className={`p-1.5 rounded-lg transition-colors ${
                        feedback[msg.id] === 'negative'
                          ? 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 hover:bg-red-50 dark:hover:bg-red-900/50'
                      }`}
                      title="Not helpful"
                    >
                      <ThumbsDown className="w-3.5 h-3.5" />
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-center space-x-2 bg-gray-100 dark:bg-gray-700 p-3 rounded-lg">
              <Loader2 className="w-5 h-5 animate-spin text-primary-600 dark:text-primary-400" />
              <span className="text-sm text-gray-600 dark:text-gray-300">
                Thinking...
              </span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        className="p-4 border-t border-gray-200 dark:border-gray-700"
      >
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about workouts, nutrition, or goals..."
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white rounded-lg transition-colors disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
