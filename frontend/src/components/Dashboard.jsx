import { useState, useEffect } from 'react';
import { Activity, Target, TrendingUp, Calendar } from 'lucide-react';
import { getUsers, getWorkouts, getGoals } from '../services/api';
import toast from 'react-hot-toast';
import { useAppContext } from '../contexts/AppContext';

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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h2>

        {users.length > 0 && (
          <select
            value={selectedUser || ''}
            onChange={(e) => setSelectedUser(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
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
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <Calendar className="w-5 h-5 mr-2 text-primary-600 dark:text-primary-400" />
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
                  className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
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

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <Target className="w-5 h-5 mr-2 text-primary-600 dark:text-primary-400" />
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
                      className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
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
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, title, value, color }) => {
  const colorClasses = {
    blue: 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300',
    green: 'bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-300',
    purple:
      'bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-300',
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
            {value}
          </p>
        </div>
        <div className={`p-3 rounded-full ${colorClasses[color]}`}>
          <Icon className="w-8 h-8" />
        </div>
      </div>
    </div>
  );
};
