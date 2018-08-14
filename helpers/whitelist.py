#!/usr/bin/env python

import os

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import arrow
import sys
import dns.resolver
from dns.resolver import NoAnswer, NXDOMAIN, NoNameservers, Timeout
from dns.name import EmptyLabel
from pprint import pprint

TIMEOUT = 5


def resolve_ns(data, t='A', timeout=TIMEOUT):
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    resolver.search = []
    try:
        answers = resolver.query(data, t)
        resp = []
        for rdata in answers:
            resp.append(rdata)
    except (NoAnswer, NXDOMAIN, EmptyLabel, NoNameservers, Timeout) as e:
        if str(e).startswith('The DNS operation timed out after'):
            return

        if not str(e).startswith('The DNS response does not contain an answer to the question'):
            if not str(e).startswith('None of DNS query names exist'):
                return

        return

    return resp



def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
                example usage:
                    $
                '''),
        formatter_class=RawDescriptionHelpFormatter,
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")

    args = p.parse_args()

    networks = set()
    for l in sys.stdin.readlines():
        l = l.rstrip()
        _, fqdn = l.split(',')
        ips = resolve_ns(fqdn)
        if not ips:
            continue

        for i in ips:
            prefix = str(i).split('.')
            prefix = prefix[:3]
            prefix.append('0')
            prefix = '.'.join(prefix)

            if prefix in networks:
                continue

            networks.add(prefix)

    ts = arrow.utcnow()
    for n in networks:
        for e in range(0, 24):
            ts = ts.replace(hour=e)
            #t = '{}-{}-{}T{}:00:00Z'.format(ts.year, ts.month, ts.day, e)
            t = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
            print("%s,%s" % (t, n))



if __name__ == '__main__':
    main()
