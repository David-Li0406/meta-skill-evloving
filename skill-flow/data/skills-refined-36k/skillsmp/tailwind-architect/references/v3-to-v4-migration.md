# Tailwind v3 vs v4.1 Migration Reference

## Configuration Shift

| Component        | v3 (Legacy)               | v4.1 (Modern)               |
| :-------------- | :------------------------ | :-------------------------- |
| Config File     | tailwind.config.js        | @theme in CSS               |
| Colors          | Hex/RGB in JS             | oklch(...) in CSS vars      |
| Content         | content array             | Auto-detected               |

## Native Utilities

| Feature           | Legacy Plugin                  | v4.1 Native Class           |
| :---------------- | :----------------------------- | :-------------------------- |
| Text Shadow       | tailwindcss-textshadow         | text-shadow-sm              |
| Container Queries | @tailwindcss/container-queries | @container, @md:grid-cols-2 |
| Masks             | tailwind-mask-image            | mask-linear, mask-to-b      |
| 3D Transforms     | tailwindcss-3d                 | perspective-*, rotate-x-*   |
