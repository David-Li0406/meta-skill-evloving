#!/usr/bin/env python3
"""
Playwright Test Template Generator

Generates Playwright test templates for Radulator calculators.
"""

def generate_playwright_test(calculator_name: str, test_data: dict) -> str:
    """
    Generate a Playwright test template for a specific calculator.
    
    Args:
        calculator_name: Name of the calculator (e.g., "Adrenal Washout CT")
        test_data: Dictionary containing test inputs and expected outputs
    
    Returns:
        JavaScript code for the Playwright test
    """
    
    # Template for adrenal CT washout
    if "adrenal" in calculator_name.lower() and "ct" in calculator_name.lower():
        return f"""const {{ test, expect }} = require('@playwright/test');

test('Adrenal CT Washout Calculator - {test_data.get("test_name", "Basic Test")}', async ({{ page }}) => {{
  // Navigate to Radulator
  await page.goto(process.env.RADULATOR_URL || 'http://localhost:5173');
  
  // Select calculator from sidebar
  await page.click('text="Adrenal Washout CT"');
  
  // Wait for calculator to load
  await page.waitForSelector('input[name="unenh"]', {{ timeout: 5000 }});
  
  // Fill input fields
  await page.fill('input[name="unenh"]', '{test_data.get("unenh", "")}');
  await page.fill('input[name="portal"]', '{test_data.get("portal", "")}');
  await page.fill('input[name="delayed"]', '{test_data.get("delayed", "")}');
  
  // Click Calculate button
  await page.click('button:has-text("Calculate")');
  
  // Wait for results
  await page.waitForSelector('.results', {{ timeout: 2000 }});
  
  // Verify results
  const absoluteWashout = await page.locator('text=/Absolute.*Washout/i').locator('..').textContent();
  const relativeWashout = await page.locator('text=/Relative.*Washout/i').locator('..').textContent();
  
  // Extract numeric values and verify
  const absValue = parseFloat(absoluteWashout.match(/[0-9.]+/)[0]);
  const relValue = parseFloat(relativeWashout.match(/[0-9.]+/)[0]);
  
  expect(absValue).toBeCloseTo({test_data.get("expected_absolute", 0)}, 1);
  expect(relValue).toBeCloseTo({test_data.get("expected_relative", 0)}, 1);
  
  // Take screenshot for documentation
  await page.screenshot({{ path: 'test-results/adrenal-ct-washout.png' }});
}});
"""
    
    # Template for prostate volume
    elif "prostate" in calculator_name.lower():
        return f"""const {{ test, expect }} = require('@playwright/test');

test('Prostate Volume Calculator - {test_data.get("test_name", "Basic Test")}', async ({{ page }}) => {{
  await page.goto(process.env.RADULATOR_URL || 'http://localhost:5173');
  await page.click('text="Prostate Volume"');
  await page.waitForSelector('input[name="length"]');
  
  await page.fill('input[name="length"]', '{test_data.get("length", "")}');
  await page.fill('input[name="height"]', '{test_data.get("height", "")}');
  await page.fill('input[name="width"]', '{test_data.get("width", "")}');
  await page.fill('input[name="psa"]', '{test_data.get("psa", "")}');
  
  await page.click('button:has-text("Calculate")');
  await page.waitForSelector('.results');
  
  const volumeText = await page.locator('text=/Volume/i').locator('..').textContent();
  const densityText = await page.locator('text=/PSA.*Density/i').locator('..').textContent();
  
  const volume = parseFloat(volumeText.match(/[0-9.]+/)[0]);
  const density = parseFloat(densityText.match(/[0-9.]+/)[0]);
  
  expect(volume).toBeCloseTo({test_data.get("expected_volume", 0)}, 1);
  expect(density).toBeCloseTo({test_data.get("expected_density", 0)}, 2);
  
  await page.screenshot({{ path: 'test-results/prostate-volume.png' }});
}});
"""
    
    # Generic template for other calculators
    else:
        return f"""const {{ test, expect }} = require('@playwright/test');

test('{calculator_name} - {test_data.get("test_name", "Basic Test")}', async ({{ page }}) => {{
  await page.goto(process.env.RADULATOR_URL || 'http://localhost:5173');
  
  // Select the calculator
  await page.click('text="{calculator_name}"');
  
  // Wait for calculator to load
  await page.waitForSelector('button:has-text("Calculate")');
  
  // TODO: Fill in calculator-specific inputs
  // TODO: Add assertions for expected results
  
  await page.screenshot({{ path: 'test-results/{calculator_name.lower().replace(" ", "-")}.png' }});
}});
"""


def main():
    """Generate sample test templates."""
    import sys
    import json
    
    if len(sys.argv) < 3:
        print("Usage: python generate_playwright_test.py <calculator_name> <test_data_json>")
        sys.exit(1)
    
    calculator_name = sys.argv[1]
    test_data = json.loads(sys.argv[2])
    
    test_code = generate_playwright_test(calculator_name, test_data)
    print(test_code)


if __name__ == "__main__":
    main()
