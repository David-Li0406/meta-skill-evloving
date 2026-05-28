---
name: PHPUnit Testing
description: Write PHPUnit tests for WordPress components following SOMA testing standards and conventions
---

# PHPUnit Testing Skill

This skill guides the creation of PHPUnit tests for the SOMA WordPress theme, ensuring proper test structure, assertions, and coverage.

## When to Use This Skill

Use this skill when you need to:
- Write unit tests for new classes
- Write integration tests for WordPress components
- Test Elementor widgets
- Test custom post types or taxonomies
- Test REST API endpoints
- Debug failing tests

## Test Organization

### Directory Structure

```
tests/
├── bootstrap.php              # Test bootstrap with WordPress loading
├── Unit/                      # Unit tests (no WordPress dependency)
│   ├── PostTypes/            # Post type unit tests
│   ├── Taxonomies/           # Taxonomy unit tests
│   ├── Elementor/            # Widget unit tests
│   └── Utils/                # Utility class tests
├── Integration/              # Integration tests (requires WordPress)
│   ├── PostTypes/            # Post type integration tests
│   ├── Taxonomies/           # Taxonomy integration tests
│   ├── Elementor/            # Widget integration tests
│   └── API/                  # REST API endpoint tests
└── Mocks/                    # Mock classes and SimpleMocks
```

### Test Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Unit Test | `{ClassName}Test.php` | `PortfolioTest.php` |
| Integration Test | `{ClassName}Test.php` | `PortfolioTest.php` |
| Widget Test | `{WidgetName}WidgetTest.php` | `TeamMembersWidgetTest.php` |
| API Test | `{Endpoint}EndpointTest.php` | `NewsEndpointTest.php` |

## Unit Test Template

**Location**: `tests/Unit/{Component}/{ClassName}Test.php`

```php
<?php
/**
 * Unit tests for {ClassName}.
 *
 * @package Soma\Tests\Unit\{Component}
 */

declare(strict_types=1);

namespace Soma\Tests\Unit\{Component};

use PHPUnit\Framework\TestCase;
use ReflectionClass;

/**
 * @group unit
 * @group {component-slug}
 */
class {ClassName}Test extends TestCase {

    /**
     * Class being tested.
     *
     * @var string
     */
    private string $class_name = \Soma\{Namespace}\{ClassName}::class;

    /**
     * Test class exists.
     */
    public function test_class_exists(): void {
        $this->assertTrue( class_exists( $this->class_name ) );
    }

    /**
     * Test singleton pattern.
     */
    public function test_singleton_instance(): void {
        $reflection = new ReflectionClass( $this->class_name );
        
        $this->assertTrue(
            $reflection->hasMethod( 'instance' ),
            'Class should have instance() method'
        );
        
        $instance_method = $reflection->getMethod( 'instance' );
        $this->assertTrue( $instance_method->isStatic() );
        $this->assertTrue( $instance_method->isPublic() );
    }

    /**
     * Test has required methods.
     */
    public function test_has_required_methods(): void {
        $reflection = new ReflectionClass( $this->class_name );
        $methods    = [
            'init',
            'register',
            // Add more required methods
        ];

        foreach ( $methods as $method ) {
            $this->assertTrue(
                $reflection->hasMethod( $method ),
                "Method {$method} should exist"
            );
        }
    }

    /**
     * Test cannot clone singleton.
     */
    public function test_cannot_clone(): void {
        $reflection      = new ReflectionClass( $this->class_name );
        $clone_method    = $reflection->getMethod( '__clone' );
        
        $this->assertTrue( $clone_method->isPrivate() );
    }
}
```

## Integration Test Template

**Location**: `tests/Integration/{Component}/{ClassName}Test.php`

```php
<?php
/**
 * Integration tests for {ClassName}.
 *
 * @package Soma\Tests\Integration\{Component}
 */

declare(strict_types=1);

namespace Soma\Tests\Integration\{Component};

use Soma\{Namespace}\{ClassName};
use WP_UnitTestCase;

/**
 * @group integration
 * @group {component-slug}
 */
class {ClassName}Test extends WP_UnitTestCase {

    /**
     * Instance being tested.
     *
     * @var {ClassName}|null
     */
    private ?{ClassName} $instance = null;

    /**
     * Set up test fixtures.
     */
    public function setUp(): void {
        parent::setUp();
        
        // Reset singleton for clean test state
        $this->reset_singleton();
        
        $this->instance = {ClassName}::instance();
    }

    /**
     * Tear down test fixtures.
     */
    public function tearDown(): void {
        $this->instance = null;
        $this->reset_singleton();
        parent::tearDown();
    }

    /**
     * Reset singleton instance for testing.
     */
    private function reset_singleton(): void {
        $reflection = new \ReflectionClass( {ClassName}::class );
        $property   = $reflection->getProperty( 'instance' );
        $property->setValue( null, null );
    }

    /**
     * Test component registers correctly.
     */
    public function test_registers_on_init(): void {
        // Test registration logic
        $this->assertNotNull( $this->instance );
    }

    /**
     * Test component functionality.
     */
    public function test_functionality(): void {
        // Add specific functionality tests
    }
}
```

