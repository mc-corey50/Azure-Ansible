#!/usr/bin/python
#
# Copyright (c) 2018 Yunge Zhu, <yungez@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_webapp_slot
version_added: "2.8"
short_description: Manage Web App slot.
description:
    - Create, update and delete Web App slot.

options:
    resource_group:
        description:
            - Name of the resource group to which the resource belongs.
        required: True
    name:
        description:
            - Unique name of the deployment slot to create or update.
        required: True
    webapp_name:
        description:
            - Web app name which this deployment slot belongs to.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    configuration_source:
        description:
            - Source slot to clone configurations from. Use webapp's name to refer to the production slot.
    auto_swap_slot_name:
        description:
            - Target slot name to auto swap.
            - Set it to 'False' to disable auto slot swap.
    swap:
        description:
            - Swap deployment slots of a web app.
        type: dict
        suboptions:
            action:
                description:
                    - Swap types.
                    - 'preview' is to apply target slot's settings on source source slot first.
                    - 'swap' is to complete swapping.
                    - 'reset' is to reset the swap.
                choices:
                    - preview
                    - swap
                    - reset
            target_slot:
                description:
                    - Name of target slot to swap. If set to None, then swap with production slot.
    frameworks:
        description:
            - Set of run time framework settings. Each setting is a dictionary.
            - See U(https://docs.microsoft.com/en-us/azure/app-service/app-service-web-overview) for more info.
        suboptions:
            name:
                description:
                    - Name of the framework.
                    - Supported framework list for Windows web app and Linux web app is different.
                    - For Windows web app, supported names(June 2018) java, net_framework, php, python, node. Multiple framework can be set at same time.
                    - For Linux web app, supported names(June 2018) java, ruby, php, dotnetcore, node. Only one framework can be set.
                    - Java framework is mutually exclusive with others.
                choices:
                    - java
                    - net_framework
                    - php
                    - python
                    - ruby
                    - dotnetcore
                    - node
            version:
                description:
                    - Version of the framework. For Linux web app supported value, see U(https://aka.ms/linux-stacks) for more info.
                    - net_framework supported value sample, 'v4.0' for .NET 4.6 and 'v3.0' for .NET 3.5.
                    - php supported value sample, 5.5, 5.6, 7.0.
                    - python supported value sample, e.g., 5.5, 5.6, 7.0.
                    - node supported value sample, 6.6, 6.9.
                    - dotnetcore supported value sample, 1.0, 1,1, 1.2.
                    - ruby supported value sample, 2.3.
                    - java supported value sample, 1.8, 1.9 for windows web app. 8 for linux web app.
            settings:
                description:
                    - List of settings of the framework.
                suboptions:
                    java_container:
                        description: Name of Java container. This is supported by specific framework C(java) only. e.g. Tomcat, Jetty.
                    java_container_version:
                        description:
                            - Version of Java container. This is supported by specific framework C(java) only.
                            - For Tomcat, e.g. 8.0, 8.5, 9.0. For Jetty, e.g. 9.1, 9.3.

    container_settings:
        description: Web app container settings.
        suboptions:
            name:
                description: Name of container. eg. "imagename:tag"
            registry_server_url:
                description: Container registry server url. eg. mydockerregistry.io
            registry_server_user:
                description: The container registry server user name.
            registry_server_password:
                description:
                    - The container registry server password.
    app_settings:
        description:
            - Configure web app application settings. Suboptions are in key value pair format.s
    purge_app_settings:
        description:
            - Purge any existing application settings. Replace web app application settings with app_settings.
        type: bool
    deployment_source:
        description:
            - Deployment source for git
        suboptions:
            url:
                description:
                    - Repository url of deployment source.

            branch:
                description:
                    - The branch name of the repository.
    app_state:
        description:
            - Start/Stop/Restart the web app.
        type: str
        choices:
            - started
            - stopped
            - restarted
        default: started

    state:
      description:
        - Assert the state of the Web App deployment slot.
        - Use 'present' to create or update a deployment slot and 'absent' to delete it.
      default: present
      choices:
        - absent
        - present

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Yunge Zhu(@yungezz)"

'''

EXAMPLES = '''
    - name: Create a windows web app with non-exist app service plan
      azure_rm_webapp:
        resource_group: myresourcegroup
        name: mywinwebapp
        plan:
          resource_group: myappserviceplan_rg
          name: myappserviceplan
          is_linux: false
          sku: S1

    - name: Create a docker web app with some app settings, with docker image
      azure_rm_webapp:
        resource_group: myresourcegroup
        name: mydockerwebapp
        plan:
          resource_group: appserviceplan_test
          name: myappplan
          is_linux: true
          sku: S1
          number_of_workers: 2
        app_settings:
          testkey: testvalue
          testkey2: testvalue2
        container_settings:
          name: ansible/ansible:ubuntu1404

    - name: Create a docker web app with private acr registry
      azure_rm_webapp:
        resource_group: myresourcegroup
        name: mydockerwebapp
        plan: myappplan
        app_settings:
          testkey: testvalue
        container_settings:
          name: ansible/ubuntu1404
          registry_server_url: myregistry.io
          registry_server_user: user
          registry_server_password: pass

    - name: Create a linux web app with Node 6.6 framework
      azure_rm_webapp:
        resource_group: myresourcegroup
        name: mylinuxwebapp
        plan:
          resource_group: appserviceplan_test
          name: myappplan
        app_settings:
          testkey: testvalue
        frameworks:
          - name: "node"
            version: "6.6"

    - name: Create a windows web app with node, php
      azure_rm_webapp:
        resource_group: myresourcegroup
        name: mywinwebapp
        plan:
          resource_group: appserviceplan_test
          name: myappplan
        app_settings:
          testkey: testvalue
        frameworks:
          - name: "node"
            version: 6.6
          - name: "php"
            version: "7.0"

    - name: Create a linux web app with java framework
      azure_rm_webapp:
        resource_group: myresourcegroup
        name: mylinuxwebapp
        plan:
          resource_group: appserviceplan_test
          name: myappplan
        app_settings:
          testkey: testvalue
        frameworks:
          - name: "java"
            version: "8"
            settings:
              java_container: "Tomcat"
              java_container_version: "8.5"
'''

RETURN = '''
azure_webapp:
    description: Id of current web app.
    returned: always
    type: dict
    sample: {
        "id": "/subscriptions/<subscription_id>/resourceGroups/ansiblewebapp1/providers/Microsoft.Web/sites/ansiblewindowsaaa"
    }
'''

import time
from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.serialization import Model
    from azure.mgmt.web.models import (
        site_config, app_service_plan, Site,
        AppServicePlan, SkuDescription, NameValuePair
    )
except ImportError:
    # This is handled in azure_rm_common
    pass

swap_sepc = dict(
    action=dict(
        type='str',
        choices=[
            'preview',
            'swap',
            'reset'
        ]
    ),
    target_slot=dict(
        type='str'
    )
)

container_settings_spec = dict(
    name=dict(type='str', required=True),
    registry_server_url=dict(type='str'),
    registry_server_user=dict(type='str'),
    registry_server_password=dict(type='str', no_log=True)
)

deployment_source_spec = dict(
    url=dict(type='str'),
    branch=dict(type='str')
)


framework_settings_spec = dict(
    java_container=dict(type='str', required=True),
    java_container_version=dict(type='str', required=True)
)


framework_spec = dict(
    name=dict(
        type='str',
        required=True,
        choices=['net_framework', 'java', 'php', 'node', 'python', 'dotnetcore', 'ruby']),
    version=dict(type='str', required=True),
    settings=dict(type='dict', options=framework_settings_spec)
)


def _normalize_sku(sku):
    if sku is None:
        return sku

    sku = sku.upper()
    if sku == 'FREE':
        return 'F1'
    elif sku == 'SHARED':
        return 'D1'
    return sku


def get_sku_name(tier):
    tier = tier.upper()
    if tier == 'F1' or tier == "FREE":
        return 'FREE'
    elif tier == 'D1' or tier == "SHARED":
        return 'SHARED'
    elif tier in ['B1', 'B2', 'B3', 'BASIC']:
        return 'BASIC'
    elif tier in ['S1', 'S2', 'S3']:
        return 'STANDARD'
    elif tier in ['P1', 'P2', 'P3']:
        return 'PREMIUM'
    elif tier in ['P1V2', 'P2V2', 'P3V2']:
        return 'PREMIUMV2'
    else:
        return None


def appserviceplan_to_dict(plan):
    return dict(
        id=plan.id,
        name=plan.name,
        kind=plan.kind,
        location=plan.location,
        reserved=plan.reserved,
        is_linux=plan.reserved,
        provisioning_state=plan.provisioning_state,
        tags=plan.tags if plan.tags else None
    )


def webapp_to_dict(webapp):
    return dict(
        id=webapp.id,
        name=webapp.name,
        location=webapp.location,
        client_cert_enabled=webapp.client_cert_enabled,
        enabled=webapp.enabled,
        reserved=webapp.reserved,
        client_affinity_enabled=webapp.client_affinity_enabled,
        server_farm_id=webapp.server_farm_id,
        host_names_disabled=webapp.host_names_disabled,
        https_only=webapp.https_only if hasattr(webapp, 'https_only') else None,
        skip_custom_domain_verification=webapp.skip_custom_domain_verification if hasattr(webapp, 'skip_custom_domain_verification') else None,
        ttl_in_seconds=webapp.ttl_in_seconds if hasattr(webapp, 'ttl_in_seconds') else None,
        state=webapp.state,
        tags=webapp.tags if webapp.tags else None
    )


def slot_to_dict(slot):
    return dict(
        id=slot.id,
        name=slot.name,
        location=slot.location,
        enabled=slot.enabled,
        reserved=slot.reserved,
        server_farm_id=slot.server_farm_id,
        host_names_disabled=slot.host_names_disabled,
        state=slot.state,
        tags=slot.tags if slot.tags else None
    )


class Actions:
    NoAction, CreateOrUpdate, UpdateAppSettings, Delete = range(4)


class AzureRMWebAppSlots(AzureRMModuleBase):
    """Configuration class for an Azure RM Web App slot resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            webapp_name=dict(
                type='str',
                required=True
            )
            location=dict(
                type='str'
            ),
            configuration_source=dict(
                type='str'
            ),
            enable_auto_swap=dict(
                type='bool',
                default=False
            ),
            auto_swap_slot=dict(
                type='str'
            ),
            swap=dict(
                type='dict',
                options=swap_spec
            ),
            frameworks=dict(
                type='list',
                elements='dict',
                options=framework_spec
            ),
            container_settings=dict(
                type='dict',
                options=container_settings_spec
            ),
            scm_type=dict(
                type='str',
            ),
            deployment_source=dict(
                type='dict',
                options=deployment_source_spec
            ),
            startup_file=dict(
                type='str'
            ),
            app_settings=dict(
                type='dict'
            ),
            purge_app_settings=dict(
                type='bool',
                default=False
            ),
            app_state=dict(
                type='str',
                choices=['started', 'stopped', 'restarted'],
                default='started'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        mutually_exclusive = [['container_settings', 'frameworks']]

        self.resource_group = None
        self.name = None
        self.webapp_name = None
        self.location = None

        self.auto_swap_slot_name = None
        self.swap = None
        self.tags = None

        # site config, e.g app settings, ssl
        self.site_config = dict()
        self.app_settings = dict()
        self.app_settings_strDic = None

        # siteSourceControl
        self.deployment_source = dict()

        # site, used at level creation, or update.
        self.site = None

        # property for internal usage, not used for sdk
        self.container_settings = None

        self.purge_app_settings = False
        self.app_state = 'started'

        self.results = dict(
            changed=False,
            id=None,
        )
        self.state = None
        self.to_do = Actions.NoAction

        self.frameworks = None

        # set site_config value from kwargs
        self.site_config_updatable_frameworks = ["net_framework_version",
                                                 "java_version",
                                                 "php_version",
                                                 "python_version",
                                                 "scm_type"]

        self.supported_linux_frameworks = ['ruby', 'php', 'dotnetcore', 'node', 'java']
        self.supported_windows_frameworks = ['net_framework', 'php', 'python', 'node', 'java']

        super(AzureRMWebAppSlots, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 mutually_exclusive=mutually_exclusive,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "scm_type":
                    self.site_config[key] = kwargs[key]

        old_response = None
        response = None
        to_be_updated = False

        # set location
        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        # get web app
        webapp_response = self.get_webapp()

        if not webapp_response:
            self.fail("Web app {0} does not exist in resource grouop {1}.".format(self.webapp_name, self.resource_group))

        # get slot
        old_response = self.get_slot()

        if self.state == 'present':
            if self.frameworks:
                # java is mutually exclusive with other frameworks
                if len(self.frameworks) > 1 and any(f['name'] == 'java' for f in self.frameworks):
                    self.fail('Java is mutually exclusive with other frameworks.')

                if is_linux:
                    if len(self.frameworks) != 1:
                        self.fail('Can specify one framework only for Linux web app.')

                    if self.frameworks[0]['name'] not in self.supported_linux_frameworks:
                        self.fail('Unsupported framework {0} for Linux web app.'.format(self.frameworks[0]['name']))

                    self.site_config['linux_fx_version'] = (self.frameworks[0]['name'] + '|' + self.frameworks[0]['version']).upper()

                    if self.frameworks[0]['name'] == 'java':
                        if self.frameworks[0]['version'] != '8':
                            self.fail("Linux web app only supports java 8.")
                        if self.frameworks[0]['settings'] and self.frameworks[0]['settings']['java_container'].lower() != 'tomcat':
                            self.fail("Linux web app only supports tomcat container.")

                        if self.frameworks[0]['settings'] and self.frameworks[0]['settings']['java_container'].lower() == 'tomcat':
                            self.site_config['linux_fx_version'] = 'TOMCAT|' + self.frameworks[0]['settings']['java_container_version'] + '-jre8'
                        else:
                            self.site_config['linux_fx_version'] = 'JAVA|8-jre8'
                else:
                    for fx in self.frameworks:
                        if fx.get('name') not in self.supported_windows_frameworks:
                            self.fail('Unsupported framework {0} for Windows web app.'.format(fx.get('name')))
                        else:
                            self.site_config[fx.get('name') + '_version'] = fx.get('version')

                        if 'settings' in fx and fx['settings'] is not None:
                            for key, value in fx['settings'].items():
                                self.site_config[key] = value

            if not self.app_settings:
                self.app_settings = dict()

            if self.container_settings:
                linux_fx_version = 'DOCKER|'

                if self.container_settings.get('registry_server_url'):
                    self.app_settings['DOCKER_REGISTRY_SERVER_URL'] = 'https://' + self.container_settings['registry_server_url']

                    linux_fx_version += self.container_settings['registry_server_url'] + '/'

                linux_fx_version += self.container_settings['name']

                self.site_config['linux_fx_version'] = linux_fx_version

                if self.container_settings.get('registry_server_user'):
                    self.app_settings['DOCKER_REGISTRY_SERVER_USERNAME'] = self.container_settings['registry_server_user']

                if self.container_settings.get('registry_server_password'):
                    self.app_settings['DOCKER_REGISTRY_SERVER_PASSWORD'] = self.container_settings['registry_server_password']

            # init site
            self.site = Site(location=self.location, site_config=self.site_config)

            # check if the slot already present in the webapp
            if not old_response:
                self.log("Web App slot doesn't exist")

                to_be_updated = True
                self.to_do = Actions.CreateOrUpdate
                self.site.tags = self.tags

                # if linux, setup startup_file
                if old_plan['is_linux']:
                    if hasattr(self, 'startup_file'):
                        self.site_config['app_command_line'] = self.startup_file

                # set app setting
                if self.app_settings:
                    app_settings = []
                    for key in self.app_settings.keys():
                        app_settings.append(NameValuePair(key, self.app_settings[key]))

                    self.site_config['app_settings'] = app_settings

                # set auto_swap_slot_name
                if self.auto_swap_slot_name:
                    self.site_config['auto_swap_slot_name'] = self.auto_swap_slot_name
            else:
                # existing slot, do update
                self.log("Web App slot already exists")

                self.log('Result: {0}'.format(old_response))

                update_tags, self.site.tags = self.update_tags(old_response.get('tags', None))

                if update_tags:
                    to_be_updated = True

                # check if site_config changed
                old_config = self.get_configuration()

                if self.is_site_config_changed(old_config):
                    to_be_updated = True
                    self.to_do = Actions.CreateOrUpdate

                # check if linux_fx_version changed
                if old_config.linux_fx_version != self.site_config.get('linux_fx_version', ''):
                    to_be_updated = True
                    self.to_do = Actions.CreateOrUpdate

                self.app_settings_strDic = self.list_app_settings()

                # purge existing app_settings:
                if self.purge_app_settings:
                    to_be_updated = True
                    self.app_settings_strDic.properties = dict()

                # check if app settings changed
                if self.purge_app_settings or self.is_app_settings_changed():
                    to_be_updated = True
                    self.to_do = Actions.CreateOrUpdate

                    if self.app_settings:
                        for key in self.app_settings.keys():
                            self.app_settings_strDic.properties[key] = self.app_settings[key]

        elif self.state == 'absent':
            if old_response:
                self.log("Delete Web App slot")
                self.results['changed'] = True

                if self.check_mode:
                    return self.results

                self.delete_slot()

                self.log('Web App slot deleted')

            else:
                self.log("Web app slot {0} not exists.".format(self.name))

        if to_be_updated:
            self.log('Need to Create/Update web app')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            if self.to_do == Actions.CreateOrUpdate:
                response = self.create_update_slot()

                self.results['id'] = response['id']

        slot = None
        if old_response:
            slot = old_response
        if response:
            slot = response

        if slot:
            if (slot['state'] != 'Stopped' and self.app_state == 'stopped') or \
               (slot['state'] != 'Running' and self.app_state == 'started') or \
               self.app_state == 'restarted':

                self.results['changed'] = True
                if self.check_mode:
                    return self.results

                self.set_slot_state(self.app_state)

            if self.swap:
                self.results['changed'] = True
                    if self.check_mode:
                        return self.results

                self.swap_slot()

        return self.results

    # compare site config
    def is_site_config_changed(self, existing_config):
        for fx_version in self.site_config_updatable_frameworks:
            if self.site_config.get(fx_version):
                if not getattr(existing_config, fx_version) or \
                        getattr(existing_config, fx_version).upper() != self.site_config.get(fx_version).upper():
                            return True
        if self.auto_swap_slot_name is False:
            if existing_config.auto_swap_slot_name is not None:
                return True
        elif self.auto_swap_slot_name and self.auto_swap_slot_name != getattr(existing_config, 'auto_swap_slot_name', None):
            return True
        return False

    # comparing existing app setting with input, determine whether it's changed
    def is_app_settings_changed(self):
        if self.app_settings:
            if len(self.app_settings_strDic.properties) != len(self.app_settings):
                return True

            elif self.app_settings_strDic.properties and len(self.app_settings_strDic.properties) > 0:
                for key in self.app_settings.keys():
                    if not self.app_settings_strDic.properties.get(key) \
                            or self.app_settings[key] != self.app_settings_strDic.properties[key]:
                        return True
        return False

    # comparing deployment source with input, determine wheather it's changed
    def is_deployment_source_changed(self, existing_webapp):
        if self.deployment_source:
            if self.deployment_source.get('url') \
                    and self.deployment_source['url'] != existing_webapp.get('site_source_control')['url']:
                return True

            if self.deployment_source.get('branch') \
                    and self.deployment_source['branch'] != existing_webapp.get('site_source_control')['branch']:
                return True

        return False

    def create_update_slot(self):
        '''
        Creates or updates Web App slot with the specified configuration.

        :return: deserialized Web App instance state dictionary
        '''
        self.log(
            "Creating / Updating the Web App slot {0}".format(self.name))

        try:
            response = self.web_client.web_apps.create_or_update_slot(resource_group_name=self.resource_group,
                                                                      slot=self.name,
                                                                      name=self.webapp_name,
                                                                      site_envelope=self.site)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Web App slot instance.')
            self.fail("Error creating the Web App slot: {0}".format(str(exc)))
        return slot_to_dict(response)

    def delete_slot(self):
        '''
        Deletes specified Web App slot in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Web App slot {0}".format(self.name))
        try:
            response = self.web_client.web_apps.delete_slot(resource_group_name=self.resource_group,
                                                            name=self.webapp_name,
                                                            slot=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Web App slot.')
            self.fail(
                "Error deleting the Web App slots: {0}".format(str(e)))

        return True

    def get_webapp(self):
        '''
        Gets the properties of the specified Web App.

        :return: deserialized Web App instance state dictionary
        '''
        self.log(
            "Checking if the Web App instance {0} is present".format(self.webapp_name))

        response = None

        try:
            response = self.web_client.web_apps.get(resource_group_name=self.resource_group,
                                                    name=self.webapp_name)

            self.log("Response : {0}".format(response))
            self.log("Web App instance : {0} found".format(response.name))
            return webapp_to_dict(response)

        except CloudError as ex:
            self.log("Didn't find web app {0} in resource group {1}".format(
                self.webapp_name, self.resource_group))

        return False

    def get_slot(self):
        '''
        Gets the properties of the specified Web App slot.

        :return: deserialized Web App slot state dictionary
        '''
        self.log(
            "Checking if the Web App slot {0} is present".format(self.name))

        response = None

        try:
            response = self.web_client.web_apps.get(resource_group_name=self.resource_group,
                                                    name=self.webapp_name,
                                                    slot=self.name)

            self.log("Response : {0}".format(response))
            self.log("Web App slot: {0} found".format(response.name))
            return slot_to_dict(response)

        except CloudError as ex:
            self.log("Didn't find web app slot s{0} in resource group {1}".format(self.name, self.resource_group))

        return False

    def list_app_settings(self):
        '''
        List application settings
        :return: deserialized list response
        '''
        self.log("List application setting")

        try:

            response = self.web_client.web_apps.list_application_settings_slot(
                resource_group_name=self.resource_group, name=self.webapp_name, slot=self.slot)
            self.log("Response : {0}".format(response))

            return response
        except CloudError as ex:
            self.log("Failed to list application settings for web app slot {0} in resource group {1}".format(
                self.name, self.resource_group))

            return False

    def update_app_settings(self):
        '''
        Update application settings
        :return: deserialized updating response
        '''
        self.log("Update application setting")

        try:
            response = self.web_client.web_apps.update_application_settings_slot(resource_group_name=self.resource_group, 
                                                                                 name=self.webapp_name,
                                                                                 slot=self.name,
                                                                                 kind='Microsoft.web/slot',
                                                                                 properties=self.app_settings_strDic)
            self.log("Response : {0}".format(response))

            return response.as_dict()
        except CloudError as ex:
            self.log("Failed to update application settings for web app slot {0} in resource group {1}".format(
                self.name, self.resource_group))

        return False

    def create_or_update_source_control(self):
        '''
        Update site source control
        :return: deserialized updating response
        '''
        self.log("Update site source control")

        if self.deployment_source is None:
            return False

        self.deployment_source['is_manual_integration'] = False
        self.deployment_source['is_mercurial'] = False

        try:
            response = self.web_client.web_client.create_or_update_source_control_slot(
                resource_group_name=self.resource_group,
                name=self.webapp_name,
                site_source_control=self.deployment_source,
                slot=self.name)
            self.log("Response : {0}".format(response))

            return response.as_dict()
        except CloudError as ex:
            self.fail("Failed to update site source control for web app slot {0} in resource group {1}".format(
                self.name, self.resource_group))

    def get_configuration(self):
        '''
        Get web app configuration
        :return: deserialized web app slot configuration response
        '''
        self.log("Get web app slot configuration")

        try:

            response = self.web_client.web_apps.get_configuration_slot(
                resource_group_name=self.resource_group, name=self.webapp_name, slot=self.name)
            self.log("Response : {0}".format(response))

            return response
        except CloudError as ex:
            self.log("Failed to get configuration for web app slot {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))

            return False

    def set_slot_state(self, appstate):
        '''
        Start/stop/restart web app slot
        :return: deserialized updating response
        '''
        try:
            if appstate == 'started':
                response = self.web_client.web_apps.start_slot(resource_group_name=self.resource_group, name=self.webapp_name, slot=self.name)
            elif appstate == 'stopped':
                response = self.web_client.web_apps.stop_slot(resource_group_name=self.resource_group, name=self.webapp_name, slot=self.name)
            elif appstate == 'restarted':
                response = self.web_client.web_apps.restart_slot(resource_group_name=self.resource_group, name=self.webapp_name, slot=self.name)
            else:
                self.fail("Invalid web app slot state {0}".format(appstate))

            self.log("Response : {0}".format(response))

            return response
        except CloudError as ex:
            request_id = ex.request_id if ex.request_id else ''
            self.log("Failed to {0} web app slot {1} in resource group {2}, request_id {3} - {4}".format(
                appstate, self.name, self.resource_group, request_id, str(ex)))

    def swap_slot(self):
        '''
        Swap slot
        :return: deserialized response
        '''
        self.log("Swap slot")

        try:
            if self.swap['action'] == 'swap':
                if self.swap['target_slot'] is None:
                    response = self.web_client.web_apps.swap_slot_with_production(resource_group_name=self.resource_group,
                                                                                  name=self.webapp_name,
                                                                                  target_slot=self.name)
                else:
                    response = self.web_client.web_apps.swap_slot_slot(resource_group_name=self.resource_group,
                                                                       name=self.webapp_name,
                                                                       slot=self.name,
                                                                       target_slot=self.swap['target_slot'])
            elif self.swap['action'] == 'preview':
                if self.swap['target_slot'] is None:
                    response = self.web_client.web_apps.apply_slot_config_to_production(resource_group_name=self.resource_group,
                                                                                        name=self.webapp_name,
                                                                                        target_slot=self.name)
                else:
                    response = self.web_client.web_apps.apply_slot_configuration_slot(resource_group_name=self.resource_group,
                                                                                      name=self.webapp_name,
                                                                                      slot=self.name,
                                                                                      target_slot=self.swap['target_slot'])
            elif self.swap['action'] == 'reset':
                if self.swap['target_slot'] is None:
                    response = self.web_client.web_apps.reset_production_slot_config(resource_group_name=self.resource_group,
                                                                                     name=self.webapp_name
                else:
                    response = self.web_client.web_apps.reset_slot_configuration_slot(resource_group_name=self.resource_group,
                                                                                      name=self.webapp_name,
                                                                                      slot=self.swap['target_slot'])
                response = self.web_client.web_apps.reset_slot_configuration_slot(resource_group_name=self.resource_group,
                                                                                  name=self.webapp_name,
                                                                                  slot=self.name)

            self.log("Response : {0}".format(response))

            return response
        except CloudError as ex:
            self.fail("Failed to swap web app slot {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))


def main():
    """Main execution"""
    AzureRMWebAppSlots()


if __name__ == '__main__':
    main()
