import { useState, useEffect } from 'react';
import { Target, Calendar, TrendingUp, CheckCircle, AlertCircle, Zap } from 'lucide-react';
import { predictGoals } from '../services/api';
import { useAppContext } from '../contexts/AppContext';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

export const GoalPredictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const { selectedUser } = useAppContext();

  useEffect(() => {
    if (!selectedUser) return;

    const fetchPredictions = async () => {
      try {
        setLoading(true);
        const data = await predictGoals(selectedUser);
        setPredictions(data.predictions || []);
      } catch (err) {
        toast.error('Failed to load goal predictions');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, [selectedUser]);

  const getConfidenceBadge = (confidence) => {
    switch (confidence) {
      case 'high':
        return {
          bg: 'bg-green-100 dark:bg-green-900/30',
          text: 'text-green-700 dark:text-green-300',
          label: 'High Confidence'
        };
      case 'medium':
        return {
          bg: 'bg-yellow-100 dark:bg-yellow-900/30',
          text: 'text-yellow-700 dark:text-yellow-300',
          label: 'Medium Confidence'
        };
      default:
        return {
          bg: 'bg-red-100 dark:bg-red-900/30',
          text: 'text-red-700 dark:text-red-300',
          label: 'Low Confidence'
        };
    }
  };

  if (loading) {
    return (
      <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 mb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl blur-md opacity-50 animate-pulse" />
            <div className="relative p-3 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl shadow-lg">
              <Target className="w-5 h-5 text-white animate-pulse" strokeWidth={2} />
            </div>
          </div>
          <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
            Goal Predictions
          </h3>
        </div>
        <div className="space-y-3">
          {[1, 2].map((i) => (
            <div key={i} className="animate-pulse bg-gray-100 dark:bg-gray-700 h-32 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (!predictions || predictions.length === 0) {
    return (
      <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 mb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl blur-md opacity-50" />
            <div className="relative p-3 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl shadow-lg">
              <Target className="w-5 h-5 text-white" strokeWidth={2} />
            </div>
          </div>
          <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
            Goal Predictions
          </h3>
        </div>
        <div className="text-center py-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-700 mb-4">
            <Target className="w-8 h-8 text-gray-400" />
          </div>
          <p className="text-gray-500 dark:text-gray-400 font-medium">
            No active goals to predict
          </p>
          <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">
            Set goals to see AI-powered completion predictions!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl blur-md opacity-50 animate-pulse-slow" />
          <div className="relative p-3 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl shadow-lg transform group-hover:scale-110 transition-transform duration-300">
            <Target className="w-5 h-5 text-white" strokeWidth={2} />
          </div>
        </div>
        <div>
          <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
            Goal Predictions
          </h3>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            AI-powered completion estimates
          </p>
        </div>
      </div>

      {/* Predictions List */}
      <div className="space-y-4">
        {predictions.map((prediction, index) => {
          const confidenceBadge = getConfidenceBadge(prediction.confidence);
          const isOnTrack = prediction.on_track !== false;

          return (
            <div
              key={index}
              className="group/item p-5 bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-700/50 dark:via-gray-800/50 dark:to-gray-700/50 rounded-xl hover:shadow-md transition-all duration-300 border border-gray-200 dark:border-gray-600"
            >
              {/* Goal Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h4 className="font-bold text-gray-900 dark:text-white capitalize mb-1">
                    {prediction.goal_type.replace(/_/g, ' ')}
                  </h4>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className={`px-2 py-0.5 ${confidenceBadge.bg} ${confidenceBadge.text} text-xs font-bold rounded-full`}>
                      {confidenceBadge.label}
                    </span>
                    {isOnTrack ? (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs font-bold rounded-full">
                        <CheckCircle className="w-3 h-3" />
                        On Track
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 text-xs font-bold rounded-full">
                        <AlertCircle className="w-3 h-3" />
                        Behind Schedule
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-display font-bold text-gray-900 dark:text-white">
                    {prediction.progress_percentage.toFixed(0)}%
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {prediction.current_value}/{prediction.target_value} {prediction.unit}
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="relative w-full h-2.5 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden mb-4">
                <div
                  className="absolute inset-y-0 left-0 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${Math.min(prediction.progress_percentage, 100)}%` }}
                />
              </div>

              {/* Prediction Info */}
              <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="flex items-center gap-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <Calendar className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                  <div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Predicted Date</div>
                    <div className="text-sm font-bold text-gray-900 dark:text-white">
                      {format(new Date(prediction.predicted_date), 'MMM dd, yyyy')}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 p-2 bg-cyan-50 dark:bg-cyan-900/20 rounded-lg">
                  <TrendingUp className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
                  <div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Days Remaining</div>
                    <div className="text-sm font-bold text-gray-900 dark:text-white">
                      ~{prediction.days_remaining} days
                    </div>
                  </div>
                </div>
              </div>

              {/* AI Recommendation */}
              {prediction.recommendation && (
                <div className="flex items-start gap-2 p-3 bg-gradient-to-r from-purple-50 via-pink-50 to-orange-50 dark:from-purple-900/20 dark:via-pink-900/20 dark:to-orange-900/20 rounded-lg border border-purple-200 dark:border-purple-700">
                  <Zap className="w-4 h-4 text-purple-600 dark:text-purple-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <div className="text-xs font-bold text-purple-700 dark:text-purple-300 mb-1">
                      AI Recommendation
                    </div>
                    <p className="text-xs text-gray-700 dark:text-gray-300 leading-relaxed">
                      {prediction.recommendation}
                    </p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
