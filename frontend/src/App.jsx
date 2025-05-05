import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import WelcomeScreen from './components/WelcomeScreen';
import './App.css';

function HomePage() {
  return (
    <div className="h-screen flex items-center justify-center bg-white text-black">
      <h2 className="text-3xl font-bold">This is the Home Page</h2>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<WelcomeScreen />} />
        <Route path="/home" element={<HomePage />} />
      </Routes>
    </Router>
  );
}

export default App;
