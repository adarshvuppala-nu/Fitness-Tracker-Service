import { useState, useEffect } from 'react';
import { Activity, Target, TrendingUp, Calendar } from 'lucide-react';
import { getUsers, getWorkouts, getGoals } from '../services/api';
import toast from 'react-hot-toast';
import { useAppContext } from '../contexts/AppContext';
import { BMICalculator } from './BMICalculator';

export const Dashboard = () => {
  const [users, setUsers] = useState([]);
  const [workouts, setWorkouts] = useState([]);
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const { selectedUser, setSelectedUser } = useAppContext();

  useEffect(() => {
    fetchData();
  }, []);

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
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    );
  }

  const totalWorkouts = filteredWorkouts.length;
  const totalCalories = filteredWorkouts.reduce(
    (sum, w) => sum + (w.calories_burned || 0),
    0
  );
  const activeGoals = filteredGoals.filter((g) => g.status === 'active').length;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Track your fitness journey and achievements
          </p>
        </div>

        {users.length > 0 && (
          <select
            value={selectedUser || ''}
            onChange={(e) => setSelectedUser(e.target.value)}
            className="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all shadow-sm"
          >
            <option value="">All Users</option>
            {users.map((user) => (
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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg mr-3">
              <Calendar className="w-5 h-5 text-white" />
            </div>
            Recent Workouts
          </h3>
          {filteredWorkouts.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 text-sm">
              No workouts recorded
            </p>
          ) : (
            <div className="space-y-3">
              {filteredWorkouts.slice(0, 5).map((workout) => (
                <div
                  key={workout.id}
                  className="p-4 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-xl hover:shadow-md transition-all border border-gray-200 dark:border-gray-600"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white capitalize">
                        {workout.type}
                      </p>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {workout.date}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {workout.duration} min
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {Math.round(workout.calories_burned)} cal
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
            <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg mr-3">
              <Target className="w-5 h-5 text-white" />
            </div>
            Active Goals
          </h3>
          {filteredGoals.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 text-sm">
              No goals set
            </p>
          ) : (
            <div className="space-y-3">
              {filteredGoals
                .filter((g) => g.status === 'active')
                .slice(0, 5)
                .map((goal) => {
                  const progress =
                    (goal.current_value / goal.target_value) * 100;
                  return (
                    <div
                      key={goal.id}
                      className="p-4 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-xl hover:shadow-md transition-all border border-gray-200 dark:border-gray-600"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <p className="font-medium text-gray-900 dark:text-white capitalize">
                          {goal.goal_type.replace(/_/g, ' ')}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {Math.round(progress)}%
                        </p>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                        <div
                          className="bg-primary-600 dark:bg-primary-400 h-2 rounded-full transition-all"
                          style={{ width: `${Math.min(progress, 100)}%` }}
                        />
                      </div>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
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
  );
};

const StatCard = ({ icon: Icon, title, value, color }) => {
  const gradients = {
    blue: 'from-blue-500 to-cyan-500',
    green: 'from-green-500 to-emerald-500',
    purple: 'from-purple-500 to-pink-500',
  };

  const glowColors = {
    blue: 'shadow-blue-500/50',
    green: 'shadow-green-500/50',
    purple: 'shadow-purple-500/50',
  };

  return (
    <div className="group bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              {title}
            </p>
            <p className="text-4xl font-bold text-gray-900 dark:text-white mt-2 group-hover:scale-105 transition-transform">
              {value}
            </p>
          </div>
          <div className={`relative p-4 rounded-2xl bg-gradient-to-br ${gradients[color]} ${glowColors[color]} shadow-lg group-hover:scale-110 transition-transform`}>
            <Icon className="w-8 h-8 text-white" />
          </div>
        </div>
      </div>
      <div className={`h-1.5 bg-gradient-to-r ${gradients[color]}`}></div>
    </div>
  );
};
