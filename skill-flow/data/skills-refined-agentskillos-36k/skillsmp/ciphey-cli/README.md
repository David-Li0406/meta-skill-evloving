# `ciphey-cli`（Codex Skill，uv 优先）

这是一个 Codex CLI Skill：提供 `scripts/ciphey.sh` 包装脚本来调用 Ciphey，对未知密文（文本或文件）进行自动解码/解密尝试。

- 技能入口与说明：`SKILL.md`
- 执行脚本：`scripts/ciphey.sh`

## 快速开始

```bash
bash "<path-to-skill>/scripts/ciphey.sh" --text "<ciphertext>"
bash "<path-to-skill>/scripts/ciphey.sh" --file "<path/to/cipher.txt>"
```

## Runner（uv-first）

默认模式是 `auto`：优先使用 `uv` 在本地创建并复用 `scripts/.venv` 运行；若 Ciphey（尤其是 `cipheycore`）在当前平台无法安装或导入，则自动回退到 Docker runner。

可显式指定 runner：

```bash
# 方式 1：环境变量
CIPHEY_RUNNER_MODE=uv     bash "<path-to-skill>/scripts/ciphey.sh" --text "<ciphertext>"
CIPHEY_RUNNER_MODE=docker bash "<path-to-skill>/scripts/ciphey.sh" --text "<ciphertext>"

# 方式 2：脚本参数
bash "<path-to-skill>/scripts/ciphey.sh" --runner uv     --text "<ciphertext>"
bash "<path-to-skill>/scripts/ciphey.sh" --runner docker --text "<ciphertext>"
```

## 环境变量

- `CIPHEY_RUNNER_MODE=uv|docker|auto`（默认：`auto`）
- `CIPHEY_VERSION=<version>`（默认：`5.14.0`，仅影响 uv runner 安装的版本）
- `CIPHEY_DOCKER_IMAGE=<image>`（默认：`remnux/ciphey`）

## 注意

- uv runner 需要 `uv`；若未安装，脚本会尝试通过官方安装脚本安装（需要 `curl`）。
- Docker runner 需要本机已安装 `docker`。
- 仅对你有授权分析的内容使用该工具。
