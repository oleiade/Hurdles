# -*- coding: utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

# Unix-like system compliant only

from __future__ import absolute_import

from .procinfo import get_procinfo


def cpu():
    """Returns system cpu info"""
    procinfo = get_procinfo()
    cpu_type = procinfo['cpuinfo']['model name']
    cpu_cores = procinfo['cpuinfo']['processor']

    return (cpu_type, cpu_cores)


def memory():
    """Returns total system memory amount in MB"""
    return (get_procinfo()['meminfo']['MemTotal'] * 1024, )
