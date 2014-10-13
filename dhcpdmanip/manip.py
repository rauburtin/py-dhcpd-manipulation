# coding=utf-8
import re


def add(parsed, name, mac, ip, desc):
    searched = 'subnet %s.0' % '.'.join(ip.split('.')[:3])
    for subnetinfo, hosts in parsed:
        if re.search(searched, subnetinfo[0]):
            hosts[mac] = {'name': name, 'ip': ip, 'desc': desc}
            return
    raise ValueError('Wrong IP, no subnet found')


def remove(parsed, mac):
    for sub in parsed:
        if mac in sub[1]:
            del(sub[1][mac])
