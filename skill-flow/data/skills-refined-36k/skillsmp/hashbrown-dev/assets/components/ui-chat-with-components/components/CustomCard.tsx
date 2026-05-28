import React from 'react'

export interface CustomCardProps {
  title: string
  children?: React.ReactNode
}

export const CustomCard: React.FC<CustomCardProps> = ({ title, children }) => {
  return (
    <div
      style={{
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '16px',
        margin: '8px 0',
        backgroundColor: '#f9f9f9',
      }}
    >
      <h3 style={{ marginTop: 0, borderBottom: '1px solid #eee', paddingBottom: '8px' }}>
        {title}
      </h3>
      <div>{children}</div>
    </div>
  )
}
