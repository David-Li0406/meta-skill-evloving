#!/usr/bin/env python3
"""
CI/CDパイプライン設定ファイルを分析し、最適化提案を出力する。

使用方法:
    python analyze_pipeline.py workflow.yml
    python analyze_pipeline.py .gitlab-ci.yml
"""

import sys
import yaml
from pathlib import Path


def analyze_github_actions(config: dict) -> list[str]:
    """GitHub Actionsワークフローを分析"""
    suggestions = []
    
    jobs = config.get("jobs", {})
    
    for job_name, job_config in jobs.items():
        steps = job_config.get("steps", [])
        
        # キャッシュ使用チェック
        has_cache = any(
            step.get("uses", "").startswith("actions/cache") or
            "cache" in str(step.get("with", {}))
            for step in steps
        )
        if not has_cache and len(steps) > 3:
            suggestions.append(f"[{job_name}] キャッシュの使用を検討してください")
        
        # checkout後のfetch-depth
        for step in steps:
            if step.get("uses", "").startswith("actions/checkout"):
                with_config = step.get("with", {})
                if "fetch-depth" not in with_config:
                    suggestions.append(
                        f"[{job_name}] checkout に fetch-depth: 0 または 1 を設定すると高速化できます"
                    )
        
        # 並列化可能性
        needs = job_config.get("needs", [])
        if not needs and job_name not in ["build", "lint", "test"]:
            suggestions.append(
                f"[{job_name}] 'needs' が未設定です。依存関係を明示すると並列実行が最適化されます"
            )
        
        # タイムアウト設定
        if "timeout-minutes" not in job_config:
            suggestions.append(
                f"[{job_name}] timeout-minutes を設定すると、ハング時のコスト削減になります"
            )
    
    # トリガー分析
    on_config = config.get("on", config.get(True, {}))
    if isinstance(on_config, dict):
        if "push" in on_config and "paths" not in on_config.get("push", {}):
            suggestions.append(
                "[trigger] paths フィルタを追加すると、不要なビルドを削減できます"
            )
    
    return suggestions


def analyze_gitlab_ci(config: dict) -> list[str]:
    """GitLab CI設定を分析"""
    suggestions = []
    
    # グローバルキャッシュ
    if "cache" not in config and "default" not in config:
        suggestions.append("[global] グローバルキャッシュの設定を検討してください")
    
    # ステージ定義
    if "stages" not in config:
        suggestions.append("[global] stages を明示的に定義すると可読性が向上します")
    
    # 各ジョブ分析
    reserved_keys = {"stages", "variables", "default", "include", "workflow", "cache"}
    for key, value in config.items():
        if key in reserved_keys or not isinstance(value, dict):
            continue
        
        job_config = value
        
        # rules vs only/except
        if "only" in job_config or "except" in job_config:
            suggestions.append(
                f"[{key}] only/except は非推奨です。rules への移行を推奨します"
            )
        
        # artifacts 有効期限
        artifacts = job_config.get("artifacts", {})
        if artifacts and "expire_in" not in artifacts:
            suggestions.append(
                f"[{key}] artifacts に expire_in を設定してストレージを節約してください"
            )
        
        # needs (DAG)
        if "needs" not in job_config and job_config.get("stage") not in ["build", ".pre"]:
            suggestions.append(
                f"[{key}] needs を使用するとDAGパイプラインで高速化できます"
            )
    
    return suggestions


def main():
    if len(sys.argv) < 2:
        print("使用方法: python analyze_pipeline.py <workflow_file>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"エラー: ファイルが見つかりません: {filepath}")
        sys.exit(1)
    
    with open(filepath) as f:
        config = yaml.safe_load(f)
    
    # ファイルタイプ判定
    if "jobs" in config:
        suggestions = analyze_github_actions(config)
        print(f"=== GitHub Actions 分析結果: {filepath} ===\n")
    elif "stages" in config or any(
        isinstance(v, dict) and "script" in v for v in config.values()
    ):
        suggestions = analyze_gitlab_ci(config)
        print(f"=== GitLab CI 分析結果: {filepath} ===\n")
    else:
        print("警告: ファイルタイプを判定できませんでした")
        suggestions = []
    
    if suggestions:
        print("最適化提案:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print("問題は見つかりませんでした。")
    
    print(f"\n分析完了: {len(suggestions)} 件の提案")


if __name__ == "__main__":
    main()
