#!/usr/bin/python
#
# Copyright 2019 Steve Wood
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

'''
This processor is based off of the work by @grahamrpugh
'''

from __future__ import absolute_import, print_function

import requests

from autopkglib import Processor, ProcessorError

# Set the webhook_url to the one provided by MS Teams when you create the webhook

__all__ = ["Teamser"]

class Teamser(Processor):
    description = ("Posts to MS Teams via webhook based on output of a JSSImporter run. "
                    "Takes elements from " "https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784"
                    "and "
                    "https://github.com/autopkg/nmcspadden-recipes/blob/master/PostProcessors/Yo.py")
    input_variables = {
        "JSS_URL": {
            "required": False,
            "description": ("JSS_URL.")
        },
        "policy_category": {
            "required": False,
            "description": ("Policy Category.")
        },
        "category": {
            "required": False,
            "description": ("Package Category.")
        },
        "prod_name": {
            "required": False,
            "description": ("Title (NAME)")
        },
        "jss_changed_objects": {
            "required": False,
            "description": ("Dictionary of added or changed values.")
        },
        "jss_importer_summary_result": {
            "required": False,
            "description": ("Description of interesting results.")
        },
        "webhook_url": {
            "required": False,
            "description": ("Slack webhook.")
        }
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):
        JSS_URL = self.env.get("JSS_URL")
        policy_category = self.env.get("policy_category")
        category = self.env.get("category")
        prod_name = self.env.get("prod_name")
        jss_changed_objects = self.env.get("jss_changed_objects")
        jss_importer_summary_result = self.env.get("jss_importer_summary_result")
        webhook_url = self.env.get("webhook_url")

        if jss_changed_objects:
            jss_policy_name = "%s" % jss_importer_summary_result["data"]["Policy"]
            jss_policy_version = "%s" % jss_importer_summary_result["data"]["Version"]
            jss_uploaded_package = "%s" % jss_importer_summary_result["data"]["Package"]
            print("JSS address: %s" % JSS_URL)
            print("Title: %s" % prod_name)
            print("Policy: %s" % jss_policy_name)
            print("Version: %s" % jss_policy_version)
            print("Category: %s" % category)
            print("Policy Category: %s" % policy_category)
            print("Package: %s" % jss_uploaded_package)
            if jss_uploaded_package:
                # teams_text = "- URL: %s\r- Title: *%s*\r- Version: *%s*\r- Category: *%s*\r- Policy Name: *%s*\r- Uploaded Package Name: *%s*" % (JSS_URL, prod_name, jss_policy_version, category, jss_policy_name, jss_uploaded_package)
                teams_data = {'@type': 'MessageCard',
                            '@context': 'https://schema.org/extensions',
                            'summary': 'AutoPKG Run',
                            'title': 'AutoPKG Upload',
                            'sections': [
                                    {'activityTitle': 'Application Updated',
                                    'activitySubtitle': '{}'.format(JSS_URL),
                                    'facts': [
                                        {'name': 'Title:','value': '{}'.format(prod_name)},
                                        {'name': 'Policy:','value': '{}'.format(jss_policy_name)},
                                        {'name': 'Version:','value': '{}'.format(jss_policy_version)},
                                        {'name': 'Category:','value': '{}'.format(category)},
                                        {'name': 'Policy Category:','value': '{}'.format(policy_category)},
                                        {'name': 'Package:','value': '{}'.format(jss_uploaded_package)},
                                    ]
                                    }
                                ]
                            }


            else:
                # teams_text = "- URL: %s\r- Title: *%s*\r- Version: *%s*\r- Category: *%s*\r- Policy Name: *%s*\r- No new package uploaded" % (JSS_URL, prod_name, jss_policy_version, category, jss_policy_name)
                teams_data = {'@type': 'MessageCard',
                            '@context': 'https://schema.org/extensions',
                            'summary': 'AutoPKG Run',
                            'title': 'AutoPKG Upload',
                            'sections': [
                                    {'activityTitle': 'Application Updated',
                                    'activitySubtitle': '{}'.format(JSS_URL),
                                    'facts': [
                                        {'name': 'Title:','value': '{}'.format(prod_name)},
                                        {'name': 'Policy:','value': '{}'.format(jss_policy_name)},
                                        {'name': 'Version:','value': '{}'.format(jss_policy_version)},
                                        {'name': 'Category:','value': '{}'.format(category)},
                                    ]
                                    }
                                ]
                            }
            #teams_data = {'text': teams_text,'subtitle': "New Item added to JSS:"}

            response = requests.post(webhook_url, json=teams_data)
            if response.status_code != 200:
                raise ValueError(
                                'Request to slack returned an error %s, the response is:\n%s'
                                % (response.status_code, response.text)
                                )


if __name__ == "__main__":
    processor = Teamser()
    processor.execute_shell()
