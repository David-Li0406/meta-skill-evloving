<?php
// Simple Laravel context detector for agents.
// Prints JSON describing detected test framework and Laravel major version constraint.

$composer = getcwd() . DIRECTORY_SEPARATOR . 'composer.json';
if (!file_exists($composer)) {
    fwrite(STDERR, "composer.json not found in current directory\n");
    exit(2);
}

$data = json_decode(file_get_contents($composer), true) ?: [];
$require = array_merge($data['require'] ?? [], $data['require-dev'] ?? []);

$laravel = $require['laravel/framework'] ?? null;
$pest = isset($require['pestphp/pest']) || isset($require['pestphp/pest-plugin-laravel']);

echo json_encode([
  'laravel_framework_constraint' => $laravel,
  'test_framework' => $pest ? 'pest' : 'phpunit',
], JSON_PRETTY_PRINT) . PHP_EOL;
