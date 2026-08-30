Usage
=====

------------
Installation
------------

| **rfnode** is available on PyPI hence you can use `pip` to install it.

It is recommended to perform the installation in an isolated `python virtual environment` (env).
You can create and activate an `env` using any tool of your preference (ie `virtualenv`, `venv`, `pyenv`).

Assuming you have 'activated' a `python virtual environment`:

.. code-block:: shell

  python -m pip install rfnode


---------------
Simple Use Case 
---------------

| Plugin in RTLSDR from  `Nooelec <https://www.nooelec.com/store/sdr/sdr-receivers/nesdr-smart-sdr.html?srsltid=AfmBOoqFB5e2jf1fsd1I9xCGV9Pz6WiBdZD2RNyXnFQp5zjB3nGYRtPX>`__ 

.. code-block:: shell

  rfnode  -s setting.json -v 40 -ld /home/alan/tmp
  **setting.json**  the setting file for frequency range and power threshold 
| **v**: extra verbose  to debug; if not supplied, it will default to error
| **ld**: log file directory location
|



--------------
Running PyTest 
--------------
| PyTest can be run from command line.

.. code-block:: shell
  
  python -m pip install -e . rfnode[test]
  pytest



