import json
import os
def get_data_from_config(data):
    """
    Reads the city name from a configuration file.
    :param data: The data that you want to read from the config.json file
    :return: The city name read from the file.
    """
    # Get abs path for config.json
    config_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'config.json'
    )
    with open(config_file, 'r') as file:
        config_dict = json.load(file)
        return config_dict[data]