import json
import os
import socket
from pathlib import Path

import meep as mp
import maxwelllink as mxl
from maxwelllink import sockets as mxs


def _load_config() -> dict:
    config_path = Path(__file__).resolve().with_name("config.json")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _pick_free_port(bind_addr: str = "0.0.0.0") -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((bind_addr, 0))
        return int(s.getsockname()[1])


def _write_host_port(path: Path, host: str, port: int) -> None:
    if mxs.am_master():
        path.write_text(f"{host}\n{port}\n", encoding="utf-8")


def main() -> None:
    cfg = _load_config()
    hub_cfg = cfg["hub"]
    mol_cfg = cfg["molecule"]

    port = _pick_free_port("0.0.0.0")
    host_for_clients = os.environ.get("MXL_HOST", socket.gethostname())
    host_port_file = Path(__file__).resolve().with_name(str(cfg["host_port_file"]))
    _write_host_port(host_port_file, host_for_clients, port)

    hub = mxl.SocketHub(
        host="",
        port=port,
        timeout=float(hub_cfg["timeout"]),
        latency=float(hub_cfg["latency"]),
    )
    print(f"Hub listening on {host_for_clients}:{port}")

    molecule = mxl.Molecule(
        hub=hub,
        center=mp.Vector3(*mol_cfg["center"]),
        size=mp.Vector3(*mol_cfg["size"]),
        sigma=float(mol_cfg["sigma"]),
        dimensions=int(mol_cfg["dimensions"]),
        rescaling_factor=float(mol_cfg.get("rescaling_factor", 1.0)),
    )

    sim = mxl.MeepSimulation(
        hub=hub,
        molecules=[molecule],
        time_units_fs=float(cfg["time_units_fs"]),
        cell_size=mp.Vector3(*cfg["cell_size"]),
        boundary_layers=[mp.PML(float(cfg["pml_thickness"]))],
        resolution=int(cfg["resolution"]),
    )
    sim.run(until=float(cfg["until"]))


if __name__ == "__main__":
    main()

