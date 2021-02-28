from devicemonitorlib import devicemonitorfunctions
from pathlib import Path


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


def test_upate_statuses():
    assert dm_non_empty.update_statuses() is True and dm_empty.update_statuses() is False, 'Error in update_statuses()!'


def test_get_statuses():
    true_dict = {
        '1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None},
        '2': {'output_current': 0.6, 'output_voltage': 449},
        '3': {'output_current': 0.4, 'output_voltage': 451}
    }

    assert true_dict == dm_non_empty.get_statuses(), 'Dicts not match!'
