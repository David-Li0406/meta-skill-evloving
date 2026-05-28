# Data Reproducibility

## Patterns

### **Environment Management**
  #### **Name**
Reproducible Computational Environments
  #### **Description**
Ensure exact environment reproduction
  #### **When**
Setting up any computational experiment
  #### **Pattern**
    # Docker for complete environment isolation
    FROM python:3.11.4-slim@sha256:abc123...  # Pin digest
    
    # Pin all dependencies with hashes
    COPY requirements.lock .
    RUN pip install --no-cache-dir -r requirements.lock
    
    # Set deterministic environment variables
    ENV PYTHONHASHSEED=0
    ENV CUBLAS_WORKSPACE_CONFIG=:4096:8
    
    # requirements.lock format:
    # numpy==1.24.3 --hash=sha256:abc...
    # pandas==2.0.1 --hash=sha256:def...
    
    # Conda alternative:
    # conda env export --from-history > environment.yml
    # conda-lock lock -f environment.yml
    
### **Seed Management**
  #### **Name**
Random Seed Management
  #### **Description**
Control all sources of randomness
  #### **Pattern**
    import random
    import numpy as np
    import torch
    import os
    
    def set_all_seeds(seed: int) -> dict:
        """Set ALL random seeds for reproducibility."""
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        os.environ['PYTHONHASHSEED'] = str(seed)
    
        return {"seed": seed, "timestamp": datetime.utcnow().isoformat()}
    
### **Data Versioning**
  #### **Name**
Data Version Control
  #### **Description**
Track data changes alongside code
  #### **Pattern**
    # DVC (Data Version Control) setup
    # dvc init
    # dvc remote add -d storage s3://bucket/data
    
    # Track large files
    # dvc add data/training.csv
    # git add data/training.csv.dvc .gitignore
    # git commit -m "Add training data"
    # dvc push
    
    # .dvc file contains hash:
    # md5: abc123...
    # outs:
    # - md5: def456...
    #   path: data/training.csv
    
    # To reproduce:
    # git checkout <commit>
    # dvc checkout
    
### **Experiment Manifest**
  #### **Name**
Experiment Manifest Creation
  #### **Description**
Document everything needed to reproduce
  #### **Pattern**
    import hashlib
    import subprocess
    import json
    
    def create_manifest(experiment_dir: str) -> dict:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "git_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"]
            ).decode().strip(),
            "git_dirty": bool(subprocess.check_output(
                ["git", "status", "--porcelain"]
            )),
            "python_version": sys.version,
            "platform": platform.platform(),
            "seeds": {"numpy": 42, "torch": 42, "random": 42},
            "data_hash": hash_directory(f"{experiment_dir}/data"),
            "config": yaml.safe_load(open(f"{experiment_dir}/config.yaml")),
        }
    
    # Save with results
    results["_provenance"] = manifest
    json.dump(results, open("results.json", "w"))
    

## Anti-Patterns

### **Hardcoded Paths**
  #### **Name**
Hardcoded File Paths
  #### **Problem**
pd.read_csv('C:/Users/me/data.csv')
  #### **Solution**
    DATA_DIR = Path(os.environ.get('DATA_DIR', './data'))
    df = pd.read_csv(DATA_DIR / 'data.csv')
    
### **Missing Seeds**
  #### **Name**
Undocumented Random Seeds
  #### **Problem**
Results change each run
  #### **Solution**
Set and log all seeds before any random operations