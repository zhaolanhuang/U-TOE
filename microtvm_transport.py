from tvm.micro.transport import Transport, TransportTimeouts
from riotctrl.ctrl import RIOTCtrl
import serial

class UTOETransport(Transport):

    def __init__(self, riot_ctrl, timeouts=None):
        self._riot_ctrl : RIOTCtrl = riot_ctrl
        self._timeouts = timeouts
        self._serial = None

    def timeouts(self):
        assert self._timeouts is not None, "Transport not yet opened"
        return self._timeouts

    def open(self):
        port = get_local_serial_port()
        self._serial = serial.Serial(port, baudrate=115200, timeout=10)
        
        self._timeouts = TransportTimeouts(
            session_start_retry_timeout_sec=2.0,
            session_start_timeout_sec=15.0,
            session_established_timeout_sec=15.0,
        )

    def close(self):
        if self._serial is None:
            return
        self._serial.close()
        self._serial = None
        self._riot_ctrl.stop_exp()

    def write(self, data, timeout_sec):
        if self._serial is None:
            return
        self._serial.write_timeout = timeout_sec
        return self._serial.write(data)

    def read(self, n, timeout_sec):
        if self._serial is None:
            return
        self._serial.timeout = timeout_sec
        return self._serial.read(n)

def get_local_serial_port():
    import subprocess, json
    output = subprocess.check_output(f"make list-ttys-json", shell=True)
    tty_info = json.loads(output)
    return tty_info[0]['path']