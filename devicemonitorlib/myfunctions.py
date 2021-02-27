import json


class DeviceMonitor:
    monitored_devices = []
    statuses = dict()

    def __init__(self, interval):
        self.interval = interval

    def update_statuses(self):
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

            self.statuses[str(device.id)] = altered_parsed_data
        return True

    def get_statuses(self):
        return self.statuses


class Device:
    def __init__(self, identifier, file_path):
        self.path = file_path
        self.id = identifier

    def data(self):
        with open(self.path) as f:
            return f.read()
