#!/usr/bin/env python3
"""鲸落 - 全局版本号一致性自检脚本.

用于在发版/版本号更新时,校验仓库内“强一致文件清单”是否已同步到同一版本号.
脚本只做检查与报告,不会自动修改文件; 发现缺失/不一致时返回非 0 退出码.

Args:
    --root: WhaleFall 仓库根目录(默认: 当前目录).
    --expected: 期望版本号(形如 1.2.3). 未提供时从 `app/settings.py` 的 `APP_VERSION` 推导.
    --relaxed: 放宽检查. 对同一文件允许“任一匹配”通过(默认要求全部匹配).

Returns:
    0 表示全部通过,1 表示存在缺失/不一致.
"""

from __future__ import annotations

import argparse
import logging
import re
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True, slots=True)
class VersionCheck:
    label: str
    relative_path: Path
    patterns: tuple[re.Pattern[str], ...]
    require_all: bool = True


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _detect_expected_version(repo_root: Path) -> str:
    settings_path = repo_root / "app" / "settings.py"
    settings_text = _read_text(settings_path)
    match = re.search(r'^APP_VERSION\s*=\s*"(?P<version>\d+\.\d+\.\d+)"\s*$', settings_text, flags=re.MULTILINE)
    if not match:
        raise ValueError("无法从 app/settings.py 解析 APP_VERSION,请先手动确认版本号")
    return match.group("version")


def _build_checks(expected: str, *, relaxed: bool) -> list[VersionCheck]:
    escaped = re.escape(expected)
    v_escaped = re.escape(f"v{expected}")

    require_all = not relaxed
    return [
        VersionCheck(
            label="运行时版本(app/settings.py)",
            relative_path=Path("app/settings.py"),
            patterns=(re.compile(rf'^APP_VERSION\s*=\s*"{escaped}"\s*$', flags=re.MULTILINE),),
        ),
        VersionCheck(
            label="项目版本(pyproject.toml)",
            relative_path=Path("pyproject.toml"),
            patterns=(re.compile(rf'^version\s*=\s*"{escaped}"\s*$', flags=re.MULTILINE),),
        ),
        VersionCheck(
            label="示例环境(env.example)",
            relative_path=Path("env.example"),
            patterns=(re.compile(rf"^APP_VERSION\s*=\s*{escaped}\s*$", flags=re.MULTILINE),),
        ),
        VersionCheck(
            label="依赖锁(uv.lock: whalefalling)",
            relative_path=Path("uv.lock"),
            patterns=(
                re.compile(
                    rf'(?ms)^\[\[package\]\]\s*$.*?^name\s*=\s*"whalefalling"\s*$.*?^version\s*=\s*"{escaped}"\s*$'
                ),
            ),
        ),
        VersionCheck(
            label="部署脚本版本(scripts/deploy/deploy-prod-all.sh)",
            relative_path=Path("scripts/deploy/deploy-prod-all.sh"),
            patterns=(
                re.compile(rf"{v_escaped}"),
                re.compile(rf"版本:\s*{escaped}"),
            ),
            require_all=require_all,
        ),
        VersionCheck(
            label="健康检查/前端元数据(app/routes/main.py)",
            relative_path=Path("app/routes/main.py"),
            patterns=(re.compile(rf'"app_version"\s*:\s*"{escaped}"'),),
        ),
        VersionCheck(
            label="页脚版本(app/templates/base.html)",
            relative_path=Path("app/templates/base.html"),
            patterns=(re.compile(rf"\b{escaped}\b"),),
        ),
        VersionCheck(
            label="Nginx 404 错误页版本(nginx/error_pages/404.html)",
            relative_path=Path("nginx/error_pages/404.html"),
            patterns=(re.compile(rf"{v_escaped}"),),
        ),
        VersionCheck(
            label="Nginx 50x 错误页版本(nginx/error_pages/50x.html)",
            relative_path=Path("nginx/error_pages/50x.html"),
            patterns=(re.compile(rf"{v_escaped}"),),
        ),
        VersionCheck(
            label="README 徽章与页脚版本(README.md)",
            relative_path=Path("README.md"),
            patterns=(
                re.compile(rf"Version-{v_escaped}-"),
                re.compile(rf"\*\*版本\*\*:\s*{v_escaped}"),
            ),
            require_all=require_all,
        ),
        VersionCheck(
            label="变更日志版本(CHANGELOG.md)",
            relative_path=Path("CHANGELOG.md"),
            patterns=(re.compile(rf"^##\s*\[{escaped}\]\s*-", flags=re.MULTILINE),),
        ),
        VersionCheck(
            label="About 时间轴版本(app/templates/about.html)",
            relative_path=Path("app/templates/about.html"),
            patterns=(
                re.compile(rf'"version"\s*:\s*"{escaped}"'),
                re.compile(rf"版本\s*{escaped}"),
            ),
            require_all=require_all,
        ),
    ]


def _check_one(repo_root: Path, check: VersionCheck) -> list[str]:
    path = repo_root / check.relative_path
    if not path.exists():
        return ["文件不存在"]

    text = _read_text(path)
    matched = [bool(pattern.search(text)) for pattern in check.patterns]

    if check.require_all:
        if all(matched):
            return []
        missing = [pattern.pattern for pattern, ok in zip(check.patterns, matched, strict=True) if not ok]
        return [f"缺失匹配: {missing_item}" for missing_item in missing]

    if any(matched):
        return []

    joined = " | ".join(pattern.pattern for pattern in check.patterns)
    return [f"未命中任一匹配: {joined}"]


def main() -> int:
    parser = argparse.ArgumentParser(description="WhaleFall 全局版本号一致性自检")
    parser.add_argument("--root", default=".", help="WhaleFall 仓库根目录(默认: 当前目录)")
    parser.add_argument("--expected", default="", help="期望版本号(形如 1.2.3). 默认从 APP_VERSION 推导")
    parser.add_argument("--relaxed", action="store_true", help="放宽检查(同一文件允许任一匹配通过)")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    expected = args.expected.strip() or _detect_expected_version(repo_root)
    if not SEMVER_PATTERN.match(expected):
        logger.error("期望版本号非法: %s (需要形如 1.2.3)", expected)
        return 1

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    checks = _build_checks(expected, relaxed=args.relaxed)
    failures: list[str] = []

    logger.info("目标版本号: %s", expected)
    logger.info("检查数量: %s", len(checks))

    for check in checks:
        problems = _check_one(repo_root, check)
        if problems:
            failures.append(f"{check.relative_path}: {check.label}")
            logger.error("❌ %s (%s)", check.label, check.relative_path)
            for problem in problems:
                logger.error("   - %s", problem)
            continue

        logger.info("✅ %s (%s)", check.label, check.relative_path)

    if failures:
        logger.error("检查未通过(失败项: %s)", len(failures))
        return 1

    logger.info("检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
