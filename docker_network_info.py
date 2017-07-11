#!/usr/bin/env python3.5
import json
import subprocess

process = subprocess.Popen(["/usr/bin/docker","ps","-q","-a"],stdout=subprocess.PIPE)
out,err = process.communicate()

ids = [ _id for _id in out.decode().split('\n') if _id ]

data = dict()

for _id in ids:
    process = subprocess.Popen(["/usr/bin/docker","inspect","{}".format(_id)],stdout=subprocess.PIPE)
    out,err = process.communicate()
    data[_id] = json.loads(out.decode())

def print_table(name,id_,network,gateway,ip_address,network_id,endpoint_id,header=False):
        if header: print("-"*238)
        print("| {} | {} | {} | {} | {} | {} | {} |".format(name.ljust(20,' '),id_.ljust(14,' '),network.ljust(24,' '),gateway.ljust(15,' '),ip_address.ljust(15,' '),network_id.ljust(64,' '),endpoint_id.ljust(64,' ')))
        if header: print("-"*238)

#'IPAMConfig', 'IPv6Gateway', 'GlobalIPv6PrefixLen', 'IPAddress', 'GlobalIPv6Address', 'NetworkID', 'Links', 'EndpointID', 'Gateway', 'IPPrefixLen', 'Aliases', 'MacAddress'

print_table("Alias","Container Id","Network Name","Gateway","IP Address","Network ID","Endpoint ID",header=True)
count = 0
last = False
for key in sorted(data.keys()):
    count += 1
    network, values = data[key][0]["NetworkSettings"]["Networks"].popitem()
    for i in values['Aliases']:
        try:
            int(i,16)
            id = i
        except ValueError:
            name = i
    print_table(name,id,network,values['Gateway'],values['IPAddress'],values['NetworkID'],values['EndpointID'])
print('-'*238)