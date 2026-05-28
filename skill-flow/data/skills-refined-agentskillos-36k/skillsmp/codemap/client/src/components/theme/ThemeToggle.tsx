import { Icon } from '@components/icons';
import { useTheme } from '@components/theme/ThemeProvider';
import { Button } from '@components/ui/Button';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <Button variant="ghost" size="sm" onClick={toggleTheme} aria-label="Toggle theme">
      {theme === 'dark' ? <Icon.Sun size={16} /> : <Icon.Moon size={16} />}
    </Button>
  );
}
