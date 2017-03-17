#!/usr/bin/env python

from __future__ import absolute_import

import os
import logging

import salt.utils

__virtualname__ = 'mayopatch'


def __virtual__():
    if salt.utils.is_linux():
        return __virtualname__

    return (False, 'The mayo patch grain module cannot be loaded: only available on Linux systems.')


def get_schedule():
    ret = {}
    retdata = {}
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
                ret['mayo-deployday'] = stat[1]
            if stat[0] == 'patch_time':
                ret['mayo-deploytime'] = stat[1]
            if stat[0] == 'patch_week':
                ret['mayo-deployweek'] = stat[1]
            if stat[0] == 'server_purpose':
                ret['mayo-purpose'] = stat[1]
            if stat[0] == 'special_instructions':
                ret['mayo-special'] = stat[1]
            if stat[0] == 'system_contact':
                ret['mayo-contact'] = stat[1]
    return ret
