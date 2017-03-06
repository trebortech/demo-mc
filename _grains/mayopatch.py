#!/usr/bin/env python

from __future__ import absolute_import

import os
import logging

__virtualname__ = 'mayopatch'


def __virtual__():
    if __grains__['kernel'] == 'Linux':
        return __virtualname__
    return (False, 'The mayo patch grain could not be loaded')


def get_schedule():
    ret = {}
    files = []

    dirname = "/etc/dcis_maintenance"
    if os.path.exists(dirname):
        for f in os.listdir(dirname):
            if os.path.isfile(os.path.join(dirname, f)):
                files.append(f)

    if files:
        for file in files:
            stat = file.split(":")

            if stat[0] == 'patch_day':
                ret['deployday'] = stat[1]
            if stat[0] == 'patch_time':
                ret['deploytime'] = stat[1]
            if stat[0] == 'patch_week':
                ret['deployweek'] = stat[1]
            if stat[0] == 'server_purpose':
                ret['purpose'] = stat[1]
            if stat[0] == 'special_instructions':
                ret['special'] = stat[1]
            if stat[0] == 'system_contact':
                ret['contact'] = stat[1]
    return ret