## Elementor Widget Test Pattern

### Unit Test

```php
<?php
namespace Soma\Tests\Unit\Elementor;

use PHPUnit\Framework\TestCase;
use ReflectionClass;

/**
 * @group unit
 * @group elementor
 * @group widgets
 */
class {WidgetName}WidgetTest extends TestCase {

    private string $widget_class = \Soma\Elementor\Widgets\{WidgetName}::class;

    public function test_class_exists(): void {
        $this->assertTrue( class_exists( $this->widget_class ) );
    }

    public function test_extends_widget_base(): void {
        $reflection = new ReflectionClass( $this->widget_class );
        $parent     = $reflection->getParentClass();
        
        $this->assertNotFalse( $parent );
        $this->assertSame( 'Elementor\Widget_Base', $parent->getName() );
    }

    public function test_has_required_methods(): void {
        $reflection = new ReflectionClass( $this->widget_class );
        $methods    = [
            'get_name',
            'get_title',
            'get_icon',
            'get_categories',
            'get_style_depends',
            'register_controls',
            'render',
        ];

        foreach ( $methods as $method ) {
            $this->assertTrue(
                $reflection->hasMethod( $method ),
                "Method {$method} should exist"
            );
        }
    }
}
```

### Integration Test

```php
<?php
namespace Soma\Tests\Integration\Elementor;

use Soma\Elementor\Widgets\{WidgetName};
use WP_UnitTestCase;

/**
 * @group integration
 * @group elementor
 * @group widgets
 */
class {WidgetName}WidgetTest extends WP_UnitTestCase {

    private ?{WidgetName} $widget = null;

    public function setUp(): void {
        parent::setUp();

        // CRITICAL: Skip if Elementor not loaded
        if ( ! did_action( 'elementor/loaded' ) ) {
            $this->markTestSkipped( 'Elementor not loaded' );
            return; // IMPORTANT: Always return after markTestSkipped
        }

        $this->widget = new {WidgetName}();
    }

    public function tearDown(): void {
        $this->widget = null;
        parent::tearDown();
    }

    public function test_widget_name(): void {
        $this->assertSame( 'soma-{widget-slug}', $this->widget->get_name() );
    }

    public function test_widget_title(): void {
        $this->assertNotEmpty( $this->widget->get_title() );
    }

    public function test_widget_categories(): void {
        $this->assertContains( 'soma', $this->widget->get_categories() );
    }

    public function test_style_depends(): void {
        $styles = $this->widget->get_style_depends();
        $this->assertContains( 'soma-{widget-slug}', $styles );
    }

    public function test_has_controls(): void {
        // Access protected method via reflection
        $reflection = new \ReflectionClass( $this->widget );
        $method     = $reflection->getMethod( 'register_controls' );
        $method->setAccessible( true );
        
        // This should not throw any exceptions
        $method->invoke( $this->widget );
        $this->assertTrue( true );
    }
}
```

## Post Type Test Pattern

```php
<?php
namespace Soma\Tests\Integration\PostTypes;

use Soma\PostTypes\Types\{PostType};
use WP_UnitTestCase;

/**
 * @group integration
 * @group post-types
 */
class {PostType}Test extends WP_UnitTestCase {

    public function test_post_type_exists(): void {
        $this->assertTrue(
            post_type_exists( '{post-type-slug}' ),
            'Post type {post-type-slug} should be registered'
        );
    }

    public function test_post_type_labels(): void {
        $post_type = get_post_type_object( '{post-type-slug}' );
        
        $this->assertNotNull( $post_type );
        $this->assertNotEmpty( $post_type->labels->name );
        $this->assertNotEmpty( $post_type->labels->singular_name );
    }

    public function test_post_type_supports(): void {
        $supports = get_all_post_type_supports( '{post-type-slug}' );
        
        $this->assertArrayHasKey( 'title', $supports );
        $this->assertArrayHasKey( 'editor', $supports );
        $this->assertArrayHasKey( 'thumbnail', $supports );
    }

    public function test_can_create_post(): void {
        $post_id = $this->factory->post->create([
            'post_type'  => '{post-type-slug}',
            'post_title' => 'Test Post',
        ]);

        $this->assertIsInt( $post_id );
        $this->assertGreaterThan( 0, $post_id );
        
        $post = get_post( $post_id );
        $this->assertSame( '{post-type-slug}', $post->post_type );
    }
}
```

## REST API Endpoint Test Pattern

