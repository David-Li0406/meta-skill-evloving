# 04 - DeepStream PeopleNet Config

Assumptions:
- You have a PeopleNet TensorRT engine (FP16) at:
  - `/home/yousuf/PROJECTS/PeopleNet/models/peoplenet_fp16.engine` (adjust if different)

Create/update a DeepStream config file:
```bash
CONF="/home/yousuf/PROJECTS/PeopleNet/configs/peoplenet_ds_config.txt"
mkdir -p "$(dirname "$CONF")"
```

Key fields to verify/edit in the config (pseudo‑snippet):
```
[primary-gie]
enable=1
model-engine-file=/home/yousuf/PROJECTS/PeopleNet/models/peoplenet_fp16.engine
network-type=1
batch-size=1
gie-unique-id=1
process-mode=1
interval=0

[sink0]
enable=0

[sink1]
enable=1
type=2
sync=0
```

If your pipeline writes detection metadata to files/JSON, ensure the sink and msgconv are configured accordingly; otherwise we will parse detections via the runner in the next step.

Checkpoint (return):
- Print the lines containing `model-engine-file=`, `gie-unique-id=`, and the `[sink*]` enables from your config.
  - e.g., `grep -E 'model-engine-file|gie-unique-id|^\[sink|^enable=' -n "$CONF" | sed -n '1,40p'`


