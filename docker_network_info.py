#!/usr/bin/env python3.5
import json
import subprocess


def print_table(name, id_, network, gateway, ip_address, network_id, endpoint_id, header=False):
    if header: print("-" * 238)
    print("| {} | {} | {} | {} | {} | {} | {} |".format(name.ljust(20, ' '), id_.ljust(14, ' '), network.ljust(24, ' '),
                                                        gateway.ljust(15, ' '), ip_address.ljust(15, ' '),
                                                        network_id.ljust(64, ' '), endpoint_id.ljust(64, ' ')))
    if header: print("-" * 238)


def get_container_ids():
    process = subprocess.Popen(["/usr/bin/docker", "ps", "-q", "-a"], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return [id for id in out.decode().split('\n') if id]


def get_data(container_ids):
    data = dict()
    for _id in container_ids:
        process = subprocess.Popen(["/usr/bin/docker", "inspect", "{}".format(_id)], stdout=subprocess.PIPE)
        out, err = process.communicate()
        data[_id] = json.loads(out.decode())
    return data


if __name__ == '__main__':
    """
    'IPAMConfig', 'IPv6Gateway', 'GlobalIPv6PrefixLen', 'IPAddress', 'GlobalIPv6Address', 'NetworkID', 'Links', 'EndpointID', 'Gateway', 'IPPrefixLen', 'Aliases', 'MacAddress'
    """
    data = get_data(get_container_ids())
    if len(data.keys()) > 0:
        print_table("Alias", "Container Id", "Network Name", "Gateway", "IP Address", "Network ID", "Endpoint ID",
                    header=True)
        count = 0
        for key in sorted(data.keys()):
            count += 1
            network, values = data[key][0]["NetworkSettings"]["Networks"].popitem()
            for i in values['Aliases']:
                try:
                    int(i, 16)
                    id = i
                except ValueError:
                    name = i
            print_table(name, id, network, values['Gateway'], values['IPAddress'], values['NetworkID'],
                        values['EndpointID'])
        print('-' * 238)
        print("{} Containers running".format(count))
