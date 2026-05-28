# Excel Loading (Polars)

## config.yaml shape
```yaml
excel:
  path: "data/users.xlsx"
  sheet_name: "Users"
  columns:
    subject: "ID"
    username: "Username"
    password: "Password"

target:
  subject: "U001"
```

## Loader snippet
```python
import os
from pathlib import Path
import yaml


def find_repo_root(start: Path) -> Path:
    for parent in [start] + list(start.parents):
        if (parent / "config.yaml").is_file():
            return parent
    raise FileNotFoundError(f"config.yaml not found from: {start}")


def load_config():
    repo_root = find_repo_root(Path(__file__).resolve())
    config_path = repo_root / "config.yaml"
    with config_path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh), repo_root


def load_data_from_excel() -> dict:
    config, repo_root = load_config()
    target_subject = os.getenv("PLAYWRIGHT_TARGET_SUBJECT", config["target"]["subject"])

    excel_path = repo_root / config["excel"]["path"]
    sheet_name = config["excel"]["sheet_name"]
    columns = config["excel"]["columns"]

    import polars as pl

    df = pl.read_excel(str(excel_path), sheet_name=sheet_name)
    filtered = df.filter(pl.col(columns["subject"]) == target_subject)
    if filtered.height == 0:
        raise ValueError(
            f"No rows for subject '{target_subject}' in {excel_path} (sheet: {sheet_name})"
        )
    row = filtered.row(0, named=True)

    return {
        var_name: row[col_name]
        for var_name, col_name in columns.items()
        if var_name != "subject"
    }
```

## Notes
- Use polars only.
- Use the first matching row only.
- Raise a clear error when no matching subject is found.
