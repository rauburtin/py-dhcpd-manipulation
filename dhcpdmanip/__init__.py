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
        rv = {}
        for r in self._parsed[1]:
            rv.update(r[1])
        return rv

    def get_leases(self):
        if not hasattr(self, '_leases'):
            with open(self._leases_file) as f:
                self._leases = LeaseInfo.parse(f)
        return self._leases

    def add(self, name, mac, ip, desc):
        manip.add(self._parsed[1], name, mac, ip, desc)

    def remove(self, mac):
        manip.remove(self._parsed[1], mac)

    def render(self, outstream=None):
        close = None
        if not outstream:
            outstream = open(self._dhcpd_conf_file, 'w')
            close = True

        for l in self._parsed[0]:
            outstream.write(l)

        for subn in self._parsed[1]:
            self._render_subnet(subn, outstream)

        if close:
            outstream.close()

    def _render_subnet(self, subn, outstream):
        for l in subn[0]:
            outstream.write(l)

        for mac, hinfo in sorted(subn[1].items(), key=lambda i: i[1]['name']):
            self._render_host(hinfo['name'],
                              mac, hinfo['ip'],
                              hinfo['desc'],
                              outstream)

        outstream.write('}\n')

    def _render_host(self, name, mac, ip, desc, outstream):
        sep = '  '
        dsep = sep + sep
        outstream.write('\n'.join([
            '%shost %s {' % (sep, name),
            '%shardware ethernet %s;' % (dsep, mac),
            '%sfixed-address %s;' % (dsep, ip),
            '%sddns-hostname "%s";' % (dsep, name),
            '%s#%s' % (dsep, desc.replace('\n', '\\n')),
            '%s}\n' % sep]))
