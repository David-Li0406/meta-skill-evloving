# Supported Color Formats

## Input Formats

| Format   | Example                                   | Notes                           |
| -------- | ----------------------------------------- | ------------------------------- |
| HEX      | `#f7931a`, `#fff`                         | Standard web hex                |
| RGB      | `rgb(247, 147, 26)`, `247, 147, 26`       | With or without function        |
| RGBA     | `rgba(247, 147, 26, 0.5)`                 | With alpha                      |
| HSL      | `hsl(30, 93%, 54%)`                       | Hue, saturation, lightness      |
| HSLA     | `hsla(30, 93%, 54%, 0.5)`                 | With alpha                      |
| HSV/HSB  | `hsv(30, 89%, 97%)`                       | Hue, saturation, value          |
| LAB      | `lab(70 30 70)`                           | Perceptual color space          |
| LCH      | `lch(70 76 64)`                           | Cylindrical LAB                 |
| oklch    | `oklch(0.75 0.16 55)`                     | Modern perceptual (CSS Color 4) |
| oklab    | `oklab(0.75 0.05 0.15)`                   | Modern perceptual (CSS Color 4) |
| ANSI 16  | `ansi:9`, `ansi:red`, `ansi:bright-green` | Standard terminal colors (0-15) |
| ANSI 256 | `ansi256:208`, `256:214`                  | Extended terminal palette       |

**Note:** CMYK is output-only. Use `convert` command to get CMYK values from other formats.

## ANSI 16 Color Names

| Code | Name    | Code | Name           |
| ---- | ------- | ---- | -------------- |
| 0    | black   | 8    | bright-black   |
| 1    | red     | 9    | bright-red     |
| 2    | green   | 10   | bright-green   |
| 3    | yellow  | 11   | bright-yellow  |
| 4    | blue    | 12   | bright-blue    |
| 5    | magenta | 13   | bright-magenta |
| 6    | cyan    | 14   | bright-cyan    |
| 7    | white   | 15   | bright-white   |

## Output Formats

The `convert` command outputs all of the above formats plus:

- ANSI 24-bit true color escape code
- Closest ANSI 16 match (with indicator if approximate)
- Closest ANSI 256 match (with indicator if approximate)

## Batch Preview Types

Available types for `--types` flag:

- **ANSI**: `24bit`, `16`, `256`
- **Notations**: `hex`, `rgb`, `hsl`, `hsv`, `cmyk`, `lab`, `lch`, `oklch`, `oklab`
