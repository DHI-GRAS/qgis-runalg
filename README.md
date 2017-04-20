# qgis_runalg
Run QGIS algorithms from outside of QGIS

For running QGIS commands from an external Python session **on Windows**.

Initializes the QGIS environment and calls the algorithm.

This involves a lot of round-tripping. Advice: Run the commands directly instead if you can (GDAL through `subprocess`, SNAP through `gpt`, GRASS7 via its native Python interface...).


### Installation

```
python setup.py install
```

### Usage

```python
import logging
logging.getLogger('qgis_runalg').setLevel('INFO')

from qgis_runalg import qgis_runalg

qgis_runalg('otb:rescaleimage', args=[...])
```

Pro-tip: Get your algorithm call signature from the processing history.
