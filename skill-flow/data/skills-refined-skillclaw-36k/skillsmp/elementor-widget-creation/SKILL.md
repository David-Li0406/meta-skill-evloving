---
name: Elementor Widget Creation
description: Create new Elementor widgets following SOMA theme standards with complete file structure, tests, and translations
---

# Elementor Widget Creation Skill

This skill guides the creation of new Elementor widgets for the SOMA WordPress theme, ensuring compliance with all project standards and conventions.

## When to Use This Skill

Use this skill when you need to:
- Create a new Elementor widget from scratch
- Add controls to existing widgets
- Create widget-specific CSS files
- Write tests for Elementor widgets
- Add translations for widget strings

## Widget Development Workflow

### Step 1: Create Widget Class

**Location**: `wp-content/themes/soma/includes/Elementor/Widgets/{WidgetName}.php`

```php
<?php
/**
 * {WidgetName} Elementor Widget.
 *
 * @package    Soma
 * @subpackage Elementor\Widgets
 * @since      3.x.x
 */

declare(strict_types=1);

namespace Soma\Elementor\Widgets;

use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Typography;
use Elementor\Core\Kits\Documents\Tabs\Global_Colors;
use Elementor\Core\Kits\Documents\Tabs\Global_Typography;

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * {WidgetName} widget for displaying {description}.
 *
 * @since 3.x.x
 */
class {WidgetName} extends Widget_Base {

    /**
     * Get widget name.
     *
     * @return string Widget name.
     */
    public function get_name(): string {
        return 'soma-{widget-slug}';
    }

    /**
     * Get widget title.
     *
     * @return string Widget title.
     */
    public function get_title(): string {
        return __( 'SOMA {Widget Title}', 'soma' );
    }

    /**
     * Get widget icon.
     *
     * @return string Widget icon.
     */
    public function get_icon(): string {
        return 'eicon-{icon-name}';
    }

    /**
     * Get widget categories.
     *
     * @return array Widget categories.
     */
    public function get_categories(): array {
        return [ 'soma' ];
    }

    /**
     * Get style dependencies.
     *
     * @return array Style dependencies.
     */
    public function get_style_depends(): array {
        return [ 'soma-{widget-slug}' ];
    }

    /**
     * Get script dependencies.
     *
     * @return array Script dependencies.
     */
    public function get_script_depends(): array {
        return [];
    }

    /**
     * Register widget controls.
     *
     * @return void
     */
    protected function register_controls(): void {
        // Content Section
        $this->start_controls_section(
            'content_section',
            [
                'label' => __( 'Content', 'soma' ),
                'tab'   => Controls_Manager::TAB_CONTENT,
            ]
        );

        // Add your content controls here

        $this->end_controls_section();

        // Style Section
        $this->start_controls_section(
            'style_section',
            [
                'label' => __( 'Style', 'soma' ),
                'tab'   => Controls_Manager::TAB_STYLE,
            ]
        );

        // Add your style controls here

        $this->end_controls_section();
    }

    /**
     * Render widget output.
     *
     * @return void
     */
    protected function render(): void {
        $settings = $this->get_settings_for_display();

        ?>
        <div class="soma-{widget-slug}">
            <!-- Widget HTML output -->
        </div>
        <?php
    }
}
```

### Step 2: Register Widget in Loader

**File**: `wp-content/themes/soma/includes/Elementor/Loader.php`

Add to `register_widgets()` method:

```php
private function register_widgets(): void {
    $widgets_manager = \Elementor\Plugin::instance()->widgets_manager;
    
    // ... existing widgets ...
    
    $widgets_manager->register( new Widgets\{WidgetName}() );
}
```

Add style registration in `register_styles()`:

```php
wp_register_style(
    'soma-{widget-slug}',
    get_template_directory_uri() . '/assets/css/widgets/{widget-slug}.css',
    [],
    $this->version
);
```

### Step 3: Create CSS File

**Location**: `wp-content/themes/soma/assets/css/widgets/{widget-slug}.css`

