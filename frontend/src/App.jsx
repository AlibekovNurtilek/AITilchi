import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import WelcomeScreen from './components/WelcomeScreen';
import Header from './components/Header';
import Footer from './components/Footer';
import MorphologyPage from './pages/MorphologyPage';
import SyntaxPage from './pages/SyntaxPage';
import CaseInflectionPage from './pages/CaseInflectionPage';
import AboutPage from './pages/AboutPage';
import HomePage from './pages/HomePage';
import './App.css';

// Layout component that conditionally renders header and footer
const Layout = ({ children }) => {
  const location = useLocation();
  const isWelcomeScreen = location.pathname === '/';

  if (isWelcomeScreen) {
    return children;
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow">
        {children}
      </main>
      <Footer />
    </div>
  );
};

function App() {
  return (
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
  );
}

export default App;
