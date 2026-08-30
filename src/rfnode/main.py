import platform
from argparse import ArgumentParser, Namespace

from rtlsdr import RtlSdr
from serial import Serial

from rfnode import (
    __author__,  # type:ignore
    __description__,  # type:ignore
    __license__,  # type:ignore
    __title__,  # type:ignore
    __url__,  # type:ignore
    __version__,  # type:ignore
)
from rfnode._help import bug_reporting
from rfnode.broker import DataBroker
from rfnode.common.log_manager import LogManager
from rfnode.common.setting import Setting
from rfnode.common.util import Util
from rfnode.devicemanager import DeviceManager
from rfnode.scanner import Scanner
from rfnode.sender.sender import Sender

"""
A- Make the project in edit mode
$ pwd
/home/alan/workspace-python/RTL-SDR/rf-surveillance
$ pip install -e .
$ rfnode setting.json -vvv -ld /home/alan/tmp

//////////////////////////////////////////

B- Using PYTHONPATH (Not recommended)
Linux:
=====
$ export PYTHONPATH=/home/alan/workspace-python/RTL-SDR/rf-surveillance/src
$ pwd
 /home/alan/workspace-python/RTL-SDR/rf-surveillance/src
$ python rfnode setting.json -vvv -ld /home/alan/tmp

Windows:
========
set PYTHONPATH=/home/alan/workspace-python/RTL-SDR/rf-surveillance/src
echo %PYTHONPATH%
python rfnode setting.json -vvv -ld /home/alan/tmp
Note: Check the devicemanager from the control panel for the port name
"""


def main() -> None:
    """
    The main function is called only when the script is executed directly,
    Execute data acquisition system using RTL-SDR devices.
    It initializes a logging manager and configures it based on command-line arguments, responsible
    for managing data flow between different components of the system.


    """
    # https://docs.python.org/3/howto/argparse.html
    parser = ArgumentParser(
        prog = "rfnode",
        usage="rfnode [-h] [-ld dir] [-v] [--version] [--author] [--report-bug] [--description] [--license] [--title] [--url]",
        description=" Radio Frequency Scanner which capture given power threshold"
    )
    parser.add_argument("-s",
                        "--setting",
                        help="path to setting file", type=str, metavar="file")
    parser.add_argument(
        "-ld",
        "--log_directory",
        help="store output log in a directory",
        type=str,
        metavar="dir",
    )
    parser.add_argument("-v",
                         "--verbose", help="increase output verbosity.Default to Error if not supplied, 40 is Debug", type=int, metavar="", default=0)

    parser.add_argument("--version", action="store_true", help="Display current library version")
    parser.add_argument("--author", action="store_true", help="Display author information")
    parser.add_argument("--report-bug", action="store_true", help="Library detail information to report a bug")
    parser.add_argument("--description", action="store_true", help="Display description of the package")
    parser.add_argument("--license", action="store_true", help="Display license information")
    parser.add_argument("--title", action="store_true", help="Display title of the package")
    parser.add_argument("--url", action="store_true", help="Display read the docs url of the package")

    args: Namespace = parser.parse_args()

    if args.version:
            print(f"Version: {__version__}")
            return

    if args.author:
        print(f"Author: {__author__}")
        return

    if args.report_bug:
        bug_reporting()
        return

    if args.description:
        print(f"Description: {__description__}")
        return

    if args.license:
        print(f"License: {__license__}")
        return

    if args.title:
        print(f"Title: {__title__}")
        return

    if args.url:
        print(f"URL: {__url__}")
        return

    Setting.load_setting(args.setting)
    LogManager().config_logger(args.verbose, args.log_directory)


    data_broker = DataBroker()

    port: str = ""
    if platform.system() == "Windows":
        port = Setting.rf_sender_port_windows
    else:
        port = "/dev/" + Setting.rf_sender_port

    ser = Serial(port=port, baudrate=115200)
    sender: Sender = Sender(ser, hold=Setting.rf_sleep_time)
    data_broker.set_rf_sender(sender)

    data_broker.start()

    serial_numbers = DeviceManager.get_device_serial_list()
    frequencies = Util.generate_array(
        Setting.freq_start, Setting.freq_end, Setting.freq_step, len(serial_numbers) # type:ignore
    )
    print(f"RTL SDR numbers {len(serial_numbers)}")

    scanners = []  # a list of scanner

    for i in range(len(serial_numbers)):
        print(f"device index {i}")
        # see https://pyrtlsdr.readthedocs.io/en/latest/rtlsdr.html
        sdr = RtlSdr(device_index=i)
        print(f"Sample rate in millions(Msps) {Setting.sample_rate/1e6}")
        sdr.set_sample_rate(
            Setting.sample_rate
        )  # default sample_rate value used on initialization: 1.024e6 (1024 Msps)
        print(f"IQ sample size(ex: 0.7 -1.5j) {Setting.sample_size}\n\n")
        scanner = Scanner(
            frequencies=frequencies[i], # type:ignore
            sample_size=Setting.sample_size,
            power_threshold=Setting.power_threshold,
            sdr=sdr,
        )
        scanners.append(scanner)

    print(f"Number of threads: {len(scanners)}\n\n")
    for scanner in scanners:
        scanner.start()

    for thread in scanners:
        thread.join()
        print(f"Thread {thread.name} is finished now")

    # Block until all tasks are done
    print("Before the join for queue ...")
    DataBroker.q.join()
    print("All work completed")


# this is important so that it does not run from pytest
if __name__ == "__main__":
    main()
