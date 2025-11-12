import { useState, useEffect } from 'react';
import { Brain, TrendingUp, Award, AlertTriangle, Lightbulb, Sparkles, RefreshCw } from 'lucide-react';
import { getAIInsights } from '../services/api';
import { useAppContext } from '../contexts/AppContext';
import toast from 'react-hot-toast';

export const AIInsightsCard = () => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const { selectedUser } = useAppContext();

  const fetchInsights = async () => {
    if (!selectedUser) return;

    try {
      setLoading(true);
      const data = await getAIInsights(selectedUser);
      setInsights(data);
    } catch (err) {
      toast.error('Failed to load AI insights');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInsights();
  }, [selectedUser]);

  const getInsightIcon = (type) => {
    switch (type) {
      case 'pattern':
        return TrendingUp;
      case 'achievement':
        return Award;
      case 'warning':
        return AlertTriangle;
      case 'recommendation':
        return Lightbulb;
      default:
        return Sparkles;
    }
  };

  const getInsightColor = (impact) => {
    switch (impact) {
      case 'high':
        return {
          bg: 'from-purple-500/10 via-pink-500/10 to-rose-500/10',
          border: 'border-purple-300 dark:border-purple-600',
          text: 'text-purple-700 dark:text-purple-300',
          badge: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
        };
      case 'medium':
        return {
          bg: 'from-blue-500/10 via-cyan-500/10 to-blue-600/10',
          border: 'border-blue-300 dark:border-blue-600',
          text: 'text-blue-700 dark:text-blue-300',
          badge: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
        };
      default:
        return {
          bg: 'from-gray-500/10 via-gray-400/10 to-gray-500/10',
          border: 'border-gray-300 dark:border-gray-600',
          text: 'text-gray-700 dark:text-gray-300',
          badge: 'bg-gray-100 dark:bg-gray-900/30 text-gray-700 dark:text-gray-300'
        };
    }
  };

  if (loading) {
    return (
      <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 mb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-primary rounded-xl blur-md opacity-50 animate-pulse" />
            <div className="relative p-3 bg-gradient-primary rounded-xl shadow-lg">
              <Brain className="w-5 h-5 text-white animate-pulse" strokeWidth={2} />
            </div>
          </div>
          <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
            AI Insights
          </h3>
        </div>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse bg-gray-100 dark:bg-gray-700 h-24 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (!insights || !insights.insights || insights.insights.length === 0) {
    return (
      <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-primary rounded-xl blur-md opacity-50" />
              <div className="relative p-3 bg-gradient-primary rounded-xl shadow-lg">
                <Brain className="w-5 h-5 text-white" strokeWidth={2} />
              </div>
            </div>
            <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
              AI Insights
            </h3>
          </div>
          <button
            onClick={fetchInsights}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <RefreshCw className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
        </div>
        <div className="text-center py-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-700 mb-4">
            <Brain className="w-8 h-8 text-gray-400" />
          </div>
          <p className="text-gray-500 dark:text-gray-400 font-medium">
            No insights available yet
          </p>
          <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">
            Log more workouts to unlock AI insights!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-primary rounded-xl blur-md opacity-50 animate-pulse-slow" />
            <div className="relative p-3 bg-gradient-primary rounded-xl shadow-lg transform group-hover:scale-110 transition-transform duration-300">
              <Brain className="w-5 h-5 text-white" strokeWidth={2} />
            </div>
          </div>
          <div>
            <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
              AI Insights
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Powered by GPT-4o
            </p>
          </div>
        </div>
        <button
          onClick={fetchInsights}
          disabled={loading}
          className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
          title="Refresh insights"
        >
          <RefreshCw className={`w-5 h-5 text-gray-600 dark:text-gray-400 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Summary Section */}
      {insights.summary && (
        <div className="mb-6 p-4 bg-gradient-to-br from-primary-50 via-secondary-50 to-accent-50 dark:from-gray-700/50 dark:via-gray-800/50 dark:to-gray-700/50 rounded-xl border border-primary-200 dark:border-gray-600">
          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 leading-relaxed">
            {insights.summary}
          </p>
        </div>
      )}

      {/* Insights List */}
      <div className="space-y-3 mb-6">
        {insights.insights.map((insight, index) => {
          const Icon = getInsightIcon(insight.type);
          const colors = getInsightColor(insight.impact);

          return (
            <div
              key={index}
              className={`group/item p-4 bg-gradient-to-br ${colors.bg} rounded-xl hover:shadow-md transition-all duration-300 border ${colors.border} cursor-pointer`}
            >
              <div className="flex items-start gap-3">
                <div className={`flex-shrink-0 p-2 rounded-lg ${colors.badge}`}>
                  <Icon className="w-5 h-5" strokeWidth={2} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-lg">{insight.emoji}</span>
                    <h4 className={`font-bold ${colors.text} text-sm`}>
                      {insight.title}
                    </h4>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                    {insight.message}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Motivation Footer */}
      {insights.motivation && (
        <div className="mt-6 p-4 bg-gradient-primary rounded-xl text-center">
          <p className="text-sm font-bold text-white">
            💪 {insights.motivation}
          </p>
        </div>
      )}
    </div>
  );
};
