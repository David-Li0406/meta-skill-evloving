/**
 * Example React component following Pricing App patterns.
 * Shows: hooks, API calls, loading states, error handling, CSS Modules.
 */
import { useState, useEffect } from 'react';
import { usePermisos } from '@/hooks/usePermisos';
import { useDebounce } from '@/hooks/useDebounce';
import api from '@/services/api';
import styles from './ProductosList.module.css';

export default function ProductosList({ onSelect }) {
  // State
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Hooks
  const { tienePermiso } = usePermisos();
  const debouncedSearch = useDebounce(searchTerm, 300);

  // Effects
  useEffect(() => {
    fetchProductos();
  }, [debouncedSearch]);

  // Handlers
  const fetchProductos = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.get('/productos', {
        params: { search: debouncedSearch }
      });
      setProductos(response.data);
    } catch (err) {
      setError('Error al cargar productos');
      console.error('Error fetching productos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (producto) => {
    if (!tienePermiso('productos')) {
      alert('No tienes permiso para ver detalles');
      return;
    }
    onSelect(producto);
  };

  // Render states
  if (loading && productos.length === 0) {
    return <div className={styles.loading}>Cargando productos...</div>;
  }

  if (error && productos.length === 0) {
    return (
      <div className={styles.error}>
        <p>{error}</p>
        <button onClick={fetchProductos}>Reintentar</button>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.searchBar}>
        <input
          type="text"
          placeholder="Buscar productos..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className={styles.searchInput}
        />
      </div>

      {loading && <div className={styles.loadingOverlay}>Actualizando...</div>}

      <div className={styles.list}>
        {productos.length === 0 ? (
          <p className={styles.empty}>No se encontraron productos</p>
        ) : (
          productos.map((producto) => (
            <div
              key={producto.id}
              className={styles.item}
              onClick={() => handleSelect(producto)}
            >
              <span className={styles.codigo}>{producto.codigo}</span>
              <span className={styles.descripcion}>{producto.descripcion}</span>
              <span className={styles.costo}>
                ${(producto.costo / 100).toFixed(2)}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
