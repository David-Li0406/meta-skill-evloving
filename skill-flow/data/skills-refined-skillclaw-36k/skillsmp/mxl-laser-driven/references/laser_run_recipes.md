# Laser-driven run recipes

Copy these into `projects/YYYY-MM-DD-NAME/` and adjust parameters/paths.

## Laser-driven + embedded TLS
`em.py`
```python
import maxwelllink as mxl
from maxwelllink.tools import gaussian_pulse

tls = mxl.Molecule(
    driver="tls",
    driver_kwargs=dict(omega=0.242, mu12=187.0, orientation=2, pe_initial=1e-3),
)

sim = mxl.LaserDrivenSimulation(
    dt_au=0.5,
    molecules=[tls],
    drive=gaussian_pulse(amplitude_au=1e-4, sigma_au=30.0),
    coupling_axis="xy",
    record_history=True,
)

sim.run(until=500.0)
```

