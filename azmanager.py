# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Based off of gist at https://gist.github.com/vishvananda/1389905

"""Nova Network Manager that limits Networks by Availability Zone."""

from nova import availability_zones
from nova import db
from nova.network import manager


class AZDHCPManager(manager.FlatDHCPManager):
    """Extends FlatDHCPManager to limit networks by availability zone."""

    def _get_networks_for_instance(self, context, instance_id, project_id,
                                   requested_networks=None):
        supercls = super(manager.FlatDHCPManager, self)
        networks = supercls._get_networks_for_instance(context,
                                                       instance_id,
                                                       project_id,
                                                       requested_networks)

        instance = db.instance_get_by_uuid(context.elevated(),
                                           instance_id)
        host = str(instance.get('host'))
        # NOTE(SlickNik): expects label to be set to the name of the
        #                 availability zone.
        return [network for network in networks if network['label'] ==
                availability_zones.get_host_availability_zone(context, host)]
