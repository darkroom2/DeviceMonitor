from time import sleep

import devicemonitorlib.myfunctions as dm

if __name__ == '__main__':
    dm_non_empty = dm.DeviceMonitor(3)

    dm_non_empty.monitored_devices.append(dm.Device(1, ['current', 'voltage'], './devices/zasilacz_00001.json'))
    dm_non_empty.monitored_devices.append(dm.Device(2, ['current', 'voltage'], './devices/zasilacz_00002.json'))
    dm_non_empty.monitored_devices.append(dm.Device(3, ['current', 'voltage'], './devices/zasilacz_00003.json'))
    dm_non_empty.monitored_devices.append(dm.Device(2, './devices/zasilacz_00002.json'))
    dm_non_empty.monitored_devices.append(dm.Device(3, './devices/zasilacz_00003.json'))

    dm_non_empty.start()

    sleep(5)
    print(dm_non_empty.get_statuses())
