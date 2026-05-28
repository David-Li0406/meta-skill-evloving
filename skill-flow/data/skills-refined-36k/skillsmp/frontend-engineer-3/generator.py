import os
import sys

def generate_component(feature, name):
    content = f"""import React from 'react';
import {{ Card, CardHeader, CardTitle, CardContent }} from '@/shared/components/ui/card';

export const {name}: React.FC = () => {{
  return (
    <Card className="bg-white/10 backdrop-blur-md border border-white/20 shadow-xl overflow-hidden">
      <CardHeader>
        <CardTitle className="text-white font-bold">{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-white/80">Premium component {name} initialized.</p>
      </CardContent>
    </Card>
  );
}};
"""
    save_file(f"sportsmanagement_frontend/src/features/{{feature}}/components/{{name}}.tsx", content)
    # Scaffold Vitest
    test_content = f"""import {{ render, screen }} from '@testing-library/react';
import {{ {name} }} from './{name}';
import {{ describe, it, expect }} from 'vitest';

describe('{name}', () => {{
  it('renders correctly', () => {{
    render(<{name} />);
    expect(screen.getByText('{name}')).toBeDefined();
  }});
}});
"""
    save_file(f"sportsmanagement_frontend/src/features/{{feature}}/components/{{name}}.test.tsx", test_content)

def generate_hook(feature, name):
    content = f"""import {{ useState, useEffect }} from 'react';

export const use{name} = () => {{
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {{
    // Logic for {name}
    setLoading(false);
  }}, []);

  return {{ data, loading }};
}};
"""
    save_file(f"sportsmanagement_frontend/src/features/{{feature}}/hooks/use{{name}}.ts", content)
    # Scaffold Vitest Hook
    test_content = f"""import {{ renderHook }} from '@testing-library/react-hooks';
import {{ use{name} }} from './use{name}';
import {{ describe, it, expect }} from 'vitest';

describe('use{name}', () => {{
  it('initializes correctly', () => {{
    const {{ result }} = renderHook(() => use{name}());
    expect(result.current.loading).toBe(false);
  }});
}});
"""
    save_file(f"sportsmanagement_frontend/src/features/{{feature}}/hooks/use{{name}}.test.ts", test_content)

def generate_service(feature, name):
    # Service logic here...
    content = f"""import {{ api }} from '@/shared/api/client';

export const {name}Service = {{
  getAll: async () => {{
    const response = await api.get('/{feature}/{name.lower()}');
    return response.data;
  }},
}};
"""
    save_file(f"sportsmanagement_frontend/src/features/{{feature}}/services/{{name}}Service.ts", content)
    # Scaffold Pytest
    backend_test = f"""import pytest
from app.domains.{feature}.services.{name.lower()}_service import {name}Service

def test_get_all_{name.lower()}():
    # Implement enterprise test logic
    assert True
"""
    save_file(f"sportsmanagement/tests/{feature}/test_{name.lower()}.py", backend_test)

def save_file(rel_path, content):
    base_dir = r"d:\Alders360"
    abs_path = os.path.join(base_dir, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w") as f:
        f.write(content)
    print(f"Generated: {{abs_path}}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generator.py <type> <feature> <name>")
        print("Types: component, hook, service, feature")
    else:
        g_type, feature, name = sys.argv[1:4]
        if g_type == "component": generate_component(feature, name)
        elif g_type == "hook": generate_hook(feature, name)
        elif g_type == "service": generate_service(feature, name)
        elif g_type == "feature":
            generate_component(feature, f"{{name}}Root")
            generate_hook(feature, name)
            generate_service(feature, name)
