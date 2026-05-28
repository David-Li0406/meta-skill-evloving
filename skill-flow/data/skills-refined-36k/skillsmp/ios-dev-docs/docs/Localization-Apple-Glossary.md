# Apple Localization Glossary

Use the applelocalization.com API to look up official Apple UI term translations.

## API Usage

```
https://applelocalization.com/api/ios/search?q=<term>&l=Japanese&l=English
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `q` | Search term (e.g., `paste`, `copy`, `settings`) |
| `l` | Languages to include (repeatable: `l=Japanese&l=English`) |

### Platform Variants

- iOS (latest): `/api/ios/search`
- iOS 18: `/api/ios/18/search`
- macOS (latest): `/api/macos/search`
- macOS 15: `/api/macos/15/search`

## Example

To find the Japanese localization for "paste":

```
WebFetch: https://applelocalization.com/api/ios/search?q=paste&l=Japanese&l=English
```

## Common Terms

| English | Japanese |
|---------|----------|
| Paste | ペースト |
| Copy | コピー |
| Cut | カット |
| Settings | 設定 |
| Done | 完了 |
| Cancel | キャンセル |
| Edit | 編集 |
| Delete | 削除 |
| Share | 共有 |
| Save | 保存 |
| OK | OK |
| Back | 戻る |
| Close | 閉じる |
| Search | 検索 |
| Add | 追加 |

## Notes

- Apple platforms use カタカナ for Paste/Copy/Cut (not 貼り付け/コピー/切り取り like Windows)
- Always verify with the API for context-specific translations
- Source: https://applelocalization.com (unofficial but comprehensive)
