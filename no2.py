#!/usr/bin/python

from subprocess import Popen
from subprocess import PIPE

def get_statistics(ping_count=10):
    """Gets and parses the statistics of pinging google.com

    Since we need to be root to send ICMP messages from a python script we are
    taking a different approach executing ping as an external command and then
    collecting the resulting information.

    Args:
        ping_count: The count of pings

    Returns:
        A dict mapping keys to the results.
    """

    ping    = Popen(['ping', '-c %s' % ping_count, 'google.com'], stdout=PIPE)
    stdout  = ping.communicate()[0].split('\n')
    packets = stdout.pop(-3)
    speeds  = stdout.pop(-2)

    # Expecting the speeds line to have the following format:
    # round-trip min/avg/max/stddev = 15.329/20.716/33.153/5.604 ms
    # OPTIMIZE: Regex. mondras
    speeds = speeds.split('=').pop()[:-2].strip().split('/')

    result = {}
    result['min']    = speeds[0];
    result['avg']    = speeds[1];
    result['max']    = speeds[2];
    result['sttdev'] = speeds[3];

    # Expecting the packets line to have the following format:
    # 1 packets transmitted, 1 packets received, 0.0% packet loss
    # OPTIMIZE: Regex. mondras
    result['loss'] = packets.split('received, ')[1].split('% ')[0]

    return result

print get_statistics()
