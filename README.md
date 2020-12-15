# autodns-cli

Command line utility for [AutoDNS by
InternetX](https://www.internetx.com/en/domains/autodns/), extended
with a bild-specific function to edit A-Records pointing to UDC origin
servers. See [BILD Use Case](#bild-use-case)

## Credentials

    export AUTODNS_USERNAME='<YOUR AUTODNS USERNAME>'
    export AUTODNS_PASSWORD='<YOUR AUTODNS PASSWORD>'


## List all zones

    autodns zone-list


## List zone records

    autodns zone-info --zone <zone-name>

## BILD Use Case

This function changes all A-Records of given zones which currently
point to any of the UDC origin servers to those at fth, nbg or both.

* List zones

  ```shell
  ./autodns.py zone-list >zones
  ```

* Edit ``zones`` appropriately

* Update zones

  ```shell
  xargs ./autodns.py bild both <zones
  ```

  Use ``fth`` or ``nbg`` instead of ``both`` if records are to point to
  one site only.

### Example

* contents of the zones file

  ```
  $ cat zones
  volkshaftpflichtversicherung.de
  spobi.de
  asmediaimpact.de
  ```

* Change zones to point to Fürth only:

  ```
  $ xargs ./autodns.py bild fth <zones
  no records: volkshaftpflichtversicherung.de
  old spobi.de: None	(ttl)	IN	A	145.243.240.20
  new spobi.de: None	(ttl)	IN	A	145.243.240.20
  old asmediaimpact.de: None	(ttl)	IN	A	145.243.240.20
  old asmediaimpact.de: None	(ttl)	IN	A	145.243.248.20
  remove main_ip 145.243.248.20
  new asmediaimpact.de: None	(ttl)	IN	A	145.243.240.20
  ```

  Output:

  * ``volkshaftpflichtversicherung.de`` has no records pointing to
    UDC origins

  * ``spobi.de`` already pointed to Fürth only (the change is a
    noop)

  * ``asmediaimpact.de`` pointed to both sites and was changed

* Change zones to point to both data centres (this should be the
  default setting):

  ```
  $ xargs ./autodns.py bild both <zones
  no records: volkshaftpflichtversicherung.de
  old spobi.de: None	(ttl)	IN	A	145.243.240.20
  new spobi.de: None	(ttl)	IN	A	145.243.240.20
  new spobi.de: None	(ttl)	IN	A	145.243.248.20
  old asmediaimpact.de: None	(ttl)	IN	A	145.243.240.20
  new asmediaimpact.de: None	(ttl)	IN	A	145.243.240.20
  new asmediaimpact.de: None	(ttl)	IN	A	145.243.248.20
  ```


## Disclaimer

bild-specific additions are the best python code ever and nothing to
brag about. The tool does the job.

egg installation is incomplete

## Copyright

Copyright 2018 Oliver Siegmar
Copyright 2020 UPLEX Nils Goroll Systemoptimierung

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
