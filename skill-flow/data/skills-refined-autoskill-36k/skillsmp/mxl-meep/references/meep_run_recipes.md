# Meep run recipes

Copy these into `projects/YYYY-MM-DD-NAME/` and adjust parameters/paths.

## Meep + TLS (embedded, no sockets)
`em.py`
```python
import meep as mp
import maxwelllink as mxl

tls = mxl.Molecule(
    driver="tls",
    driver_kwargs=dict(omega=0.242, mu12=187.0, orientation=2, pe_initial=1e-3),
    center=mp.Vector3(0, 0, 0),
    size=mp.Vector3(1, 1, 1),
    sigma=0.1,
    dimensions=2,
)

sim = mxl.MeepSimulation(
    molecules=[tls],
    time_units_fs=0.1,
    cell_size=mp.Vector3(8, 8, 0),
    boundary_layers=[mp.PML(3.0)],
    resolution=10,
)

sim.run(until=90)
```
Run: `python em.py`

## Meep + socket driver (UNIX socket)
`em.py`
```python
import meep as mp
import maxwelllink as mxl

hub = mxl.SocketHub(unixsocket="tls_demo", timeout=10.0, latency=1e-4)

tls = mxl.Molecule(
    hub=hub,
    center=mp.Vector3(),
    size=mp.Vector3(1, 1, 1),
    sigma=0.1,
    dimensions=2,
)

sim = mxl.MeepSimulation(
    hub=hub,
    molecules=[tls],
    time_units_fs=0.1,
    cell_size=mp.Vector3(8, 8, 0),
    boundary_layers=[mp.PML(3.0)],
    resolution=10,
)

sim.run(until=90)
```

Driver (same machine):
`mxl_driver --model tls --unix --address tls_demo --param "omega=0.242, mu12=187, orientation=2, pe_initial=1e-3"`

## Meep + socket drivers (TCP, HPC-friendly)
Use this pattern when the EM job and driver job run on different nodes (SLURM two-step).

`em_main.py`
```python
import meep as mp
import maxwelllink as mxl
from maxwelllink import sockets as mxs

# Writes tcp_host_port_info.txt on rank 0
host, port = mxs.get_available_host_port(localhost=False, save_to_file="tcp_host_port_info.txt")
hub = mxl.SocketHub(host=host, port=port, timeout=200.0, latency=1e-4)

molecule = mxl.Molecule(hub=hub, center=mp.Vector3(), size=mp.Vector3(1, 1, 1), sigma=0.1, dimensions=2)
sim = mxl.MeepSimulation(
    hub=hub,
    molecules=[molecule],
    time_units_fs=0.1,
    cell_size=mp.Vector3(8, 8, 0),
    boundary_layers=[mp.PML(3.0)],
    resolution=10,
)
sim.run(until=90)
```

Driver (separate job/node):
`mxl_driver --model tls --address "$HOST" --port "$PORT" --param "omega=0.242, mu12=187, orientation=2, pe_initial=1e-3"`

## Notes for many molecules
- For thousands of molecules, set `store_additional_data=False` on most molecules to limit memory usage.
