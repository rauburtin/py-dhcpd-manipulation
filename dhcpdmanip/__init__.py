# coding=utf-8
import os
import LeaseInfo

from .parser import parse as _dhcp_parse
from . import manip


class Manipulator(object):
    _dhcpd_conf_file = os.environ.get('DHCPD_CONF_FILE', 'dhcpd.conf')
    _leases_file = os.environ.get('DHCPD_LEASES_FILE', 'dhcpd.leases')
    _range_min = int(os.environ.get('DHCPD_RANGEBEGIN', 10))
    _range_max = int(os.environ.get('DHCPD_RANGEEND', 254))

    def __init__(self):
        with open(self._dhcpd_conf_file) as f:
            self._parsed = _dhcp_parse(f)

    def get_reserved(self):
        rv = {}
        for r in self._parsed[1].values():
            rv.update(r['hosts'])
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

        for subn, subinfo in self._parsed[1].items():
            self._render_subnet(subn, subinfo, outstream)

        if close:
            outstream.close()

    def _render_range(self, subn, hosts, outstream):
        ranges = []
        curr_begin = self._range_min
        ips = [int(h['ip'].split('.')[-1]) for h in hosts.values()]
        for i in sorted(ips):
            if i < self._range_min:
                continue
            elif i > self._range_max:
                continue
            elif curr_begin == i:
                curr_begin += 1
            else:
                ranges.append((curr_begin, i - 1))
                curr_begin = i + 1
        if curr_begin < self._range_max:
            ranges.append((curr_begin, self._range_max))
        #range 192.168.1.10 192.168.1.200;
        for beg, end in ranges:
            outstream.write('  range %s.%s %s.%s;\n' % (subn, beg, subn, end))

    def _render_subnet(self, subn, subinfo, outstream):
        outstream.write(subinfo['info'][0])
        self._render_range(subn, subinfo['hosts'], outstream)
        for l in subinfo['info'][1:]:
            if not l.lstrip().startswith('range'):
                outstream.write(l)

        sortedh = sorted(subinfo['hosts'].items(), key=lambda i: i[1]['name'])
        for mac, hinfo in sortedh:
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
