import { useState } from 'react';
import { Modal } from './Modal';
import { createGoal } from '../services/api';
import toast from 'react-hot-toast';

export const AddGoalModal = ({ isOpen, onClose, users, onSuccess }) => {
  const [formData, setFormData] = useState({
    user_id: users[0]?.id || '',
    goal_type: 'Weight Loss',
    target_value: 10,
    current_value: 0,
    unit: 'kg',
    deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    status: 'active',
  });
  const [loading, setLoading] = useState(false);

  const goalTypes = [
    { type: 'Weight Loss', unit: 'kg' },
    { type: 'Distance', unit: 'km' },
    { type: 'Calories', unit: 'kcal' },
    { type: 'Workouts', unit: 'sessions' },
    { type: 'Strength Gain', unit: 'kg' },
    { type: 'Endurance', unit: 'minutes' },
  ];

  const handleGoalTypeChange = (goalType) => {
    const selected = goalTypes.find(g => g.type === goalType);
    setFormData({
      ...formData,
      goal_type: goalType,
      unit: selected?.unit || 'units',
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const goalData = {
        user_id: parseInt(formData.user_id),
        goal_type: formData.goal_type,
        target_value: parseFloat(formData.target_value),
        current_value: parseFloat(formData.current_value),
        unit: formData.unit,
        deadline: formData.deadline,
        status: formData.status,
      };

      console.log('Sending goal data:', goalData);
      await createGoal(goalData);

      toast.success('Goal added successfully!');
      onSuccess?.();
      onClose();

      // Reset form
      setFormData({
        user_id: users[0]?.id || '',
        goal_type: 'Weight Loss',
        target_value: 10,
        current_value: 0,
        unit: 'kg',
        deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        status: 'active',
      });
    } catch (error) {
      toast.error('Failed to add goal');
      console.error('Full error:', error);
      console.error('Error response:', error.response?.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Set New Goal">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* User Select */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            User
          </label>
          <select
            value={formData.user_id}
            onChange={(e) => setFormData({ ...formData, user_id: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500"
            required
          >
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </select>
        </div>

        {/* Goal Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Goal Type
          </label>
          <select
            value={formData.goal_type}
            onChange={(e) => handleGoalTypeChange(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500"
            required
          >
            {goalTypes.map((goal) => (
              <option key={goal.type} value={goal.type}>
                {goal.type}
              </option>
            ))}
          </select>
        </div>

        {/* Target Value */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Target Value ({formData.unit})
          </label>
          <input
            type="number"
            value={formData.target_value}
            onChange={(e) => setFormData({ ...formData, target_value: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500"
            min="0"
            step="0.1"
            required
          />
        </div>

        {/* Current Value */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Current Value ({formData.unit})
          </label>
          <input
            type="number"
            value={formData.current_value}
            onChange={(e) => setFormData({ ...formData, current_value: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500"
            min="0"
            step="0.1"
            required
          />
        </div>

        {/* Deadline */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Deadline
          </label>
          <input
            type="date"
            value={formData.deadline}
            onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500"
            required
          />
        </div>

        {/* Buttons */}
        <div className="flex gap-3 pt-4">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="flex-1 px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-600 text-white rounded-lg hover:shadow-lg transition-all disabled:opacity-50"
          >
            {loading ? 'Adding...' : 'Set Goal'}
          </button>
        </div>
      </form>
    </Modal>
  );
};
