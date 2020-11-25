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


class ZoneUpdate:

    def __init__(self, apiClient):
        self.apiClient = apiClient

    def run(self, args):

        request = self.apiClient.new_req('0202001')
        task = request.find('task')

	# check if all arguments are provided
        if args.rr_name == None:
            print("Please privide resource record name! (--rr-name)")
            exit()
        if args.rr_type == None:
            print("Please privide resource record type! (--rr-type)")
            exit()
        if args.rr_ttl == None:
            print("Please privide resource record ttl value! (--rr-ttl)")
            exit()
        if args.rr_value == None:
            print("Please privide resource record value! (--rr-value)")
            exit()
        if args.zone_system_ns == None:
            print("Please provide zones system name server value! (--zone-system_ns)")
            exit()

        # add provided zones to work on
        for zone in args.zone:
            task_zone = ET.SubElement(task, 'zone')
            ET.SubElement(task_zone, 'name').text = zone
            ET.SubElement(task_zone, 'system_ns').text = args.zone_system_ns

        default = ET.SubElement(task, 'default')
        rr_add = ET.SubElement(default, 'rr_add')

        ET.SubElement(rr_add, 'name').text = args.rr_name
        ET.SubElement(rr_add, 'type').text = args.rr_type
        ET.SubElement(rr_add, 'ttl').text = args.rr_ttl
        ET.SubElement(rr_add, 'value').text = args.rr_value

        test = ET.tostring(request).decode()
        print(test)

        response = self.apiClient.call_api(ET.tostring(request).decode())
        print(ET.tostring(response).decode())
