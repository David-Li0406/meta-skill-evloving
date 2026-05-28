# Examples

Use these examples as formatting references for the subject/body style and
heredoc-based commit command.

```bash
git commit -m "$(cat <<'EOF'
fix: correct regex escaping for JetBrains IDE bundle identifiers

Karabiner 설정에서 JetBrains IDE 애플리케이션 번들 식별자의 정규식
이스케이프를 수정했습니다. 기존의 `^com\.jetbrains\\..*$` 패턴이
백슬래시를 잘못 이스케이프하여 정규식이 의도대로 작동하지 않았던
문제를 해결했습니다. 이제 `^com\\.jetbrains\\..*$`로 올바르게
수정되어 JetBrains IDE 제품군이 Karabiner 키 매핑 예외 목록에서
정상적으로 인식됩니다.
EOF
)"
```

```bash
git commit -m "$(cat <<'EOF'
feat(karabiner): add JetBrains IDE exception to PC-Style mappings

JetBrains IDE 제품군을 Karabiner 키 매핑 예외에 추가하여
IDE 내장 단축키가 정상 작동하도록 함 (특히 Copy/Paste와 Reload)

- PC-Style Copy/Paste/Cut (Ctrl+C/V/X)에 예외 추가
- PC-Style Reload (Ctrl+R, F5)에 예외 추가
- 들여쓰기 일관성 수정 (탭 → 공백)
EOF
)"
```
