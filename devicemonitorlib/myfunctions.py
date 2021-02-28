import concurrent.futures
import json
import sched
import threading

statuses = dict()
s = sched.scheduler()


def start(interval, devices_list):
    t = threading.Thread(target=start_monitoring, args=(interval, devices_list))
    t.start()


def start_monitoring(interval, devices_list):
    s.enter(0, 0, update_statuses, (interval, devices_list))
    s.run()


def update_statuses(interval, devices_list):
    s.enter(interval, 0, update_statuses, (interval, devices_list))

    with concurrent.futures.ThreadPoolExecutor(1) as executor:
        executor.map(update_status, devices_list)


def update_status(device):
    # Parse device parameters
    parsed_data = json.loads(device.data())

    # ...make new dict with alter key names
    altered_parsed_data = dict()

    # ...for every parameter...
    for key in parsed_data:
        # ......add 'output_' prefix to parameter
        new_key = f'output_{key}'
        # ......add parameter value to new parameter name key
        altered_parsed_data[new_key] = parsed_data[key]

    statuses[str(device.id)] = altered_parsed_data


def get_statuses():
    return statuses
