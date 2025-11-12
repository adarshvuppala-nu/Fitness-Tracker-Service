import { useState } from 'react';
import { Moon, Sun, Dumbbell, Sparkles, Menu } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';
import { Sidebar } from './Sidebar';

export const Header = ({ onAddWorkout, onAddGoal }) => {
  const { theme, toggleTheme } = useTheme();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <>
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onAddWorkout={onAddWorkout}
        onAddGoal={onAddGoal}
      />

      <header className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border-b border-gray-200/50 dark:border-gray-800/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            {/* Left Side - Menu + Logo */}
            <div className="flex items-center space-x-4 group">
              {/* Menu Button */}
              <button
                onClick={() => setSidebarOpen(true)}
                className="p-2.5 rounded-xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 hover:from-primary-100 hover:to-secondary-100 dark:hover:from-primary-900/30 dark:hover:to-secondary-900/30 border border-gray-300 dark:border-gray-700 shadow-md hover:shadow-lg transition-all duration-300"
                aria-label="Open menu"
              >
                <Menu className="w-5 h-5 text-gray-700 dark:text-gray-300" strokeWidth={2.5} />
              </button>
              {/* Logo with Gradient Background */}
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-primary rounded-2xl blur-lg opacity-50 group-hover:opacity-75 transition-opacity" />
                <div className="relative p-3 bg-gradient-primary rounded-2xl shadow-lg transform group-hover:scale-110 transition-transform duration-300">
                  <Dumbbell className="w-6 h-6 text-white" strokeWidth={2.5} />
                </div>
              </div>

              {/* Brand Text */}
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-2xl font-display font-bold bg-gradient-primary bg-clip-text text-transparent">
                    FitBot AI
                  </h1>
                  <Sparkles className="w-4 h-4 text-primary-500 dark:text-primary-400 animate-pulse" />
                </div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400 tracking-wide">
                  Intelligent Fitness Companion
                </p>
              </div>
            </div>

            {/* Theme Toggle Button */}
            <button
              onClick={toggleTheme}
              className="relative p-3 rounded-xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 hover:from-primary-100 hover:to-secondary-100 dark:hover:from-primary-900/30 dark:hover:to-secondary-900/30 border border-gray-300 dark:border-gray-700 shadow-md hover:shadow-lg transition-all duration-300 group"
              aria-label="Toggle theme"
            >
              <div className="relative z-10">
                {theme === 'light' ? (
                  <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300 group-hover:text-primary-600 transition-colors" />
                ) : (
                  <Sun className="w-5 h-5 text-gray-700 dark:text-gray-300 group-hover:text-accent-400 transition-colors" />
                )}
              </div>
              <div className="absolute inset-0 rounded-xl bg-gradient-primary opacity-0 group-hover:opacity-10 transition-opacity" />
            </button>
          </div>
        </div>
      </header>
    </>
  );
};
