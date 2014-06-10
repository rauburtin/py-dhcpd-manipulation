# coding=utf-8

import re

subnet_re = re.compile('subnet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
host_re = re.compile('host ([^ ]{1,}) {')
end_re = re.compile('}\n')


def parse(i_stream):
    prefix, subs, curr_subnet, curr_host = [], [], None, None

    for line in i_stream:

        if not curr_subnet:
            # not yet within subnet part
            if subnet_re.search(line):
                curr_subnet = ([line], [])
            else:
                prefix.append(line)
        else:
            # already in subnet part
            end_found = end_re.search(line)
            if end_found and curr_host:
                curr_subnet[1].append(curr_host)
                curr_host = None
            elif end_found and not curr_host:
                subs.append(curr_subnet)
                curr_subnet = None
            elif not curr_host:
                host = host_re.search(line)
                if host:
                    curr_host = [host.group(1)]
                else:
                    curr_subnet[0].append(line)
            else:
                curr_host.append(line)

    postprocessed = []
    for s in subs:
        postprocessed.append(_postprocess_subnet(s))

    return prefix, postprocessed


_mac = '([0-9A-Fa-f]{2}[:-]?){5}([0-9A-Fa-f]{2})'
mac_re = re.compile('hardware ethernet (%s);' % _mac)
ip_re = re.compile('fixed-address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3});')


def get_host(rawhost):
    info = {'name': rawhost[0]}

    for l in rawhost[1:]:
        found = ip_re.search(l)
        if found:
            info['ip'] = found.group(1)
        else:
            found = mac_re.search(l)
            if found:
                info['mac'] = found.group(1)

    return info


def _postprocess_subnet(rawsub):
    hosts = {}
    for h in rawsub[1]:
        info = get_host(h)
        hosts[info.pop('mac')] = info

    return rawsub[0], hosts
