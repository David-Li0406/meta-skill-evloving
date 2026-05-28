import csv
import json
from pathlib import Path

import maxwelllink as mxl
from maxwelllink.tools import cosine_drive, gaussian_enveloped_cosine, gaussian_pulse


def _load_config() -> dict:
    config_path = Path(__file__).resolve().with_name("config.json")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _make_drive(cfg: dict):
    kind = str(cfg["kind"])
    if kind == "gaussian_pulse":
        return gaussian_pulse(
            amplitude_au=float(cfg.get("amplitude_au", 1.0)),
            t0_au=float(cfg.get("t0_au", 0.0)),
            sigma_au=float(cfg.get("sigma_au", 10.0)),
        )
    if kind == "gaussian_enveloped_cosine":
        return gaussian_enveloped_cosine(
            amplitude_au=float(cfg.get("amplitude_au", 1.0)),
            t0_au=float(cfg.get("t0_au", 0.0)),
            sigma_au=float(cfg.get("sigma_au", 10.0)),
            omega_au=float(cfg.get("omega_au", 0.1)),
            phase_rad=float(cfg.get("phase_rad", 0.0)),
        )
    if kind == "cosine_drive":
        return cosine_drive(
            amplitude_au=float(cfg.get("amplitude_au", 1.0)),
            omega_au=float(cfg.get("omega_au", 0.1)),
            phase_rad=float(cfg.get("phase_rad", 0.0)),
        )
    raise ValueError(f"Unsupported drive.kind: {kind!r}")


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
    sim_cfg = cfg["sim"]
    tls_cfg = cfg["tls"]

    tls = mxl.Molecule(
        driver="tls",
        driver_kwargs=dict(
            omega=float(tls_cfg["omega_au"]),
            mu12=float(tls_cfg["mu12_au"]),
            orientation=int(tls_cfg["orientation"]),
            pe_initial=float(tls_cfg["pe_initial"]),
            checkpoint=bool(tls_cfg.get("checkpoint", False)),
            restart=bool(tls_cfg.get("restart", False)),
        ),
    )

    drive = _make_drive(cfg["drive"])
    sim = mxl.LaserDrivenSimulation(
        dt_au=float(sim_cfg["dt_au"]),
        molecules=[tls],
        drive=drive,
        coupling_axis=str(sim_cfg["coupling_axis"]),
        record_history=bool(sim_cfg.get("record_history", True)),
    )

    sim.run(until=float(sim_cfg["until_au"]))

    out_csv = Path(__file__).resolve().with_name(str(cfg.get("output_csv", "tls_history.csv")))
    _write_tls_history_csv(tls, out_csv=out_csv)
    print(f"Wrote TLS history: {out_csv}")


if __name__ == "__main__":
    main()

