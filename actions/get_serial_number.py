"""
Copyright 2016 Brocade Communications Systems, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import re
from lib import actions
from lib import ztp_utils


class GetSerialAction(actions.SessionAction):
    def __init__(self, config):
        super(GetSerialAction, self).__init__(config)

    def run(self, via, device, username='', password='', enable_username='', enable_password=''):
        ztp_utils.replace_default_userpass(self, username, password,
                                           enable_username, enable_password)
        session = ztp_utils.start_session(device, self._username, self._password,
                                          self._enable_username, self._enable_password, via)

        command = 'show version | inc Serial'
        (success, results) = ztp_utils.send_commands_to_session(session, command, conf_mode=False)
        
        print "session output is %s" % results

        if success:
            # Built JSON Record from parsed results
            sn = {}
            unit = re.compile('^\s+Serial\W+(\w+)')
            for line in results[0]['output']:
                match = unit.match(line)
            sn = match.group().split()[-1]

            return (True, json.dumps(sn))

        return (False, "Broken")
