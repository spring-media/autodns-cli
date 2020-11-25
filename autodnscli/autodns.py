#!/usr/bin/env python3
# Copyright 2018 Oliver Siegmar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import sys

from ApiClient import ApiClient
from ZoneInfo import ZoneInfo
from DomainInfo import DomainInfo
from ZoneList import ZoneList
from ZoneUpdate import ZoneUpdate
from DomainList import DomainList

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-z','--zone', nargs='+', help='<Required> Set flag')
    parser.add_argument('-d','--domain', nargs='+', help='<Required> Set flag')
    parser.add_argument('-k','--key', nargs='+', help='<Required> Set flag')
    parser.add_argument('--zone-system_ns', help='Zone System Nameserver')
    parser.add_argument('--rr-name', help='Resource Record Name')
    parser.add_argument('--rr-type', help='Resource Record Type')
    parser.add_argument('--rr-ttl', help='Resource Record TTL Seconds')
    parser.add_argument('--rr-value', help='Resource Record Value')
    parser.add_argument('--output_format', help='Specify output format (csv)')
    parser.add_argument('commands', metavar='cmd', nargs='+',
                        help='commands to operate (zone-list, zone-info, zone-update, domain-list, domain-info)')
    args = parser.parse_args()

    apiClient = ApiClient(os.environ['AUTODNS_USERNAME'], os.environ['AUTODNS_PASSWORD'],
                          os.getenv('AUTODNS_CONTEXT', '4'))

    for cmd in args.commands:
        if cmd == 'zone-list':
            ZoneList(apiClient).run()
        elif cmd == 'zone-info':
            return ZoneInfo(apiClient).run(args)
        elif cmd == 'zone-update':
            ZoneUpdate(apiClient).run(args)
        elif cmd == 'domain-list':
            DomainList(apiClient).run()
        elif cmd == 'domain-info':
            DomainInfo(apiClient).run(args.domain, args.key)
        else:
            sys.exit("Unknown command: " + cmd)

    return 0


if __name__ == '__main__':
    sys.exit(main())
