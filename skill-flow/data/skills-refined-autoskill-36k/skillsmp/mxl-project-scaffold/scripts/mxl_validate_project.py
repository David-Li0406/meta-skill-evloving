#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ValidationError:
    message: str


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "projects").is_dir() and (candidate / "skills").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate repo root (missing projects/ and skills/)")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(cond: bool, msg: str, errors: list[ValidationError]) -> None:
    if not cond:
        errors.append(ValidationError(msg))


def _require_number(x: Any, msg: str, errors: list[ValidationError]) -> None:
    _require(isinstance(x, (int, float)) and not isinstance(x, bool), msg, errors)


def _require_int(x: Any, msg: str, errors: list[ValidationError]) -> None:
    _require(isinstance(x, int) and not isinstance(x, bool), msg, errors)


def _require_str(x: Any, msg: str, errors: list[ValidationError]) -> None:
    _require(isinstance(x, str) and x.strip() != "", msg, errors)


def _validate_common(cfg: Any, errors: list[ValidationError]) -> None:
    _require(isinstance(cfg, dict), "config.json must contain a JSON object", errors)
    if not isinstance(cfg, dict):
        return
    _require_str(cfg.get("template_id"), "Missing or empty 'template_id'", errors)


def _validate_tls_block(tls: Any, errors: list[ValidationError]) -> None:
    _require(isinstance(tls, dict), "'tls' must be an object", errors)
    if not isinstance(tls, dict):
        return
    _require_number(tls.get("omega_au"), "tls.omega_au must be a number", errors)
    _require_number(tls.get("mu12_au"), "tls.mu12_au must be a number", errors)
    _require_int(tls.get("orientation"), "tls.orientation must be an int (0|1|2)", errors)
    _require_number(tls.get("pe_initial"), "tls.pe_initial must be a number (0..1)", errors)


def _validate_meep_cfg(cfg: dict, errors: list[ValidationError]) -> None:
    _require_number(cfg.get("time_units_fs"), "time_units_fs must be a number", errors)
    cell = cfg.get("cell_size")
    _require(
        isinstance(cell, list) and len(cell) == 3 and all(isinstance(v, (int, float)) for v in cell),
        "cell_size must be a length-3 list of numbers",
        errors,
    )
    _require_number(cfg.get("pml_thickness"), "pml_thickness must be a number", errors)
    _require_int(cfg.get("resolution"), "resolution must be an int", errors)
    _require_number(cfg.get("until"), "until must be a number (Meep time units)", errors)
    molecule = cfg.get("molecule")
    _require(isinstance(molecule, dict), "molecule must be an object", errors)
    if isinstance(molecule, dict):
        _require_number(molecule.get("sigma"), "molecule.sigma must be a number", errors)
        _require_int(molecule.get("dimensions"), "molecule.dimensions must be an int (1|2|3)", errors)

    _validate_tls_block(cfg.get("tls"), errors)


def _validate_meep_cfg_no_tls(cfg: dict, errors: list[ValidationError]) -> None:
    _require_number(cfg.get("time_units_fs"), "time_units_fs must be a number", errors)
    cell = cfg.get("cell_size")
    _require(
        isinstance(cell, list) and len(cell) == 3 and all(isinstance(v, (int, float)) for v in cell),
        "cell_size must be a length-3 list of numbers",
        errors,
    )
    _require_number(cfg.get("pml_thickness"), "pml_thickness must be a number", errors)
    _require_int(cfg.get("resolution"), "resolution must be an int", errors)

    until = cfg.get("until")
    steps = cfg.get("steps")
    _require(
        until is not None or steps is not None,
        "Provide either 'until' (Meep time units) or 'steps' (integer timesteps)",
        errors,
    )
    if until is not None:
        _require_number(until, "until must be a number (Meep time units)", errors)
    if steps is not None:
        _require_int(steps, "steps must be an int (timesteps)", errors)

    molecule = cfg.get("molecule")
    _require(isinstance(molecule, dict), "molecule must be an object", errors)
    if isinstance(molecule, dict):
        _require_number(molecule.get("sigma"), "molecule.sigma must be a number", errors)
        _require_int(molecule.get("dimensions"), "molecule.dimensions must be an int (1|2|3)", errors)



def _validate_singlemode_cfg(cfg: dict, errors: list[ValidationError]) -> None:
    hub = cfg.get("hub")
    _require(isinstance(hub, dict), "hub must be an object", errors)
    if isinstance(hub, dict):
        _require_str(hub.get("host"), "hub.host must be a non-empty string", errors)
        _require_int(hub.get("port"), "hub.port must be an int", errors)
    sim = cfg.get("sim")
    _require(isinstance(sim, dict), "sim must be an object", errors)
    if isinstance(sim, dict):
        _require_number(sim.get("dt_au"), "sim.dt_au must be a number", errors)
        _require_number(sim.get("frequency_au"), "sim.frequency_au must be a number", errors)
        _require_number(sim.get("damping_au"), "sim.damping_au must be a number", errors)
        _require_str(sim.get("coupling_axis"), "sim.coupling_axis must be a non-empty string", errors)
        _require_int(sim.get("steps"), "sim.steps must be an int", errors)
    _validate_tls_block(cfg.get("tls"), errors)


def _validate_laser_cfg(cfg: dict, errors: list[ValidationError]) -> None:
    sim = cfg.get("sim")
    _require(isinstance(sim, dict), "sim must be an object", errors)
    if isinstance(sim, dict):
        _require_number(sim.get("dt_au"), "sim.dt_au must be a number", errors)
        _require_number(sim.get("until_au"), "sim.until_au must be a number", errors)
        _require_str(sim.get("coupling_axis"), "sim.coupling_axis must be a non-empty string", errors)
    drive = cfg.get("drive")
    _require(isinstance(drive, dict), "drive must be an object", errors)
    if isinstance(drive, dict):
        _require_str(drive.get("kind"), "drive.kind must be a non-empty string", errors)
    _validate_tls_block(cfg.get("tls"), errors)


