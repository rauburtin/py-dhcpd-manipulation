#!/usr/bin/env python
# coding=utf-8
'''
Created on Jun 2, 2014

CLI for dhcpdtools
'''
import sys
import logging
import json
from optparse import OptionParser
import dhcpdmanip
import os

usage = '''\
python %prog [action] [options]

action: add, remove, getleases, getreserved
'''

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-m', '--mac', action='store', dest='mac',
                      help='mac address (12 hexadigits)',)
    parser.add_option('-i', '--ip', action='store', dest='ip',
                      help='IP address (x.x.x.x)',)
    parser.add_option('-H', '--host', action='store', dest='name',
                      help='host name',)
    parser.add_option('-d', '--desc', action='store', dest='desc',
                      help='host description',)
    parser.set_usage(usage + parser.format_option_help())

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error('wrong argument count. Action required.')

    logging.basicConfig(level=logging.INFO)

    action = args[0]
    manipulator = dhcpdmanip.Manipulator()

    def _render():
        tmp = 'dhcpd.conf.render'
        with open(tmp, 'w') as f:
            manipulator.render(f)
        os.rename(tmp, manipulator._dhcpd_conf_file)

    try:
        if action == 'add':
            desc = getattr(options, 'desc', None)
            manipulator.add(options.name, options.mac, options.ip, desc)
            _render()
        elif action == 'remove':
            manipulator.remove(options.mac)
            _render()
        elif action == 'getleases':
            json.dump(manipulator.get_leases(), sys.stdout, indent=2)
        elif action == 'getreserved':
            json.dump(manipulator.get_reserved(), sys.stdout, indent=2)
        else:
            parser.error('Bad action')
    except ValueError, e:
        sys.stderr.write(e.message)
        sys.exit(-1)
