# Shell Commands

## OS detection
- Unix/macOS: `uname -s`
- Windows: `$env:OS`

## Config merge (bash, requires jq)
- Merge two JSON files: `jq -s '.[0] * .[1]' base.json override.json > output.json`
- Merge detected patterns: `jq -s '.[0] * .[1]' .code-quality.json detected-patterns.json > .code-quality.json.tmp && mv .code-quality.json.tmp .code-quality.json`
- Backup: `cp .code-quality.json ".code-quality.json.bak.$(date +%Y%m%d_%H%M%S)"`
- Extract category: `jq '.patterns.naming' .code-quality.json`
- Add custom rule: `jq '.custom_rules += [{"name": "new-rule", "category": "naming"}]' .code-quality.json > tmp.json && mv tmp.json .code-quality.json`

## Config merge (PowerShell)
```
function Merge-Configs {
  param([string]$BasePath,[string]$OverridePath,[string]$OutputPath)
  $base = Get-Content $BasePath | ConvertFrom-Json -AsHashtable
  $override = Get-Content $OverridePath | ConvertFrom-Json -AsHashtable
  function Merge-Hashtable($Base,$Override){
    $result = $Base.Clone()
    foreach($key in $Override.Keys){
      if($result.ContainsKey($key) -and $result[$key] -is [hashtable] -and $Override[$key] -is [hashtable]){
        $result[$key] = Merge-Hashtable $result[$key] $Override[$key]
      } else { $result[$key] = $Override[$key] }
    }
    return $result
  }
  $merged = Merge-Hashtable $base $override
  $merged | ConvertTo-Json -Depth 10 | Set-Content $OutputPath
}
```
- Backup: `Copy-Item .code-quality.json ".code-quality.json.bak.$(Get-Date -Format 'yyyyMMdd_HHmmss')"`
- Extract category: `(Get-Content .code-quality.json | ConvertFrom-Json).patterns.naming`
- Add custom rule: `$config = Get-Content .code-quality.json | ConvertFrom-Json; $config.custom_rules += @{name="new-rule"; category="naming"}; $config | ConvertTo-Json -Depth 10 | Set-Content .code-quality.json`

## Pattern operations (bash)
- Find files: `find src -type f \( -name "*.ts" -o -name "*.tsx" \) -not -path "*/node_modules/*"`
- Count pattern: `grep -r "useDataService" src --include="*.ts" --include="*.tsx" | wc -l`
- Locations: `grep -rn "useDataService" src --include="*.ts" --include="*.tsx"`
- Import patterns: `grep -rho "^import.*from.*" src --include="*.ts" | sort | uniq -c | sort -rn | head -20`

## Pattern operations (PowerShell)
- Find files: `Get-ChildItem -Path src -Recurse -Include "*.ts","*.tsx" | Where-Object { $_.FullName -notlike "*node_modules*" }`
- Count pattern: `(Select-String -Path "src\**\*.ts","src\**\*.tsx" -Pattern "useDataService" -Recurse).Count`
- Locations: `Select-String -Path "src\**\*.ts","src\**\*.tsx" -Pattern "useDataService" -Recurse | Select-Object Path, LineNumber, Line`
- Import patterns: `Select-String -Path "src\**\*.ts" -Pattern "^import.*from.*" -Recurse | ForEach-Object { $_.Line } | Sort-Object | Get-Unique | Group-Object | Sort-Object Count -Descending | Select-Object -First 20`

## Validation (bash)
- JSON syntax: `jq empty .code-quality.json`
- Required fields: `jq -e '.version and .patterns' .code-quality.json > /dev/null`
- Version check: `config_version=$(jq -r '.version' .code-quality.json); [[ "$config_version" == "1.0" ]] && echo "Compatible" || echo "Version mismatch"`

## Validation (PowerShell)
- JSON syntax: `Get-Content .code-quality.json | ConvertFrom-Json | Out-Null`
- Required fields: `$c = Get-Content .code-quality.json | ConvertFrom-Json; if ($c.version -and $c.patterns) { "Required fields present" } else { "Missing required fields" }`
- Version check: `$c = Get-Content .code-quality.json | ConvertFrom-Json; if ($c.version -eq "1.0") { "Compatible" } else { "Version mismatch" }`
