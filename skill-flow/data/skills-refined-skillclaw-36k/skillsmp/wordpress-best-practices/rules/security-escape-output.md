---
title: Always Escape Output
impact: CRITICAL
impactDescription: Prevents XSS attacks and data corruption
tags: security, xss, escaping, output
---

## Always Escape Output

Unescaped output enables XSS attacks. Always escape data when outputting to HTML, attributes, URLs, or JavaScript.

**Incorrect (unescaped output):**

```php
<?php
// ❌ Direct output - XSS vulnerability
echo $user_input;
echo '<a href="' . $url . '">' . $title . '</a>';
echo '<div class="' . $class . '">' . $content . '</div>';

// ❌ In templates
<h1><?php echo $post->post_title; ?></h1>
<p><?php echo get_the_content(); ?></p>
```

**Correct (escaped output):**

```php
<?php
// ✓ HTML context
echo esc_html($user_input);

// ✓ HTML attributes
echo '<a href="' . esc_url($url) . '">' . esc_html($title) . '</a>';
echo '<div class="' . esc_attr($class) . '">' . wp_kses_post($content) . '</div>';

// ✓ In templates
<h1><?php echo esc_html($post->post_title); ?></h1>
<p><?php echo wp_kses_post(get_the_content()); ?></p>

// ✓ JavaScript context
<script>
var settings = <?php echo wp_json_encode($settings); ?>;
</script>

// ✓ Textarea content
<textarea><?php echo esc_textarea($content); ?></textarea>
```

**Escaping functions reference:**

```php
<?php
// esc_html() - For text content in HTML
echo '<p>' . esc_html($text) . '</p>';

// esc_attr() - For HTML attribute values
echo '<input value="' . esc_attr($value) . '">';

// esc_url() - For URLs (href, src)
echo '<a href="' . esc_url($link) . '">Link</a>';
echo '<img src="' . esc_url($image) . '">';

// esc_textarea() - For textarea content
echo '<textarea>' . esc_textarea($content) . '</textarea>';

// wp_kses_post() - For post content (allows safe HTML)
echo wp_kses_post($post_content);

// wp_kses() - Custom allowed HTML
$allowed = ['a' => ['href' => [], 'title' => []], 'br' => []];
echo wp_kses($html, $allowed);

// wp_json_encode() - For JavaScript data
echo '<script>var data = ' . wp_json_encode($data) . ';</script>';
```

**Late escaping principle:**

```php
<?php
// ✓ Escape at the point of output, not earlier
$title = get_the_title(); // Raw - don't escape here
// ... later in template ...
echo esc_html($title); // Escape here - at output
```

Reference: [Data Validation](https://developer.wordpress.org/plugins/security/data-validation/)
