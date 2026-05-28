# Testing Actions

## scan / run_tests

Run unit and UI tests for iOS/macOS.

```ruby
run_tests(
  workspace: "MyApp.xcworkspace",
  scheme: "MyApp",
  
  # Devices
  devices: ["iPhone 15 Pro", "iPad Pro (12.9-inch)"],
  
  # Configuration
  configuration: "Debug",
  clean: true,
  code_coverage: true,
  
  # Output
  output_directory: "./test_output",
  output_types: "html,junit",
  
  # Options
  fail_build: true,
  skip_build: false,
  parallel_testing: true,
  concurrent_workers: 4,
  
  # Specific tests
  only_testing: ["MyAppTests/LoginTests"],
  skip_testing: ["MyAppTests/SlowTests"],
  
  # Xcode options
  xcargs: "-enableCodeCoverage YES",
  derived_data_path: "./DerivedData"
)
```

**Scanfile Configuration:**
```ruby
# fastlane/Scanfile
workspace("MyApp.xcworkspace")
scheme("MyApp")
devices(["iPhone 15 Pro"])
clean(true)
code_coverage(true)
output_types("html,junit")
output_directory("./test_output")
```

**Key Parameters:**
- `parallel_testing`: Run tests in parallel
- `result_bundle`: Generate xcresult bundle
- `buildlog_path`: Custom build log location
- `disable_concurrent_testing`: Run tests serially
- `test_without_building`: Skip build step

## trainer

Convert xcresult to JUnit XML format.

```ruby
trainer(
  path: "./test_output",
  output_directory: "./junit_output",
  fail_build: true
)
```

## slather

Generate code coverage reports.

```ruby
slather(
  proj: "MyApp.xcodeproj",
  scheme: "MyApp",
  
  # Output format
  html: true,
  output_directory: "./coverage",
  
  # Options
  ignore: ["Pods/*", "*/Tests/*"],
  source_directory: "./Sources",
  
  # CI integration
  cobertura_xml: true,  # For Jenkins
  jenkins: true,
  
  # Coverage services
  coveralls: false,
  codecov: false
)
```

## xcov

Generate beautiful code coverage reports.

```ruby
xcov(
  workspace: "MyApp.xcworkspace",
  scheme: "MyApp",
  output_directory: "./xcov_output",
  html_report: true,
  minimum_coverage_percentage: 80.0,
  skip_slack: false
)
```

## swiftlint

Run SwiftLint for code style checking.

```ruby
swiftlint(
  mode: :lint,  # :lint, :fix, :analyze
  
  # Configuration
  config_file: ".swiftlint.yml",
  
  # Output
  output_file: "./swiftlint_output.txt",
  reporter: "html",  # html, json, checkstyle, junit
  
  # Options
  strict: true,
  raise_if_swiftlint_error: true,
  ignore_exit_status: false,
  
  # Paths
  path: "./Sources",
  executable: "Pods/SwiftLint/swiftlint"
)

# Auto-fix issues
swiftlint(mode: :fix)
```

## oclint

Static analysis with OCLint.

```ruby
oclint(
  compile_commands: "./compile_commands.json",
  report_type: "html",
  report_path: "./oclint_report.html",
  max_priority_1: 0,
  max_priority_2: 10,
  max_priority_3: 20,
  thresholds: [
    "LONG_METHOD=60",
    "LONG_LINE=120"
  ]
)
```

## sonar

Run SonarQube analysis.

```ruby
sonar(
  project_key: "com.example.app",
  project_name: "My App",
  project_version: "1.0.0",
  sources_path: "./Sources",
  sonar_runner_args: "-Dsonar.host.url=https://sonarqube.example.com"
)
```

## danger

Run Danger for PR automation.

```ruby
danger(
  danger_id: "danger",
  dangerfile: "Dangerfile",
  github_api_token: ENV["GITHUB_TOKEN"],
  new_comment: true,
  remove_previous_comments: true
)
```

## appium

Run Appium tests.

```ruby
appium(
  app_path: "./MyApp.app",
  spec_path: "./spec/",
  platform: "iOS",
  caps: {
    platformVersion: "17.0",
    deviceName: "iPhone 15 Pro"
  }
)
```

## Test Workflow Examples

### Full Test Suite

```ruby
lane :test do
  # Run unit tests
  run_tests(
    scheme: "MyApp",
    code_coverage: true
  )
  
  # Generate coverage report
  slather(
    scheme: "MyApp",
    html: true,
    output_directory: "./coverage"
  )
  
  # Run SwiftLint
  swiftlint(strict: true)
end
```

### CI Test Lane

```ruby
lane :ci_test do
  # Setup CI environment
  setup_ci
  
  # Run tests with JUnit output
  run_tests(
    scheme: "MyApp",
    output_types: "junit",
    output_directory: ENV["CIRCLE_TEST_REPORTS"]
  )
  
  # Check coverage threshold
  xcov(
    scheme: "MyApp",
    minimum_coverage_percentage: 80.0
  )
end
```

### PR Checks

```ruby
lane :pr_check do
  swiftlint(strict: true)
  
  run_tests(scheme: "MyApp")
  
  danger(
    github_api_token: ENV["GITHUB_TOKEN"]
  )
end
```

### Android Testing with Gradle

```ruby
lane :android_test do
  # Unit tests
  gradle(task: "test")
  
  # Instrumentation tests
  gradle(task: "connectedAndroidTest")
  
  # Lint
  gradle(task: "lint")
end
```

## Test Output Integration

```ruby
lane :test_and_report do
  begin
    run_tests(
      scheme: "MyApp",
      result_bundle: true,
      output_directory: "./test_output"
    )
  rescue => ex
    # Tests failed
    slack(
      message: "Tests failed: #{ex.message}",
      success: false
    )
    raise ex
  end
  
  # Convert results for CI
  trainer(
    path: "./test_output/MyApp.xcresult",
    output_directory: "./junit"
  )
  
  slack(message: "All tests passed! ✅")
end
```
