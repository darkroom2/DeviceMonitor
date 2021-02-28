import concurrent.futures
import json
import sched
import threading

# TODO:
# - zrobic docstring dokumentacje numpydoc
#
# - zrobic strukture pip package library
#
# - dodac testy
#
# - zrobic metode stop
#
# - sprawdzic thread-safety

lock = threading.Lock()
statuses = dict()
s = sched.scheduler()



def start(interval, devices_list):
    t = threading.Thread(target=start_monitoring, args=(interval, devices_list))
    t.start()

def stop():



def start_monitoring(interval, devices_list):
    s.enter(0, 0, update_statuses, (interval, devices_list))
    s.run()


def update_statuses(interval, devices_list):
    s.enter(interval, 0, update_statuses, (interval, devices_list))

    for device in devices_list:
        update_status(device)

    # with concurrent.futures.ThreadPoolExecutor(4) as executor:
    #     executor.map(update_status, devices_list)


def update_status(device):
    success = False

    # Parse device parameters
    parsed_data = json.loads(device.data())

    # Make new dict with altered key names
    altered_parsed_data = dict()

    # For every monitored parameter...
    for key in device.param_list:
        # ...add 'output_' prefix to it
        new_key = f'output_{key}'
        # ...add parameter value to new parameter name key
        altered_parsed_data[new_key] = parsed_data[key] if key in parsed_data.keys() else None

    try:
        statuses[str(device.id)] = altered_parsed_data
        success = True
    finally:
        return success


def get_statuses():
    return statuses
