#!/usr/bin/env python3
"""
Generate a new feature scaffold for MagentaLine EFB.

Creates the standard directory structure with:
- Domain layer (entities, repositories, use cases)
- Data layer (models, data sources, repository implementations)
- Presentation layer (BLoC, pages, widgets)

Usage:
    python create_feature.py --name weather
    python create_feature.py --name airports --bloc --freezed
"""

import argparse
import os
from pathlib import Path


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return ''.join(word.capitalize() for word in snake_str.split('_'))


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    pascal = to_pascal_case(snake_str)
    return pascal[0].lower() + pascal[1:]


def create_directory(path: Path):
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    print(f"  Created: {path}")


def write_file(path: Path, content: str):
    """Write content to file."""
    path.write_text(content)
    print(f"  Created: {path}")


def generate_entity(feature_name: str, use_freezed: bool) -> str:
    """Generate the main entity file."""
    class_name = to_pascal_case(feature_name)

    if use_freezed:
        return f'''import 'package:freezed_annotation/freezed_annotation.dart';

part '{feature_name}.freezed.dart';

@freezed
class {class_name} with _${class_name} {{
  const factory {class_name}({{
    required String id,
    // TODO: Add fields
  }}) = _{class_name};
}}
'''
    else:
        return f'''class {class_name} {{
  final String id;
  // TODO: Add fields

  const {class_name}({{
    required this.id,
  }});

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is {class_name} &&
          runtimeType == other.runtimeType &&
          id == other.id;

  @override
  int get hashCode => id.hashCode;
}}
'''


def generate_repository_interface(feature_name: str) -> str:
    """Generate repository interface."""
    class_name = to_pascal_case(feature_name)
    var_name = to_camel_case(feature_name)

    return f'''import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/{feature_name}.dart';

abstract class {class_name}Repository {{
  Future<Either<Failure, {class_name}>> get{class_name}(String id);
  Future<Either<Failure, List<{class_name}>>> getAll{class_name}s();
  // TODO: Add more methods
}}
'''


def generate_use_case(feature_name: str) -> str:
    """Generate a use case."""
    class_name = to_pascal_case(feature_name)

    return f'''import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/{feature_name}.dart';
import '../repositories/{feature_name}_repository.dart';

class Get{class_name} implements UseCase<{class_name}, String> {{
  final {class_name}Repository repository;

  Get{class_name}(this.repository);

  @override
  Future<Either<Failure, {class_name}>> call(String id) {{
    return repository.get{class_name}(id);
  }}
}}
'''


def generate_model(feature_name: str) -> str:
    """Generate data model."""
    class_name = to_pascal_case(feature_name)

    return f'''import '../../domain/entities/{feature_name}.dart';

class {class_name}Model extends {class_name} {{
  const {class_name}Model({{
    required super.id,
  }});

  factory {class_name}Model.fromJson(Map<String, dynamic> json) {{
    return {class_name}Model(
      id: json['id'] as String,
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
      'id': id,
    }};
  }}

  {class_name} toEntity() => this;

  factory {class_name}Model.fromEntity({class_name} entity) {{
    return {class_name}Model(
      id: entity.id,
    );
  }}
}}
'''


def generate_data_source(feature_name: str) -> str:
    """Generate local data source."""
    class_name = to_pascal_case(feature_name)

    return f'''import '../models/{feature_name}_model.dart';

abstract class {class_name}LocalDataSource {{
  Future<{class_name}Model> get{class_name}(String id);
  Future<List<{class_name}Model>> getAll{class_name}s();
  Future<void> cache{class_name}({class_name}Model model);
}}

class {class_name}LocalDataSourceImpl implements {class_name}LocalDataSource {{
  final Database database;

  {class_name}LocalDataSourceImpl({{required this.database}});

  @override
  Future<{class_name}Model> get{class_name}(String id) async {{
    // TODO: Implement database query
    throw UnimplementedError();
  }}

  @override
  Future<List<{class_name}Model>> getAll{class_name}s() async {{
    // TODO: Implement database query
    throw UnimplementedError();
  }}

  @override
  Future<void> cache{class_name}({class_name}Model model) async {{
    // TODO: Implement database insert
    throw UnimplementedError();
  }}
}}
'''


def generate_repository_impl(feature_name: str) -> str:
    """Generate repository implementation."""
    class_name = to_pascal_case(feature_name)

    return f'''import 'package:dartz/dartz.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/error/failures.dart';
import '../../domain/entities/{feature_name}.dart';
import '../../domain/repositories/{feature_name}_repository.dart';
import '../datasources/{feature_name}_local_datasource.dart';

class {class_name}RepositoryImpl implements {class_name}Repository {{
  final {class_name}LocalDataSource localDataSource;

  {class_name}RepositoryImpl({{required this.localDataSource}});

  @override
  Future<Either<Failure, {class_name}>> get{class_name}(String id) async {{
    try {{
      final model = await localDataSource.get{class_name}(id);
      return Right(model.toEntity());
    }} on CacheException {{
      return Left(CacheFailure());
    }}
  }}

  @override
  Future<Either<Failure, List<{class_name}>>> getAll{class_name}s() async {{
    try {{
      final models = await localDataSource.getAll{class_name}s();
      return Right(models.map((m) => m.toEntity()).toList());
    }} on CacheException {{
      return Left(CacheFailure());
    }}
  }}
}}
'''


