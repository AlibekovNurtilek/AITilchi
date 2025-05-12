import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import WelcomeScreen from './components/WelcomeScreen';
import Header from './components/Header';
import Footer from './components/Footer';
import MorphologyPage from './pages/MorphologyPage';
import SyntaxPage from './pages/SyntaxPage';
import CaseInflectionPage from './pages/CaseInflectionPage';
import AboutPage from './pages/AboutPage';
import HomePage from './pages/HomePage';
import ChatWidget from './components/ChatWidget';
import { ThemeProvider } from './context/ThemeContext';
import './App.css';

// Layout component that conditionally renders header and footer
const Layout = ({ children }) => {
  const location = useLocation();
  const isWelcomeScreen = location.pathname === '/';

  if (isWelcomeScreen) {
    return children;
  }

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-[#1a1a1a] transition-colors duration-200">
      <Header />
      <main className="flex-grow">
        {children}
      </main>
      <Footer />
      <ChatWidget />
    </div>
  );
};

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<WelcomeScreen />} />
            <Route path="/home" element={<HomePage />} />
            <Route path="/morphology" element={<MorphologyPage />} />
            <Route path="/syntax" element={<SyntaxPage />} />
            <Route path="/inflection" element={<CaseInflectionPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
