# Copyright 2018 Oliver Siegmar
# Copyright 2020 UPLEX Nils Goroll Systemoptimierung
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

import xml.etree.ElementTree as ET

ips = {}
ips['fth'] = '145.243.240.20'
ips['nbg'] = '145.243.248.20'


class Bild:
    def __init__(self, apiClient):
        self.apiClient = apiClient
        self.returnCode = 0

    def run(self, loc, name):
        new = []
        if loc in ips:
            new = [ips[loc]]
        elif loc == 'both':
            new = ips.values()
        else:
            raise Exception("loc")

        request = self.apiClient.new_req('0205')
        task = request.find('task')

        task_zone = ET.SubElement(task, 'zone')
        ET.SubElement(task_zone, 'name').text = name

        key = ET.SubElement(task, 'key')
        key.text = 'rr'

        request = ET.tostring(request).decode()
        try:
            response = self.apiClient.call_api(request)
        except:
            print("query failed: " + name)
            return

        remove_main = False
        rem = []
        add = {}

        for zone in response.findall('result/data/zone'):
            for rec in list(zone):
                if rec.tag in 'main':
                    val = rec.find('value')
                    if val is None:
                        continue
                    val = val.text
                    if val in ips.values():
                        remove_main = val
                    continue
                if rec.tag not in 'rr':
                    continue
                typ = rec.find('type').text
                if typ != 'A':
                    continue
                val = rec.find('value').text
                if val not in ips.values():
                    continue
                rrname = rec.find('name').text
                print('old %s: %s\t(ttl)\tIN\t%s\t%s' %
                      (name, rrname, typ, val))
                rem.append(rec)
                add[rrname] = 1

        if len(rem) == 0:
            if remove_main is False:
                print("no records: " + name)
                return
            print("add nexus A records because main ip matches: " + name)
            add[''] = 1

        request = self.apiClient.new_req('0202001')
        task = request.find('task')
        task_zone = ET.SubElement(task, 'zone')
        ET.SubElement(task_zone, 'name').text = name

        default = ET.SubElement(task, 'default')

        if remove_main:
            ET.SubElement(default, 'remove_main_ip').text = 'true'
            repl = ET.SubElement(default, 'search_and_replace')
            ET.SubElement(repl, 'search').text = remove_main
            ET.SubElement(repl, 'type').text = 'MAIN_IP'
            ET.SubElement(repl, 'replace').text = ''
            print('remove main_ip %s' % remove_main)

        for rec in rem:
            rr_rem = ET.SubElement(default, 'rr_rem')
            rr_rem.extend(rec.findall('*'))

        for a in add.keys():
            for ip in new:
                rr_add = ET.SubElement(default, 'rr_add')
                ET.SubElement(rr_add, 'name').text = a or ''
                ET.SubElement(rr_add, 'type').text = 'A'
                ET.SubElement(rr_add, 'ttl').text = '600'
                ET.SubElement(rr_add, 'value').text = ip
                print('new %s: %s\t(ttl)\tIN\t%s\t%s' %
                      (name, a, 'A', ip))

        request = ET.tostring(request).decode()
        try:
            response = self.apiClient.call_api(request)
        except:
            print("change failed: " + name)
            return
