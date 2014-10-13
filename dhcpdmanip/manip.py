# coding=utf-8
import string


def add(parsed, name, mac, ip, desc):
    subnet = '.'.join(ip.split('.')[:3])
    mac = _normalize_mac(mac)
    try:
        if not _unique_mac(parsed, mac):
            raise ValueError('MAC already in DB')
        elif not _unique_ip(parsed[subnet], ip):
            raise ValueError('IP already in subnet')
        elif not _unique_name(parsed, name):
            raise ValueError('Name already in DB')
        else:
            parsed[subnet]['hosts'][mac] = {
                'name': name, 'ip': ip, 'desc': desc
            }
    except IndexError:
        raise ValueError('Wrong IP, no subnet found')


def _normalize_mac(mac):
    normm = []
    for l in mac:
        if l in string.hexdigits:
            normm.append(l.lower())
    if len(normm) != 12:
        raise ValueError('Invalid MAC address')

    return ':'.join([
        ''.join(normm[0:2]), ''.join(normm[2:4]), ''.join(normm[4:6]),
        ''.join(normm[6:8]), ''.join(normm[8:10]), ''.join(normm[10:12])
    ])


def _unique_name(parsed, name):
    for subnet in parsed.values():
        for h in subnet['hosts'].values():
            if h['name'] == name:
                return False
    return True


def _unique_mac(parsed, mac):
    for s in parsed.values():
        if mac in s['hosts']:
            return False
    return True


def _unique_ip(subnet, ip):
    for h in subnet['hosts'].values():
        if h['ip'] == ip:
            return False
    return True


def remove(parsed, mac):
    for sub in parsed.values():
        if mac in sub['hosts']:
            del(sub['hosts'][mac])
