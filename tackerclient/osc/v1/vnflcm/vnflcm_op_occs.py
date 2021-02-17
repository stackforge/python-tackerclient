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

from osc_lib.command import command
from osc_lib import utils
from tackerclient.i18n import _
from tackerclient.osc import sdk_utils
from tackerclient.osc import utils as tacker_osc_utils

_VNF_LCM_OP_OCC_ID = 'vnf_lcm_op_occ_id'

_MIXED_CASE_FIELDS = ('operationState', 'stateEnteredTime', 'startTime',
                      'vnfInstanceId', 'isAutomaticInvocation',
                      'isCancelPending')

_FORMATTERS = {'error': tacker_osc_utils.FormatComplexDataColumn,
               '_links': tacker_osc_utils.FormatComplexDataColumn}


def _get_columns(vnflcm_op_occ_obj):
    column_map = {
        'id': 'ID',
        'operationState': 'Operation State',
        'stateEnteredTime': 'State Entered Time',
        'startTime': 'Start Time',
        'vnfInstanceId': 'VNF Instance ID',
        'operation': 'Operation',
        'isAutomaticInvocation': 'Is Automatic Invocation',
        'isCancelPending': 'Is Cancel Pending',
        'error': 'Error',
        '_links': 'Links'
    }

    return sdk_utils.get_osc_show_columns_for_sdk_resource(vnflcm_op_occ_obj,
                                                           column_map)


class RollbackVnfLcmOp(command.Command):
    def get_parser(self, prog_name):
        """Add arguments to parser.

        Args:
            prog_name ([type]): program name

        Returns:
            parser([ArgumentParser]):
        """
        parser = super(RollbackVnfLcmOp, self).get_parser(prog_name)
        parser.add_argument(
            _VNF_LCM_OP_OCC_ID,
            metavar="<vnf-lcm-op-occ-id>",
            help=_('VNF lifecycle management operation occurrence ID.'))

        return parser

    def take_action(self, parsed_args):
        """Execute rollback_vnf_instance and output comment.

        Args:
            parsed_args ([Namespace]): arguments of CLI.
        """
        client = self.app.client_manager.tackerclient
        result = client.rollback_vnf_instance(parsed_args.vnf_lcm_op_occ_id)
        if not result:
            print((_('Rollback request for LCM operation %(id)s has been'
                     ' accepted') % {'id': parsed_args.vnf_lcm_op_occ_id}))


class FailVnfLcmOp(command.ShowOne):
    _description = _("Fail VNF Instance")

    def get_parser(self, prog_name):
        """Add arguments to parser.

        Args:
            prog_name ([type]): program name

        Returns:
            parser([ArgumentParser]):
        """
        parser = super(FailVnfLcmOp, self).get_parser(prog_name)
        parser.add_argument(
            _VNF_LCM_OP_OCC_ID,
            metavar="<vnf-lcm-op-occ-id>",
            help=_('VNF lifecycle management operation occurrence ID.'))
        return parser

    def take_action(self, parsed_args):
        """Execute fail_vnf_instance and output response.

        Args:
            parsed_args ([Namespace]): arguments of CLI.
        """
        client = self.app.client_manager.tackerclient
        obj = client.fail_vnf_instance(parsed_args.vnf_lcm_op_occ_id)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(
            sdk_utils.DictModel(obj),
            columns, formatters=_FORMATTERS,
            mixed_case_fields=_MIXED_CASE_FIELDS)
        return (display_columns, data)
