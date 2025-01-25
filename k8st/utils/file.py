import os
import json
import time
from ..constants import Constants
import tempfile

class FileUtils:
    @staticmethod
    def get_temp_file_path(filename):
        return os.path.join(tempfile.gettempdir(), filename)

    @staticmethod
    def read_from_file(filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file)
                if 'timestamp' in data and time.time() - data['timestamp'] < Constants.ONE_DAY:  # 24 hours = 86400 seconds
                    return data['content']
        return None

    @staticmethod
    def write_to_file(filepath, data):
        with open(filepath, 'w') as file:
            json.dump({'timestamp': time.time(), 'content': data}, file)

    @staticmethod
    def write_config_file(filepath, data):
        with open(filepath, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def read_config_file(filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return json.load(file)
        return None