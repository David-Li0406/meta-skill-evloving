# Theme Switching

## Dictionary layout

```
Themes/
  Light.xaml
  Dark.xaml
Styles/
  Typography.xaml
  Controls.xaml
```

## App.xaml merge order

- Base styles first (typography, controls)
- Theme dictionary last (so theme resources override defaults)

## Runtime swap

Replace the theme dictionary in `Application.Current.Resources.MergedDictionaries` by
matching its `Source` path and swapping with the target theme.

## Notes

- Keep theme dictionaries limited to colors and brushes.
- Avoid defining control styles inside theme dictionaries to reduce duplication.
