import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Rocket, History, Home, FlaskConical } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/history', label: 'History', icon: History },
  ];

  return (
    <nav
      className="sticky top-0 z-50"
      style={{
        background: 'rgba(8,11,24,0.82)',
        backdropFilter: 'blur(20px) saturate(180%)',
        WebkitBackdropFilter: 'blur(20px) saturate(180%)',
        borderBottom: '1px solid rgba(99,102,241,0.15)',
        boxShadow: '0 4px 32px rgba(0,0,0,0.4), 0 1px 0 rgba(129,140,248,0.08) inset',
      }}
    >
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">

          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div
              className="relative w-10 h-10 rounded-xl flex items-center justify-center"
              style={{
                background: 'linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.2))',
                border: '1px solid rgba(99,102,241,0.35)',
                boxShadow: '0 0 14px rgba(99,102,241,0.25)',
                transition: 'box-shadow 0.3s',
              }}
            >
              <Rocket
                className="w-5 h-5 text-indigo-400"
                style={{ filter: 'drop-shadow(0 0 6px rgba(129,140,248,0.7))' }}
              />
              <FlaskConical
                className="w-3 h-3 text-purple-400 absolute -top-1 -right-1"
                style={{ filter: 'drop-shadow(0 0 4px rgba(167,139,250,0.8))' }}
              />
            </div>
            <div className="flex flex-col leading-none">
              <span
                className="text-lg font-bold gradient-text"
                style={{ fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.01em' }}
              >
                Exoplanet
              </span>
              <span className="text-xs font-semibold" style={{ color: 'rgba(139,92,246,0.9)', letterSpacing: '0.12em' }}>
                INTELLIGENCE
              </span>
            </div>
          </Link>

          {/* Navigation Links */}
          <div
            className="flex items-center gap-1 p-1 rounded-xl"
            style={{
              background: 'rgba(8,11,24,0.6)',
              border: '1px solid rgba(99,102,241,0.15)',
            }}
          >
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className="relative flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-220 font-medium text-sm"
                  style={
                    isActive
                      ? {
                        background: 'linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.25))',
                        color: '#a5b4fc',
                        border: '1px solid rgba(99,102,241,0.3)',
                        boxShadow: '0 0 12px rgba(99,102,241,0.2)',
                      }
                      : {
                        color: 'rgba(139,156,195,0.8)',
                        border: '1px solid transparent',
                      }
                  }
                >
                  <Icon
                    className="w-4 h-4"
                    style={isActive ? { filter: 'drop-shadow(0 0 5px rgba(129,140,248,0.7))' } : {}}
                  />
                  <span>{item.label}</span>
                  {isActive && (
                    <span
                      className="absolute bottom-0.5 left-1/2 -translate-x-1/2 w-1.5 h-1.5 rounded-full"
                      style={{ background: 'rgba(129,140,248,0.9)', boxShadow: '0 0 6px rgba(129,140,248,0.8)' }}
                    />
                  )}
                </Link>
              );
            })}
          </div>

        </div>
      </div>

      {/* Gradient bottom border */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: '10%',
          right: '10%',
          height: '1px',
          background: 'linear-gradient(90deg, transparent, rgba(99,102,241,0.5), rgba(139,92,246,0.5), transparent)',
        }}
      />
    </nav>
  );
};

export default Navbar;
