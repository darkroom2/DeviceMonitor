# import concurrent.futures
import json
import sched
import threading

from typing import Union

# Slownik zawierajacy statusy urzadzen
statuses = dict()

# Scheduler odswiezajacy statusy urzadzen
s = sched.scheduler()

# Mutex blokujacy czytanie/pisanie zasobu
lock = threading.Lock()

# Zmienna informujaca czy bilbioteka zostala uruchomiona
running = None


def start(interval: int, devices_list: list):
    """Funkcja tworzaca nowy watek DeviceMonitora

    Parameters
    ----------
    interval
        Czas odstepu miedzy kolejnymi odswiezeniami parametrow
    devices_list
        Lista monitorowanych urzadzen
    """
    t = threading.Thread(target=start_monitoring, args=(interval, devices_list))
    t.start()
    with lock:
        global running
        running = True


def stop():
    """Funkcja zatrzymujaca watek DeviceMonitora

    """
    # Wyczyszczenie schedulera spowoduje czyste zakonczenie watku
    with lock:
        global running, s

        for event in s.queue:
            s.cancel(event)

        running = False
        s = sched.scheduler()
        statuses.clear()


def get_statuses() -> Union[dict, None]:
    """Funkcja zwracajaca status monitorowanych urzadzen

    Returns
    -------
    dict
        Statusy monitorowanych urzadzen
    None
        Zwracane gdy monitorowanie zostalo zatrzymane

    """
    with lock:
        if running:
            return statuses
    return None


def start_monitoring(interval: int, devices_list: list):
    """Funkcja uruchamiajaca cykliczne odswiezanie parametrow

    """
    s.enter(0, 0, update_statuses, (interval, devices_list))
    s.run()


def update_statuses(interval: int, devices_list: list):
    """Funkcja odswiezajaca kazde monitorowane urzadzenie

    """
    s.enter(interval, 0, update_statuses, (interval, devices_list))

    for device in devices_list:
        update_status(device)

    # Zrownoleglone odswiezanie statusu
    # with concurrent.futures.ThreadPoolExecutor(4) as executor:
    #     executor.map(update_status, devices_list)


def update_status(device):
    """Funkcja pobierajaca parametry konkretnego urzadzenia i dodajaca je do slownika statusu wszystkich urzadzen

    Parameters
    ----------
    device
        Konkretne urzadzenie, ktorego parametry nalezy pobrac
    """
    # Zamiana JSON stringa na slownik
    parsed_data = json.loads(device.data())

    # Nowy slownik wyjsciowy dla danego urzadzenia
    altered_parsed_data = dict()

    # Do kazdego parametru z listy monitorowanych
    for key in device.param_list:
        # ...dodaj prefix 'output_'
        new_key = f'output_{key}'
        # ...i dodaj do slownika wyjsciowego jesli urzadzenie go dostarcza
        altered_parsed_data[new_key] = parsed_data[key] if key in parsed_data.keys() else None

    with lock:
        statuses[str(device.id)] = altered_parsed_data