def generate_bloc(feature_name: str) -> tuple[str, str, str]:
    """Generate BLoC files."""
    class_name = to_pascal_case(feature_name)

    event = f'''part of '{feature_name}_bloc.dart';

abstract class {class_name}Event {{}}

class Load{class_name} extends {class_name}Event {{
  final String id;
  Load{class_name}(this.id);
}}

class LoadAll{class_name}s extends {class_name}Event {{}}
'''

    state = f'''part of '{feature_name}_bloc.dart';

abstract class {class_name}State {{}}

class {class_name}Initial extends {class_name}State {{}}

class {class_name}Loading extends {class_name}State {{}}

class {class_name}Loaded extends {class_name}State {{
  final {class_name} {to_camel_case(feature_name)};
  {class_name}Loaded(this.{to_camel_case(feature_name)});
}}

class {class_name}sLoaded extends {class_name}State {{
  final List<{class_name}> {to_camel_case(feature_name)}s;
  {class_name}sLoaded(this.{to_camel_case(feature_name)}s);
}}

class {class_name}Error extends {class_name}State {{
  final String message;
  {class_name}Error(this.message);
}}
'''

    bloc = f'''import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/entities/{feature_name}.dart';
import '../../domain/usecases/get_{feature_name}.dart';

part '{feature_name}_event.dart';
part '{feature_name}_state.dart';

class {class_name}Bloc extends Bloc<{class_name}Event, {class_name}State> {{
  final Get{class_name} get{class_name};

  {class_name}Bloc({{required this.get{class_name}}}) : super({class_name}Initial()) {{
    on<Load{class_name}>(_onLoad{class_name});
  }}

  Future<void> _onLoad{class_name}(
    Load{class_name} event,
    Emitter<{class_name}State> emit,
  ) async {{
    emit({class_name}Loading());

    final result = await get{class_name}(event.id);

    result.fold(
      (failure) => emit({class_name}Error(failure.message)),
      ({to_camel_case(feature_name)}) => emit({class_name}Loaded({to_camel_case(feature_name)})),
    );
  }}
}}
'''

    return event, state, bloc


def generate_page(feature_name: str) -> str:
    """Generate the main page."""
    class_name = to_pascal_case(feature_name)

    return f'''import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/{feature_name}_bloc.dart';

class {class_name}Page extends StatelessWidget {{
  const {class_name}Page({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('{class_name}'),
      ),
      body: BlocBuilder<{class_name}Bloc, {class_name}State>(
        builder: (context, state) {{
          if (state is {class_name}Loading) {{
            return const Center(child: CircularProgressIndicator());
          }}

          if (state is {class_name}Error) {{
            return Center(child: Text(state.message));
          }}

          if (state is {class_name}Loaded) {{
            return Center(
              child: Text('Loaded: ${{state.{to_camel_case(feature_name)}.id}}'),
            );
          }}

          return const Center(child: Text('Press button to load'));
        }},
      ),
    );
  }}
}}
'''


def create_feature(feature_name: str, use_bloc: bool, use_freezed: bool, base_path: str):
    """Create the complete feature scaffold."""
    base = Path(base_path) / 'lib' / 'features' / feature_name

    print(f"\nCreating feature: {feature_name}")
    print("=" * 50)

    # Domain layer
    domain = base / 'domain'
    create_directory(domain / 'entities')
    create_directory(domain / 'repositories')
    create_directory(domain / 'usecases')

    write_file(domain / 'entities' / f'{feature_name}.dart', generate_entity(feature_name, use_freezed))
    write_file(domain / 'repositories' / f'{feature_name}_repository.dart', generate_repository_interface(feature_name))
    write_file(domain / 'usecases' / f'get_{feature_name}.dart', generate_use_case(feature_name))

    # Data layer
    data = base / 'data'
    create_directory(data / 'datasources')
    create_directory(data / 'models')
    create_directory(data / 'repositories')

    write_file(data / 'models' / f'{feature_name}_model.dart', generate_model(feature_name))
    write_file(data / 'datasources' / f'{feature_name}_local_datasource.dart', generate_data_source(feature_name))
    write_file(data / 'repositories' / f'{feature_name}_repository_impl.dart', generate_repository_impl(feature_name))

    # Presentation layer
    presentation = base / 'presentation'
    create_directory(presentation / 'pages')
    create_directory(presentation / 'widgets')

    if use_bloc:
        create_directory(presentation / 'bloc')
        event, state, bloc = generate_bloc(feature_name)
        write_file(presentation / 'bloc' / f'{feature_name}_event.dart', event)
        write_file(presentation / 'bloc' / f'{feature_name}_state.dart', state)
        write_file(presentation / 'bloc' / f'{feature_name}_bloc.dart', bloc)

    write_file(presentation / 'pages' / f'{feature_name}_page.dart', generate_page(feature_name))

    print("\n" + "=" * 50)
    print(f"Feature '{feature_name}' created successfully!")

    if use_freezed:
        print("\nRun build_runner to generate freezed files:")
        print("  flutter pub run build_runner build")


def main():
    parser = argparse.ArgumentParser(description='Generate a new feature scaffold')
    parser.add_argument('--name', '-n', required=True, help='Feature name (snake_case)')
    parser.add_argument('--bloc', action='store_true', help='Include BLoC state management')
    parser.add_argument('--freezed', action='store_true', help='Use freezed for entities')
    parser.add_argument('--path', '-p', default='.', help='Base project path')

    args = parser.parse_args()

    create_feature(args.name, args.bloc, args.freezed, args.path)


if __name__ == '__main__':
    main()