def _validate_meep_unix_cfg(cfg: dict, errors: list[ValidationError]) -> None:
    _validate_meep_cfg(cfg, errors)
    _require_str(cfg.get("unixsocket"), "unixsocket must be a non-empty string", errors)


def _validate_meep_lammps_unix_cfg(cfg: dict, errors: list[ValidationError]) -> None:
    _validate_meep_cfg_no_tls(cfg, errors)
    _require_str(cfg.get("unixsocket"), "unixsocket must be a non-empty string", errors)
    lammps = cfg.get("lammps")
    _require(isinstance(lammps, dict), "'lammps' must be an object", errors)
    if isinstance(lammps, dict):
        _require_str(lammps.get("input_template"), "lammps.input_template must be a non-empty string", errors)
        _require_str(lammps.get("data"), "lammps.data must be a non-empty string", errors)


def _validate_slurm_meep_cfg(cfg: dict, errors: list[ValidationError]) -> None:
    _validate_meep_cfg(cfg, errors)
    _require_str(cfg.get("host_port_file"), "host_port_file must be a non-empty string", errors)

def _validate_slurm_meep_lammps_tcp_cfg(cfg: dict, errors: list[ValidationError]) -> None:
    _validate_meep_cfg_no_tls(cfg, errors)
    _require_str(cfg.get("host_port_file"), "host_port_file must be a non-empty string", errors)
    lammps = cfg.get("lammps")
    _require(isinstance(lammps, dict), "'lammps' must be an object", errors)
    if isinstance(lammps, dict):
        _require_str(lammps.get("input_template"), "lammps.input_template must be a non-empty string", errors)
        _require_str(lammps.get("data"), "lammps.data must be a non-empty string", errors)


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: mxl_validate_project.py <path/to/projects/YYYY-MM-DD-NAME>", file=sys.stderr)
        return 2

    repo_root = _find_repo_root(Path(__file__).resolve())
    project_dir = Path(argv[0]).resolve()
    projects_root = (repo_root / "projects").resolve()

    errors: list[ValidationError] = []
    _require(project_dir.is_dir(), f"Project directory does not exist: {project_dir}", errors)
    _require(
        str(project_dir).startswith(str(projects_root) + os.sep),
        f"Project must live under {projects_root}",
        errors,
    )

    config_path = project_dir / "config.json"
    _require(config_path.exists(), f"Missing config.json: {config_path}", errors)
    if config_path.exists():
        try:
            cfg = _read_json(config_path)
        except Exception as exc:
            errors.append(ValidationError(f"config.json is not valid JSON: {exc}"))
            cfg = None

        if isinstance(cfg, dict):
            _validate_common(cfg, errors)
            template_id = cfg.get("template_id")
            if template_id == "meep-tls-embedded":
                _validate_meep_cfg(cfg, errors)
                _require((project_dir / "em.py").exists(), "Missing em.py", errors)
            elif template_id == "meep-tls-socket-unix":
                _validate_meep_unix_cfg(cfg, errors)
                _require((project_dir / "em.py").exists(), "Missing em.py", errors)
                _require((project_dir / "driver.py").exists(), "Missing driver.py", errors)
            elif template_id == "meep-lammps-socket-unix":
                _validate_meep_lammps_unix_cfg(cfg, errors)
                _require((project_dir / "em.py").exists(), "Missing em.py", errors)
                _require((project_dir / "driver.py").exists(), "Missing driver.py", errors)
                _require((project_dir / "in_mxl.lmp").exists(), "Missing in_mxl.lmp", errors)
                _require((project_dir / "data.lmp").exists(), "Missing data.lmp", errors)
            elif template_id == "singlemode-tls-socket-tcp":
                _validate_singlemode_cfg(cfg, errors)
                _require((project_dir / "em.py").exists(), "Missing em.py", errors)
                _require((project_dir / "driver.py").exists(), "Missing driver.py", errors)
            elif template_id == "laser-tls-embedded":
                _validate_laser_cfg(cfg, errors)
                _require((project_dir / "em.py").exists(), "Missing em.py", errors)
            elif template_id == "slurm-meep-tls-tcp":
                _validate_slurm_meep_cfg(cfg, errors)
                _require((project_dir / "em_main.py").exists(), "Missing em_main.py", errors)
                _require((project_dir / "driver.py").exists(), "Missing driver.py", errors)
                _require((project_dir / "submit_main.sh").exists(), "Missing submit_main.sh", errors)
                _require((project_dir / "submit_driver.sh").exists(), "Missing submit_driver.sh", errors)
            elif template_id == "slurm-meep-lammps-tcp":
                _validate_slurm_meep_lammps_tcp_cfg(cfg, errors)
                _require((project_dir / "em_main.py").exists(), "Missing em_main.py", errors)
                _require((project_dir / "lammps_driver.py").exists(), "Missing lammps_driver.py", errors)
                _require((project_dir / "submit_main.sh").exists(), "Missing submit_main.sh", errors)
                _require((project_dir / "submit_lammps.sh").exists(), "Missing submit_lammps.sh", errors)
                _require((project_dir / "in_mxl.lmp").exists(), "Missing in_mxl.lmp", errors)
                _require((project_dir / "data.lmp").exists(), "Missing data.lmp", errors)
            else:
                _require(False, f"Unknown template_id: {template_id!r}", errors)

    if errors:
        for err in errors:
            print(f"[ERROR] {err.message}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
