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
    <div className="flex flex-col h-[calc(100vh-180px)] bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-high border border-gray-200 dark:border-gray-700 overflow-hidden">
      {/* Chat Header */}
      <div className="flex items-center justify-between p-5 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-primary-50 via-secondary-50 to-accent-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-900">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-primary rounded-xl blur-md opacity-50" />
            <div className="relative p-2.5 bg-gradient-primary rounded-xl shadow-lg">
              <Bot className="w-5 h-5 text-white" strokeWidth={2.5} />
            </div>
          </div>
          <div>
            <h2 className="text-lg font-display font-bold text-gray-900 dark:text-white">
              AI Assistant
            </h2>
            <p className="text-xs text-gray-500 dark:text-gray-400 font-medium">Powered by GPT-4o-mini</p>
          </div>
        </div>
        <button
          onClick={handleClear}
          className="p-2.5 text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 transition-all duration-300 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl"
          title="Clear chat"
        >
          <Trash2 className="w-5 h-5" strokeWidth={2} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-hide">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center px-4 animate-fade-in-up">
            <div className="relative mb-8">
              <div className="absolute inset-0 bg-gradient-primary rounded-full blur-3xl opacity-30 animate-pulse-slow"></div>
              <div className="relative p-6 bg-gradient-primary rounded-3xl shadow-2xl">
                <Bot className="w-16 h-16 text-white relative" strokeWidth={2} />
              </div>
            </div>

            <h2 className="text-3xl font-display font-bold text-gray-900 dark:text-white mb-3">
              Welcome to FitBot AI
            </h2>
            <p className="text-gray-600 dark:text-gray-300 text-base mb-8 max-w-lg font-medium">
              Your intelligent fitness companion. I can help you with workouts, nutrition, goal tracking, and personalized fitness advice.
            </p>

            <div className="w-full max-w-3xl space-y-4">
              <div className="flex items-center justify-center gap-2 mb-4">
                <Sparkles className="w-4 h-4 text-primary-500 animate-pulse" />
                <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider font-bold">
                  Quick Actions
                </p>
                <Sparkles className="w-4 h-4 text-primary-500 animate-pulse" />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Array.isArray(QUICK_ACTIONS) && QUICK_ACTIONS.map((action, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickAction(action.message)}
                    disabled={isLoading}
                    className="group relative flex flex-col items-center p-6 bg-gradient-to-br from-white to-gray-50 dark:from-gray-700 dark:to-gray-800 hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/30 dark:hover:to-secondary-900/30 rounded-2xl border-2 border-gray-200 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500 transition-all duration-300 hover:shadow-xl hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
                  >
                    <div className="absolute inset-0 bg-gradient-primary opacity-0 group-hover:opacity-5 transition-opacity" />
                    <div className="relative z-10 flex flex-col items-center">
                      <div className="p-3 bg-gradient-primary rounded-xl mb-3 group-hover:scale-110 transition-transform shadow-lg">
                        <action.icon className="w-6 h-6 text-white" strokeWidth={2.5} />
                      </div>
                      <span className="text-sm font-bold text-gray-700 dark:text-gray-200 text-center">
                        {action.label}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-10 flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary-100/50 to-secondary-100/50 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-full border border-primary-200 dark:border-primary-800">
              <Sparkles className="w-3.5 h-3.5 text-primary-600 dark:text-primary-400" />
              <span className="text-xs font-bold text-gray-600 dark:text-gray-400">
                Powered by OpenAI GPT-4o-mini with RAG
              </span>
            </div>
          </div>
        )}

        {Array.isArray(messages) && messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.role === 'user' ? 'justify-end' : 'justify-start'
            } animate-slide-up`}
          >
            <div
              className={`flex items-start space-x-3 max-w-[85%] ${
                msg.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
              }`}
            >
              <div
                className={`flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center shadow-md ${
                  msg.role === 'user'
                    ? 'bg-gradient-primary'
                    : 'bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800'
                }`}
              >
                {msg.role === 'user' ? (
                  <User className="w-5 h-5 text-white" strokeWidth={2.5} />
                ) : (
                  <Bot className="w-5 h-5 text-gray-700 dark:text-gray-300" strokeWidth={2.5} />
                )}
              </div>

              <div className="flex flex-col space-y-2">
                <div
                  className={`p-4 rounded-2xl shadow-md ${
                    msg.role === 'user'
                      ? 'bg-gradient-primary text-white'
                      : 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white border border-gray-200 dark:border-gray-600'
                  }`}
                >
                  <p className="text-sm leading-relaxed whitespace-pre-wrap font-medium">{msg.content}</p>

                  {msg.tools_used && Array.isArray(msg.tools_used) && msg.tools_used.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-white/20 dark:border-gray-600/50">
                      <p className="text-xs opacity-75 font-medium">
                        🛠️ Tools: {Array.isArray(msg.tools_used) ? msg.tools_used.map((t) => t.tool).join(', ') : ''}
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
          <div className="flex justify-start animate-slide-up">
            <div className="flex items-center space-x-3 bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-gray-700 dark:to-gray-800 px-5 py-3.5 rounded-2xl border border-primary-200 dark:border-gray-600 shadow-md">
              <Loader2 className="w-5 h-5 animate-spin text-primary-600 dark:text-primary-400" strokeWidth={2.5} />
              <span className="text-sm font-bold text-gray-700 dark:text-gray-300">
                Thinking...
              </span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        className="p-5 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900"
      >
        <div className="flex space-x-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about workouts, nutrition, or goals..."
            className="flex-1 px-5 py-3.5 border-2 border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all font-medium shadow-sm"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-6 py-3.5 bg-gradient-primary hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl transition-all duration-300 font-bold shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-95 flex items-center space-x-2"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" strokeWidth={2.5} />
            ) : (
              <Send className="w-5 h-5" strokeWidth={2.5} />
            )}
            <span className="hidden sm:inline">Send</span>
          </button>
        </div>
      </form>
    </div>
  );
};
