import { NavLink } from 'react-router-dom';

const Header = () => {
  const navLinks = [
    { path: '/morphology', label: 'Морфология' },
    { path: '/syntax', label: 'Синтаксис' },
    { path: '/inflection', label: 'Склонение' },
    { path: '/about', label: 'О нас' },
  ];

  return (
    <header className="bg-gray-900 border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <NavLink to="/home" className="flex items-center">
            <span className="text-2xl font-bold text-white">
              <span className="text-red-500">AI</span>Tilchi
            </span>
          </NavLink>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navLinks.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                className={({ isActive }) =>
                  `text-sm font-medium transition-colors duration-200 ${
                    isActive
                      ? 'text-red-500'
                      : 'text-gray-300 hover:text-white'
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              type="button"
              className="text-gray-400 hover:text-white focus:outline-none"
              aria-label="Open menu"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 