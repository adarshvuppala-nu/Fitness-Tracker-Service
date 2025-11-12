import { useState, useEffect } from 'react';
import { Dumbbell, Clock, Activity, Lightbulb, Repeat, RefreshCw } from 'lucide-react';
import { getWorkoutRecommendation } from '../services/api';
import { useAppContext } from '../contexts/AppContext';
import toast from 'react-hot-toast';

export const WorkoutRecommendation = () => {
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const { selectedUser } = useAppContext();

  const fetchRecommendation = async () => {
    if (!selectedUser) return;

    try {
      setLoading(true);
      const data = await getWorkoutRecommendation(selectedUser);
      setRecommendation(data);
    } catch (err) {
      toast.error('Failed to load workout recommendation');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendation();
  }, [selectedUser]);

  const getIntensityColor = (intensity) => {
    switch (intensity?.toLowerCase()) {
      case 'high':
        return {
          bg: 'from-red-500/10 via-orange-500/10 to-red-600/10',
          badge: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300',
          dot: 'bg-red-500'
        };
      case 'moderate':
        return {
          bg: 'from-yellow-500/10 via-amber-500/10 to-yellow-600/10',
          badge: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300',
          dot: 'bg-yellow-500'
        };
      default:
        return {
          bg: 'from-green-500/10 via-emerald-500/10 to-green-600/10',
          badge: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300',
          dot: 'bg-green-500'
        };
    }
  };

  if (loading) {
    return (
      <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 mb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl blur-md opacity-50 animate-pulse" />
            <div className="relative p-3 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl shadow-lg">
              <Dumbbell className="w-5 h-5 text-white animate-pulse" strokeWidth={2} />
            </div>
          </div>
          <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
            Next Workout
          </h3>
        </div>
        <div className="animate-pulse">
          <div className="bg-gray-100 dark:bg-gray-700 h-32 rounded-xl mb-4" />
          <div className="space-y-2">
            <div className="bg-gray-100 dark:bg-gray-700 h-4 rounded w-3/4" />
            <div className="bg-gray-100 dark:bg-gray-700 h-4 rounded w-1/2" />
          </div>
        </div>
      </div>
    );
  }

  if (!recommendation) {
    return null;
  }

  const intensityColors = getIntensityColor(recommendation.intensity);

  return (
    <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl blur-md opacity-50 animate-pulse-slow" />
            <div className="relative p-3 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
              <Dumbbell className="w-5 h-5 text-white" strokeWidth={2} />
            </div>
          </div>
          <div>
            <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
              Next Workout
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              AI-powered recommendation
            </p>
          </div>
        </div>
        <button
          onClick={fetchRecommendation}
          disabled={loading}
          className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
          title="Get new recommendation"
        >
          <RefreshCw className={`w-5 h-5 text-gray-600 dark:text-gray-400 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Main Recommendation Card */}
      <div className={`p-5 bg-gradient-to-br ${intensityColors.bg} rounded-xl border-2 border-gray-200 dark:border-gray-600 mb-4`}>
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h4 className="text-2xl font-display font-bold text-gray-900 dark:text-white mb-2">
              {recommendation.workout_type}
            </h4>
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`inline-flex items-center gap-1.5 px-3 py-1 ${intensityColors.badge} text-sm font-bold rounded-full`}>
                <span className={`w-2 h-2 rounded-full ${intensityColors.dot} animate-pulse`} />
                {recommendation.intensity.charAt(0).toUpperCase() + recommendation.intensity.slice(1)} Intensity
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-sm font-bold rounded-full">
                <Clock className="w-3.5 h-3.5" />
                {recommendation.duration} min
              </span>
            </div>
          </div>
          <div className="p-4 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
            <Activity className="w-8 h-8 text-orange-600 dark:text-orange-400" strokeWidth={2} />
          </div>
        </div>

        {/* Reasoning */}
        {recommendation.reasoning && (
          <div className="p-4 bg-white/80 dark:bg-gray-800/80 rounded-lg backdrop-blur-sm">
            <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
              {recommendation.reasoning}
            </p>
          </div>
        )}
      </div>

      {/* Tips Section */}
      {recommendation.tips && recommendation.tips.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-3">
            <Lightbulb className="w-4 h-4 text-yellow-600 dark:text-yellow-400" />
            <h5 className="font-bold text-sm text-gray-900 dark:text-white">
              Pro Tips
            </h5>
          </div>
          <div className="space-y-2">
            {recommendation.tips.map((tip, index) => (
              <div
                key={index}
                className="flex items-start gap-2 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800"
              >
                <span className="flex-shrink-0 w-5 h-5 flex items-center justify-center rounded-full bg-yellow-200 dark:bg-yellow-800 text-yellow-800 dark:text-yellow-200 text-xs font-bold">
                  {index + 1}
                </span>
                <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                  {tip}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Alternatives Section */}
      {recommendation.alternatives && recommendation.alternatives.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-3">
            <Repeat className="w-4 h-4 text-purple-600 dark:text-purple-400" />
            <h5 className="font-bold text-sm text-gray-900 dark:text-white">
              Alternatives
            </h5>
          </div>
          <div className="flex flex-wrap gap-2">
            {recommendation.alternatives.map((alt, index) => (
              <span
                key={index}
                className="px-3 py-1.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-sm font-semibold rounded-lg border border-purple-200 dark:border-purple-800"
              >
                {alt}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* CTA Button */}
      <button className="w-full mt-6 px-6 py-3 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white rounded-xl transition-all duration-300 font-bold shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-2">
        <Dumbbell className="w-5 h-5" strokeWidth={2} />
        Start This Workout
      </button>
    </div>
  );
};
