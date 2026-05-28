import { useState, useMemo } from 'react'
import { TkButton, TkInput } from '@takeoff-ui/react'
import { cn } from '@/lib/cn'

export interface Column<T = any> {
  key: string
  label: string
  sortable?: boolean
  width?: string
  align?: 'left' | 'center' | 'right'
  render?: (row: T) => React.ReactNode
}

interface DataTableProps<T = any> {
  data: T[]
  columns: Column<T>[]
  isLoading?: boolean
  enableSearch?: boolean
  enablePagination?: boolean
  pageSize?: number
  onRowClick?: (row: T) => void
  className?: string
}

export function DataTable<T extends Record<string, any>>({
  data = [],
  columns,
  isLoading = false,
  enableSearch = true,
  enablePagination = true,
  pageSize = 10,
  onRowClick,
  className,
}: DataTableProps<T>) {
  const [currentPage, setCurrentPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortColumn, setSortColumn] = useState<string | null>(null)
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc')
  
  // Filter data by search term
  const filteredData = useMemo(() => {
    if (!enableSearch || !searchTerm) return data
    
    return data.filter((row) =>
      Object.values(row).some((value) =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      )
    )
  }, [data, searchTerm, enableSearch])
  
  // Sort data
  const sortedData = useMemo(() => {
    if (!sortColumn) return filteredData
    
    return [...filteredData].sort((a, b) => {
      const aVal = a[sortColumn]
      const bVal = b[sortColumn]
      
      if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1
      if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1
      return 0
    })
  }, [filteredData, sortColumn, sortDirection])
  
  // Paginate data
  const paginatedData = useMemo(() => {
    if (!enablePagination) return sortedData
    
    const startIndex = (currentPage - 1) * pageSize
    return sortedData.slice(startIndex, startIndex + pageSize)
  }, [sortedData, currentPage, pageSize, enablePagination])
  
  const totalPages = Math.ceil(sortedData.length / pageSize)
  
  const handleSort = (column: Column<T>) => {
    if (!column.sortable) return
    
    if (sortColumn === column.key) {
      setSortDirection((prev) => (prev === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortColumn(column.key)
      setSortDirection('asc')
    }
  }
  
  const renderCell = (row: T, column: Column<T>) => {
    if (column.render) {
      return column.render(row)
    }
    
    return String(row[column.key] ?? '-')
  }
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Loading...</span>
      </div>
    )
  }
  
  return (
    <div className={cn('space-y-4', className)}>
      {/* Search */}
      {enableSearch && (
        <div className="flex items-center justify-between">
          <TkInput
            type="search"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value)
              setCurrentPage(1) // Reset to first page on search
            }}
            className="max-w-sm"
          />
        </div>
      )}
      
      {/* Table */}
      <div className="overflow-x-auto rounded-lg border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={cn(
                    'px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider',
                    column.align === 'center' && 'text-center',
                    column.align === 'right' && 'text-right',
                    column.sortable && 'cursor-pointer hover:bg-gray-100 select-none'
                  )}
                  style={{ width: column.width }}
                  onClick={() => handleSort(column)}
                >
                  <div className="flex items-center gap-2">
                    {column.label}
                    {column.sortable && sortColumn === column.key && (
                      <span className="text-blue-600">
                        {sortDirection === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedData.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-6 py-12 text-center text-gray-500"
                >
                  No data available
                </td>
              </tr>
            ) : (
              paginatedData.map((row, rowIndex) => (
                <tr
                  key={rowIndex}
                  className={cn(
                    'hover:bg-gray-50 transition-colors',
                    onRowClick && 'cursor-pointer'
                  )}
                  onClick={() => onRowClick?.(row)}
                >
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className={cn(
                        'px-6 py-4 text-sm text-gray-900 whitespace-nowrap',
                        column.align === 'center' && 'text-center',
                        column.align === 'right' && 'text-right'
                      )}
                    >
                      {renderCell(row, column)}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      
      {/* Pagination */}
      {enablePagination && totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 bg-white border border-gray-200 rounded-lg">
          <div className="text-sm text-gray-700">
            Showing{' '}
            <span className="font-medium">{(currentPage - 1) * pageSize + 1}</span>
            {' to '}
            <span className="font-medium">
              {Math.min(currentPage * pageSize, sortedData.length)}
            </span>
            {' of '}
            <span className="font-medium">{sortedData.length}</span>
            {' results'}
          </div>
          
          <div className="flex items-center gap-2">
            <TkButton
              label="Previous"
              size="small"
              variant="outline"
              onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
            />
            
            <span className="text-sm text-gray-700">
              Page <span className="font-medium">{currentPage}</span> of{' '}
              <span className="font-medium">{totalPages}</span>
            </span>
            
            <TkButton
              label="Next"
              size="small"
              variant="outline"
              onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
            />
          </div>
        </div>
      )}
    </div>
  )
}