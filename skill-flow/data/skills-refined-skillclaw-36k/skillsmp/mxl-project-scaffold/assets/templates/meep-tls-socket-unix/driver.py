import json
import subprocess
from pathlib import Path


def _load_config() -> dict:
    config_path = Path(__file__).resolve().with_name("config.json")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    cfg = _load_config()
    tls_cfg = cfg["tls"]

    unixsocket = str(cfg["unixsocket"])
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
        "--unix",
        "--address",
        unixsocket,
        "--param",
        param,
    ]
    subprocess.check_call(cmd)


if __name__ == "__main__":
    main()

