# coding=utf-8


def add(parsed, name, mac, ip):
    parsed[0][1][mac] = {'name': name, 'ip': ip}


def remove(parsed, mac):
    for sub in parsed:
        if mac in sub[1]:
            del(sub[1][mac])
