# qgis_runalg
Run QGIS algorithms from outside of QGIS

### Installation

```
python setup.py install
```

### Usage

```
import logging
logging.getLogger('qgis_runalg').setLevel('INFO')

from qgis_runalg import qgis_runalg

qgis_runalg('otb:rescaleimage', args=[...])
```

Pro-tip: Get your algorithm call signature from the processing history.
