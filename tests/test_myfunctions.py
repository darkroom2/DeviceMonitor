from devicemonitorlib import myfunctions

dm = myfunctions.DeviceMonitor(1000)

dm.monitored_devices.append(myfunctions.Device(1, './devices/zasilacz_00001.json'))
dm.monitored_devices.append(myfunctions.Device(2, './devices/zasilacz_00002.json'))
dm.monitored_devices.append(myfunctions.Device(3, './devices/zasilacz_00003.json'))

dm.update_statuses()


def test_get_statuses():
    true_dict = {
        '1': {'output_current': 0.5, 'output_voltage': 450},
        '2': {'output_current': 0.6, 'output_voltage': 449},
        '3': {'output_current': 0.4, 'output_voltage': 451}
    }

    assert true_dict == dm.get_statuses(), 'Dicts not match!'


def test_upate_statuses():
    assert dm.update_statuses() is True, 'Error in update_statuses()!'
