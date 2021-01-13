# phpipam-api

An incomplete phpIPAM API implementation in python.

```
import phpipam_api

ipam = phpipam_api.PhpipamAPI("https://phpipam.example.com/", "myapp", "apiuser", "p4s5word")
```

Usage:

```
data = ipam.<controller>.<operation>(<arguments>)
```

All functions return a dictionary object or a list of dictionary objects.
Refer to the [API Doc](https://phpipam.net/api-documentation/) for data layout.
If an error is encountered, an exception is raised.

## Controllers

Functions shared by all controllers:

* `get()` returns all obejcts in in controller
* `byID(object_id=<object id>)` get specific obejct by ID
* `create(data=<data>)`
* `edit(data=<data>)`
* `delete(object_id=<object id>)`

### sections

* `getSubnets(section_id=<section id>)`

### subnets

* `search(search=<query>)` search for subnet by CIDR
* `getIP(subnet_id=<subnet id>, ip=<ip>)` get address object from subnet by IP
* `getAddresses(subnet_id=<subnet id>)` get all addresses in subnet

### addresses

* `getByIP(subnet_id=<subnet id>, ip=<ip>)`
* `getByTag(tag_id=<tag id>)`
* `search(ip=<ip>)`
* `getFirstFree(subnet_id=<subnet id>)`
* `getTags()`
* `getTag(tag_id=<tag id>)`
* `createFirstFree(subnet_id=<subnet id>)`

### vlan

### l2domains

### vrf

### devices

* `getAddresses(device_id=<device id>)`
* `getSubnets(device_id=<device id>)`

### prefix


## requires

* `dateutil`
* `requests`

License: MIT
