import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { Header } from './components/Header';
import { Dashboard } from './components/Dashboard';
import { Chat } from './components/Chat';
import { Analytics } from './components/Analytics';
import { AppProvider } from './contexts/AppContext';
import { MessageSquare, LayoutDashboard, BarChart3 } from 'lucide-react';

function App() {
  return (
    <AppProvider>
      <Router>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
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

          <Header />

          <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex space-x-8">
                <NavLink to="/" icon={LayoutDashboard} label="Dashboard" />
                <NavLink to="/analytics" icon={BarChart3} label="Analytics" />
                <NavLink to="/chat" icon={MessageSquare} label="AI Chat" />
              </div>
            </div>
          </nav>

          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/chat" element={<Chat />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AppProvider>
  );
}

const NavLink = ({ to, icon: Icon, label }) => {
  return (
    <Link
      to={to}
      className="flex items-center space-x-2 px-3 py-4 border-b-2 border-transparent hover:border-primary-600 dark:hover:border-primary-400 text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-colors"
    >
      <Icon className="w-5 h-5" />
      <span className="font-medium">{label}</span>
    </Link>
  );
};

export default App;
