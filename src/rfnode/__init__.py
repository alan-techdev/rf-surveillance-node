"""
| **RF Node** allows you to plugin as many as SDR devices to scan across defined frequency range
| If you have 10 SDR nodes plugged into a computer device, and you have frequency range from 100 Mhz to 20 GHZ.
| The application will split the frequency range across 10 SDR node devices  to start scanning and send to RF Central

| The Hub ( RF Central) will receive each scanned information from each node to be stored.
| The RF Analysis Engine will start to use ML model to extract different meta data and identify different finger prints
| The RF Meta Data Display will query the RF Analysis Engine to display the data in a graphical friendly interface (Desktop client application )
"""

from .__version__ import __author__ as __author__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__


