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

PAGE_SIZE = 100


class DomainList:

    def __init__(self, apiClient):
        self.apiClient = apiClient

    def run(self):
        total_domain_cnt = None
        page = 0
        pages = 1

        while pages >= page:
            response = self.call(page * PAGE_SIZE, PAGE_SIZE)
            domains = response.findall('result/data/domain')
            for domain in domains:
                print(domain.find('name').text)

            if total_domain_cnt is None:
                total_domain_cnt = int(response.find("result/data/summary").text)
                pages = (total_domain_cnt + len(domains) // 2) // len(domains)

            page = page + 1

    def call(self, r_offset, r_limit):
        request = self.apiClient.new_req('0105')
        task = request.find('task')

        view = ET.SubElement(task, 'view')

        offset = ET.SubElement(view, 'offset')
        offset.text = str(r_offset)

        limit = ET.SubElement(view, 'limit')
        limit.text = str(r_limit)

        children = ET.SubElement(view, 'children')
        children.text = '1'

        return self.apiClient.call_api(ET.tostring(request).decode())
