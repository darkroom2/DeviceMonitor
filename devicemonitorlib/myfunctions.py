import json
import sched


class DeviceMonitor:
    def __init__(self, interval):
        self.interval = interval
        self.monitored_devices = []
        self.statuses = dict()

        self.s = sched.scheduler()

    def start(self):
        self.update_statuses()
        self.s.run()

    def update_statuses(self):
        self.s.enter(self.interval, 0, self.update_statuses)

        success = False

        # For every device in path...
        for device in self.monitored_devices:
            # ...parse device parameters
            parsed_data = json.loads(device.data())
            # ...make new dict with alter key names
            altered_parsed_data = dict()
            # ...for every parameter...
            for key in parsed_data:
                # ......add 'output_' prefix to parameter
                new_key = f'output_{key}'
                # ......add parameter value to new parameter name key
                altered_parsed_data[new_key] = parsed_data[key]

            # TODO: LOCK HERE and set success = True
            self.statuses[str(device.id)] = altered_parsed_data
            success = True

        print(self.statuses)
        return success

    def get_statuses(self):
        return self.statuses


class Device:
    def __init__(self, identifier, file_path):
        self.path = file_path
        self.id = identifier

    def data(self):
        with open(self.path) as f:
            return f.read()
