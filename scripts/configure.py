import json
from os.path import isfile

def load_config(file_name):
    if isfile(file_name):
        with open(file_name) as fh:
            return json.load(fh)
    else:
        return dict()


def get_value(value):
    if value.startswith("shared:"):
        return shared_vars.get(value[7:], value)
    else:
        return value


if __name__ == '__main__':
    config = load_config('static.json')

    for env_file, entry in load_config('config.json').items():
        if env_file in config:
            config[env_file].update(entry)
        else:
            config[env_file] = entry

    shared_vars = config.pop('shared', dict())
    for env_file, entry in config.items():
        with open(env_file, 'w') as fh:
            lines = [ "{}={}\n".format(key, get_value(val)) for key, val in entry.items()]
            print("### Writing {}...". format(env_file))
            fh.writelines(lines)
