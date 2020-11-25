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

import xml.etree.ElementTree as ET


class DomainInfo:

    def __init__(self, apiClient):
        self.apiClient = apiClient

    def run(self, a_domain_name, a_key):
        request = self.apiClient.new_req('0105')
        task = request.find('task')

        task_domain = ET.SubElement(task, 'domain')
        domain_name = ET.SubElement(task_domain, 'name')

        for name in a_domain_name:
            domain_name.text = name

        response = self.apiClient.call_api(ET.tostring(request).decode())

        ignored_records = ['changed', 'comment', 'created', 'domainsafe', 'name', 'ns_action',
                           'owner', 'soa', 'system_ns', 'updated_by']

        for domain in response.findall('result/data/domain'):
            ET.dump(domain)
            for rec in list(domain):

                if rec.tag == a_key:
                    print(rec.text)

                if rec.tag not in ignored_records:
                    parsed_record = self.parse_record(rec, domain)

                    if parsed_record is not None:
                        parsed_record.print_out()

    def parse_record(self, rec, domain):
        if rec.tag == 'nserver':
            return self.parse_nserver(rec, domain)
        if rec.tag == 'main':
            return self.parse_main(rec, domain)
        if rec.tag == 'www_include':
            return self.parse_www_include(rec, domain)
        if rec.tag == 'rr':
            return self.parse_rr(rec, domain)

        #print("Unsupported element: " + rec.tag)

    def parse_nserver(self, rec, domain):
        return ZoneRecord('@', domain.findtext('soa/default'), 'NS', rec.find('name').text + '.')

    def parse_main(self, rec, domain):
        ttl = rec.find('ttl').text if rec.find('ttl') is not None else domain.findtext('soa/default')
        return ZoneRecord('@', ttl, 'A', rec.find('value').text)

    def parse_www_include(self, rec, domain):
        if rec.text != '1':
            return None

        main_rec = domain.find('main')
        if main_rec is None or main_rec.find('ttl') is None or main_rec.find('value') is None:
            return None

        return ZoneRecord('www', main_rec.find('ttl').text, 'A', main_rec.find('value').text)

    def parse_rr(self, rec, domain):
        name = rec.find('name').text or '@'
        ttl = rec.find('ttl').text if rec.find('ttl') is not None else domain.findtext('soa/default')
        pref = rec.find('pref').text + " " if rec.find('pref') is not None else ''
        type = rec.find('type').text
        value = pref + rec.find('value').text
        if type == 'TXT':
            value = '"' + value + '"'
        return ZoneRecord(name, ttl, type, value)


class ZoneRecord:

    def __init__(self, name, ttl, type, value):
        self.name = name
        self.ttl = ttl
        self.type = type
        self.value = value

    def print_out(self):
        print('{}\t{}\tIN\t{}\t{}'.format(self.name, self.ttl, self.type, self.value))
