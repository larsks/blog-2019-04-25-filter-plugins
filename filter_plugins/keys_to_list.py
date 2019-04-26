#!/usr/bin/python


def filter_keys_to_list(v):
    key_list = []
    key = {}
    found_start = False

    # iterate over lines of output from keytool
    for line in v.splitlines():
        # Discard any lines that don't look like "key: value" lines
        if ': ' not in line:
            continue

        # Look for "Alias name" at the beginning of a line to identify
        # the start of a new key.
        if line.startswith('Alias name'):
            found_start = True

            # If we have already collected data on a key, append that to
            # the list of keys.
            if key:
                key_list.append(key)
                key = {}

        # Read the next line if we haven't found the start of a key
        # yet.
        if not found_start:
            continue

        # Split fields and values into dictionary items.
        field, value = line.split(': ', 1)
        if field in ['Alias name', 'Owner', 'Issuer', 'Creation date']:
            key[field] = value
        elif field == 'Valid from':
            key['Valid from'], key['Valid until'] = value.split(' until: ')

    # Append the final key.
    if key:
        key_list.append(key)

    return key_list


class FilterModule(object):
    filter_map = {
        'keys_to_list': filter_keys_to_list,
    }

    def filters(self):
        return self.filter_map
