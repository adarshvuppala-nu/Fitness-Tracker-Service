import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  X,
  User,
  Dumbbell,
  Target,
  Calendar,
  Settings,
  Download,
  LogOut,
  Plus,
  TrendingUp,
  Award,
  Activity
} from 'lucide-react';
import { getWorkouts, getGoals, getWorkoutStreak } from '../services/api';
import { useAppContext } from '../contexts/AppContext';

export const Sidebar = ({ isOpen, onClose, onAddWorkout, onAddGoal }) => {
  const navigate = useNavigate();
  const { selectedUser } = useAppContext();
  const [stats, setStats] = useState({
    workouts: 0,
    goals: 0,
    streak: 0,
    badges: 0
  });

  useEffect(() => {
    if (isOpen && selectedUser) {
      fetchStats();
    }
  }, [isOpen, selectedUser]);

  const fetchStats = async () => {
    try {
      const [workoutsData, goalsData, streakData] = await Promise.all([
        getWorkouts({ limit: 1000 }),
        getGoals({ limit: 100 }),
        getWorkoutStreak(selectedUser).catch(() => ({ current_streak: 0 }))
      ]);

      // Filter by selected user on the frontend
      const userWorkouts = selectedUser
        ? workoutsData.filter(w => w.user_id === selectedUser)
        : workoutsData;

      const userGoals = selectedUser
        ? goalsData.filter(g => g.user_id === selectedUser)
        : goalsData;

      setStats({
        workouts: userWorkouts?.length || 0,
        goals: userGoals?.filter(g => g.status === 'active').length || 0,
        streak: streakData?.current_streak || 0,
        badges: 0
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };
  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 transition-opacity duration-300"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed top-0 left-0 h-full w-80 bg-white dark:bg-gray-900 shadow-2xl z-50 transform transition-transform duration-300 ease-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-800 bg-gradient-to-br from-primary-50 via-secondary-50 to-accent-50 dark:from-gray-800 dark:via-gray-900 dark:to-gray-800">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-display font-bold text-gray-900 dark:text-white">
                Menu
              </h2>
              <button
                onClick={onClose}
                className="p-2 rounded-xl hover:bg-white/50 dark:hover:bg-gray-700/50 transition-colors"
              >
                <X className="w-5 h-5 text-gray-600 dark:text-gray-400" strokeWidth={2.5} />
              </button>
            </div>

            {/* Profile Section */}
            <div className="flex items-center gap-4 p-4 bg-white/60 dark:bg-gray-800/60 rounded-2xl backdrop-blur-sm">
              <div className="w-14 h-14 rounded-2xl bg-gradient-primary flex items-center justify-center shadow-lg">
                <User className="w-7 h-7 text-white" strokeWidth={2.5} />
              </div>
              <div>
                <h3 className="font-bold text-gray-900 dark:text-white">Fitness User</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Level 5 Athlete</p>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-800">
            <p className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
              Quick Stats
            </p>
            <div className="grid grid-cols-2 gap-3">
              <StatBadge icon={Activity} label="Workouts" value={stats.workouts} color="blue" />
              <StatBadge icon={TrendingUp} label="Streak" value={`${stats.streak}d`} color="orange" />
              <StatBadge icon={Target} label="Goals" value={stats.goals} color="purple" />
              <StatBadge icon={Award} label="Badges" value={stats.badges} color="green" />
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex-1 p-6 overflow-y-auto">
            <p className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
              Quick Actions
            </p>
            <div className="space-y-2">
              <ActionButton
                icon={Plus}
                label="Add Workout"
                onClick={() => {
                  onClose();
                  onAddWorkout?.();
                }}
              />
              <ActionButton
                icon={Target}
                label="Set New Goal"
                onClick={() => {
                  onClose();
                  onAddGoal?.();
                }}
              />
              <ActionButton
                icon={Calendar}
                label="View Calendar"
                onClick={() => {
                  onClose();
                  navigate('/');
                }}
              />
              <ActionButton
                icon={Download}
                label="Export Data"
                onClick={() => console.log('Export data')}
              />
            </div>

            {/* Settings */}
            <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-800">
              <p className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
                Settings
              </p>
              <div className="space-y-2">
                <ActionButton
                  icon={Settings}
                  label="Preferences"
                  onClick={() => console.log('Settings')}
                />
                <ActionButton
                  icon={LogOut}
                  label="Logout"
                  variant="danger"
                  onClick={() => console.log('Logout')}
                />
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-gray-200 dark:border-gray-800">
            <div className="text-center text-xs text-gray-500 dark:text-gray-400">
              <p className="font-semibold">FitBot AI v1.0</p>
              <p className="mt-1">© 2025 All rights reserved</p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

const StatBadge = ({ icon: Icon, label, value, color }) => {
  const colors = {
    blue: 'from-blue-500 to-cyan-500',
    orange: 'from-orange-500 to-red-500',
    purple: 'from-purple-500 to-pink-500',
    green: 'from-green-500 to-emerald-500',
  };

  return (
    <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl">
      <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${colors[color]} flex items-center justify-center mb-2`}>
        <Icon className="w-4 h-4 text-white" strokeWidth={2.5} />
      </div>
      <p className="text-lg font-display font-bold text-gray-900 dark:text-white">{value}</p>
      <p className="text-xs text-gray-600 dark:text-gray-400">{label}</p>
    </div>
  );
};

const ActionButton = ({ icon: Icon, label, onClick, variant = 'default' }) => {
  const styles = variant === 'danger'
    ? 'hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400'
    : 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300';

  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all duration-200 ${styles}`}
    >
      <Icon className="w-5 h-5" strokeWidth={2} />
      <span className="font-semibold">{label}</span>
    </button>
  );
};
