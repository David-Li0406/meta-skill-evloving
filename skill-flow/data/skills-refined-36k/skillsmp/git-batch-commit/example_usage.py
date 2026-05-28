#!/usr/bin/env python3
"""
Example usage script for git-batch-commit skill.
Demonstrates how to use the skill modules programmatically.
"""

import json
from git_analyzer import GitAnalyzer
from batch_committer import BatchCommitter
from commit_language import CommitLanguageHandler


def main():
    """Main execution function demonstrating skill usage."""

    print("=" * 70)
    print("Git Batch Commit Skill - Example Usage")
    print("=" * 70)
    print()

    # Step 1: Analyze repository
    print("Step 1: Analyzing repository...")
    print("-" * 70)

    analyzer = GitAnalyzer(threshold=10)
    analysis = analyzer.analyze_repository()

    print(f"Total files: {analysis['batch_analysis']['total_files']}")
    print(f"Threshold: {analysis['batch_analysis']['threshold']}")
    print(f"Requires batching: {analysis['batch_analysis']['requires_batching']}")
    print(f"Recommended batches: {analysis['batch_analysis']['recommended_batches']}")
    print()

    # Step 2: Create batch plans
    print("Step 2: Creating batch commit plans...")
    print("-" * 70)

    # Example with English
    committer_en = BatchCommitter(language='en', dry_run=True)
    plans_en = committer_en.create_batch_plan(analysis)

    print("\nEnglish Batch Plans:")
    for plan in plans_en[:3]:  # Show first 3 batches
        print(f"\nBatch {plan['batch_id']}: {plan['change_type']}({plan['scope']})")
        print(f"Files ({plan['file_count']}): {', '.join(plan['files'][:2])}...")
        print(f"Message: {plan['commit_message'].split(chr(10))[0]}")

    # Example with Chinese
    print("\n" + "=" * 70)
    print("Chinese Batch Plans:")
    print("-" * 70)

    committer_zh = BatchCommitter(language='zh', dry_run=True)
    plans_zh = committer_zh.create_batch_plan(analysis)

    for plan in plans_zh[:3]:  # Show first 3 batches
        print(f"\nBatch {plan['batch_id']}: {plan['change_type']}({plan['scope']})")
        print(f"Files ({plan['file_count']}): {', '.join(plan['files'][:2])}...")
        print(f"Message: {plan['commit_message'].split(chr(10))[0]}")

    # Step 3: Preview batch commits
    print("\n" + "=" * 70)
    print("Step 3: Preview batch commits (Dry Run)")
    print("-" * 70)

    preview = committer_en.preview_batch_commits(plans_en)
    print(preview[:500] + "...\n[Preview truncated]")

    # Step 4: Language handler examples
    print("\n" + "=" * 70)
    print("Step 4: Language Handler Examples")
    print("-" * 70)

    lang_handler = CommitLanguageHandler(default_language='en')

    # Test language detection
    print("\nLanguage Detection:")
    test_texts = [
        ("This is English text", "en"),
        ("这是中文测试", "zh"),
        ("これはテストです", "ja"),
        ("Esto es español", "es")
    ]

    for text, expected in test_texts:
        detected = lang_handler.detect_language_preference(text)
        status = "✓" if detected == expected else "✗"
        print(f"{status} '{text}' -> {detected} (expected: {expected})")

    # Show commit type translations
    print("\nCommit Type Translations:")
    commit_types = ['feat', 'fix', 'docs', 'refactor']
    languages = ['en', 'zh', 'ja']

    for lang in languages:
        print(f"\n{lang.upper()}:")
        for commit_type in commit_types:
            type_name = lang_handler.get_commit_type_name(commit_type, lang)
            action_verb = lang_handler.get_action_verb(commit_type, lang)
            print(f"  {commit_type}: {type_name} ({action_verb})")

    # Step 5: Example commit messages in multiple languages
    print("\n" + "=" * 70)
    print("Step 5: Example Commit Messages in Multiple Languages")
    print("-" * 70)

    for lang in ['en', 'zh', 'ja', 'es']:
        examples = lang_handler.get_language_examples(lang)
        print(f"\n{lang.upper()} Examples:")
        for example in list(examples.values())[:2]:  # Show 2 examples per language
            print(f"  {example}")

    # Step 6: Execution summary (dry run)
    print("\n" + "=" * 70)
    print("Step 6: Execute Batch Commits (DRY RUN)")
    print("-" * 70)

    result = committer_en.execute_batch_commits(plans_en)

    print(f"\nExecution Result:")
    print(f"Success: {result['success']}")
    print(f"Total batches: {result['total_batches']}")
    print(f"Successful: {len(result['successful_commits'])}")
    print(f"Failed: {len(result['failed_commits'])}")
    print(f"Summary: {result['summary']}")

    # Export results to JSON
    print("\n" + "=" * 70)
    print("Step 7: Exporting Results to JSON")
    print("-" * 70)

    output_data = {
        'analysis': analysis['batch_analysis'],
        'batches_en': plans_en,
        'batches_zh': plans_zh,
        'execution_result': result
    }

    output_file = 'batch_commit_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Results exported to: {output_file}")

    # Final summary
    print("\n" + "=" * 70)
    print("✓ Example Execution Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. GitAnalyzer detects when batching is needed (> threshold files)")
    print("2. BatchCommitter groups files by feature/functionality")
    print("3. Conventional Commit messages generated automatically")
    print("4. Multilingual support (9 languages)")
    print("5. Dry-run mode allows preview before committing")
    print("6. Smart scope detection from file paths")
    print("7. Safety features: validation, rollback support, conflict detection")
    print("\nReady to use in production! 🚀")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
