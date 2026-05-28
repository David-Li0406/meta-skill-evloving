import json
import subprocess
import time
from pathlib import Path


def _load_config() -> dict:
    config_path = Path(__file__).resolve().with_name("config.json")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _read_host_port(host_port_file: Path) -> tuple[str, int]:
    lines = host_port_file.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2:
        raise ValueError(f"Invalid host/port file: {host_port_file}")
    return lines[0].strip(), int(lines[1].strip())


def main() -> None:
    cfg = _load_config()
    tls_cfg = cfg["tls"]

    host_port_file = Path(__file__).resolve().with_name(str(cfg["host_port_file"]))
    for _ in range(60):
        if host_port_file.exists():
            break
        time.sleep(1.0)
    if not host_port_file.exists():
        raise FileNotFoundError(f"Host/port file not found: {host_port_file}")

    host, port = _read_host_port(host_port_file)

    omega = float(tls_cfg["omega_au"])
    mu12 = float(tls_cfg["mu12_au"])
    orientation = int(tls_cfg["orientation"])
    pe_initial = float(tls_cfg["pe_initial"])

    param = f"omega={omega}, mu12={mu12}, orientation={orientation}, pe_initial={pe_initial}"
    if bool(tls_cfg.get("checkpoint", False)):
        param += ", checkpoint=true"
    if bool(tls_cfg.get("restart", False)):
        param += ", restart=true"

    cmd = [
        "mxl_driver",
        "--model",
        "tls",
        "--address",
        host,
        "--port",
        str(port),
        "--param",
        param,
    ]
    subprocess.check_call(cmd)


if __name__ == "__main__":
    main()

