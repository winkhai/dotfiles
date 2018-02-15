#!/usr/bin/env python3

import json
import os
import sys
import time

from wrappers import digitalocean


# TODO 1: Write a module for AWS Lightsail.
# TODO 2: Write an error handler.

def spin_up():
    timestamp_utc = time.time()
    writeout_file = 'logs/build-{timestamp_utc}.json'.format(timestamp_utc=timestamp_utc)
    aws_lightsail = ['awsl', 'aws lightsail']
    digital_ocean = ['do', 'digital ocean']
    iaas_platform = aws_lightsail + digital_ocean
    # vendor_choice = input('vendor_choice: ') # FIXME Parameter hard-coded to expedite testing.
    vendor_choice = 'do'                       # FIXME Parameter hard-coded to expedite testing.
    if vendor_choice in iaas_platform:
        if vendor_choice in aws_lightsail:
            pass # TODO 1
        elif vendor_choice in digital_ocean:
            os.system('{unix_command} > {writeout_file}'             \
                        .format(unix_command=digitalocean.builder(), \
                                writeout_file=writeout_file))
            time.sleep(60)
            return harden(writeout_file)
    else:
        pass # TODO 2

def harden(writeout_file):
    response = json.load(open(writeout_file))
    payloads = []
    if 'droplets' in response:
        payloads = response['droplets']
    else:
        payloads = [response['droplet']]
    ip_addresses = []
    for payload in payloads:
        ip_addresses.append(digitalocean.get_host(payload['id'], writeout_file))
    for ip_address in ip_addresses:
        os.system('ssh -o "StrictHostKeyChecking no" root@{remote_computer} \'bash -s\' < procedures/remote0.sh'.format(remote_computer=ip_address))
        os.system('scp /Users/khaingwin/.ssh/id_rsa.pub root@{remote_computer}:/etc/ssh/new_user/authorized_keys'.format(remote_computer=ip_address))
        os.system('sh -c \'echo "new_user:swordfish" > /Users/khaingwin/byte_aces/dotfiles/setup/.credentials\'')
        os.system('scp /Users/khaingwin/byte_aces/dotfiles/setup/.credentials root@{remote_computer}:/home/new_user/'.format(remote_computer=ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{remote_computer} \'bash -s\' < procedures/remote1.sh'.format(remote_computer=ip_address))
    os.system('rm /Users/khaingwin/byte_aces/dotfiles/setup/.credentials')
    return ip_addresses

if __name__ == '__main__':
    from pprint import pprint
    pprint(spin_up())