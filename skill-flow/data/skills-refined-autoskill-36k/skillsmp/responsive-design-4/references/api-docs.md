# Responsive Design - API Reference

API reference for responsive design patterns in web applications.

## Media Queries

### CSS Media Queries

\`\`\`css
/* Mobile first */
.container {
  width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    width: 750px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    width: 1000px;
  }
}
\`\`\`

### styled-components Media Queries

\`\`\`typescript
const Container = styled.div\`
  width: 100%;

  \${({ theme }) => theme.media.tablet\`
    width: 750px;
  \`}

  \${({ theme }) => theme.media.desktop\`
    width: 1000px;
  \`}
\`;
\`\`\`

## Zest Responsive Arrays

\`\`\`typescript
<Box width={['100%', '50%', '33.33%']} />
// Mobile: 100%, Tablet: 50%, Desktop: 33.33%
\`\`\`

## Window Size Hook

\`\`\`typescript
export function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
}
\`\`\`

## Best Practices

1. Mobile-first approach
2. Use responsive arrays in Zest
3. Test on multiple screen sizes
4. Use relative units (%, rem)
5. Consider touch targets
