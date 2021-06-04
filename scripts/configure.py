import json

with open('config.json') as fh:
  config = json.load(fh)
shared_vars = config.pop('shared', dict())

def get_value(value):
  if value.startswith("shared:"):
    return shared_vars.get(value[7:], value)
  else:
    return value

for env_file, entry in config.items():
  with open(env_file, 'w') as fh:
    lines = [ "{}={}\n".format(key, get_value(val)) for key, val in entry.items()]
    print("### Writing {}...". format(env_file))
    fh.writelines(lines)