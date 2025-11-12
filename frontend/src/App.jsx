import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { Header } from './components/Header';
import { Dashboard } from './components/Dashboard';
import { Chat } from './components/Chat';
import { Analytics } from './components/Analytics';
import { AnimatedBackground } from './components/AnimatedBackground';
import { AddWorkoutModal } from './components/AddWorkoutModal';
import { AddGoalModal } from './components/AddGoalModal';
import { AppProvider } from './contexts/AppContext';
import { MessageSquare, LayoutDashboard, BarChart3 } from 'lucide-react';
import { getUsers } from './services/api';

const NavLink = ({ to, icon: Icon, label }) => {
  const location = window.location;
  const isActive = location.pathname === to;

  return (
    <Link
      to={to}
      className={`group relative flex items-center space-x-2 px-4 py-4 transition-all duration-300 ${
        isActive
          ? 'text-primary-600 dark:text-primary-400'
          : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'
      }`}
    >
      <Icon className={`w-5 h-5 transition-transform duration-300 ${
        isActive ? 'scale-110' : 'group-hover:scale-110'
      }`} strokeWidth={isActive ? 2.5 : 2} />
      <span className="font-semibold">{label}</span>

      {/* Active indicator */}
      {isActive && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-primary rounded-t-full" />
      )}

      {/* Hover indicator */}
      {!isActive && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-primary rounded-t-full scale-x-0 group-hover:scale-x-100 transition-transform duration-300" />
      )}
    </Link>
  );
};

function AppContent() {
  const [showWorkoutModal, setShowWorkoutModal] = useState(false);
  const [showGoalModal, setShowGoalModal] = useState(false);
  const [users, setUsers] = useState([]);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    const usersData = await getUsers(0, 10);
    setUsers(usersData);
  };

  const handleDataRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <Router>
      <div className="min-h-screen relative transition-colors">
        <AnimatedBackground />

        <Toaster
          position="top-right"
          toastOptions={{
            duration: 3000,
            style: {
              background: 'var(--bg-primary)',
              color: 'var(--text-primary)',
            },
          }}
        />

        <AddWorkoutModal
          isOpen={showWorkoutModal}
          onClose={() => setShowWorkoutModal(false)}
          users={users}
          onSuccess={() => {
            fetchUsers();
            handleDataRefresh();
          }}
        />

        <AddGoalModal
          isOpen={showGoalModal}
          onClose={() => setShowGoalModal(false)}
          users={users}
          onSuccess={() => {
            fetchUsers();
            handleDataRefresh();
          }}
        />

        <Header
          onAddWorkout={() => setShowWorkoutModal(true)}
          onAddGoal={() => setShowGoalModal(true)}
        />

        <nav className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border-b border-gray-200 dark:border-gray-800 sticky top-[73px] z-40">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex space-x-2">
              <NavLink to="/" icon={LayoutDashboard} label="Dashboard" />
              <NavLink to="/analytics" icon={BarChart3} label="Analytics" />
              <NavLink to="/chat" icon={MessageSquare} label="AI Chat" />
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard refreshTrigger={refreshTrigger} onAddWorkout={() => setShowWorkoutModal(true)} onAddGoal={() => setShowGoalModal(true)} />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
