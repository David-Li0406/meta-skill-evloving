<?php
/**
 * TheHUB Theme Loader
 * Single source of truth for theme color variables from /uploads/branding.json
 * Outputs CSS variables for dark/light modes.
 */

if (headers_sent()) {
  // Still ok to echo <style>, but keep this guard minimal
}

$root = dirname(__DIR__); // project root if /includes is directly under root
$brandingPath = $root . '/uploads/branding.json';

$branding = null;
if (is_readable($brandingPath)) {
  $json = file_get_contents($brandingPath);
  $data = json_decode($json, true);
  if (is_array($data)) $branding = $data;
}

// Helper: allow only CSS custom properties and safe-ish values
function hub_is_valid_css_var_name(string $k): bool {
  return (strpos($k, '--') === 0) && preg_match('/^--[a-zA-Z0-9_-]+$/', $k);
}
function hub_is_valid_css_value(string $v): bool {
  $v = trim($v);
  if ($v === '') return false;
  // Permit common CSS color formats + keywords (kept simple on purpose)
  return (bool) preg_match('/^(#[0-9A-Fa-f]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-zA-Z]+)$/', $v);
}
function hub_css_escape(string $v): string {
  return htmlspecialchars($v, ENT_QUOTES, 'UTF-8');
}

$darkCss = '';
$lightCss = '';

if (is_array($branding) && !empty($branding['colors']) && is_array($branding['colors'])) {
  $colors = $branding['colors'];

  // New format: colors.dark + colors.light
  if (isset($colors['dark']) || isset($colors['light'])) {
    if (!empty($colors['dark']) && is_array($colors['dark'])) {
      foreach ($colors['dark'] as $k => $v) {
        if (hub_is_valid_css_var_name((string)$k) && hub_is_valid_css_value((string)$v)) {
          $darkCss .= $k . ':' . hub_css_escape((string)$v) . ';';
        }
      }
    }
    if (!empty($colors['light']) && is_array($colors['light'])) {
      foreach ($colors['light'] as $k => $v) {
        if (hub_is_valid_css_var_name((string)$k) && hub_is_valid_css_value((string)$v)) {
          $lightCss .= $k . ':' . hub_css_escape((string)$v) . ';';
        }
      }
    }
  } else {
    // Legacy flat format: treat as dark
    foreach ($colors as $k => $v) {
      if (hub_is_valid_css_var_name((string)$k) && hub_is_valid_css_value((string)$v)) {
        $darkCss .= $k . ':' . hub_css_escape((string)$v) . ';';
      }
    }
  }
}

if ($darkCss === '' && $lightCss === '') {
  // Nothing to output; do not emit empty style
  return;
}

echo "<style id=\"hub-theme-loader\">\n";
if ($darkCss !== '') {
  // Dark is the default baseline
  echo ":root,html[data-theme=\"dark\"]{" . $darkCss . "}\n";
}
if ($lightCss !== '') {
  echo "html[data-theme=\"light\"]{" . $lightCss . "}\n";
}
echo "</style>\n";