```css
/**
 * {WidgetName} Widget Styles
 *
 * @package Soma
 * @since   3.x.x
 */

.soma-{widget-slug} {
    /* Use SOMA CSS variables for consistency */
    font-family: var(--soma-font-family-primary);
    color: var(--soma-color-text-primary);
}

/* Responsive styles */
@media (max-width: 991px) {
    .soma-{widget-slug} {
        /* Tablet styles */
    }
}

@media (max-width: 767px) {
    .soma-{widget-slug} {
        /* Mobile styles */
    }
}
```

### Step 4: Create Integration Tests

> **⚠️ IMPORTANT**: Elementor widgets have **Integration tests ONLY**. Do NOT create Unit tests for widgets.
>
> **Why?**
> - Widgets require Elementor loaded (`did_action('elementor/loaded')`)
> - Widgets extend `\Elementor\Widget_Base` (needs Elementor classes)
> - Controls registration needs Elementor infrastructure

**Location**: `wp-content/themes/soma/tests/Integration/Elementor/{WidgetName}WidgetTest.php`

```php
<?php
/**
 * Integration tests for {WidgetName} Elementor widget.
 *
 * @package Soma\Tests\Integration\Elementor
 */

declare(strict_types=1);

namespace Soma\Tests\Integration\Elementor;

use Soma\Elementor\Widgets\{WidgetName};
use WP_UnitTestCase;

/**
 * @group integration
 * @group elementor
 * @group widgets
 */
class {WidgetName}WidgetTest extends WP_UnitTestCase {

    /**
     * Widget instance.
     *
     * @var {WidgetName}|null
     */
    private ?{WidgetName} $widget = null;

    /**
     * Set up test fixtures.
     */
    public function setUp(): void {
        parent::setUp();

        if ( ! did_action( 'elementor/loaded' ) ) {
            $this->markTestSkipped( 'Elementor not loaded' );
            return;
        }

        $this->widget = new {WidgetName}();
    }

    /**
     * Tear down test fixtures.
     */
    public function tearDown(): void {
        $this->widget = null;
        parent::tearDown();
    }

    /**
     * Test widget name.
     */
    public function test_widget_name(): void {
        $this->assertSame( 'soma-{widget-slug}', $this->widget->get_name() );
    }

    /**
     * Test widget title.
     */
    public function test_widget_title(): void {
        $this->assertSame( 'SOMA {Widget Title}', $this->widget->get_title() );
    }

    /**
     * Test widget categories.
     */
    public function test_widget_categories(): void {
        $this->assertContains( 'soma', $this->widget->get_categories() );
    }

    /**
     * Test style dependencies.
     */
    public function test_style_depends(): void {
        $this->assertContains( 'soma-{widget-slug}', $this->widget->get_style_depends() );
    }
}
```

### Step 5: Update AllWidgetsTest.php

**File**: `wp-content/themes/soma/tests/Integration/Elementor/AllWidgetsTest.php`

Add to `$widget_classes` array:

```php
'{WidgetName}' => \Soma\Elementor\Widgets\{WidgetName}::class,
```

Add to `$widget_names` array:

```php
'{WidgetName}' => 'soma-{widget-slug}',
```

### Step 6: Add Translations

Update translation files:

```bash
# Generate .pot file
cd wp-content/themes/soma
wp i18n make-pot . languages/soma.pot --domain=soma

# Update .po files
wp i18n update-po languages/soma.pot languages/

# Compile .mo files
wp i18n make-mo languages/
```

### Step 7: Update Documentation

**File**: `wp-content/themes/soma/docs/WIDGETS.md`

Add widget entry to the catalog with:
- Widget description
- Content controls table
- Style controls table
- CSS variables used
- Usage example
- ACF integration (if applicable)

## Common Control Types

### Text Controls

```php
$this->add_control(
    'title',
    [
        'label'       => __( 'Title', 'soma' ),
        'type'        => Controls_Manager::TEXT,
        'default'     => __( 'Default Title', 'soma' ),
        'placeholder' => __( 'Enter title', 'soma' ),
    ]
);
```

