import json

def get_data_from_config(data, config_file='config.json'):
    """
    Reads the city name from a configuration file.
    :param config_file: The path to the configuration.json file
    :return: The city name read from the file.
    """
    with open(config_file, 'r') as file:
        config_dict = json.load(file)
        return config_dict[data]