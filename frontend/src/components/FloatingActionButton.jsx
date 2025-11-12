import { useState } from 'react';
import { Plus, X, Dumbbell, Target } from 'lucide-react';

export const FloatingActionButton = ({ onAddWorkout, onAddGoal }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleAction = (action) => {
    setIsOpen(false);
    if (action === 'workout') onAddWorkout?.();
    if (action === 'goal') onAddGoal?.();
  };

  const actions = [
    { icon: Dumbbell, label: 'Add Workout', color: 'from-blue-500 to-cyan-500', action: 'workout' },
    { icon: Target, label: 'Set Goal', color: 'from-purple-500 to-pink-500', action: 'goal' },
  ];

  return (
    <div className="fixed bottom-8 right-8 z-30">
      {/* Action Buttons */}
      {isOpen && (
        <div className="absolute bottom-20 right-0 space-y-3 animate-slide-up">
          {actions.map((action, index) => (
            <div
              key={index}
              className="flex items-center gap-3 animate-slide-in-right"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <span className="px-4 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-xl shadow-lg text-sm font-semibold whitespace-nowrap">
                {action.label}
              </span>
              <button
                onClick={() => handleAction(action.action)}
                className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${action.color} shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-300 flex items-center justify-center`}
              >
                <action.icon className="w-6 h-6 text-white" strokeWidth={2.5} />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Main FAB */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-2xl hover:shadow-3xl transform hover:scale-110 transition-all duration-300 flex items-center justify-center ${
          isOpen ? 'rotate-45' : ''
        }`}
      >
        {isOpen ? (
          <X className="w-7 h-7 text-white" strokeWidth={2.5} />
        ) : (
          <Plus className="w-7 h-7 text-white" strokeWidth={2.5} />
        )}
      </button>

      {/* Pulsing ring */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 opacity-50 animate-ping pointer-events-none" />
    </div>
  );
};
