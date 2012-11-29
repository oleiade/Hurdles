# -*- coding: utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

# Unix-like system compliant only

procinfo_files = {
    'cpuinfo': '/proc/cpuinfo',
    'meminfo': '/proc/meminfo',
}


def extract_procinfo(path):
    datas = {}
    f = open(path, 'r')
    lines = f.readlines()

    for line in lines:
        try:
            key, value = line.split(':')
        except ValueError:
            continue
        datas[key.strip()] = value.strip()

    return datas


def get_procinfo():
    procinfo = {}

    for name, path in procinfo_files.iteritems():
        procinfo[name] = extract_procinfo(path)

    return procinfo
