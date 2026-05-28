/**
 * Example React Context following Pricing App patterns.
 * Shows: Provider pattern, useContext hook, permission logic.
 */
import { createContext, useContext, useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';

// Permission categories mapping
const PERMISOS_CATEGORIAS = {
  admin: ['config', 'ventas', 'productos', 'reportes', 'usuarios'],
  ventas: ['ventas', 'productos', 'reportes'],
  logistica: ['productos'],
  viewer: []
};

// Create context
const PermisosContext = createContext();

/**
 * PermisosProvider - Manages user permissions based on roles.
 */
export function PermisosProvider({ children }) {
  const { user } = useAuthStore();
  const [permisos, setPermisos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user?.roles) {
      // Calculate permissions from user roles
      const allPermisos = user.roles.flatMap(role => 
        PERMISOS_CATEGORIAS[role] || []
      );
      
      // Remove duplicates
      const uniquePermisos = [...new Set(allPermisos)];
      
      setPermisos(uniquePermisos);
      setLoading(false);
    } else {
      setPermisos([]);
      setLoading(false);
    }
  }, [user]);

  /**
   * Check if user has specific permission.
   * @param {string} categoria - Permission category to check
   * @returns {boolean}
   */
  const tienePermiso = (categoria) => {
    return permisos.includes(categoria);
  };

  /**
   * Check if user has any of the specified permissions.
   * @param {string[]} categorias - Array of permission categories
   * @returns {boolean}
   */
  const tieneAlgunPermiso = (categorias) => {
    return categorias.some(cat => permisos.includes(cat));
  };

  /**
   * Check if user has all specified permissions.
   * @param {string[]} categorias - Array of permission categories
   * @returns {boolean}
   */
  const tieneTodosPermisos = (categorias) => {
    return categorias.every(cat => permisos.includes(cat));
  };

  const value = {
    permisos,
    loading,
    tienePermiso,
    tieneAlgunPermiso,
    tieneTodosPermisos
  };

  return (
    <PermisosContext.Provider value={value}>
      {children}
    </PermisosContext.Provider>
  );
}

/**
 * Hook to access permissions context.
 * @returns {object} Permissions context value
 */
export function usePermisos() {
  const context = useContext(PermisosContext);
  
  if (!context) {
    throw new Error('usePermisos must be used within PermisosProvider');
  }
  
  return context;
}

/**
 * HOC to protect components with permission check.
 * @param {Component} Component - Component to protect
 * @param {string} requiredPermiso - Required permission category
 * @returns {Component}
 */
export function withPermiso(Component, requiredPermiso) {
  return function ProtectedComponent(props) {
    const { tienePermiso } = usePermisos();
    
    if (!tienePermiso(requiredPermiso)) {
      return (
        <div style={{ 
          padding: '2rem', 
          textAlign: 'center',
          color: 'var(--error-text)'
        }}>
          No tienes permiso para acceder a esta sección.
        </div>
      );
    }
    
    return <Component {...props} />;
  };
}

// Usage example:
/*
import { usePermisos, withPermiso } from '@/contexts/PermisosContext';

// Using hook
function AdminPanel() {
  const { tienePermiso } = usePermisos();

  if (!tienePermiso('config')) {
    return <div>Sin acceso</div>;
  }

  return <div>Panel de Configuración</div>;
}

// Using HOC
const ProtectedAdminPanel = withPermiso(AdminPanel, 'config');

// Conditional rendering
function Dashboard() {
  const { tienePermiso } = usePermisos();

  return (
    <div>
      {tienePermiso('reportes') && <ReportesSection />}
      {tienePermiso('ventas') && <VentasSection />}
    </div>
  );
}
*/
