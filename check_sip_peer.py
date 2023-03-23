#!/usr/bin/python3
# GPL v3+ arekm@pld

import argparse
import re
import sarge
import sys

NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2
NAGIOS_UNKNOWN = 3

STATUS_MAP = {NAGIOS_CRITICAL: 'CRITICAL', NAGIOS_WARNING: 'WARNING', NAGIOS_OK: 'OK',  NAGIOS_UNKNOWN: 'UNKNOWN'}

nagios_status = NAGIOS_OK

try:
    parser = argparse.ArgumentParser(description='Check SIP peer status in Asterisk')
    parser.add_argument('--peer', action='store', dest='peer', help='SIP peer name', required=True)
    parser.add_argument('--socket', action='store', dest='socket', help='Asterisk socket path', default=" /var/run/asterisk/asterisk.ctl")
    args = parser.parse_args()
except Exception as e:
    nagios_status = NAGIOS_UNKNOWN
    print("{status}: {msg}".format(status=STATUS_MAP[nagios_status], msg=e))
    sys.exit(nagios_status)

try:
    cmd = '/usr/sbin/asterisk -r -s {socket} -x "sip show peer {peer}"'.format(socket=args.socket, peer=args.peer)
    c = sarge.capture_both(cmd)
    if c.returncode != 0:
        nagios_status = NAGIOS_CRITICAL
        print("{status}: peer={peer}, {msg}".format(status=STATUS_MAP[nagios_status], peer=args.peer,
            msg=c.stdout.text.replace('\n', '; ') + "; " + c.stderr.text.replace('\n', '; ')))
        sys.exit(nagios_status)

    host = re.search(r"Addr->IP\s+: (.*)", c.stdout.text)
    if host:
        host = host.group(1)
    else:
        host = "(unknown host)"
    status = re.search(r"Status\s+: (.*)", c.stdout.text)
    if not status:
        nagios_status = NAGIOS_CRITICAL
        print("{status}: peer={peer}, {msg}".format(status=STATUS_MAP[nagios_status], peer=args.peer,
            msg=c.stdout.text.replace('\n', '; ') + "; " + c.stderr.text.replace('\n', '; ')))
        sys.exit(nagios_status)

    sip_status = status.group(1)
    if sip_status.find("OK") >= 0:
        nagios_status = NAGIOS_OK
    elif sip_status.find("LAGGED") >= 0:
         nagios_status = NAGIOS_WARNING
    elif sip_status.find("UNREACHABLE") >= 0:
        nagios_status = NAGIOS_CRITICAL
    else:
        nagios_status = NAGIOS_UNKNOWN
    print("{status}: peer={peer}, sip_status={sip_status}, host={host}".format(status=STATUS_MAP[nagios_status],
        peer=args.peer, sip_status=sip_status, host=host))
    sys.exit(nagios_status)

except Exception as e:
    nagios_status = NAGIOS_UNKNOWN
    print("{status}: peer={peer}, {msg}".format(status=STATUS_MAP[nagios_status], peer=args.peer, msg=e))
    sys.exit(nagios_status)

