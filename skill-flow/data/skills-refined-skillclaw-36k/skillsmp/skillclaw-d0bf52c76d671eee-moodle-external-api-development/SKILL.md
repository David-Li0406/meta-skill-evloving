---
name: moodle-external-api-development
description: Use this skill when creating custom external web service APIs for Moodle LMS, including course management, user tracking, and quiz operations.
---

# Moodle External API Development

This skill guides you through creating custom external web service APIs for Moodle LMS, following Moodle's external API framework and coding standards.

## When to Use This Skill

- Creating custom web services for Moodle plugins
- Implementing REST/AJAX endpoints for course management
- Building APIs for quiz operations, user tracking, or reporting
- Exposing Moodle functionality to external applications
- Developing mobile app backends using Moodle

## Core Architecture Pattern

Moodle external APIs follow a strict three-method pattern:

1. **`execute_parameters()`** - Defines input parameter structure
2. **`execute()`** - Contains business logic
3. **`execute_returns()`** - Defines return structure

## Step-by-Step Implementation

### Step 1: Create the External API Class File

**Location**: `/local/yourplugin/classes/external/your_api_name.php`

```php
<?php
namespace local_yourplugin\external;

defined('MOODLE_INTERNAL') || die();
require_once("$CFG->libdir/externallib.php");

use external_api;
use external_function_parameters;
use external_single_structure;
use external_value;

class your_api_name extends external_api {
    
    // Three required methods will go here
    
}
```

**Key Points**:
- Class must extend `external_api`
- Namespace follows: `local_pluginname\external` or `mod_modname\external`
- Include the security check: `defined('MOODLE_INTERNAL') || die();`
- Require `externallib.php` for base classes

### Step 2: Define Input Parameters

```php
public static function execute_parameters() {
    return new external_function_parameters([
        'userid' => new external_value(PARAM_INT, 'User ID', VALUE_REQUIRED),
        'courseid' => new external_value(PARAM_INT, 'Course ID', VALUE_REQUIRED),
        'options' => new external_single_structure([
            'includedetails' => new external_value(PARAM_BOOL, 'Include details', VALUE_DEFAULT, false),
            'limit' => new external_value(PARAM_INT, 'Result limit', VALUE_DEFAULT, 10)
        ], 'Options', VALUE_OPTIONAL)
    ]);
}
```

**Common Parameter Types**:
- `PARAM_INT` - Integers
- `PARAM_TEXT` - Text values
- `PARAM_BOOL` - Boolean values

### Step 3: Implement Business Logic

```php
public static function execute($userid, $courseid, $options) {
    // Business logic goes here
}
```

### Step 4: Define Return Structure

```php
public static function execute_returns() {
    return new external_single_structure([
        'result' => new external_value(PARAM_TEXT, 'Result data'),
        // Add more return values as needed
    ]);
}
```