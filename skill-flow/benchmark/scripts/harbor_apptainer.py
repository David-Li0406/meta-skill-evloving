"""Run harbor's CLI with the ApptainerEnvironment registered.

``harbor jobs start`` (= ``harbor run``) has no ``--environment-import-path``
flag (only ``trials start`` does), so to use our custom Apptainer backend we
register it into harbor's ``EnvironmentType`` enum + ``EnvironmentFactory`` in
this process, then hand off to harbor's Typer app. Invoke exactly like harbor:

    python -m benchmark.scripts.harbor_apptainer run --env apptainer ...
"""

from __future__ import annotations

import sys


def _register_apptainer() -> None:
    """Make harbor's ``docker`` env resolve to ApptainerEnvironment.

    Typer freezes the ``--env`` choices from EnvironmentType at import time, so a
    new enum member can't be passed on the CLI. Instead we remap the existing
    ``docker`` slot in the factory: this process is dedicated to apptainer runs,
    so ``--env docker`` here means "run via Apptainer".
    """
    from harbor.environments.factory import EnvironmentFactory
    from harbor.models.environment_type import EnvironmentType

    from benchmark.environments.apptainer import ApptainerEnvironment

    EnvironmentFactory._ENVIRONMENT_MAP[EnvironmentType.DOCKER] = ApptainerEnvironment


def main() -> None:
    _register_apptainer()
    from harbor.cli.main import app

    # Drop "-m benchmark.scripts.harbor_apptainer" from argv; pass the rest to harbor.
    sys.argv = ["harbor", *sys.argv[1:]]
    app()


if __name__ == "__main__":
    main()
