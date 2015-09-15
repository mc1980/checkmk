#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2015             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# Copyright by Mathias Kettner and Mathias Kettner GmbH.  All rights reserved.
#
# Check_MK is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.
#
# Check_MK is  distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY;  without even the implied warranty of
# MERCHANTABILITY  or  FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have  received  a copy of the  GNU  General Public
# License along with Check_MK.  If  not, email to mk@mathias-kettner.de
# or write to the postal address provided at www.mathias-kettner.de

# Send notifications remote to mkeventd
# Including Service Level

mkevent_host = ''
mkevent_port = 514
application  = "notify"

import time, socket, os
host = os.environ['NOTIFY_HOSTNAME'] 
#0       Emergency
#1       Alert
#2       Critical
#3       Error
#4       Warning
#5       Notice
#6       Informational
#7       Debug

def state_to_prio(state):
    state = int(state)
    if state == 0:
        return 5 
    elif state == 1:
        return 4
    elif state == 2:
        return 2
    elif state == 3:
        return 7


if os.environ['NOTIFY_WHAT'] == 'SERVICE':
    sl = os.environ.get('NOTIFY_SVC_SL', 0)
    prio = state_to_prio(os.environ['NOTIFY_SERVICESTATEID'])
    message = "%s|%s|%s" % \
    ( sl, os.environ['NOTIFY_SERVICEDESC'], os.environ['NOTIFY_SERVICEOUTPUT'] )
else:
    sl = os.environ.get('NOTIFY_HOST_SL', 0)
    prio = state_to_prio(os.environ['NOTIFY_HOSTSTATEID'])
    message = "%s|HOSTSTATE|%s" % (sl,  os.environ['NOTIFY_HOSTOUTPUT'] ) 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((mkevent_host, mkevent_port))

timestamp = time.strftime("%b %d %H:%M:%S", time.localtime(time.time()))
sock.send("<%s>%s %s %s: %s\n" % (prio, timestamp, host, application,  message))
sock.close()
