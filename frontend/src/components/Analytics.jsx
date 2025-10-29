import { useState, useEffect } from 'react';
import { LineChart, Line, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Award, Calendar, Download, Flame } from 'lucide-react';
import { getUserAnalytics, getWorkoutStreak, exportUserData } from '../services/api';
import { useAppContext } from '../contexts/AppContext';
import toast from 'react-hot-toast';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [streak, setStreak] = useState(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);
  const { selectedUser } = useAppContext();

  useEffect(() => {
    if (selectedUser) {
      fetchAnalytics();
    }
  }, [selectedUser, days]);

  const fetchAnalytics = async () => {
    if (!selectedUser) {
      toast.error('Please select a user');
      return;
    }

    try {
      setLoading(true);
      const [analyticsData, streakData] = await Promise.all([
        getUserAnalytics(selectedUser, days),
        getWorkoutStreak(selectedUser),
      ]);
      setAnalytics(analyticsData);
      setStreak(streakData);
    } catch (err) {
      toast.error('Failed to load analytics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!selectedUser) {
      toast.error('Please select a user');
      return;
    }

    try {
      const data = await exportUserData(selectedUser);
      const blob = new Blob([data.csv_data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `fitness-data-${data.username}-${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success('Data exported successfully');
    } catch (err) {
      toast.error('Failed to export data');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!selectedUser) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 dark:text-gray-400">Please select a user to view analytics</p>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 dark:text-gray-400">No analytics data available</p>
      </div>
    );
  }

  const workoutTypeData = Object.entries(analytics.workout_by_type).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
  }));

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Analytics</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Comprehensive workout insights and trends
          </p>
        </div>

        <div className="flex gap-3">
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all shadow-sm"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
            <option value={365}>Last year</option>
          </select>

          <button
            onClick={handleExport}
            className="flex items-center gap-2 px-4 py-2.5 bg-primary-600 hover:bg-primary-700 text-white rounded-xl transition-colors shadow-sm"
          >
            <Download className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          icon={TrendingUp}
          title="Total Workouts"
          value={analytics.total_workouts}
          color="blue"
        />
        <StatCard
          icon={Calendar}
          title="Avg Duration"
          value={`${analytics.avg_duration} min`}
          color="green"
        />
        <StatCard
          icon={Flame}
          title="Total Calories"
          value={Math.round(analytics.total_calories)}
          color="orange"
        />
        <StatCard
          icon={Award}
          title="Current Streak"
          value={`${streak?.current_streak || 0} days`}
          color="purple"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
            Weekly Trend
          </h3>
          {analytics.weekly_trend.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analytics.weekly_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis
                  dataKey="week"
                  stroke="#9ca3af"
                  tick={{ fill: '#9ca3af' }}
                />
                <YAxis stroke="#9ca3af" tick={{ fill: '#9ca3af' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: 'none',
                    borderRadius: '0.5rem',
                    color: '#fff'
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="workouts"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  name="Workouts"
                />
                <Line
                  type="monotone"
                  dataKey="duration"
                  stroke="#10b981"
                  strokeWidth={2}
                  name="Duration (min)"
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 dark:text-gray-400 text-sm text-center py-12">
              No trend data available
            </p>
          )}
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
            Workout Distribution
          </h3>
          {workoutTypeData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={workoutTypeData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {workoutTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: 'none',
                    borderRadius: '0.5rem',
                    color: '#fff'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 dark:text-gray-400 text-sm text-center py-12">
              No workout data available
            </p>
          )}
        </div>
      </div>

      {analytics.achievements.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
            <Award className="w-5 h-5 mr-2 text-yellow-500" />
            Achievements
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {analytics.achievements.map((achievement, index) => (
              <div
                key={index}
                className="p-4 bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-gray-700 dark:to-gray-800 rounded-xl border border-yellow-200 dark:border-yellow-700 hover:shadow-md transition-all"
              >
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-yellow-500 rounded-lg">
                    <Award className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 dark:text-white">
                      {achievement.title}
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                      {achievement.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {streak && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
            Workout Streaks
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-gray-700 dark:to-gray-800 rounded-xl">
              <p className="text-sm text-gray-600 dark:text-gray-400">Current Streak</p>
              <p className="text-3xl font-bold text-blue-600 dark:text-blue-400 mt-2">
                {streak.current_streak} days
              </p>
            </div>
            <div className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-gray-700 dark:to-gray-800 rounded-xl">
              <p className="text-sm text-gray-600 dark:text-gray-400">Longest Streak</p>
              <p className="text-3xl font-bold text-purple-600 dark:text-purple-400 mt-2">
                {streak.longest_streak} days
              </p>
            </div>
            <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-gray-700 dark:to-gray-800 rounded-xl">
              <p className="text-sm text-gray-600 dark:text-gray-400">Last Workout</p>
              <p className="text-lg font-bold text-green-600 dark:text-green-400 mt-2">
                {streak.last_workout_date || 'N/A'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const StatCard = ({ icon: Icon, title, value, color }) => {
  const gradients = {
    blue: 'from-blue-500 to-cyan-500',
    green: 'from-green-500 to-emerald-500',
    orange: 'from-orange-500 to-red-500',
    purple: 'from-purple-500 to-pink-500',
  };

  return (
    <div className="group bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-all overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              {title}
            </p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2 group-hover:scale-105 transition-transform">
              {value}
            </p>
          </div>
          <div className={`relative p-3 rounded-2xl bg-gradient-to-br ${gradients[color]} shadow-lg group-hover:scale-110 transition-transform`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
        </div>
      </div>
      <div className={`h-1 bg-gradient-to-r ${gradients[color]}`}></div>
    </div>
  );
};
