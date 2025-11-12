import { useState, useEffect } from 'react';
import { Activity, Target, TrendingUp, Calendar } from 'lucide-react';
import { getUsers, getWorkouts, getGoals } from '../services/api';
import toast from 'react-hot-toast';
import { useAppContext } from '../contexts/AppContext';
import { BMICalculator } from './BMICalculator';
import { MotivationCard } from './MotivationCard';
import { FloatingActionButton } from './FloatingActionButton';
import { AIInsightsCard } from './AIInsightsCard';
import { GoalPredictions } from './GoalPredictions';
import { WorkoutRecommendation } from './WorkoutRecommendation';

export const Dashboard = ({ refreshTrigger, onAddWorkout, onAddGoal }) => {
  const [users, setUsers] = useState([]);
  const [workouts, setWorkouts] = useState([]);
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const { selectedUser, setSelectedUser } = useAppContext();

  useEffect(() => {
    fetchData();
  }, [refreshTrigger]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [usersData, workoutsData, goalsData] = await Promise.all([
        getUsers(0, 10),
        getWorkouts({ limit: 10 }),
        getGoals({ limit: 10 }),
      ]);

      setUsers(usersData);
      setWorkouts(workoutsData);
      setGoals(goalsData);

      if (!selectedUser && usersData.length > 0) {
        setSelectedUser(usersData[0].id);
      }
    } catch (err) {
      toast.error('Failed to load data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredWorkouts = selectedUser
    ? workouts.filter((w) => w.user_id === selectedUser)
    : workouts;

  const filteredGoals = selectedUser
    ? goals.filter((g) => g.user_id === selectedUser)
    : goals;

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 space-y-4 animate-fade-in">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-primary rounded-full blur-2xl opacity-30 animate-pulse-slow" />
          <div className="relative animate-spin rounded-full h-16 w-16 border-4 border-transparent border-t-primary-600 border-r-secondary-600" />
        </div>
        <p className="text-gray-600 dark:text-gray-400 font-semibold">Loading your fitness data...</p>
      </div>
    );
  }

  const totalWorkouts = Array.isArray(filteredWorkouts) ? filteredWorkouts.length : 0;
  const totalCalories = Array.isArray(filteredWorkouts)
    ? filteredWorkouts.reduce((sum, w) => sum + (w.calories_burned || 0), 0)
    : 0;
  const activeGoals = Array.isArray(filteredGoals)
    ? filteredGoals.filter((g) => g.status === 'active').length
    : 0;

  return (
    <>
      <FloatingActionButton
        onAddWorkout={onAddWorkout}
        onAddGoal={onAddGoal}
      />

      <div className="space-y-8 animate-fade-in-up">
        {/* Motivation Card */}
        <MotivationCard />

        {/* Dashboard Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
        <div className="space-y-2">
          <h2 className="text-4xl font-display font-bold text-gray-900 dark:text-white">
            Dashboard
          </h2>
          <p className="text-base font-medium text-gray-600 dark:text-gray-400 flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-gradient-primary animate-pulse" />
            Track your fitness journey and achievements
          </p>
        </div>

        {users.length > 0 && (
          <select
            value={selectedUser || ''}
            onChange={(e) => setSelectedUser(e.target.value)}
            className="px-5 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-800 text-gray-900 dark:text-white font-medium focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:focus:border-primary-400 transition-all shadow-sm hover:shadow-md cursor-pointer"
          >
            <option value="">All Users</option>
            {Array.isArray(users) && users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </select>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          icon={Activity}
          title="Total Workouts"
          value={totalWorkouts}
          color="blue"
        />
        <StatCard
          icon={TrendingUp}
          title="Calories Burned"
          value={Math.round(totalCalories)}
          color="green"
        />
        <StatCard
          icon={Target}
          title="Active Goals"
          value={activeGoals}
          color="purple"
        />
      </div>

      {/* AI-Powered Features Section */}
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <div className="h-px flex-1 bg-gradient-primary opacity-20" />
          <h2 className="text-2xl font-display font-bold text-gray-900 dark:text-white">
            🤖 AI-Powered Intelligence
          </h2>
          <div className="h-px flex-1 bg-gradient-primary opacity-20" />
        </div>

        {/* Top Row: Insights and Recommendation */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <AIInsightsCard />
          <WorkoutRecommendation />
        </div>

        {/* Bottom Row: Goal Predictions */}
        <GoalPredictions />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Workouts Card */}
        <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-blue-cyan rounded-xl blur-md opacity-50" />
              <div className="relative p-3 bg-gradient-blue-cyan rounded-xl shadow-lg">
                <Calendar className="w-5 h-5 text-white" strokeWidth={2} />
              </div>
            </div>
            <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
              Recent Workouts
            </h3>
          </div>

          {filteredWorkouts.length === 0 ? (
            <div className="text-center py-12">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-700 mb-4">
                <Calendar className="w-8 h-8 text-gray-400" />
              </div>
              <p className="text-gray-500 dark:text-gray-400 font-medium">
                No workouts recorded yet
              </p>
              <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">
                Start tracking your fitness journey!
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {Array.isArray(filteredWorkouts) && filteredWorkouts.slice(0, 5).map((workout) => (
                <div
                  key={workout.id}
                  className="group/item p-4 bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-700/50 dark:via-gray-800/50 dark:to-gray-700/50 rounded-xl hover:shadow-md transition-all duration-300 border border-gray-200 dark:border-gray-600 hover:border-blue-300 dark:hover:border-blue-600 cursor-pointer"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-900 dark:text-white capitalize group-hover/item:text-blue-600 dark:group-hover/item:text-blue-400 transition-colors">
                        {workout.type}
                      </p>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                        {workout.date}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-bold text-gray-900 dark:text-white">
                        {workout.duration} min
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                        {Math.round(workout.calories_burned)} cal
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Active Goals Card */}
        <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-purple-pink rounded-xl blur-md opacity-50" />
              <div className="relative p-3 bg-gradient-purple-pink rounded-xl shadow-lg">
                <Target className="w-5 h-5 text-white" strokeWidth={2} />
              </div>
            </div>
            <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
              Active Goals
            </h3>
          </div>

          {filteredGoals.length === 0 ? (
            <div className="text-center py-12">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-700 mb-4">
                <Target className="w-8 h-8 text-gray-400" />
              </div>
              <p className="text-gray-500 dark:text-gray-400 font-medium">
                No goals set yet
              </p>
              <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">
                Set your first goal and start achieving!
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {Array.isArray(filteredGoals) && filteredGoals
                .filter((g) => g.status === 'active')
                .slice(0, 5)
                .map((goal) => {
                  const progress =
                    (goal.current_value / goal.target_value) * 100;
                  return (
                    <div
                      key={goal.id}
                      className="group/item p-4 bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-700/50 dark:via-gray-800/50 dark:to-gray-700/50 rounded-xl hover:shadow-md transition-all duration-300 border border-gray-200 dark:border-gray-600 hover:border-purple-300 dark:hover:border-purple-600 cursor-pointer"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <p className="font-semibold text-gray-900 dark:text-white capitalize group-hover/item:text-purple-600 dark:group-hover/item:text-purple-400 transition-colors">
                          {goal.goal_type.replace(/_/g, ' ')}
                        </p>
                        <span className="px-2.5 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs font-bold rounded-full">
                          {Math.round(progress)}%
                        </span>
                      </div>

                      {/* Progress Bar */}
                      <div className="relative w-full h-2.5 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden mb-2">
                        <div
                          className="absolute inset-y-0 left-0 bg-gradient-purple-pink rounded-full transition-all duration-500 ease-out"
                          style={{ width: `${Math.min(progress, 100)}%` }}
                        />
                      </div>

                      <p className="text-xs font-medium text-gray-500 dark:text-gray-400">
                        {goal.current_value} / {goal.target_value} {goal.unit}
                      </p>
                    </div>
                  );
                })}
            </div>
          )}
        </div>

          <BMICalculator />
        </div>
      </div>
    </>
  );
};

const StatCard = ({ icon: Icon, title, value, color }) => {
  const gradients = {
    blue: 'from-blue-500 via-cyan-500 to-blue-600',
    green: 'from-green-500 via-emerald-500 to-teal-600',
    purple: 'from-purple-500 via-pink-500 to-rose-500',
  };

  const bgGradients = {
    blue: 'from-blue-500/10 via-cyan-500/10 to-blue-600/10',
    green: 'from-green-500/10 via-emerald-500/10 to-teal-600/10',
    purple: 'from-purple-500/10 via-pink-500/10 to-rose-500/10',
  };

  const iconBg = {
    blue: 'from-blue-500 to-cyan-500',
    green: 'from-green-500 to-emerald-500',
    purple: 'from-purple-500 to-pink-500',
  };

  return (
    <div className="group relative bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-500 overflow-hidden card-hover border border-gray-200 dark:border-gray-700">
      {/* Animated Background Gradient */}
      <div className={`absolute inset-0 bg-gradient-to-br ${bgGradients[color]} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />

      {/* Content */}
      <div className="relative p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1 space-y-2">
            <p className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              {title}
            </p>
            <p className="text-4xl font-display font-bold text-gray-900 dark:text-white group-hover:scale-105 transition-transform duration-300">
              {value}
            </p>
          </div>

          {/* Icon with Glow Effect */}
          <div className="relative">
            <div className={`absolute inset-0 bg-gradient-to-br ${iconBg[color]} rounded-2xl blur-xl opacity-50 group-hover:opacity-75 animate-pulse-slow`} />
            <div className={`relative p-4 rounded-2xl bg-gradient-to-br ${iconBg[color]} shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
              <Icon className="w-7 h-7 text-white" strokeWidth={2} />
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Accent Bar */}
      <div className={`h-1 bg-gradient-to-r ${gradients[color]} group-hover:h-1.5 transition-all duration-300`} />
    </div>
  );
};
