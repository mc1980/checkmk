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

manpage_catalog_titles = {
    "hw"       : "Appliances, other dedicated Hardware",
        "environment" : "Environmental sensors",
            "akcp"         : "AKCP",
            "allnet"       : "ALLNET",
            "bachmann"     : "Bachmann",
            "betternet"    : "better networks",
            "carel"        : "CAREL",
            "climaveneta"  : "Climaveneta",
            "eaton"        : "Eaton",
            "emerson"      : "EMERSON",
            "hwg"          : "HW group",
            "kentix"       : "Kentix",
            "knuerr"       : "Knuerr",
            "rittal"       : "Rittal",
            "sensatronics" : "Sensatronics",
            "socomec"      : "Socomec",
            "stulz"        : "STULZ",
            "wagner"       : "WAGNER Group",
            "wut"          : "Wiesemann & Theis",
        "other"       : "Other devices",
        "time"        : "Clock Devices",
            "meinberg"   : "Meinberg",
        "network"     : "Networking (Switches, Routers, etc.)",
            "aerohive"    : "Aerohive Networking",
            "adva"        : "ADVA Optical Networking",
            "alcatel"     : "Alcatel",
            "arris"       : "ARRIS",
            "avm"         : "AVM",
            "bintec"      : "Bintec",
            "bluecat"     : "BlueCat Networks",
            "bluecoat"    : "Blue Coat Systems",
            "casa"        : "Casa",
            "cbl"         : "Communication by light (CBL)",
            "checkpoint"  : "Checkpoint",
            "cisco"       : "Cisco Systems (also IronPort)",
            "decru"       : "Decru",
            "dell"        : "DELL",
            "enterasys"   : "Enterasys Networks",
            "f5"          : "F5 Networks",
            "fortinet"    : "Fortinet",
            "genua"       : "genua",
            "h3c"         : "H3C Technologies (also 3Com)",
            "hp"          : "Hewlett-Packard (HP)",
            "ibm"         : "IBM",
            "innovaphone" : "Innovaphone",
            "juniper"     : "Juniper Networks",
            "kemp"        : "KEMP",
            "lancom"      : "LANCOM Systems GmbH",
            "mikrotik"    : "MikroTik",
            "netgear"     : "Netgear",
            "qnap"        : "QNAP Systems",
            "riverbed"    : "Riverbed Technology",
            "symantec"    : "Symantec",
            "tplink"      : "TP-LINK",
            "viprinet"    : "Viprinet",
        "power"       : "Power supplies and PDUs",
            "apc"        : "APC",
            "gude"       : "Gude",
        "printer"     : "Printers",
        "server"      : "Server hardware, blade enclosures",
            "ibm"        : "IBM",
        "storagehw"   : "Storage (filers, SAN, tape libs)",
            "brocade"    : "Brocade",
            "fastlta"    : "FAST LTA",
            "fujitsu"    : "Fujitsu",
            "mcdata"     : "McDATA",
            "netapp"     : "NetApp",
            "hitachi"    : "Hitachi",
            "emc"        : "EMC",
            "qlogic"     : "QLogic",
            "quantum"    : "Quantum",
        "phone"       : "Telephony",

    "app"      : "Applications",
        "ad"            : "Active Directory",
        "apache"        : "Apache Webserver",
        "activemq"      : "Apache ActiveMQ",
        "db2"           : "IBM DB2",
        "citrix"        : "Citrix",
        "netscaler"     : "Citrix Netscaler",
        "exchange"      : "Microsoft Exchange",
        "haproxy"       : "HAProxy Loadbalancer",
        "java"          : "Java (Tomcat, Weblogic, JBoss, etc.)",
        "libelle"       : "Libelle Business Shadow",
        "lotusnotes"    : "IBM Lotus Domino",
        "mailman"       : "Mailman",
        "mssql"         : "Microsoft SQL Server",
        "mysql"         : "MySQL",
        "omd"           : "Open Monitoring Distribution (OMD)",
        "check_mk"      : "Check_MK Monitoring System",
        "oracle"        : "ORACLE Database",
        "plesk"         : "Plesk",
        "postfix"       : "Postfix",
        "postgresql"    : "PostgreSQL",
        "qmail"         : "qmail",
        "ruckus"        : "Ruckus Spot",
        "sap"           : "SAP R/3",
        "tsm"           : "IBM Tivoli Storage Manager (TSM)",
        "unitrends"     : "Unitrends",
        "sansymphony"   : "Datacore SANsymphony",

    "os"       : "Operating Systems",
        "aix"           : "AIX",
        "freebsd"       : "FreeBSD",
        "hpux"          : "HP-UX",
        "linux"         : "Linux",
        "macosx"        : "Mac OS X",
        "netbsd"        : "NetBSD",
        "openbsd"       : "OpenBSD",
        "openvms"       : "OpenVMS",
        "snmp"          : "SNMP",
        "solaris"       : "Solaris",
        "vsphere"       : "VMWare ESX (via vSphere)",
        "windows"       : "Microsoft Windows",
        "z_os"          : "IBM zOS Mainframes",

        "hardware"    : "Hardware Sensors",
        "kernel"      : "CPU, Memory and Kernel Performance",
        "ps"          : "Processes, Services and Jobs",
        "files"       : "Files and Logfiles",
        "services"    : "Specific Daemons and Operating System Services",
        "networking"  : "Networking",
        "misc"        : "Miscellaneous",
        "storage"     : "Filesystems, Disks and RAID",

    "agentless" : "Networking checks without agent",
    "generic"  : "Generic check plugins",
    "unsorted" : "Uncategorized",
}
