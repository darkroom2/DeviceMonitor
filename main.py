import sched
from pathlib import Path
import devicemonitorlib.myfunctions as dm


class DeviceByFile:
    """
    Przykladowa reprezentacja urzadzenia poprzez plik

    Attributes
    ---
    id : str
        identyfikator urzadzenia
    param_list : list
        lista mmonitorowanych parametrow
    file_path :
    """
    def __init__(self, identifier: str, param_list: list, file_path):
        # START Parametry konieczne
        self.id = identifier
        self.param_list = param_list
        # END Parametry konieczne

        self.path = Path(file_path)

    def data(self) -> str:
        """
        Funkcja konieczna do napisania

        :return: String w formacie JSON
        :rtype: str
        """
        with self.path.open() as f:
            return f.read()


def print_statuses(print_interval, statuses):
    s.enter(print_interval, 0, print_statuses, (print_interval, dm.get_statuses()))
    print(statuses)


def main():
    device_list = [
        DeviceByFile('1', ['current', 'voltage'], './devices/zasilacz_00001.json'),
        DeviceByFile('2', ['current', 'voltage'], './devices/zasilacz_00002.json'),
        DeviceByFile('3', ['current', 'voltage'], './devices/zasilacz_00003.json')
    ]
    params_update_interval = 1
    dm.start(params_update_interval, device_list)

    print_interval = 1
    s.enter(0, 0, print_statuses, (print_interval, dm.get_statuses()))
    s.run()


if __name__ == '__main__':
    s = sched.scheduler()
    main()
