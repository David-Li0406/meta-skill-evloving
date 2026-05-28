"""
High-performance batch orchestrator for processing front-camera audio files.
Implements the Grand Schemer pattern with single-agent task orchestration.
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
import logging
import time
from datetime import datetime
import yaml
import subprocess
import concurrent.futures
from queue import Queue
import threading

from .hardware_optimizer import HardwareOptimizer, auto_configure
from .gpu_pipeline import ParallelGPUPipeline, TranscriptionJob

logger = logging.getLogger(__name__)


@dataclass
class BatchManifest:
    """Manifest for batch processing operations"""
    manifest_id: str
    timestamp: str
    objective: str
    base_root: str
    cwd: str
    
    # File discovery
    scan_results: Dict[str, Any] = field(default_factory=dict)
    front_files: List[str] = field(default_factory=list)
    rear_files_skipped: List[str] = field(default_factory=list)
    
    # Processing configuration
    hardware_config: Dict[str, Any] = field(default_factory=dict)
    processing_config: Dict[str, Any] = field(default_factory=dict)
    
    # Execution tracking
    jobs_total: int = 0
    jobs_completed: int = 0
    jobs_failed: int = 0
    
    # Results
    transcripts: List[Dict[str, Any]] = field(default_factory=list)
    verification_results: List[Dict[str, Any]] = field(default_factory=list)
    
    # Timing
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    total_duration_seconds: Optional[float] = None


class BatchOrchestrator:
    """
    Grand Schemer implementation for batch audio transcription.
    Single-agent that plans, executes, and verifies in one pass.
    """
    
    def __init__(self, base_root: str = r"G:\My Drive\App development", cwd: Optional[Path] = None):
        self.base_root = Path(base_root)
        self.cwd = Path(cwd) if cwd else Path.cwd()
        
        # Ensure we're within base_root
        try:
            self.cwd.relative_to(self.base_root)
        except ValueError:
            logger.warning(f"CWD {self.cwd} is outside BASE_ROOT {self.base_root}, using CWD as base")
            self.base_root = self.cwd
        
        # Initialize components
        self.hardware_optimizer = None
        self.gpu_pipeline = None
        self.manifest = None
        self.ops_log = []
        
        # Create output directories
        self.reports_dir = self.cwd / "reports"
        self.outputs_dir = self.cwd / "outputs"
        self.reports_dir.mkdir(exist_ok=True, parents=True)
        self.outputs_dir.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"BatchOrchestrator initialized: CWD={self.cwd}, BASE_ROOT={self.base_root}")
    
    def execute(self, input_pattern: str = "F*/*.mp4", options: Dict = None) -> Dict:
        """
        Main execution entry point - single pass plan→act→verify.
        """
        
        print("\n" + "="*50)
        print("GRAND SCHEMER - BATCH ORCHESTRATOR")
        print("="*50)
        
        # 1. USER_BRIEF
        brief = self._generate_user_brief(input_pattern, options)
        print("\n## USER BRIEF\n")
        print(brief)
        
        # 2. STRATEGY_PROPOSAL
        strategy = self._generate_strategy_proposal(input_pattern, options)
        print("\n## STRATEGY PROPOSAL\n")
        print(json.dumps(strategy, indent=2))
        
        # 3. TASK_PLAN
        task_plan = self._generate_task_plan(input_pattern, options)
        print("\n## TASK PLAN\n")
        print(json.dumps(task_plan, indent=2))
        
        # 4. Execute the plan
        print("\n## EXECUTION\n")
        execution_result = self._execute_plan(task_plan, options)
        
        # 5. VERIFIER_SPEC and verification
        verifier_spec = self._generate_verifier_spec()
        print("\n## VERIFIER SPEC\n")
        print(json.dumps(verifier_spec, indent=2))
        
        verification_results = self._verify_results(verifier_spec)
        
        # 6. COMPLETION_REPORT
        completion_report = self._generate_completion_report(execution_result, verification_results)
        print("\n## COMPLETION REPORT\n")
        print(json.dumps(completion_report, indent=2))
        
        # Save all reports
        self._save_reports(completion_report)
        
        return completion_report
    
    def _generate_user_brief(self, input_pattern: str, options: Dict) -> str:
        """Generate user-friendly brief of what will be done"""
        
        brief = f"""
