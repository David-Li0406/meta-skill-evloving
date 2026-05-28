import csv
import json
from pathlib import Path

import maxwelllink as mxl


def _load_config() -> dict:
    config_path = Path(__file__).resolve().with_name("config.json")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_tls_history_csv(molecule: mxl.Molecule, out_csv: Path):
    rows = molecule.additional_data_history
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "idx",
                "time_au",
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
            w.writerow(
                [
                    idx,
                    float(frame.get("time_au", 0.0)),
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
    hub_cfg = cfg["hub"]
    sim_cfg = cfg["sim"]

    hub = mxl.SocketHub(
        host=str(hub_cfg["host"]),
        port=int(hub_cfg["port"]),
        timeout=float(hub_cfg["timeout"]),
        latency=float(hub_cfg["latency"]),
    )

    molecule = mxl.Molecule(hub=hub)

    sim = mxl.SingleModeSimulation(
        dt_au=float(sim_cfg["dt_au"]),
        frequency_au=float(sim_cfg["frequency_au"]),
        damping_au=float(sim_cfg["damping_au"]),
        molecules=[molecule],
        coupling_strength=float(sim_cfg["coupling_strength"]),
        coupling_axis=str(sim_cfg["coupling_axis"]),
        qc_initial=list(sim_cfg["qc_initial"]),
        hub=hub,
        record_history=bool(sim_cfg.get("record_history", True)),
    )

    sim.run(steps=int(sim_cfg["steps"]))

    out_csv = Path(__file__).resolve().with_name(str(cfg.get("output_csv", "tls_history.csv")))
    _write_tls_history_csv(molecule, out_csv=out_csv)
    print(f"Wrote TLS history: {out_csv}")


if __name__ == "__main__":
    main()

