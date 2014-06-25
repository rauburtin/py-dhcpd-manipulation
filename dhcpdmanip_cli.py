# coding=utf-8
'''
Created on Jun 2, 2014

CLI for dhcpdtools
'''
import sys
import logging
from optparse import OptionParser
import dhcpdmanip

usage = '''\
python %prog [action] [options]

mac - mac 12 hexadigits
ip - x.x.x.x
name - hostnames
'''

if __name__ == '__main__':
    parser = OptionParser(usage=usage)

    parser.add_option('-m', '--mac', action='store', dest='mac',
                      help='mac address',)
    parser.add_option('-i', '--ip', action='store', dest='ip',
                      help='IP address',)
    parser.add_option('-H', '--host', action='store', dest='name',
                      help='host name',)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error('wrong number of arguments')

    logging.basicConfig(level=logging.INFO)

    action = args
    manipulator = dhcpdmanip.Manipulator()

    if action == 'add':
        manipulator.add(options.name, options.mac, options.ip)
        manipulator.render()
    elif action == 'add':
        manipulator.remove(options.mac)
        manipulator.render()
    elif action == 'getleases':
        sys.stdout.write(manipulator.get_leases())
    elif action == 'getreserved':
        sys.stdout.write(manipulator.get_reserved())
    else:
        parser.error('Bad action')
