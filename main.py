import sched
import threading
from pathlib import Path
from time import sleep

import devicemonitorlib as device_monitor


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Klasa reprezentujaca urzadzenie KONIECZNIE musi dostarczyć nastepujace rzeczy:#
# - metode `data()`, zwracajaca string JSON z parametrami urzadzenia,           #
# - atrybut `id`, identyfikujacy urzadzenie                                     #
# - atrybut `param_list`, okreslajacy jakie parametry nalezy monitorowa         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class DeviceByFile:
    """Przykladowa reprezentacja urzadzenia poprzez plik

    Parameters
    ----------
    identifier : str
        ID urzadzenia
    param_list : list
        lista monitorowanych parametrow
    file_path : str
        sciezka do pliku z parametrami

    """

    def __init__(self, identifier: str, param_list: list, file_path: str):
        self.id = identifier
        self.param_list = param_list
        self.path = Path(file_path)

    def data(self) -> str:
        """Funkcja dostarczajaca reprezentacje parametrow w formacie JSON

        Returns
        ----------
        str
            String w formacie JSON

        """
        with self.path.open() as f:
            return f.read()


# Przyklad innego typu urzadzenia
#
# class DeviceByHTTP:
#     def __init__(self, identifier: str, param_list: list, ip_address: str, port: int):
#         self.id = identifier
#         self.param_list = param_list
#         self.ip_address = ip_address
#         self.port = port
#
#     def data(self) -> str:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#             sock.connect((self.ip_address, self.port))
#             response = sock.recv(1024)
#             return str(response)


def main():
    # Lista urzadzen do monitorowania.
    device_list = [
        DeviceByFile('1', ['current', 'voltage', 'pressure'], './devices/zasilacz_00001.json'),
        DeviceByFile('2', ['current', 'voltage'], './devices/zasilacz_00002.json'),
        DeviceByFile('3', ['current', 'voltage'], './devices/zasilacz_00003.json'),
        # DeviceByHTTP('4', ['current', 'voltage', 'pressure'], '127.0.0.1', 6666),
    ]

    # Jak czesto odswiezac parametry urzadzenia
    update_interval = 1

    print('Main thread is starting the DeviceMonitor...')
    device_monitor.start(update_interval, device_list)
    print('DeviceMonitor started successfully!')

    sleep(1)

    # Scheduler wypisujacy cyklicznie parametry
    s = sched.scheduler()

    # Jak czesto wypisywac statusy urzadzen
    print_interval = 1

    print('Main thread is creating a new thread with scheduler that periodically calls the get_statuses() method...')
    t = threading.Thread(target=start_print_scheduler, args=(s, print_interval))
    t.start()
    print('Thread with print scheduler started successfully!')

    sleep(1)

    print('Main thread sleeping for 5 secs while other thread prints...')
    sleep(5)

    print('Main thread calling get_statuses()...')
    print(device_monitor.get_statuses())
    print('Main thread called get_statuses() successfully!')

    sleep(2)
    print('Changing device parameter in file zasilacz_00001.json...')
    v1 = 450
    v2 = 666
    file = Path('./devices/zasilacz_00001.json')
    text_orig = file.read_text()
    text_changed = text_orig.replace(f'"voltage": {v1}', f'"voltage": {v2}')
    file.write_text(text_changed)
    print(f'Changed voltage from {v1} to {v2}')

    sleep(5)

    print('Reverting device parameter changes...')
    file.write_text(text_orig)
    print(f'Reverted voltage from {v2} to {v1}')

    sleep(5)

    print('Main thread stops the DeviceMonitor...')
    device_monitor.stop()
    print('Main thread stopped the DeviceMoniotor successfully!')

    sleep(5)

    print('Main thread stops the printer thread...')
    stop_scheduler(s)
    print('Printer thread stopped successfully!')

    sleep(5)

    print('Main thread is ending...')


def print_statuses(s, print_interval, statuses):
    """Funkcja wypisujaca statusy urzadzen

    Parameters
    ----------
    s
        Referencja schedulera
    print_interval
        Interwal wypisywania statusow urzadzen (w sekundach)
    statuses
        Slownik zawierajacy statusy urzadzen

    """
    # Rekurencyjne dodawanie eventu do schedulera z konkretnym interwalem
    s.enter(print_interval, 0, print_statuses, (s, print_interval, device_monitor.get_statuses()))

    # Wypisanie statusow
    print(statuses)


def start_print_scheduler(s, print_interval):
    """Funkcja uruchamiajaca cykliczne wypisywanie parametrow

    Parameters
    ----------
    s
        Referencja schedulera
    print_interval
        Czas odstepu miedzy kolejnymi wypisaniami parametrow
    """
    # Dodanie pierwszego wywolania funkcji wypisujacej do schedulera z zerowym oczekiwaniem
    s.enter(0, 0, print_statuses, (s, print_interval, device_monitor.get_statuses()))
    # Uruchomienie schedulera
    s.run()


def stop_scheduler(s):
    """Funkcja czyszczaca scheduler

    Parameters
    ----------
    s
        Referencja schedulera do wyczyszczenia
    """
    for ev in s.queue:
        s.cancel(ev)


if __name__ == '__main__':
    main()
