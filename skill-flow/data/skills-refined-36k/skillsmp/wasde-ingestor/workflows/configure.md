<required_reading>
**執行此工作流程前，請先閱讀：**
1. references/commodities-overview.md - 了解可配置的商品範圍
2. templates/config.yaml - 標準配置模板
</required_reading>

<objective>
配置 WASDE Ingestor 的商品範圍、輸出路徑、解析選項等參數。
</objective>

<process>
**Step 1: 確認配置需求**

詢問用戶要配置哪些項目：

1. **商品範圍** - 選擇要抓取的商品
2. **數據範圍** - US only, World only, 或兩者
3. **輸出設定** - 輸出目錄、格式、儲存後端
4. **解析設定** - PDF/HTML 優先順序、fallback 行為
5. **驗證設定** - 驗證嚴格度、容許誤差

**Step 2: 商品配置**

```yaml
# 商品群組快捷選項
commodity_groups:
  all:
    description: "所有商品"
    includes:
      - grains
      - oilseeds
      - cotton
      - livestock
      - sugar

  grains:
    description: "穀物類"
    includes:
      - wheat
      - wheat_by_class
      - corn
      - rice
      - barley
      - sorghum
      - oats

  oilseeds:
    description: "油籽類"
    includes:
      - soybeans
      - soybean_oil
      - soybean_meal

  cotton:
    description: "棉花"
    includes:
      - cotton_us
      - cotton_world

  livestock:
    description: "畜產品（僅 US）"
    includes:
      - beef
      - pork
      - broiler
      - turkey
      - eggs
      - dairy

  sugar:
    description: "糖（US + Mexico）"
    includes:
      - sugar_us
      - sugar_mexico

# 單一商品選項
individual_commodities:
  - wheat
  - corn
  - soybeans
  - rice
  - cotton
  - beef
  - pork
  # ... 完整列表見 references/commodities-overview.md
```

**Step 3: 生成配置文件**

```python
def generate_config(user_selections):
    """根據用戶選擇生成配置文件"""

    config = {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),

        # 商品配置
        "commodities": {
            "selection": user_selections.get('commodities', 'all'),
            "scope": user_selections.get('scope', ['us', 'world']),
            "exclude": user_selections.get('exclude', [])
        },

        # 輸出配置
        "output": {
            "dir": user_selections.get('output_dir', './data/wasde'),
            "format": user_selections.get('format', 'parquet'),
            "storage": {
                "kind": user_selections.get('storage_kind', 'local'),
                "bucket": user_selections.get('bucket'),
                "prefix": user_selections.get('prefix')
            }
        },

        # 解析配置
        "parsing": {
            "prefer": user_selections.get('prefer_format', 'pdf'),
            "allow_fallback": user_selections.get('allow_fallback', True),
            "fuzzy_match_threshold": user_selections.get('fuzzy_threshold', 0.8),
            "locale": user_selections.get('locale', 'en_US')
        },

        # 驗證配置
        "validation": {
            "strict_mode": user_selections.get('strict_mode', False),
            "balance_tolerance": user_selections.get('balance_tolerance', 'auto'),
            "range_check": user_selections.get('range_check', True),
            "schema_drift_action": user_selections.get('drift_action', 'warn')
        },

        # 網路配置
        "network": {
            "timeout_seconds": user_selections.get('timeout', 30),
            "max_retries": user_selections.get('max_retries', 5),
            "backoff_strategy": "exponential",
            "user_agent": "WASDE-Ingestor/0.2.0"
        },

        # 日誌配置
        "logging": {
            "level": user_selections.get('log_level', 'info'),
            "emit_metrics": user_selections.get('emit_metrics', True),
            "trace_spans": user_selections.get('trace_spans', True)
        }
    }

    return config
```

**Step 4: 驗證配置**

```python
def validate_config(config):
    """驗證配置的有效性"""

    errors = []
    warnings = []

    # 檢查商品配置
    valid_commodities = get_all_valid_commodities()
    if config['commodities']['selection'] not in ['all'] + list(commodity_groups.keys()):
        if not all(c in valid_commodities for c in config['commodities']['selection']):
            errors.append("Invalid commodity in selection")

    # 檢查 scope 配置
    if 'world' in config['commodities']['scope']:
        livestock_selected = any(
            c in ['beef', 'pork', 'broiler', 'turkey', 'eggs', 'dairy', 'livestock']
            for c in expand_commodity_selection(config['commodities']['selection'])
        )
        if livestock_selected:
            warnings.append("Livestock commodities only have US data, world scope will be ignored")

    # 檢查輸出目錄
    output_dir = config['output']['dir']
    if not os.path.exists(output_dir):
        warnings.append(f"Output directory {output_dir} does not exist, will be created")

    # 檢查儲存配置
    if config['output']['storage']['kind'] in ['s3', 'gcs']:
        if not config['output']['storage']['bucket']:
            errors.append("Bucket is required for S3/GCS storage")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
```

**Step 5: 保存配置**

```python
import yaml

def save_config(config, output_path=None):
    """保存配置到文件"""

    if output_path is None:
        output_path = os.path.join(config['output']['dir'], 'wasde_config.yaml')

    # 確保目錄存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

    print(f"Configuration saved to: {output_path}")
    return output_path
```

**Step 6: 載入配置**

```python
def load_config(config_path=None):
    """載入配置文件"""

    if config_path is None:
        # 嘗試默認位置
        default_paths = [
            './wasde_config.yaml',
            './data/wasde/wasde_config.yaml',
            os.path.expanduser('~/.wasde/config.yaml')
        ]
        for path in default_paths:
            if os.path.exists(path):
                config_path = path
                break

    if config_path is None:
        return get_default_config()

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # 合併默認值
    config = merge_with_defaults(config, get_default_config())

    return config
```
</process>

<config_templates>
**常用配置模板：**

**穀物分析師：**
```yaml
commodities:
  selection: grains
  scope: [us, world]
output:
  dir: ./data/grains
validation:
  strict_mode: true
```

**大豆專家：**
```yaml
commodities:
  selection: oilseeds
  scope: [us, world]
output:
  dir: ./data/oilseeds
validation:
  balance_tolerance: 5.0
```

**美國畜產：**
```yaml
commodities:
  selection: livestock
  scope: [us]
output:
  dir: ./data/livestock
```

**完整監控：**
```yaml
commodities:
  selection: all
  scope: [us, world]
output:
  dir: ./data/wasde
logging:
  level: debug
  emit_metrics: true
```
</config_templates>

<success_criteria>
此工作流程成功完成時：
- [ ] 用戶確認商品選擇
- [ ] 生成有效的配置文件
- [ ] 配置驗證通過（無 errors）
- [ ] 配置文件保存成功
- [ ] 用戶了解所有 warnings
</success_criteria>
