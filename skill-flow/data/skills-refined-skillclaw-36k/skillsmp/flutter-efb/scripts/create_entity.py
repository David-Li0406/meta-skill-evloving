#!/usr/bin/env python3
"""
Generate a domain entity with optional freezed support.

Usage:
    python create_entity.py --name Airport --fields "id:String,name:String,lat:double"
    python create_entity.py --name Airport --fields "id:String,name:String" --freezed
"""

import argparse
from pathlib import Path


def to_snake_case(pascal_str: str) -> str:
    """Convert PascalCase to snake_case."""
    result = []
    for i, char in enumerate(pascal_str):
        if char.isupper() and i > 0:
            result.append('_')
        result.append(char.lower())
    return ''.join(result)


def parse_fields(fields_str: str) -> list[tuple[str, str, bool]]:
    """Parse field definitions into (name, type, required) tuples."""
    fields = []
    for field in fields_str.split(','):
        field = field.strip()
        if not field:
            continue

        required = not field.endswith('?')
        field = field.rstrip('?')

        parts = field.split(':')
        if len(parts) == 2:
            name, type_ = parts
            fields.append((name.strip(), type_.strip(), required))
        else:
            fields.append((parts[0].strip(), 'String', required))

    return fields


def generate_freezed_entity(class_name: str, fields: list[tuple[str, str, bool]]) -> str:
    """Generate a freezed entity."""
    snake_name = to_snake_case(class_name)

    field_lines = []
    for name, type_, required in fields:
        if required:
            field_lines.append(f'    required {type_} {name},')
        else:
            field_lines.append(f'    {type_}? {name},')

    fields_code = '\n'.join(field_lines)

    return f'''import 'package:freezed_annotation/freezed_annotation.dart';

part '{snake_name}.freezed.dart';
part '{snake_name}.g.dart';

@freezed
class {class_name} with _${class_name} {{
  const factory {class_name}({{
{fields_code}
  }}) = _{class_name};

  factory {class_name}.fromJson(Map<String, dynamic> json) =>
      _${class_name}FromJson(json);
}}
'''


def generate_plain_entity(class_name: str, fields: list[tuple[str, str, bool]]) -> str:
    """Generate a plain Dart entity."""
    # Field declarations
    field_decls = []
    for name, type_, required in fields:
        if required:
            field_decls.append(f'  final {type_} {name};')
        else:
            field_decls.append(f'  final {type_}? {name};')

    # Constructor params
    constructor_params = []
    for name, type_, required in fields:
        if required:
            constructor_params.append(f'    required this.{name},')
        else:
            constructor_params.append(f'    this.{name},')

    # Equality fields
    equality_checks = ' &&\n          '.join(
        f'{name} == other.{name}' for name, _, _ in fields
    )

    # Hash fields
    hash_fields = ', '.join(name for name, _, _ in fields)

    # FromJson
    from_json_fields = []
    for name, type_, required in fields:
        if type_ == 'String':
            from_json_fields.append(f"      {name}: json['{name}'] as String{'?' if not required else ''},")
        elif type_ == 'int':
            from_json_fields.append(f"      {name}: json['{name}'] as int{'?' if not required else ''},")
        elif type_ == 'double':
            from_json_fields.append(f"      {name}: (json['{name}'] as num{'?' if not required else ''}){'?' if not required else ''}.toDouble(),")
        elif type_ == 'bool':
            from_json_fields.append(f"      {name}: json['{name}'] as bool{'?' if not required else ''},")
        else:
            from_json_fields.append(f"      {name}: json['{name}'],")

    # ToJson
    to_json_fields = ',\n      '.join(f"'{name}': {name}" for name, _, _ in fields)

    return f'''class {class_name} {{
{chr(10).join(field_decls)}

  const {class_name}({{
{chr(10).join(constructor_params)}
  }});

  factory {class_name}.fromJson(Map<String, dynamic> json) {{
    return {class_name}(
{chr(10).join(from_json_fields)}
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
      {to_json_fields},
    }};
  }}

  {class_name} copyWith({{
{chr(10).join(f'    {type_}{"?" if not req else ""} {name},' for name, type_, req in fields)}
  }}) {{
    return {class_name}(
{chr(10).join(f'      {name}: {name} ?? this.{name},' for name, _, _ in fields)}
    );
  }}

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is {class_name} &&
          runtimeType == other.runtimeType &&
          {equality_checks};

  @override
  int get hashCode => Object.hash({hash_fields});

  @override
  String toString() => '{class_name}({", ".join(f"{name}: ${name}" for name, _, _ in fields)})';
}}
'''


def main():
    parser = argparse.ArgumentParser(description='Generate a domain entity')
    parser.add_argument('--name', '-n', required=True, help='Entity name (PascalCase)')
    parser.add_argument('--fields', '-f', required=True, help='Fields: "name:Type,field2:Type?"')
    parser.add_argument('--freezed', action='store_true', help='Use freezed annotations')
    parser.add_argument('--output', '-o', help='Output directory')

    args = parser.parse_args()

    fields = parse_fields(args.fields)

    if args.freezed:
        content = generate_freezed_entity(args.name, fields)
    else:
        content = generate_plain_entity(args.name, fields)

    if args.output:
        output_path = Path(args.output) / f'{to_snake_case(args.name)}.dart'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        print(f"Created: {output_path}")
    else:
        print(content)


if __name__ == '__main__':
    main()