• Scanning for front-camera video files matching pattern: {input_pattern}
• Detecting and optimizing for available hardware (GPUs, CPUs, memory)
• Extracting and transcribing audio with maximum throughput
• Adding speaker diarization and confidence scores
• Generating transcripts in multiple formats (JSON, SRT, VTT, CSV)
• Creating verification reports and hashes for reproducibility
        """
        
        return brief.strip()
    
    def _generate_strategy_proposal(self, input_pattern: str, options: Dict) -> Dict:
        """Generate strategy proposal JSON"""
        
        return {
            "envelope_type": "strategy_proposal",
            "timestamp": datetime.now().isoformat(),
            "manager_id": "batch_orchestrator",
            "content": {
                "objective": f"Batch transcribe front-camera audio files matching {input_pattern} with GPU acceleration",
                "plan": [
                    {
                        "step": 1,
                        "action": "Hardware detection and optimization profile generation",
                        "verification": "reports/hardware_optimization.json exists with GPU/CPU specs"
                    },
                    {
                        "step": 2,
                        "action": f"Scan for files matching {input_pattern} and filter front-camera only",
                        "verification": "reports/scan_summary.json contains front_files list"
                    },
                    {
                        "step": 3,
                        "action": "Initialize GPU pipeline with optimized settings",
                        "verification": "Pipeline initialized with detected GPU count"
                    },
                    {
                        "step": 4,
                        "action": "Process files in parallel batches across GPUs",
                        "verification": "All transcripts generated in outputs/*/transcript.json"
                    },
                    {
                        "step": 5,
                        "action": "Generate hashes and verification reports",
                        "verification": "reports/hashes/*.sha256 files exist"
                    }
                ],
                "required_evidence": [
                    "reports/hardware_optimization.json",
                    "reports/scan_summary.json",
                    "reports/batch_manifest.json",
                    "outputs/*/transcript.json",
                    "reports/completion_report.json"
                ]
            }
        }
    
    def _generate_task_plan(self, input_pattern: str, options: Dict) -> Dict:
        """Generate concrete task plan"""
        
        task_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "id": task_id,
            "objective": "Execute batch transcription with GPU acceleration",
            "instructions": [
                {
                    "op": "run_hardware_detection",
                    "params": {
                        "output_path": "reports/hardware_optimization.json"
                    }
                },
                {
                    "op": "scan_files",
                    "params": {
                        "pattern": input_pattern,
                        "filter": "front_only",
                        "output_path": "reports/scan_summary.json"
                    }
                },
                {
                    "op": "initialize_pipeline",
                    "params": {
                        "use_hardware_config": True
                    }
                },
                {
                    "op": "process_batch",
                    "params": {
                        "parallel_mode": "gpu_balanced",
                        "export_formats": ["json", "srt", "vtt", "csv"]
                    }
                },
                {
                    "op": "generate_hashes",
                    "params": {
                        "target_files": "outputs/*/transcript.json"
                    }
                },
                {
                    "op": "save_manifest",
                    "params": {
                        "output_path": "reports/batch_manifest.json"
                    }
                }
            ]
        }
    
    def _execute_plan(self, task_plan: Dict, options: Dict) -> Dict:
        """Execute the task plan"""
        
        self.manifest = BatchManifest(
            manifest_id=task_plan['id'],
            timestamp=datetime.now().isoformat(),
            objective=task_plan['objective'],
            base_root=str(self.base_root),
            cwd=str(self.cwd),
            start_time=time.time()
        )
        
        results = {}
        
        for instruction in task_plan['instructions']:
            op = instruction['op']
            params = instruction['params']
            
            logger.info(f"Executing operation: {op}")
            
            try:
                if op == "run_hardware_detection":
                    result = self._op_hardware_detection(params)
                elif op == "scan_files":
                    result = self._op_scan_files(params)
                elif op == "initialize_pipeline":
                    result = self._op_initialize_pipeline(params)
                elif op == "process_batch":
                    result = self._op_process_batch(params)
                elif op == "generate_hashes":
                    result = self._op_generate_hashes(params)
                elif op == "save_manifest":
                    result = self._op_save_manifest(params)
                else:
                    result = {"error": f"Unknown operation: {op}"}
                
                results[op] = result
                self._log_operation(op, params, result)
                
            except Exception as e:
                logger.error(f"Operation {op} failed: {e}")
                results[op] = {"error": str(e)}
                self._log_operation(op, params, {"error": str(e)})
        
        self.manifest.end_time = time.time()
        self.manifest.total_duration_seconds = self.manifest.end_time - self.manifest.start_time
        
        return results
    
    def _op_hardware_detection(self, params: Dict) -> Dict:
        """Operation: Detect and optimize hardware"""
        
        output_path = self.cwd / params['output_path']
        
        # Run hardware detection
        self.hardware_optimizer = HardwareOptimizer()
        report = self.hardware_optimizer.save_hardware_report(output_path)
        
        # Run benchmarks
        benchmarks = self.hardware_optimizer.benchmark_hardware()
        report['benchmarks'] = benchmarks
        
        # Save updated report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.manifest.hardware_config = report
        
        return {
            "success": True,
            "hardware_tier": report['hardware_tier'],
            "gpu_count": self.hardware_optimizer.specs.gpu_count,
            "output_path": str(output_path)
        }
    
    def _op_scan_files(self, params: Dict) -> Dict:
        """Operation: Scan for input files"""
        
        pattern = params['pattern']
        filter_mode = params.get('filter', 'front_only')
        output_path = self.cwd / params['output_path']
        
        # Find all matching files
        all_files = list(self.cwd.rglob(pattern))
        
        front_files = []
        rear_files = []
        
        for file_path in all_files:
            # Check if it's a front or rear camera file
            parts = file_path.parts
            for part in parts:
                if part.startswith('F'):
                    front_files.append(str(file_path.relative_to(self.cwd)))
                    break
                elif part.startswith('R'):
                    rear_files.append(str(file_path.relative_to(self.cwd)))
                    break
        
        scan_summary = {
            "timestamp": datetime.now().isoformat(),
            "pattern": pattern,
            "total_files_found": len(all_files),
            "front_files": front_files,
            "front_files_count": len(front_files),
            "rear_files_skipped": rear_files,
            "rear_files_count": len(rear_files),
            "skipped_rear_no_audio": rear_files
        }
        
        # Save scan summary
        with open(output_path, 'w') as f:
            json.dump(scan_summary, f, indent=2)
        
        self.manifest.scan_results = scan_summary
        self.manifest.front_files = front_files
        self.manifest.rear_files_skipped = rear_files
        
        return {
            "success": True,
            "front_files_count": len(front_files),
            "rear_files_skipped_count": len(rear_files),
            "output_path": str(output_path)
        }
    
    def _op_initialize_pipeline(self, params: Dict) -> Dict:
        """Operation: Initialize GPU pipeline"""
        
        if not self.hardware_optimizer:
            self.hardware_optimizer = HardwareOptimizer()
        
        # Create pipeline with hardware optimization
        self.gpu_pipeline = ParallelGPUPipeline()
        self.gpu_pipeline.initialize()
        
        # Get initial stats
        stats = self.gpu_pipeline.get_statistics()
        
        self.manifest.processing_config = {
            "pipeline_type": "ParallelGPU",
            "gpu_count": stats['pipeline']['gpu_count'],
            "active_workers": stats['pipeline']['active_workers']
        }
        
        return {
            "success": True,
            "gpu_count": stats['pipeline']['gpu_count'],
            "workers_initialized": stats['pipeline']['active_workers']
        }
    
    def _op_process_batch(self, params: Dict) -> Dict:
        """Operation: Process batch of files"""
        
        if not self.gpu_pipeline:
            raise RuntimeError("Pipeline not initialized")
        
        export_formats = params.get('export_formats', ['json', 'srt', 'vtt', 'csv'])
        
        # Prepare input files
        input_files = []
        for file_str in self.manifest.front_files:
            file_path = self.cwd / file_str
            if file_path.exists():
                input_files.append(file_path)
        
        self.manifest.jobs_total = len(input_files)
        
        # Process options
        process_options = {
            'diarization': True,
            'export_formats': export_formats,
            'language': 'en',
            'task': 'transcribe',
            'beam_size': 5,
            'best_of': 5,
            'vad_filter': True
        }
        
        # Process batch
        logger.info(f"Processing {len(input_files)} files across {self.gpu_pipeline.gpu_count} GPU(s)")
        
        jobs = self.gpu_pipeline.process_batch(
            input_files=input_files,
            output_dir=self.outputs_dir,
            options=process_options
        )
        
        # Collect results
        for job in jobs:
            if job.status == 'completed':
                self.manifest.jobs_completed += 1
                transcript_info = {
                    "job_id": job.job_id,
                    "input_file": str(job.input_path),
                    "output_path": str(job.output_path),
                    "gpu_id": job.gpu_id,
                    "duration": job.end_time - job.start_time if job.end_time and job.start_time else 0,
                    "status": job.status
                }
                
                # Add result details if available
                if job.result:
                    transcript_info["segment_count"] = len(job.result.get('segments', []))
                    transcript_info["language"] = job.result.get('language', 'unknown')
                    transcript_info["duration_seconds"] = job.result.get('duration', 0)
                
                self.manifest.transcripts.append(transcript_info)
                
            elif job.status == 'failed':
                self.manifest.jobs_failed += 1
                logger.error(f"Job {job.job_id} failed: {job.error}")
        
        # Get final stats
        final_stats = self.gpu_pipeline.get_statistics()
        
        return {
            "success": True,
            "jobs_total": self.manifest.jobs_total,
            "jobs_completed": self.manifest.jobs_completed,
            "jobs_failed": self.manifest.jobs_failed,
            "gpu_stats": final_stats['aggregate']
        }
    
    def _op_generate_hashes(self, params: Dict) -> Dict:
        """Operation: Generate SHA256 hashes for transcripts"""
        
        hashes_dir = self.reports_dir / "hashes"
        hashes_dir.mkdir(exist_ok=True)
        
        pattern = params['target_files']
        transcript_files = list(self.cwd.glob(pattern))
        
        hashes_generated = []
        
        for transcript_file in transcript_files:
            if transcript_file.exists():
                # Calculate hash
                with open(transcript_file, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                
                # Save hash file
                hash_filename = transcript_file.stem + '.sha256'
                hash_path = hashes_dir / hash_filename
                
                with open(hash_path, 'w') as f:
                    f.write(f"{file_hash}  {transcript_file.relative_to(self.cwd)}\n")
                
                hashes_generated.append({
                    "file": str(transcript_file.relative_to(self.cwd)),
                    "sha256": file_hash,
                    "hash_file": str(hash_path.relative_to(self.cwd))
                })
        
        return {
            "success": True,
            "hashes_generated": len(hashes_generated),
            "hash_files": hashes_generated
        }
    
    def _op_save_manifest(self, params: Dict) -> Dict:
        """Operation: Save batch manifest"""
        
        output_path = self.cwd / params['output_path']
        
        # Convert manifest to dict
        manifest_dict = asdict(self.manifest)
        
        # Save manifest
        with open(output_path, 'w') as f:
            json.dump(manifest_dict, f, indent=2)
        
        return {
            "success": True,
            "output_path": str(output_path),
            "manifest_id": self.manifest.manifest_id
        }
    
    def _generate_verifier_spec(self) -> Dict:
        """Generate verification specification"""
        
        return {
            "checks": [
                {
                    "type": "file_exists",
                    "path": "reports/hardware_optimization.json"
                },
                {
                    "type": "file_exists",
                    "path": "reports/scan_summary.json"
                },
                {
                    "type": "file_exists",
                    "path": "reports/batch_manifest.json"
                },
                {
                    "type": "jsonpath_exists",
                    "path": "reports/hardware_optimization.json",
                    "jsonpath": "$.hardware_specs.gpu_count"
                },
                {
                    "type": "jsonpath_exists",
                    "path": "reports/scan_summary.json",
                    "jsonpath": "$.front_files"
                },
                {
                    "type": "glob_count_at_least",
                    "pattern": "outputs/*/transcript.json",
                    "min": 1
                }
            ],
            "verifier_guidance": "Fail only when required artifacts are missing; warn for optional items."
        }
    
    def _verify_results(self, verifier_spec: Dict) -> List[Dict]:
        """Execute verification checks"""
        
        results = []
        
        for check in verifier_spec['checks']:
            check_type = check['type']
            
            try:
                if check_type == "file_exists":
                    path = self.cwd / check['path']
                    exists = path.exists()
                    results.append({
                        "check": check_type,
                        "target": check['path'],
                        "pass": exists
                    })
                    
                elif check_type == "jsonpath_exists":
                    path = self.cwd / check['path']
                    if path.exists():
                        with open(path) as f:
                            data = json.load(f)
                        
                        # Simple jsonpath check (using dot notation)
                        jsonpath_parts = check['jsonpath'].strip('$.').split('.')
                        current = data
                        exists = True
                        
                        for part in jsonpath_parts:
                            if isinstance(current, dict) and part in current:
                                current = current[part]
                            else:
                                exists = False
                                break
                        
                        results.append({
                            "check": check_type,
                            "target": f"{check['path']}:{check['jsonpath']}",
                            "pass": exists
                        })
                    else:
                        results.append({
                            "check": check_type,
                            "target": f"{check['path']}:{check['jsonpath']}",
                            "pass": False
                        })
                
                elif check_type == "glob_count_at_least":
                    pattern = check['pattern']
                    files = list(self.cwd.glob(pattern))
                    count = len(files)
                    min_required = check['min']
                    
                    results.append({
                        "check": check_type,
                        "target": pattern,
                        "pass": count >= min_required,
                        "found": count,
                        "required": min_required
                    })
                    
            except Exception as e:
                results.append({
                    "check": check_type,
                    "target": check.get('path', check.get('pattern', 'unknown')),
                    "pass": False,
                    "error": str(e)
                })
        
        self.manifest.verification_results = results
        
        return results
    
    def _generate_completion_report(self, execution_result: Dict, verification_results: List[Dict]) -> Dict:
        """Generate completion report"""
        
        # Check if all verifications passed
        all_passed = all(v.get('pass', False) for v in verification_results)
        
        # Collect evidence
        evidence_files = []
        for pattern in ["reports/*.json", "outputs/*/transcript.json", "reports/hashes/*.sha256"]:
            for file_path in self.cwd.glob(pattern):
                evidence_files.append(str(file_path.relative_to(self.cwd)))
        
        return {
            "envelope_type": "completion_report",
            "timestamp": datetime.now().isoformat(),
            "manager_id": "batch_orchestrator",
            "content": {
                "objective_achieved": all_passed and self.manifest.jobs_failed == 0,
                "tasks_completed": len([r for r in execution_result.values() if r.get('success')]),
                "tasks_failed": len([r for r in execution_result.values() if not r.get('success')]),
                "verification_results": verification_results,
                "evidence_collected": evidence_files[:20],  # Limit to first 20
                "performance_metrics": {
                    "total_duration_seconds": self.manifest.total_duration_seconds,
                    "jobs_total": self.manifest.jobs_total,
                    "jobs_completed": self.manifest.jobs_completed,
                    "jobs_failed": self.manifest.jobs_failed,
                    "throughput_files_per_minute": (self.manifest.jobs_completed / (self.manifest.total_duration_seconds / 60)) if self.manifest.total_duration_seconds else 0
                },
                "notes": f"Processed {self.manifest.jobs_completed}/{self.manifest.jobs_total} files using {self.gpu_pipeline.gpu_count if self.gpu_pipeline else 0} GPU(s)"
            }
        }
    
    def _save_reports(self, completion_report: Dict):
        """Save all reports to disk"""
        
        # Save completion report
        report_path = self.reports_dir / "completion_report.json"
        with open(report_path, 'w') as f:
            json.dump(completion_report, f, indent=2)
        
        # Save ops log
        ops_log_path = self.cwd / "ops_log.ndjson"
        with open(ops_log_path, 'a') as f:
            for op in self.ops_log:
                f.write(json.dumps(op) + '\n')
        
        logger.info(f"Reports saved to {self.reports_dir}")
    
    def _log_operation(self, op: str, params: Dict, result: Dict):
        """Log operation to ops log"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "op": op,
            "params": params,
            "result": result
        }
        
        self.ops_log.append(log_entry)


def main():
    """Main entry point for batch orchestration"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*50)
    print("GRAND SCHEMER - READY")
    print("="*50)
    print("\nI am your single-agent task orchestrator:")
    print("  - Plan → Act → Verify in one pass")
    print("  - All artifacts written to CWD")
    print("  - No Redis, no polling, no background services")
    print("\nDescribe what you want accomplished!")
    print("="*50 + "\n")
    
    # Create orchestrator
    orchestrator = BatchOrchestrator()
    
    # Execute batch processing
    try:
        result = orchestrator.execute(
            input_pattern="F*/*.mp4",
            options={
                "use_gpu": True,
                "optimize_performance": True
            }
        )
        
        if result['content']['objective_achieved']:
            print("\n✅ OBJECTIVE ACHIEVED")
        else:
            print("\n⚠️ OBJECTIVE PARTIALLY COMPLETED")
        
    except Exception as e:
        logger.error(f"Batch orchestration failed: {e}")
        print(f"\n❌ FAILED: {e}")
    
    finally:
        # Cleanup
        if orchestrator.gpu_pipeline:
            orchestrator.gpu_pipeline.shutdown()


if __name__ == "__main__":
    main()