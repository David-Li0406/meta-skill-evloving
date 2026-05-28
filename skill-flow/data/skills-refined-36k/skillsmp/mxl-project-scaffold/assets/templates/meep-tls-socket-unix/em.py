import csv
import json
from pathlib import Path

import meep as mp
import maxwelllink as mxl

AU_TIME_TO_FS = 0.02418884254  # 1 a.u. time in femtoseconds


def _load_config() -> dict:
    config_path = Path(__file__).resolve().with_name("config.json")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_tls_history_csv(molecule: mxl.Molecule, time_units_fs: float, out_csv: Path):
    rows = molecule.additional_data_history
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "idx",
                "time_au",
                "time_fs",
                "time_meep_units",
                "Pe",
                "Pg",
                "Pge_real",
                "Pge_imag",
                "energy_au",
                "mux_au",
                "muy_au",
                "muz_au",
            ]
        )
        for idx, frame in enumerate(rows):
            time_au = float(frame.get("time_au", 0.0))
            time_fs = time_au * AU_TIME_TO_FS
            time_meep = time_fs / float(time_units_fs)
            w.writerow(
                [
                    idx,
                    time_au,
                    time_fs,
                    time_meep,
                    float(frame.get("Pe", 0.0)),
                    float(frame.get("Pg", 0.0)),
                    float(frame.get("Pge_real", 0.0)),
                    float(frame.get("Pge_imag", 0.0)),
                    float(frame.get("energy_au", 0.0)),
                    float(frame.get("mux_au", 0.0)),
                    float(frame.get("muy_au", 0.0)),
                    float(frame.get("muz_au", 0.0)),
                ]
            )


def main() -> None:
    cfg = _load_config()
    time_units_fs = float(cfg["time_units_fs"])
    mol_cfg = cfg["molecule"]

    hub = mxl.SocketHub(
        unixsocket=str(cfg["unixsocket"]),
        timeout=float(cfg["hub"]["timeout"]),
        latency=float(cfg["hub"]["latency"]),
    )

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
        time_units_fs=time_units_fs,
        cell_size=mp.Vector3(*cfg["cell_size"]),
        boundary_layers=[mp.PML(float(cfg["pml_thickness"]))],
        resolution=int(cfg["resolution"]),
    )
    sim.run(until=float(cfg["until"]))

    if mp.am_master():
        out_csv = Path(__file__).resolve().with_name(str(cfg.get("output_csv", "tls_history.csv")))
        _write_tls_history_csv(molecule, time_units_fs=time_units_fs, out_csv=out_csv)
        print(f"Wrote TLS history: {out_csv}")


if __name__ == "__main__":
    main()

