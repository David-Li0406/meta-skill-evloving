"""Extract real API schemas from AppWorld environment.

Run with: source /opt/conda/bin/activate appworld-env && python scripts/extract_appworld_schemas.py
"""

import os
import json
import sys

os.environ["APPWORLD_ROOT"] = "/ossfs/workspace/SkillKB/inference/appworld"
sys.path.insert(0, "/ossfs/workspace/SkillKB/inference/appworld")


def extract_all_api_schemas(output_path: str):
    """Extract all API schemas from AppWorld."""
    from appworld import AppWorld, load_task_ids

    task_ids = load_task_ids("train")
    task_id = task_ids[0]

    all_schemas = {}

    with AppWorld(task_id=task_id, experiment_name="schema_extraction") as world:
        app_output = world.execute("print(apis.api_docs.show_app_descriptions())")

        apps_json = json.loads(app_output.strip())
        apps = [app["name"] for app in apps_json]

        print(f"Found {len(apps)} apps: {apps}")

        for app_name in apps:
            print(f"\nExtracting APIs from: {app_name}")

            try:
                api_output = world.execute(f"print(apis.api_docs.show_api_descriptions(app_name='{app_name}'))")

                apis_json = json.loads(api_output.strip())
                api_names = [api["name"] for api in apis_json]

                print(f"  Found {len(api_names)} APIs: {api_names[:5]}...")

                for api_name in api_names:
                    full_name = f"apis.{app_name}.{api_name}"

                    try:
                        doc_output = world.execute(
                            f"print(apis.api_docs.show_api_doc(app_name='{app_name}', api_name='{api_name}'))"
                        )

                        doc_json = json.loads(doc_output.strip())

                        params_props = {}
                        required_params = []
                        for param in doc_json.get("parameters", []):
                            param_name = param["name"]
                            params_props[param_name] = {
                                "type": param.get("type", "string"),
                                "description": param.get("description", "")
                            }
                            if param.get("required", False):
                                required_params.append(param_name)

                        schema = {
                            "type": "function",
                            "function": {
                                "name": full_name,
                                "description": doc_json.get("description", ""),
                                "parameters": {
                                    "type": "object",
                                    "properties": params_props,
                                    "required": required_params
                                },
                                "response_schemas": doc_json.get("response_schemas", {})
                            }
                        }

                        all_schemas[full_name] = schema

                    except Exception as e:
                        print(f"    Error extracting {api_name}: {e}")

            except Exception as e:
                print(f"  Error listing APIs for {app_name}: {e}")

    print(f"\nExtracted {len(all_schemas)} API schemas total")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_schemas, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_path}")

    return all_schemas


def convert_to_list_format(schemas_dict: dict) -> list:
    """Convert dict format to list format for ToolSchemaRegistry."""
    return list(schemas_dict.values())


if __name__ == "__main__":
    output_dir = "/ossfs/workspace/AutoSkills/SkillX/config/schemas"
    os.makedirs(output_dir, exist_ok=True)

    try:
        full_path = f"{output_dir}/appworld_full.json"
        schemas = extract_all_api_schemas(full_path)

        schemas_list = convert_to_list_format(schemas)
        list_path = f"{output_dir}/appworld_schemas.json"
        with open(list_path, "w", encoding="utf-8") as f:
            json.dump(schemas_list, f, ensure_ascii=False, indent=2)
        print(f"List format saved to: {list_path}")

    except Exception as e:
        print(f"Extraction failed: {e}")
        import traceback
        traceback.print_exc()
