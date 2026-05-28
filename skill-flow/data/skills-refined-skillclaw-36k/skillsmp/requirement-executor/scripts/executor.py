#!/usr/bin/env python3
"""
Requirement Executor - 自動化需求驅動任務執行系統
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json
import re

class RequirementExecutor:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.req_dir = self.base_dir / "workspace" / "requirement"
        self.plan_dir = self.base_dir / "workspace" / "plan"
        self.task_dir = self.base_dir / "workspace" / "task"
        self.result_dir = self.base_dir / "workspace" / "report"
        self.history_dir = self.base_dir / "workspace" / "history"
        
        # 確保目錄存在
        self.req_dir.mkdir(exist_ok=True)
        self.plan_dir.mkdir(exist_ok=True)
        self.task_dir.mkdir(exist_ok=True)
        self.result_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)
        
        self.requirements = []
        self.tasks = []
        
    def log(self, message, level="INFO"):
        """記錄訊息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def check_requirements_exist(self):
        """檢查需求文件是否存在"""
        req_files = list(self.req_dir.glob("**/*"))
        req_files = [f for f in req_files if f.is_file() and not f.name.startswith('.')]
        
        if not req_files:
            self.log("❌ requirement 目錄中沒有找到需求文件", "ERROR")
            self.log("請在 requirement/ 目錄下放置需求文件（.md, .txt 等格式）", "INFO")
            return False
        
        self.log(f"✅ 找到 {len(req_files)} 個需求文件", "INFO")
        return True
    
    def read_requirements(self):
        """讀取所有需求文件"""
        self.log("=== 階段 1: 需求分析 ===")
        
        req_files = sorted(self.req_dir.glob("**/*"))
        req_files = [f for f in req_files if f.is_file() and not f.name.startswith('.')]
        
        for req_file in req_files:
            self.log(f"讀取需求文件: {req_file.relative_to(self.base_dir)}")
            
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                requirement = {
                    'file': req_file,
                    'content': content,
                    'id': f"REQ-{len(self.requirements):03d}",
                    'name': req_file.stem,
                }
                self.requirements.append(requirement)
                
            except Exception as e:
                self.log(f"讀取文件失敗: {e}", "ERROR")
        
        self.log(f"成功讀取 {len(self.requirements)} 個需求")
        return True
    
    def create_requirement_summary(self):
        """創建需求總覽"""
        summary_file = self.task_dir / "00_requirement_summary.md"
        
        content = "# 需求總覽\n\n"
        content += f"**產生時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        content += "## 需求來源\n"
        for req in self.requirements:
            rel_path = req['file'].relative_to(self.base_dir)
            content += f"- `{rel_path}`\n"
        
        content += "\n## 需求清單\n\n"
        for req in self.requirements:
            content += f"### {req['id']}: {req['name']}\n"
            content += f"- **來源**: {req['file'].relative_to(self.base_dir)}\n"
            content += f"- **內容預覽**:\n```\n{req['content'][:300]}...\n```\n\n"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ 需求總覽已保存: {summary_file.relative_to(self.base_dir)}")
        return True
    
    def generate_task_manifest(self):
        """產生任務清單"""
        self.log("=== 階段 2: 任務規劃 ===")
        
        manifest_file = self.plan_dir / "00_task_manifest.md"
        
        content = "# 任務執行清單\n\n"
        content += f"**產生時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        content += "## 任務總覽\n"
        content += f"- 需求數量: {len(self.requirements)}\n"
        content += f"- 任務數量: （待產生）\n\n"
        
        content += "## 執行說明\n\n"
        content += "此文件將在任務產生後更新，包含：\n"
        content += "1. 所有任務列表\n"
        content += "2. 執行順序\n"
        content += "3. 依賴關係\n\n"
        
        content += "## 需求對應\n\n"
        for req in self.requirements:
            content += f"### {req['id']}: {req['name']}\n"
            content += "- 對應任務: （待產生）\n\n"
        
        with open(manifest_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ 任務清單框架已保存: {manifest_file.relative_to(self.base_dir)}")
        return True
    
    def list_tasks(self):
        """列出所有任務文件"""
        task_files = sorted(self.task_dir.glob("*.md"))
        task_files = [f for f in task_files if re.match(r'\d+_task_.*\.md', f.name)]
        
        self.tasks = []
        for task_file in task_files:
            task_id = task_file.stem.split('_')[0]
            self.tasks.append({
                'file': task_file,
                'id': task_id,
                'name': task_file.stem
            })
        
        return self.tasks
    
    def check_task_status(self, task_file):
        """檢查任務狀態"""
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 尋找狀態標記
            if re.search(r'-\s*\[x\]\s*已完成', content, re.IGNORECASE):
                return "completed"
            elif re.search(r'-\s*\[x\]\s*進行中', content, re.IGNORECASE):
                return "in_progress"
            elif re.search(r'-\s*\[x\]\s*需要修正', content, re.IGNORECASE):
                return "needs_fix"
            else:
                return "not_started"
        except:
            return "unknown"
    
    def generate_verification_report(self):
        """產生驗證報告"""
        self.log("=== 階段 4: 完成驗證 ===")
        
        tasks = self.list_tasks()
        
        report_file = self.task_dir / "99_verification_report.md"
        
        content = "# 任務驗證報告\n\n"
        content += f"**驗證時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 統計
        total = len(tasks)
        completed = sum(1 for t in tasks if self.check_task_status(t['file']) == 'completed')
        in_progress = sum(1 for t in tasks if self.check_task_status(t['file']) == 'in_progress')
        needs_fix = sum(1 for t in tasks if self.check_task_status(t['file']) == 'needs_fix')
        
        content += "## 任務完成統計\n"
        content += f"- 總任務數: {total}\n"
        content += f"- 已完成: {completed}\n"
        content += f"- 進行中: {in_progress}\n"
        content += f"- 需要修正: {needs_fix}\n"
        if total > 0:
            content += f"- 完成率: {(completed/total*100):.1f}%\n\n"
        
        content += "## 詳細驗證結果\n\n"
        for task in tasks:
            status = self.check_task_status(task['file'])
            status_emoji = {
                'completed': '✅',
                'in_progress': '🔄',
                'needs_fix': '⚠️',
                'not_started': '⏸️',
                'unknown': '❓'
            }.get(status, '❓')
            
            content += f"### {status_emoji} {task['name']}\n"
            content += f"- 檔案: {task['file'].name}\n"
            content += f"- 狀態: {status}\n\n"
        
        content += "## 整體評估\n\n"
        if completed == total:
            content += "✅ **所有任務已完成**\n\n"
        elif completed > total * 0.8:
            content += "🎯 **大部分任務已完成，少數待處理**\n\n"
        else:
            content += "⚠️ **仍有較多任務需要完成**\n\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ 驗證報告已保存: {report_file.relative_to(self.base_dir)}")
        return True
    
    def generate_final_report(self):
        """產生最終報告"""
        self.log("=== 階段 5: 總結報告 ===")
        
        tasks = self.list_tasks()
        
        report_file = self.result_dir / "final_report.md"
        
        content = "# 需求執行最終報告\n\n"
        content += f"**報告產生時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        content += "## 📊 執行總覽\n\n"
        content += f"- 處理的需求數量: {len(self.requirements)}\n"
        content += f"- 產生的任務數量: {len(tasks)}\n\n"
        
        content += "## ✅ 需求完成狀態\n\n"
        for req in self.requirements:
            content += f"### {req['id']}: {req['name']}\n"
            content += f"- 來源: {req['file'].relative_to(self.base_dir)}\n"
            content += "- 狀態: （需人工確認）\n\n"
        
        content += "## 📁 產出物清單\n\n"
        content += "### 需求文件\n"
        for req in self.requirements:
            content += f"- {req['file'].relative_to(self.base_dir)}\n"
        
        content += "\n### 任務文件\n"
        for task in tasks:
            content += f"- {task['file'].relative_to(self.base_dir)}\n"
        
        content += "\n### 報告文件\n"
        content += "- task/00_requirement_summary.md\n"
        content += "- task/00_task_manifest.md\n"
        content += "- task/99_verification_report.md\n"
        content += "- result/final_report.md\n"
        
        content += "\n## 🎯 結論\n\n"
        content += "本專案已完成需求分析、任務規劃、執行追蹤和驗證報告的完整流程。\n"
        content += "詳細的執行狀況請參考各個任務文件和驗證報告。\n\n"
        
        content += "---\n"
        content += f"**執行者**: Requirement Executor\n"
        content += f"**報告時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ 最終報告已保存: {report_file.relative_to(self.base_dir)}")
        
        # 同時產生簡單的執行摘要
        summary_file = self.result_dir / "execution_summary.md"
        summary = f"""# 執行摘要

**時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 快速統計
- 需求文件: {len(self.requirements)}
- 任務文件: {len(tasks)}
- 完成率: （待更新）

詳細報告請查看: final_report.md
"""
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return True
    
    def generate_archive(self):
        return True

    def run(self, stages=None):
        """執行完整流程"""
        if stages is None:
            stages = ['analyze', 'plan', 'verify', 'report', 'archive']
        
        try:
            if 'analyze' in stages:
                if not self.check_requirements_exist():
                    return False
                
                self.read_requirements()
                self.create_requirement_summary()
            
            if 'plan' in stages:
                self.generate_task_manifest()
            
            if 'verify' in stages:
                self.generate_verification_report()
            
            if 'report' in stages:
                self.generate_final_report()

            if 'archive' in stages:
                self.generate_archive()
            
            self.log("=" * 50)
            self.log("✅ 所有階段執行完成！")
            self.log("=" * 50)
            return True
            
        except Exception as e:
            self.log(f"執行過程中發生錯誤: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            return False

def main():
    """主程序"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Requirement Executor - 自動化需求驅動任務執行系統')
    parser.add_argument('--dir', default='.', help='工作目錄（預設: 當前目錄）')
    parser.add_argument('--stage', choices=['analyze', 'plan', 'verify', 'report', 'archive', 'all'], 
                      default='all', help='執行階段')
    
    args = parser.parse_args()
    
    executor = RequirementExecutor(args.dir)
    
    if args.stage == 'all':
        stages = ['analyze', 'plan', 'verify', 'report', 'archive']
    else:
        stages = [args.stage]
    
    success = executor.run(stages)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
