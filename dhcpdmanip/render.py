# coding=utf-8


def _render_subnet(subn):
    r = ''.join(subn[0])

    for mac, hinfo in sorted(subn[1].items(), key=lambda i: i[1]['name']):
        r += _render_host(hinfo['name'], mac, hinfo['ip'])

    return r + '}\n'


def _render_host(name, mac, ip):
    return '\n'.join([
        '\thost %s {' % name,
        '\t\thardware ethernet %s;' % mac,
        '\t\tfixed-address %s;' % ip,
        '\t}\n'])


def render(parsed):
    r = '\n'.join(parsed[0])
    for subn in parsed[1]:
        r += _render_subnet(subn)
    return r
