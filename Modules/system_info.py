#!/usr/bin/env python3

# Libraries
##############################################################################
import platform
import psutil
import socket

from .helper_funcs import convert_size
##############################################################################


# Functions
##############################################################################
def get_system_info():
    # Basic system information
    system_info = {
        "os": {
            "system": platform.system(),
            "kernel": platform.release(),
            "distro": platform.freedesktop_os_release()['NAME'],
            "version": platform.freedesktop_os_release()['VERSION'],
        },
        "domain": {
            "domain": socket.getfqdn(),
            "dns_hostname": socket.gethostname(),
        },
    }

    # CPU information
    cpu_info = {
        "cpu": platform.processor(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
    }
    system_info["cpu"] = cpu_info

    # Memory information
    virtual_memory = psutil.virtual_memory()
    memory_info = {
        "total_memory": convert_size(virtual_memory.total),
        "available_memory": convert_size(virtual_memory.available),
        "memory_percent": virtual_memory.percent,
    }
    system_info["memory"] = memory_info

    # Disk information (excluding /dev/loop devices)
    disk_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if not partition.device.startswith('/dev/loop'):
            partition_info = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.device] = {
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'filesystem': partition.fstype,
                'total_size': convert_size(partition_info.total)
            }
    system_info["disks"] = disk_info

    # Network interfaces information (including MAC addresses)
    network_info = {}
    network_interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in network_interfaces.items():
        network_info[interface_name] = { 
            'mac_address': ''
        }

        for address in interface_addresses:
            if address.family == psutil.AF_LINK:  
                # AF_LINK represents MAC address
                network_info[interface_name]['mac_address'] = address.address
            elif address.family == socket.AF_INET:
                # IP v4
                network_info[interface_name]['IPv4'] ={
                    'address': address.address,
                    'netmask': address.netmask,
                    'broadcast': address.broadcast
                }
            elif address.family == socket.AF_INET6:
                # IP v6
                network_info[interface_name]['IPv6'] ={
                    'address': address.address,
                    'netmask': address.netmask,
                    'broadcast': None
                }
    system_info["network_interfaces"] = network_info

    return system_info
##############################################################################