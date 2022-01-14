#! /usr/bin/env python3

import json, sys, argparse
from os.path import isfile

# ******************************************************************************
parser = argparse.ArgumentParser(description='Reads config.json and writes out docker-environment files.')

parser.add_argument('file', nargs='?', help='optional input file, if omitted, read from stdin', default='-')
parser.add_argument('-v', '--verbose', action='store_true', help="be verbose")
args = parser.parse_args()
# ******************************************************************************


def load_config(file_name):
    if isfile(file_name):
        with open(file_name) as fh:
            return json.load(fh)
    elif file_name == '-':
        return json.loads(sys.stdin.read())
    else :
        return dict()


def get_value(value):
    if value.startswith("shared:"):
        return shared_vars.get(value[7:], value)
    else:
        return value


if __name__ == '__main__':
    config = load_config('static.json')

    # prevents script from trying to read interactively from tty, only "proper" pipe allowed
    if (args.file == '-' and sys.stdin.isatty()):
        print ("Won't read input from tty (please use -h for help)", file=sys.stderr)
        exit(1)
    else:
        filename = args.file

    for env_file, entry in load_config(filename).items():
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
