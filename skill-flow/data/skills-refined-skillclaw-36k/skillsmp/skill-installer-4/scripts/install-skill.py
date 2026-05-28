#!/usr/bin/env python3
"""从 Git 仓库、本地目录或 .skill 文件安装技能到指定目录"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import zipfile

from git_utils import parse_git_url, build_repo_url, run_git_command, git_request


class InstallError(Exception):
    """安装技能时的错误"""
    pass


def validate_skill_directory(path: str) -> None:
    """验证技能目录
    
    Args:
        path: 技能目录路径
    
    Raises:
        InstallError: 验证失败
    """
    if not os.path.isdir(path):
        raise InstallError(f"技能目录不存在: {path}")
    
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        raise InstallError(f"技能目录中缺少 SKILL.md: {path}")


def install_from_skill_file(skill_file: str, dest_dir: str, force: bool = False) -> str:
    """从 .skill 文件安装技能
    
    Args:
        skill_file: .skill 文件路径
        dest_dir: 目标目录
        force: 是否强制覆盖
    
    Returns:
        安装后的技能路径
    """
    if not os.path.isfile(skill_file):
        raise InstallError(f".skill 文件不存在: {skill_file}")
    
    if not skill_file.endswith('.skill'):
        raise InstallError(f"文件必须以 .skill 结尾: {skill_file}")
    
    # 创建临时目录解压
    temp_dir = tempfile.mkdtemp(prefix="skill-extract-")
    
    try:
        # 解压 .skill 文件（实际上是 zip 文件）
        with zipfile.ZipFile(skill_file, 'r') as zf:
            zf.extractall(temp_dir)
            # 获取顶层目录
            top_levels = {name.split("/")[0] for name in zf.namelist() if name and "/" in name}
            if not top_levels:
                # 没有目录层级，直接使用临时目录
                skill_dir = temp_dir
                skill_name = os.path.splitext(os.path.basename(skill_file))[0]
            else:
                if len(top_levels) != 1:
                    raise InstallError(".skill 文件结构异常，应包含单个技能目录")
                skill_name = next(iter(top_levels))
                skill_dir = os.path.join(temp_dir, skill_name)
        
        # 验证技能
        validate_skill_directory(skill_dir)
        
        # 复制到目标目录
        dest_skill_dir = os.path.join(dest_dir, skill_name)
        
        if os.path.exists(dest_skill_dir):
            if not force:
                raise InstallError(f"技能已存在: {dest_skill_dir}。使用 --force 强制覆盖")
            shutil.rmtree(dest_skill_dir)
        
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copytree(skill_dir, dest_skill_dir)
        
        return dest_skill_dir
        
    finally:
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


def install_from_local(source_path: str, skill_name: str, dest_dir: str, force: bool = False) -> str:
    """从本地目录安装技能
    
    Args:
        source_path: 源技能目录路径
        skill_name: 技能名称
        dest_dir: 目标目录
        force: 是否强制覆盖
    
    Returns:
        安装后的技能路径
    """
    if not os.path.isdir(source_path):
        raise InstallError(f"源目录不存在: {source_path}")
    
    validate_skill_directory(source_path)
    
    dest_skill_dir = os.path.join(dest_dir, skill_name)
    
    if os.path.exists(dest_skill_dir):
        if not force:
            raise InstallError(f"技能已存在: {dest_skill_dir}。使用 --force 强制覆盖")
        shutil.rmtree(dest_skill_dir)
    
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copytree(source_path, dest_skill_dir)
    
    return dest_skill_dir


def download_skill_file(url: str, temp_dir: str) -> str:
    """下载远程 .skill 文件
    
    Args:
        url: .skill 文件的 URL
        temp_dir: 临时目录
    
    Returns:
        下载的 .skill 文件路径
    """
    if not url.endswith('.skill'):
        raise InstallError("URL 必须指向 .skill 文件")
    
    skill_filename = os.path.basename(url)
    skill_path = os.path.join(temp_dir, skill_filename)
    
    try:
        # 尝试使用 git_request（支持认证）
        import urllib.request
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            payload = resp.read()
    except Exception as exc:
        raise InstallError(f"下载 .skill 文件失败: {exc}") from exc
    
    with open(skill_path, "wb") as f:
        f.write(payload)
    
    return skill_path


def download_repo_zip(url_info: dict, temp_dir: str) -> str:
    """下载仓库 ZIP 文件
    
    Args:
        url_info: URL 解析信息
        temp_dir: 临时目录
    
    Returns:
        解压后的仓库根目录
    """
    platform = url_info["platform"]
    owner = url_info["owner"]
    repo = url_info["repo"]
    ref = url_info["ref"]
    host = url_info["host"]
    
    # 构造下载 URL
    if platform == "github":
        zip_url = f"https://codeload.github.com/{owner}/{repo}/zip/{ref}"
    elif platform == "gitlab":
        zip_url = f"https://{host}/{owner}/{repo}/-/archive/{ref}/{repo}-{ref}.zip"
    elif platform == "gitea":
        zip_url = f"https://{host}/{owner}/{repo}/archive/{ref}.zip"
    else:
        raise InstallError(f"不支持的平台: {platform}")
    
    zip_path = os.path.join(temp_dir, "repo.zip")
    
    try:
        payload = git_request(zip_url, "skill-installer", platform)
    except Exception as exc:
        raise InstallError(f"下载失败: {exc}") from exc
    
    with open(zip_path, "wb") as f:
        f.write(payload)
    
    # 解压
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(temp_dir)
        # 获取顶层目录
        top_levels = {name.split("/")[0] for name in zf.namelist() if name}
    
    if not top_levels:
        raise InstallError("下载的压缩包为空")
    
    if len(top_levels) != 1:
        raise InstallError("压缩包结构异常")
    
    return os.path.join(temp_dir, next(iter(top_levels)))


def git_sparse_checkout(url_info: dict, skill_paths: list[str], temp_dir: str) -> str:
    """使用 Git 稀疏检出
    
    Args:
        url_info: URL 解析信息
        skill_paths: 技能路径列表
        temp_dir: 临时目录
    
    Returns:
        仓库根目录
    """
    repo_url = build_repo_url(
        url_info["platform"],
        url_info["host"],
        url_info["owner"],
        url_info["repo"],
        "https"
    )
    
    repo_dir = os.path.join(temp_dir, "repo")
    ref = url_info["ref"]
    
    # 尝试克隆
    returncode, stdout, stderr = run_git_command([
        "git", "clone",
        "--filter=blob:none",
        "--depth", "1",
        "--sparse",
        "--single-branch",
        "--branch", ref,
        repo_url,
        repo_dir
    ])
    
    if returncode != 0:
        # 尝试 SSH
        repo_url = build_repo_url(
            url_info["platform"],
            url_info["host"],
            url_info["owner"],
            url_info["repo"],
            "ssh"
        )
        returncode, stdout, stderr = run_git_command([
            "git", "clone",
            "--filter=blob:none",
            "--depth", "1",
            "--sparse",
            "--single-branch",
            repo_url,
            repo_dir
        ])
        
        if returncode != 0:
            raise InstallError(f"Git 克隆失败: {stderr}")
    
    # 设置稀疏检出
    returncode, stdout, stderr = run_git_command(
        ["git", "sparse-checkout", "set"] + skill_paths,
        cwd=repo_dir
    )
    
    if returncode != 0:
        raise InstallError(f"Git 稀疏检出失败: {stderr}")
    
    # 检出指定引用
    returncode, stdout, stderr = run_git_command(
        ["git", "checkout", ref],
        cwd=repo_dir
    )
    
    if returncode != 0:
        raise InstallError(f"Git 检出失败: {stderr}")
    
    return repo_dir


def install_from_remote(url: str, skill_paths: list[str], dest_dir: str, 
                       ref: str = "main", force: bool = False, 
                       method: str = "auto") -> list[str]:
    """从远程仓库安装技能
    
    Args:
        url: Git 仓库 URL
        skill_paths: 技能路径列表
        dest_dir: 目标目录
        ref: 分支或标签
        force: 是否强制覆盖
        method: 安装方法 (auto/download/git)
    
    Returns:
        已安装技能路径列表
    """
    url_info = parse_git_url(url)
    if ref:
        url_info["ref"] = ref
    
    temp_dir = tempfile.mkdtemp(prefix="skill-install-")
    
    try:
        # 准备仓库
        if method in ("download", "auto"):
            try:
                repo_root = download_repo_zip(url_info, temp_dir)
            except InstallError as exc:
                if method == "download":
                    raise
                # 回退到 Git
                repo_root = git_sparse_checkout(url_info, skill_paths, temp_dir)
        else:
            repo_root = git_sparse_checkout(url_info, skill_paths, temp_dir)
        
        # 安装技能
        installed = []
        for skill_path in skill_paths:
            # 组合完整路径
            if url_info["path"]:
                full_path = os.path.join(url_info["path"], skill_path)
            else:
                full_path = skill_path
            
            source_skill_dir = os.path.join(repo_root, full_path)
            skill_name = os.path.basename(skill_path.rstrip("/"))
            
            validate_skill_directory(source_skill_dir)
            
            dest_skill_dir = os.path.join(dest_dir, skill_name)
            
            if os.path.exists(dest_skill_dir):
                if not force:
                    raise InstallError(f"技能已存在: {dest_skill_dir}。使用 --force 强制覆盖")
                shutil.rmtree(dest_skill_dir)
            
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copytree(source_skill_dir, dest_skill_dir)
            installed.append(dest_skill_dir)
        
        return installed
        
    finally:
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="从 Git 仓库、本地目录或 .skill 文件安装技能到指定目录"
    )
    parser.add_argument(
        "source",
        help="技能源 (Git 仓库 URL、本地路径或 .skill 文件)"
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="要安装的技能路径（相对于源）。如果源是 .skill 文件则不需要"
    )
    parser.add_argument(
        "--dest",
        required=True,
        help="安装目标目录"
    )
    parser.add_argument(
        "--ref",
        default="main",
        help="Git 分支或标签 (默认: main)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制覆盖已存在的技能"
    )
    parser.add_argument(
        "--method",
        choices=["auto", "download", "git"],
        default="auto",
        help="安装方法 (默认: auto - 优先下载，失败时回退到 git)"
    )
    
    args = parser.parse_args(argv)
    
    try:
        dest_dir = os.path.abspath(args.dest)
        
        # 判断源类型
        # 1. 本地 .skill 文件
        if os.path.isfile(args.source) and args.source.endswith('.skill'):
            installed_path = install_from_skill_file(args.source, dest_dir, args.force)
            skill_name = os.path.basename(installed_path)
            print(f"✓ 已安装 {skill_name} 到 {installed_path}")
        
        # 2. 远程 .skill 文件
        elif args.source.startswith(('http://', 'https://')) and args.source.endswith('.skill'):
            temp_dir = tempfile.mkdtemp(prefix="skill-download-")
            try:
                skill_file = download_skill_file(args.source, temp_dir)
                installed_path = install_from_skill_file(skill_file, dest_dir, args.force)
                skill_name = os.path.basename(installed_path)
                print(f"✓ 已安装 {skill_name} 到 {installed_path}")
            finally:
                if os.path.isdir(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
        
        # 3. 本地目录
        elif os.path.exists(args.source):
            if not args.skills:
                raise InstallError("从本地目录安装时必须指定技能路径")
            if len(args.skills) != 1:
                raise InstallError("从本地目录安装时只能指定一个技能")
            
            skill_path = os.path.join(args.source, args.skills[0])
            skill_name = os.path.basename(args.skills[0].rstrip("/"))
            
            installed_path = install_from_local(
                skill_path,
                skill_name,
                dest_dir,
                args.force
            )
            print(f"✓ 已安装 {skill_name} 到 {installed_path}")
        
        # 4. 远程 Git 仓库
        else:
            if not args.skills:
                raise InstallError("从 Git 仓库安装时必须指定技能路径")
            
            installed_paths = install_from_remote(
                args.source,
                args.skills,
                dest_dir,
                args.ref,
                args.force,
                args.method
            )
            
            for path in installed_paths:
                skill_name = os.path.basename(path)
                print(f"✓ 已安装 {skill_name} 到 {path}")
        
        return 0
        
    except InstallError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"未预期的错误: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