```php
<?php
namespace Soma\Tests\Integration\API;

use WP_REST_Request;
use WP_UnitTestCase;

/**
 * @group integration
 * @group api
 */
class {Endpoint}EndpointTest extends WP_UnitTestCase {

    public function setUp(): void {
        parent::setUp();
        
        // Ensure REST API is initialized
        do_action( 'rest_api_init' );
    }

    public function test_endpoint_registered(): void {
        $routes = rest_get_server()->get_routes();
        
        $this->assertArrayHasKey(
            '/soma/{endpoint-slug}',
            $routes,
            'Endpoint should be registered'
        );
    }

    public function test_get_items(): void {
        // Create test data
        $this->factory->post->create_many( 3, [
            'post_type'   => '{post-type}',
            'post_status' => 'publish',
        ]);

        $request  = new WP_REST_Request( 'GET', '/soma/{endpoint-slug}' );
        $response = rest_get_server()->dispatch( $request );

        $this->assertSame( 200, $response->get_status() );
        
        $data = $response->get_data();
        $this->assertIsArray( $data );
        $this->assertGreaterThanOrEqual( 3, count( $data ) );
    }

    public function test_endpoint_with_parameters(): void {
        $request = new WP_REST_Request( 'GET', '/soma/{endpoint-slug}' );
        $request->set_param( 'per_page', 5 );
        
        $response = rest_get_server()->dispatch( $request );
        
        $this->assertSame( 200, $response->get_status() );
    }
}
```

## Assertion Reference

### Common Assertions

```php
// Basic assertions
$this->assertTrue( $condition );
$this->assertFalse( $condition );
$this->assertNull( $value );
$this->assertNotNull( $value );

// Equality
$this->assertSame( $expected, $actual );    // Strict comparison (===)
$this->assertEquals( $expected, $actual );  // Loose comparison (==)
$this->assertNotSame( $expected, $actual );

// Type assertions
$this->assertIsArray( $value );
$this->assertIsString( $value );
$this->assertIsInt( $value );
$this->assertIsBool( $value );
$this->assertInstanceOf( ClassName::class, $object );

// Array assertions
$this->assertArrayHasKey( 'key', $array );
$this->assertContains( $needle, $array );
$this->assertCount( 3, $array );
$this->assertEmpty( $array );
$this->assertNotEmpty( $array );

// String assertions
$this->assertStringContainsString( 'needle', $haystack );
$this->assertStringStartsWith( 'prefix', $string );
$this->assertMatchesRegularExpression( '/pattern/', $string );

// WordPress-specific
$this->assertWPError( $result );            // Check is WP_Error
$this->assertNotWPError( $result );
```

## Running Tests

```bash
# Run all tests
composer test

# Run with verbose output
vendor/bin/phpunit --testdox

# Run specific test file
vendor/bin/phpunit tests/Unit/PostTypes/PortfolioTest.php

# Run specific test method
vendor/bin/phpunit --filter test_singleton_instance

# Run by group
vendor/bin/phpunit --group unit
vendor/bin/phpunit --group integration
vendor/bin/phpunit --group elementor

# Run with coverage
vendor/bin/phpunit --coverage-html coverage/

# Skip coverage (faster)
composer test
# or
vendor/bin/phpunit --no-coverage
```

## Test Data Factories

```php
// Create single post
$post_id = $this->factory->post->create([
    'post_type'   => 'portfolio',
    'post_title'  => 'Test Portfolio',
    'post_status' => 'publish',
]);

// Create multiple posts
$post_ids = $this->factory->post->create_many( 5, [
    'post_type' => 'news',
]);

// Create user
$user_id = $this->factory->user->create([
    'role' => 'administrator',
]);

// Create term
$term_id = $this->factory->term->create([
    'taxonomy' => 'portfolio-taxonomy',
    'name'     => 'Commercial',
]);

// Create attachment
$attachment_id = $this->factory->attachment->create([
    'post_mime_type' => 'image/jpeg',
]);
```

## Common Test Patterns

### Testing Singleton Reset

```php
private function reset_singleton(): void {
    $reflection = new \ReflectionClass( ClassName::class );
    $property   = $reflection->getProperty( 'instance' );
    // PHP 8.1+: setAccessible() not needed
    $property->setValue( null, null );
}
```

### Testing Private Methods

```php
public function test_private_method(): void {
    $reflection = new \ReflectionClass( $this->instance );
    $method     = $reflection->getMethod( 'private_method_name' );
    $method->setAccessible( true );
    
    $result = $method->invoke( $this->instance, $arg1, $arg2 );
    
    $this->assertSame( $expected, $result );
}
```

### Testing Hooks

```php
public function test_action_registered(): void {
    $this->assertNotFalse(
        has_action( 'init', [ $this->instance, 'register' ] ),
        'Action should be registered on init'
    );
}

public function test_filter_registered(): void {
    $this->assertNotFalse(
        has_filter( 'the_content', [ $this->instance, 'filter_content' ] )
    );
}
```

## Checklist Before Committing Tests

- [ ] All tests pass locally (`composer test`)
- [ ] Tests follow naming conventions
- [ ] Unit tests don't require WordPress
- [ ] Integration tests use `WP_UnitTestCase`
- [ ] Elementor tests skip when Elementor not loaded
- [ ] Singleton tests reset state in setUp/tearDown
- [ ] Test methods are properly annotated with `@group`
- [ ] Assertions have descriptive messages for failures
- [ ] No debugging code left (var_dump, print_r)
- [ ] PHPCS passes on test files
