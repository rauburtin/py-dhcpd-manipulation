# coding=utf-8
import os
import LeaseInfo

from .parser import parse as _dhcp_parse
from . import manip


class Manipulator(object):
    _dhcpd_conf_file = os.environ.get('DHCPD_CONF_FILE', 'dhcpd.conf')
    _leases_file = os.environ.get('DHCPD_LEASES_FILE', 'dhcpd.leases')

    def __init__(self):
        with open(self._dhcpd_conf_file) as f:
            self._parsed = _dhcp_parse(f)

    def get_reserved(self):
        return self._parsed

    def get_leases(self):
        if not hasattr(self, '_leases'):
            with open(self._leases_file) as f:
                self._leases = LeaseInfo.parse(f)
        return self._leases

    def add(self, name, mac, ip):
        manip.add(self._parsed, name, mac, ip)

    def remove(self, mac):
        manip.remove(self._parsed, mac)
