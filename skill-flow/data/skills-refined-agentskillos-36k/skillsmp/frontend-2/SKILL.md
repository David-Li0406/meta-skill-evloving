---
name: frontend
description: React frontend development patterns. Use when creating pages, components, API integration, or UI features.
tools:
  - read
  - write
  - bash
metadata:
  version: "1.0"
  category: development
  framework: react
---

# Frontend Development Skill

This skill provides patterns and guidance for developing the React frontend.

## Page Component Pattern

When creating a new page:

### 1. Create Page Component

```jsx
// frontend/src/pages/Example.jsx
import { useState, useEffect } from 'react';
import { exampleAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

export default function Example() {
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [filters, setFilters] = useState({ search: '', status: '' });
  const [modalOpen, setModalOpen] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadData(); }, [filters]);

  const loadData = async () => {
    try {
      const res = await exampleAPI.getAll(filters);
      setItems(res.data.items || []);
    } catch (error) {
      console.error('Failed to load:', error);
    } finally {
      setLoading(false);
    }
  };

  const openModal = (item = null) => {
    setEditItem(item);
    setFormData(item || { name: '', amount: 0, status: 'active' });
    setModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editItem) {
        await exampleAPI.update(editItem.id, formData);
      } else {
        await exampleAPI.create(formData);
      }
      setModalOpen(false);
      loadData();
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to save');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this item?')) return;
    try {
      await exampleAPI.delete(id);
      loadData();
    } catch (error) {
      alert('Failed to delete');
    }
  };

  if (loading) return <div className="text-center text-muted">Loading...</div>;

  return (
    <>
      {/* Toolbar */}
      <div className="toolbar">
        <input
          type="text"
          className="form-input"
          placeholder="Search..."
          value={filters.search}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
        />
        <select
          className="form-select"
          value={filters.status}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
        >
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
        {user?.role === 'admin' && (
          <button className="btn btn-primary" onClick={() => openModal()}>
            + New Item
          </button>
        )}
      </div>

      {/* Data Table */}
      <div className="section">
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr className="empty-row">
                  <td colSpan="4">No items found</td>
                </tr>
              ) : items.map(item => (
                <tr key={item.id}>
                  <td className="font-bold">{item.name}</td>
                  <td className="font-mono">${item.amount}</td>
                  <td>
                    <span className={`badge badge-${item.status === 'active' ? 'success' : 'gray'}`}>
                      {item.status}
                    </span>
                  </td>
                  <td>
                    <button className="btn btn-secondary btn-sm" onClick={() => openModal(item)}>
                      Edit
                    </button>
                    {user?.role === 'admin' && (
                      <button className="btn btn-danger btn-sm ml-2" onClick={() => handleDelete(item.id)}>
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {modalOpen && (
        <div className="modal-overlay" onClick={() => setModalOpen(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">{editItem ? 'Edit Item' : 'New Item'}</h3>
              <button className="modal-close" onClick={() => setModalOpen(false)}>&times;</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="form-group">
                  <label className="form-label">Name *</label>
                  <input
                    className="form-input"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Amount</label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-input"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) || 0 })}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">Save</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
```

### 2. Add API Service

```javascript
// In frontend/src/services/api.js
export const exampleAPI = {
  getAll: (params) => api.get('/example', { params }),
  getById: (id) => api.get(`/example/${id}`),
  create: (data) => api.post('/example', data),
  update: (id, data) => api.put(`/example/${id}`, data),
  delete: (id) => api.delete(`/example/${id}`)
};
```

### 3. Add Route

```jsx
// In frontend/src/App.jsx
import Example from './pages/Example';

// Add to routes
<Route path="/example" element={
  <PrivateRoute allowedRoles={['admin', 'supplier']}>
    <Layout><Example /></Layout>
  </PrivateRoute>
} />
```

## Component Patterns

### Stats Card

```jsx
<div className="stat-card">
  <span className="stat-icon">📊</span>
  <div className="stat-content">
    <div className="stat-label">Total Items</div>
    <div className="stat-value success">{count}</div>
  </div>
</div>
```

### Badge

```jsx
<span className={`badge badge-${status}`}>{label}</span>
// status: primary, success, warning, danger, gray
```

### Grid Layout

```jsx
<div className="grid-2">
  <div className="form-group">...</div>
  <div className="form-group">...</div>
</div>

<div className="stats-grid">
  <div className="stat-card">...</div>
  <div className="stat-card">...</div>
</div>
```

## Chart.js Integration

```jsx
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const chartData = {
  labels: data.map(d => d.label),
  datasets: [{
    label: 'Values',
    data: data.map(d => d.value),
    backgroundColor: '#667eea'
  }]
};

<div className="chart-container">
  <Bar data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
</div>
```

## Auth Context Usage

```jsx
import { useAuth } from '../contexts/AuthContext';

function MyComponent() {
  const { user, logout } = useAuth();
  
  // Check role
  if (user?.role === 'admin') {
    // Show admin features
  }
  
  // Logout
  const handleLogout = () => logout();
}
```

## API Error Handling

```jsx
try {
  const res = await api.get('/endpoint');
  setData(res.data);
} catch (error) {
  if (error.response?.status === 401) {
    // Token expired, user will be redirected by interceptor
  } else if (error.response?.status === 403) {
    alert('Permission denied');
  } else {
    alert(error.response?.data?.detail || 'An error occurred');
  }
}
```

## CSS Classes Reference

```css
/* Layout */
.toolbar         /* Horizontal toolbar with flex wrap */
.section         /* Card container with shadow */
.grid-2          /* 2-column grid */
.stats-grid      /* Responsive stats grid */

/* Forms */
.form-group      /* Form field container */
.form-label      /* Field label */
.form-input      /* Text input */
.form-select     /* Dropdown */
.form-textarea   /* Multiline input */

/* Buttons */
.btn             /* Base button */
.btn-primary     /* Purple gradient */
.btn-success     /* Green */
.btn-danger      /* Red */
.btn-secondary   /* Gray */
.btn-sm          /* Small size */

/* Tables */
.table-container /* Scrollable wrapper */
.data-table      /* Styled table */
.empty-row       /* No data message */

/* Modals */
.modal-overlay   /* Backdrop */
.modal           /* Modal container */
.modal-header    /* Title bar */
.modal-body      /* Content */
.modal-footer    /* Action buttons */

/* Text */
.font-bold       /* Bold text */
.font-mono       /* Monospace */
.text-success    /* Green text */
.text-danger     /* Red text */
.text-muted      /* Gray text */
```