### Switcher Controls

```php
$this->add_control(
    'show_title',
    [
        'label'        => __( 'Show Title', 'soma' ),
        'type'         => Controls_Manager::SWITCHER,
        'label_on'     => __( 'Show', 'soma' ),
        'label_off'    => __( 'Hide', 'soma' ),
        'return_value' => 'yes',
        'default'      => 'yes',
    ]
);
```

### SELECT2 with Post Selection

```php
$this->add_control(
    'selected_post',
    [
        'label'       => __( 'Select Post', 'soma' ),
        'type'        => Controls_Manager::SELECT2,
        'options'     => $this->get_posts_options(),
        'default'     => '',
        'label_block' => true,
    ]
);

// IMPORTANT: Use get_the_title() for WP-Multilang compatibility
private function get_posts_options(): array {
    $options = [];
    $posts   = get_posts( [ 'post_type' => 'post', 'numberposts' => -1 ] );
    
    foreach ( $posts as $post ) {
        // ✅ CORRECT - Applies 'the_title' filter for WP-Multilang
        $options[ $post->ID ] = get_the_title( $post->ID );
        
        // ❌ WRONG - Bypasses filters, shows raw multilang delimiters
        // $options[ $post->ID ] = $post->post_title;
    }
    
    return $options;
}
```

### Typography Controls

```php
$this->add_group_control(
    Group_Control_Typography::get_type(),
    [
        'name'     => 'title_typography',
        'label'    => __( 'Title Typography', 'soma' ),
        'selector' => '{{WRAPPER}} .soma-widget-title',
        'global'   => [
            'default' => Global_Typography::TYPOGRAPHY_PRIMARY,
        ],
    ]
);
```

### Color Controls with Global Colors

```php
$this->add_control(
    'title_color',
    [
        'label'     => __( 'Title Color', 'soma' ),
        'type'      => Controls_Manager::COLOR,
        'global'    => [
            'default' => Global_Colors::COLOR_PRIMARY,
        ],
        'selectors' => [
            '{{WRAPPER}} .soma-widget-title' => 'color: {{VALUE}};',
        ],
    ]
);
```

## SOMA CSS Variables Reference

Use these CSS variables for consistency:

```css
/* Typography */
--soma-font-family-primary
--soma-font-size-h1, h2, h3, h4, h5, h6
--soma-font-size-body, body-mobile, small

/* Colors */
--soma-color-text-primary
--soma-color-text-secondary
--soma-color-primary
--soma-color-secondary

/* Spacing */
--soma-spacing-xs, sm, md, lg, xl, 2xl

/* Layout */
--soma-container-max-width
--soma-border-radius

/* Transitions */
--soma-transition-base
--soma-transition-slow
```

## Checklist Before Committing

- [ ] Widget class created in `includes/Elementor/Widgets/`
- [ ] Widget registered in `Loader.php`
- [ ] CSS file created in `assets/css/widgets/`
- [ ] CSS style registered in `Loader.php`
- [ ] Integration tests created (⚠️ NOT unit tests - widgets use integration tests ONLY)
- [ ] AllWidgetsTest.php updated
- [ ] PHPCS passes (`composer phpcs`)
- [ ] PHPStan passes (`composer phpstan`)
- [ ] All tests pass (`composer test`)
- [ ] Translations regenerated
- [ ] WIDGETS.md documentation updated

## Elementor Icon Reference

Common icons for widgets:
- `eicon-posts-grid` - Grid layouts
- `eicon-post-list` - List layouts
- `eicon-person` - Team/profile
- `eicon-document-file` - Documents
- `eicon-price-table` - Pricing/tables
- `eicon-form-horizontal` - Forms
- `eicon-nav-menu` - Navigation
- `eicon-footer` - Footer elements
- `eicon-gallery-grid` - Galleries
- `eicon-calendar` - Events/dates
