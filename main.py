import sched
from pathlib import Path

import devicemonitorlib.devicemonitorfunctions as device_monitor


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


def main():
    # Lista urzadzen do monitorowania.
    device_list = [
        DeviceByFile('1', ['current', 'voltage', 'pressure'], './devices/zasilacz_00001.json'),
        DeviceByFile('2', ['current', 'voltage'], './devices/zasilacz_00002.json'),
        DeviceByFile('3', ['current', 'voltage'], './devices/zasilacz_00003.json'),
        # DeviceByHTTP('4', ['current', 'voltage', 'pressure'], '127.0.0.1', 6666),
    ]

    # Jak czesto odswiezac parametry urzadzenia
    params_update_interval = 1

    # Uruchomienie monitorowania
    device_monitor.start(params_update_interval, device_list)

    # Scheduler wypisujacy cyklicznie parametry
    s = sched.scheduler()

    # Jak czesto pobierac statusy urzadzen
    print_interval = 1

    # Dodanie pierwszego wywolania funkcji wypisujacej do schedulera z zerowym oczekiwaniem
    s.enter(0, 0, print_statuses, (s, print_interval, device_monitor.get_statuses()))

    # Uruchomienie schedulera
    s.run()


if __name__ == '__main__':
    main()
