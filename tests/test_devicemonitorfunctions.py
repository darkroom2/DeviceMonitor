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
    # Wyczyszczenie biblioteki z ewentualnych poprzednich wywolan
    dm.stop()
    sleep(1)

    # Uruchomienie biblioteki
    dm.start(interval, devices_list)
    sleep(1)

    # Zatrzymanie biblioteki
    dm.stop()
    sleep(3)

    # Sprawdzenie czy watek zostal zamkniety i czy zostaly 'wyzerowane' zmienne oraz czy kolejka schedulera jest pusta
    assert (len(threading.enumerate()) == 1)\
           and (dm.running is False) \
           and dm.statuses == {} \
           and not dm.s.queue, 'Thread wasnt properly closed!'


@pytest.mark.parametrize(('interval', 'devices_list'), [(0, []), (1, []), (1, device_list)])
def test_start(interval, devices_list):
    errors = []

    # Wyczyszczenie biblioteki z ewentualnych poprzednich wywolan
    dm.stop()
    sleep(1)

    # Uruchomienie biblioteki
    dm.start(interval, devices_list)
    sleep(1)

    # Jesli watek biblioteki nie zostal uruchomiony to dodajemy blad do listy
    if len(threading.enumerate()) == 1:
        errors.append(f'Thread with params: {interval}, {devices_list} is not running.')

    # Jesli zmienna running nie zostala ustawiona na True, to dodajemy blad do listy
    if not dm.running:
        errors.append('Function did not finish!')

    # Sprawdzenie czy lista bledow jest pusta, jesli nie, to wypisanie komunikatow bledow
    assert not errors, 'Errors occured:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize(('device', 'expected'), [(device_list[0], true_dict[device_list[0].id]),
                                                  (device_list[1], true_dict[device_list[1].id]),
                                                  (device_list[2], true_dict[device_list[2].id])])
def test_update_status(device, expected):
    # Wyczyszczenie biblioteki z ewentualnych poprzednich wywolan
    dm.stop()
    sleep(1)

    # Pobranie aktualnych wartosci parametrow konkretnego urzadzenia
    dm.update_status(device)

    # Sprawdzenie czy funkcja utworzyla odpowiedni status danego urzadzenia
    assert dm.statuses[device.id] == expected, 'Dicts doesnt match!'


@pytest.mark.parametrize(('interval', 'devices_list', 'expected'),
                         [(0, [], {}), (1, [], {}), (1, device_list, true_dict)])
def test_update_statuses(interval, devices_list, expected):
    # Wyczyszczenie biblioteki z ewentualnych poprzednich wywolan
    dm.stop()
    sleep(1)

    # Pobranie aktualnych wartosci parametrow wszystkich urzadzen
    dm.update_statuses(interval, devices_list)

    # Sprawdzenie czy utworzono odpowiedni status urzadzen oraz czy zainicjowano scheduler
    assert dm.s.queue and dm.statuses == expected, 'Dicts doesnt match!'


@pytest.mark.parametrize(('interval', 'devices_list'), [(0, []), (1, []), (1, device_list)])
def test_start_monitoring(interval, devices_list):
    errors = []

    # Wyczyszczenie biblioteki z ewentualnych poprzednich wywolan
    dm.stop()
    sleep(1)

    # Utworzenie watku ze schedulerem pobierajacym cyklicznie parametry urzadzen
    t = threading.Thread(target=dm.start_monitoring, args=(interval, devices_list))
    t.start()
    sleep(1)

    # Sprawdzenie czy udalo sie uruchomi scheduler, jesli jego kolejka jest pusta, to dodajemy blad
    if not dm.s.queue:
        errors.append('Schedulers queue empty!')

    # Zatrzymanie biblioteki
    dm.stop()
    sleep(1)

    # Sprawdzenie czy lista bledow jest pusta, jesli nie, to wypisanie komunikatow bledow
    assert not errors, 'Errors occured:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize(('interval', 'devices_list', 'expected'),
                         [(0, [], {}), (1, [], {}), (1, device_list, true_dict)])
def test_get_statuses(interval, devices_list, expected):
    # Wyczyszczenie biblioteki z ewentualnych poprzednich wywolan
    dm.stop()
    sleep(1)

    # Uruchomienie biblioteki
    dm.start(interval, devices_list)
    sleep(1)

    # Sprawdzenie zgodnosci slownikow
    assert dm.get_statuses() == expected, 'Dicts doesnt match!'


def test_get_statuses_without_start():
    # Wyczyszczenie biblioteki z ewentualnych poprzednich wywolan
    dm.stop()
    sleep(1)

    # Jesli nie uruchomiono biblioteki, testowana funkcja powinna zwracac None
    assert dm.get_statuses() is None, 'Should be None if DeviceMonitor isnt running!'
