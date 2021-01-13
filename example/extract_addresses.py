#!/usr/bin/env python3
#
# example/extract_addresses.py
# (c) 2021 Jonas Gunz <himself@jonasgunz.de>
# License: MIT
#

import phpipam_api
import re

phpipam_url="https://phpipam.example.com/"
appid="appid"
user="apiuser"
passw="P45sw0rd"

tag='Used'
domain='sub.example.com.'
cidrs=['10.1.0.0/16','192.168.42.0/24']

ipam = phpipam.PhpipamAPI(phpipam_url, appid, user, passw)

tags = ipam.addresses.getTags()
for _tag in tags:
    if _tag['type'] == tag:
        tag_id=_tag['id']
if len(tag_id) == 0:
    raise Exception(f'tag "{tag}" was not found.')

print(f'tag "{tag}" has id {tag_id}')

selected_addresses = {}

for _cidr in cidrs:
    subnets = ipam.subnets.search(search=_cidr)

    if not len(subnets) == 1:
        print(f'CIDR {_cidr} has no or no exact match. Ignoring.')
        continue
    subnet = subnets[0]

    addresses = ipam.subnets.getAddresses(subnet_id=subnet['id'])
    for _address in addresses:
        hostname = _address['hostname']
        ip = _address['ip']

        if not _address['tag'] == tag_id:
            continue
        if not hostname.endswith(domain.strip('.')):
            continue

        if hostname in selected_addresses:
            selected_addresses[hostname].append(ip)
        else:
            selected_addresses[hostname]=[ip]

for _selected_address in selected_addresses:
    print(_selected_address + '::' + str(selected_addresses[_selected_address]))
