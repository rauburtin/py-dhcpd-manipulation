# coding=utf-8

import re

from . import manip

subnet_re = re.compile('subnet (\d{1,3}\.\d{1,3}\.\d{1,3})\.\d{1,3}')
host_re = re.compile('host ([^ ]{1,}) {')
end_re = re.compile('}\n')


def parse(i_stream):
    globalinfo, subs, curr_subnet, curr_host = [], {}, None, None
    hosts, subninfo = [], []

    for line in i_stream:

        if not curr_subnet:
            # not yet within subnet part
            found = subnet_re.search(line)
            if found:
                curr_subnet = found.group(1)
                subninfo.append(line)
            else:
                globalinfo.append(line)
        else:
            # already in subnet part
            end_found = end_re.search(line)
            if end_found and curr_host:
                hosts.append(curr_host)
                curr_host = None
            elif end_found and not curr_host:
                subs[curr_subnet] = {
                    'rawhosts': hosts, 'info': subninfo, 'hosts': {}
                }
                curr_subnet = None
                hosts, subninfo = [], []
            elif not curr_host:
                host = host_re.search(line)
                if host:
                    curr_host = [host.group(1)]
                else:
                    subninfo.append(line)
            else:
                curr_host.append(line)

    for s in subs.values():
        _postprocess_subnet(subs, s)

    return globalinfo, subs


_mac = '([0-9A-Fa-f]{2}[:-]?){5}([0-9A-Fa-f]{2})'
mac_re = re.compile('hardware ethernet (%s);' % _mac)
ip_re = re.compile('fixed-address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3});')


def get_host(rawhost):
    info = {'name': rawhost[0], 'desc': ''}

    for l in rawhost[1:]:
        found = ip_re.search(l)
        if found:
            info['ip'] = found.group(1)
        elif mac_re.search(l):
            info['mac'] = mac_re.search(l).group(1)
        elif l.lstrip().startswith('#'):
            info['desc'] += l.lstrip().lstrip('#').rstrip()

    return info


def _postprocess_subnet(parsed, rawsub):
    for h in rawsub['rawhosts']:
        info = get_host(h)
        manip.add(parsed, info['name'], info['mac'], info['ip'], info['desc'])

    del(rawsub['rawhosts'])
