import threading
from pathlib import Path
from time import sleep

import pytest

from devicemonitorlib import devicemonitorfunctions as dm


class DeviceByFile:
    def __init__(self, identifier: str, param_list: list, file_path: str):
        self.id = identifier
        self.param_list = param_list
        self.path = Path(file_path)

    def data(self) -> str:
        with self.path.open() as f:
            return f.read()


device_list = [
    DeviceByFile('1', ['current', 'voltage', 'pressure'], './devices/zasilacz_00001.json'),
    DeviceByFile('2', ['current', 'voltage'], './devices/zasilacz_00002.json'),
    DeviceByFile('3', ['current', 'voltage'], './devices/zasilacz_00003.json'),
]

true_dict = {
    '1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None},
    '2': {'output_current': 0.6, 'output_voltage': 449},
    '3': {'output_current': 0.4, 'output_voltage': 451}
}


@pytest.mark.parametrize(('interval', 'devices_list'), [(0, []), (1, []), (1, device_list)])
def test_stop(interval, devices_list):
    dm.stop()
    sleep(1)

    dm.start(interval, devices_list)
    sleep(1)

    dm.stop()
    sleep(3)
    assert len(threading.enumerate()) == 1 and dm.running is False and dm.statuses == {} and not dm.s.queue


@pytest.mark.parametrize(('interval', 'devices_list'), [(0, []), (1, []), (1, device_list)])
def test_start(interval, devices_list):
    errors = []

    dm.stop()
    sleep(1)

    dm.start(interval, devices_list)
    sleep(1)

    # Jesli poza watkiem glownym nie ma innego watku to blad
    if len(threading.enumerate()) == 1:
        errors.append(f'Thread with params: {interval}, {devices_list} is not running.')

    if not dm.running:
        errors.append('Function did not finish!')

    assert not errors, 'Errors occured:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize(('device', 'expected'), [(device_list[0], true_dict[device_list[0].id]),
                                                  (device_list[1], true_dict[device_list[1].id]),
                                                  (device_list[2], true_dict[device_list[2].id])])
def test_update_status(device, expected):
    dm.stop()
    sleep(1)

    dm.update_status(device)
    assert dm.statuses[device.id] == expected


@pytest.mark.parametrize(('interval', 'devices_list', 'expected'), [(0, [], {}), (1, [], {}), (1, device_list, true_dict)])
def test_update_statuses(interval, devices_list, expected):
    dm.stop()
    sleep(1)

    dm.update_statuses(interval, devices_list)
    assert dm.s.queue and dm.statuses == expected


@pytest.mark.parametrize(('interval', 'devices_list'), [(0, []), (1, []), (1, device_list)])
def test_start_monitoring(interval, devices_list):
    errors = []

    dm.stop()
    sleep(1)

    t = threading.Thread(target=dm.start_monitoring, args=(interval, devices_list))
    t.start()

    sleep(1)

    if not dm.s.queue:
        errors.append('Schedulers queue empty!')

    dm.stop()
    sleep(1)

    assert not errors, 'Errors occured:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize(('interval', 'devices_list', 'expected'),
                         [(0, [], {}), (1, [], {}), (1, device_list, true_dict)])
def test_get_statuses(interval, devices_list, expected):
    """Symuluje odswiezanie parametrow

    """
    dm.stop()
    sleep(1)

    dm.start(interval, devices_list)
    sleep(1)
    assert expected == dm.get_statuses(), 'Dicts doesnt match!'


def test_get_statuses_without_start():
    """Symuluje pobranie statusow bez wystartowania biblioteki

    """
    dm.stop()
    sleep(1)
    assert dm.get_statuses() is None, 'Should be None if DeviceMonitor isnt running.'
