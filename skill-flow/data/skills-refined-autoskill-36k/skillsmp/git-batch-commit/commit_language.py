"""
Commit Language Module
Handles multilingual commit message generation and language detection.
"""

from typing import Dict, List, Optional


class CommitLanguageHandler:
    """Manages multilingual commit message generation."""

    # Supported languages
    SUPPORTED_LANGUAGES = ['en', 'zh', 'es', 'fr', 'de', 'ja', 'ko', 'ru', 'pt']

    # Conventional Commit type translations
    COMMIT_TYPE_NAMES = {
        'en': {
            'feat': 'Feature',
            'fix': 'Bug Fix',
            'docs': 'Documentation',
            'refactor': 'Refactor',
            'chore': 'Chore',
            'style': 'Style',
            'test': 'Test',
            'perf': 'Performance'
        },
        'zh': {
            'feat': '新功能',
            'fix': '修复',
            'docs': '文档',
            'refactor': '重构',
            'chore': '杂项',
            'style': '样式',
            'test': '测试',
            'perf': '性能'
        },
        'es': {
            'feat': 'Funcionalidad',
            'fix': 'Corrección',
            'docs': 'Documentación',
            'refactor': 'Refactorización',
            'chore': 'Tarea',
            'style': 'Estilo',
            'test': 'Prueba',
            'perf': 'Rendimiento'
        },
        'ja': {
            'feat': '機能',
            'fix': 'バグ修正',
            'docs': 'ドキュメント',
            'refactor': 'リファクタリング',
            'chore': '雑務',
            'style': 'スタイル',
            'test': 'テスト',
            'perf': 'パフォーマンス'
        },
        'fr': {
            'feat': 'Fonctionnalité',
            'fix': 'Correction',
            'docs': 'Documentation',
            'refactor': 'Refactorisation',
            'chore': 'Tâche',
            'style': 'Style',
            'test': 'Test',
            'perf': 'Performance'
        },
        'de': {
            'feat': 'Funktion',
            'fix': 'Fehlerbehebung',
            'docs': 'Dokumentation',
            'refactor': 'Refaktorierung',
            'chore': 'Aufgabe',
            'style': 'Stil',
            'test': 'Test',
            'perf': 'Leistung'
        }
    }

    # Action verb templates by language
    ACTION_TEMPLATES = {
        'en': {
            'feat': ['add', 'implement', 'introduce', 'create'],
            'fix': ['fix', 'resolve', 'correct', 'repair'],
            'docs': ['update', 'improve', 'add', 'clarify'],
            'refactor': ['refactor', 'restructure', 'improve', 'optimize'],
            'chore': ['update', 'configure', 'maintain', 'upgrade'],
            'style': ['format', 'style', 'improve', 'clean'],
            'test': ['add', 'update', 'improve', 'fix'],
            'perf': ['optimize', 'improve', 'enhance', 'boost']
        },
        'zh': {
            'feat': ['新增', '添加', '实现', '创建'],
            'fix': ['修复', '解决', '纠正', '修正'],
            'docs': ['更新', '完善', '添加', '优化'],
            'refactor': ['重构', '优化', '改进', '调整'],
            'chore': ['更新', '配置', '维护', '升级'],
            'style': ['格式化', '美化', '优化', '调整'],
            'test': ['添加', '更新', '完善', '修复'],
            'perf': ['优化', '提升', '改进', '加速']
        },
        'es': {
            'feat': ['agregar', 'implementar', 'introducir', 'crear'],
            'fix': ['corregir', 'resolver', 'reparar', 'solucionar'],
            'docs': ['actualizar', 'mejorar', 'agregar', 'aclarar'],
            'refactor': ['refactorizar', 'reestructurar', 'mejorar', 'optimizar'],
            'chore': ['actualizar', 'configurar', 'mantener', 'actualizar'],
            'style': ['formatear', 'estilizar', 'mejorar', 'limpiar'],
            'test': ['agregar', 'actualizar', 'mejorar', 'corregir'],
            'perf': ['optimizar', 'mejorar', 'potenciar', 'acelerar']
        },
        'ja': {
            'feat': ['追加', '実装', '導入', '作成'],
            'fix': ['修正', '解決', '訂正', '修復'],
            'docs': ['更新', '改善', '追加', '明確化'],
            'refactor': ['リファクタリング', '再構築', '改善', '最適化'],
            'chore': ['更新', '設定', '保守', 'アップグレード'],
            'style': ['整形', 'スタイル調整', '改善', 'クリーンアップ'],
            'test': ['追加', '更新', '改善', '修正'],
            'perf': ['最適化', '改善', '強化', '高速化']
        }
    }

    def __init__(self, default_language: str = 'en'):
        """
        Initialize language handler.

        Args:
            default_language: Default language code (en, zh, etc.)
        """
        self.default_language = default_language if default_language in self.SUPPORTED_LANGUAGES else 'en'

    def detect_language_preference(self, text_sample: Optional[str] = None) -> str:
        """
        Detect language preference from text sample or system settings.

        Args:
            text_sample: Optional text sample to analyze

        Returns:
            Language code (en, zh, etc.)
        """
        if not text_sample:
            return self.default_language

        # Simple character-based detection
        text_lower = text_sample.lower()

        # Chinese detection (CJK characters)
        chinese_chars = sum(1 for char in text_sample if '\u4e00' <= char <= '\u9fff')
        if chinese_chars > len(text_sample) * 0.2:
            return 'zh'

        # Japanese detection (Hiragana/Katakana)
        japanese_chars = sum(1 for char in text_sample if '\u3040' <= char <= '\u30ff')
        if japanese_chars > len(text_sample) * 0.2:
            return 'ja'

        # Korean detection (Hangul)
        korean_chars = sum(1 for char in text_sample if '\uac00' <= char <= '\ud7af')
        if korean_chars > len(text_sample) * 0.2:
            return 'ko'

        # Spanish indicators
        if any(word in text_lower for word in ['el', 'la', 'de', 'que', 'con', 'por']):
            return 'es'

        # French indicators
        if any(word in text_lower for word in ['le', 'la', 'de', 'que', 'avec', 'pour', 'être']):
            return 'fr'

        # German indicators
        if any(word in text_lower for word in ['der', 'die', 'das', 'und', 'mit', 'für']):
            return 'de'

        # Russian detection (Cyrillic)
        cyrillic_chars = sum(1 for char in text_sample if '\u0400' <= char <= '\u04ff')
        if cyrillic_chars > len(text_sample) * 0.2:
            return 'ru'

        # Default to English
        return 'en'

    def get_commit_type_name(self, commit_type: str, language: str) -> str:
        """
        Get localized name for commit type.

        Args:
            commit_type: Conventional commit type (feat/fix/etc.)
            language: Language code

        Returns:
            Localized commit type name
        """
        lang_names = self.COMMIT_TYPE_NAMES.get(language, self.COMMIT_TYPE_NAMES['en'])
        return lang_names.get(commit_type, commit_type)

    def get_action_verb(self, commit_type: str, language: str, index: int = 0) -> str:
        """
        Get action verb for commit type in specified language.

        Args:
            commit_type: Conventional commit type
            language: Language code
            index: Index of verb variant (0 for default)

        Returns:
            Action verb
        """
        lang_templates = self.ACTION_TEMPLATES.get(language, self.ACTION_TEMPLATES['en'])
        verbs = lang_templates.get(commit_type, lang_templates['feat'])
        return verbs[index % len(verbs)]

    def format_commit_message(
        self,
        commit_type: str,
        scope: str,
        description: str,
        language: str,
        body: Optional[str] = None,
        footer: Optional[str] = None
    ) -> str:
        """
        Format a complete commit message in specified language.

        Args:
            commit_type: Conventional commit type
            scope: Commit scope
            description: Short description
            language: Language code
            body: Optional commit body
            footer: Optional commit footer (breaking changes, refs)

        Returns:
            Formatted commit message
        """
        # Build header (always use English type for Conventional Commits standard)
        if scope and scope != 'general':
            header = f"{commit_type}({scope}): {description}"
        else:
            header = f"{commit_type}: {description}"

        # Build full message
        parts = [header]

        if body:
            parts.append('')  # Blank line
            parts.append(body)

        if footer:
            parts.append('')  # Blank line
            parts.append(footer)

        return '\n'.join(parts)

    def translate_scope(self, scope: str, language: str) -> str:
        """
        Translate scope to target language (for description, not scope field).

        Args:
            scope: Scope name
            language: Target language

        Returns:
            Translated scope (or original if no translation)
        """
        scope_translations = {
            'zh': {
                'auth': '认证',
                'api': '接口',
                'ui': '界面',
                'database': '数据库',
                'core': '核心',
                'config': '配置',
                'tests': '测试',
                'docs': '文档',
                'utils': '工具',
                'backend': '后端',
                'frontend': '前端'
            },
            'ja': {
                'auth': '認証',
                'api': 'API',
                'ui': 'UI',
                'database': 'データベース',
                'core': 'コア',
                'config': '設定',
                'tests': 'テスト',
                'docs': 'ドキュメント',
                'utils': 'ユーティリティ',
                'backend': 'バックエンド',
                'frontend': 'フロントエンド'
            }
        }

        lang_translations = scope_translations.get(language, {})
        return lang_translations.get(scope, scope)

    def get_language_examples(self, language: str) -> Dict[str, str]:
        """
        Get example commit messages in specified language.

        Args:
            language: Language code

        Returns:
            Dictionary of example messages by commit type
        """
        examples = {
            'en': {
                'feat': 'feat(auth): add OAuth2 login support',
                'fix': 'fix(api): resolve null pointer exception in user endpoint',
                'docs': 'docs(readme): update installation instructions',
                'refactor': 'refactor(database): optimize query performance',
                'chore': 'chore(deps): update dependencies to latest versions'
            },
            'zh': {
                'feat': 'feat(auth): 新增OAuth2登录支持',
                'fix': 'fix(api): 修复用户接口空指针异常',
                'docs': 'docs(readme): 更新安装说明',
                'refactor': 'refactor(database): 优化查询性能',
                'chore': 'chore(deps): 更新依赖到最新版本'
            },
            'ja': {
                'feat': 'feat(auth): OAuth2ログインサポートを追加',
                'fix': 'fix(api): ユーザーエンドポイントのnullポインタ例外を修正',
                'docs': 'docs(readme): インストール手順を更新',
                'refactor': 'refactor(database): クエリパフォーマンスを最適化',
                'chore': 'chore(deps): 依存関係を最新バージョンに更新'
            }
        }

        return examples.get(language, examples['en'])


if __name__ == "__main__":
    # Example usage
    handler = CommitLanguageHandler(default_language='en')

    # Test language detection
    print("Language Detection:")
    print(f"Chinese text: {handler.detect_language_preference('这是中文测试')}")
    print(f"English text: {handler.detect_language_preference('This is a test')}")
    print(f"Japanese text: {handler.detect_language_preference('これはテストです')}")

    # Test commit message formatting
    print("\nCommit Message Examples:")

    for lang in ['en', 'zh', 'ja']:
        msg = handler.format_commit_message(
            commit_type='feat',
            scope='auth',
            description=f"{handler.get_action_verb('feat', lang)} OAuth2 login",
            language=lang
        )
        print(f"{lang}: {msg}")

    # Show examples
    print("\nStandard Examples:")
    for lang in ['en', 'zh']:
        examples = handler.get_language_examples(lang)
        print(f"\n{lang.upper()}:")
        for example in examples.values():
            print(f"  {example}")
