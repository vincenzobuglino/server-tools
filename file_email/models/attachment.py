# coding: utf-8
#   @author Sébastien BEAU @ Akretion
#   @author Florian DA COSTA @ Akretion
#   @author Benoit GUILLOT @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import base64


class IrAttachmentMetadata(models.Model):
    _inherit = "ir.attachment.metadata"

    fetchmail_attachment_condition_id = fields.Many2one(
         'fetchmail.attachment.condition',
         string='FetchMail condition',
         help="The Fetchemail attachment condition used"
              "to create this attachment")
    fetchmail_server_id = fields.Many2one(
        'fetchmail.server',
        string='Email Server',
        related='fetchmail_attachment_condition_id.server_id', store=True,
        readonly=True,
        help="The email server used to create this attachment")

    def message_process(self, cr, uid, model, message, custom_values=None,
                        save_original=False, strip_attachments=False,
                        thread_id=None, context=None):
        if context is None:
            context = {}
        context['no_post'] = True
        return True

    def message_post(self, cr, uid, thread_id, body='', subject=None,
                     type='notification', subtype=None, parent_id=False,
                     attachments=None, content_subtype='html', context=None,
                     **kwargs):
        if context.get('no_post'):
            return None
        return True

    @api.model
    def _get_attachment_metadata_data(self, condition, msg, att):
        values = {
            'fetchmail_attachment_condition_id': condition.id,
            'file_type': condition.server_id.file_type,
            'name': msg['subject'],
            'direction': 'input',
            'date': msg['date'],
            'ext_id': msg['message_id'],
            'datas_fname': att[0],
            'datas': base64.b64encode(att[1]),
            'state': 'pending'
        }
        return values

    @api.model
    def prepare_data_from_basic_condition(self, condition, msg):
        vals = {}
        if (condition.from_email in msg['from'] and
                condition.mail_subject in msg['subject']):
            for att in msg['attachments']:
                if condition.file_extension in att[0]:
                    vals = self._get_attachment_metadata_data(
                        condition, msg, att)
                    break
        return vals

    @api.model
    def _prepare_data_for_attachment_metadata(self, msg):
        """Method to prepare the data for creating a attachment metadata.
        :param msg: a dictionnary with the email data
        :type: dict

        :return: a list of dictionnary that containt
            the attachment metadata data
        :rtype: list
        """
        res = []
        server_id = self._context.get('fetchmail_server_id', False)
        file_condition_obj = self.env['fetchmail.attachment.condition']
        cond_ids = file_condition_obj.search([('server_id', '=', server_id)])
        if cond_ids:
            for cond in cond_ids:
                if cond.type == 'normal':
                    vals = self.prepare_data_from_basic_condition(cond, msg)
                else:
                    vals = getattr(self, cond.type)(cond, msg)
                if vals:
                    res.append(vals)
        return res

    @api.model
    def message_new(self, msg, custom_values):
        created_ids = []
        res = self._prepare_data_for_attachment_metadata(msg)
        if res:
            for vals in res:
                default = self._context.get('default_attachment_metadata_vals')
                if default:
                    for key in default:
                        if key not in vals:
                            vals[key] = default[key]
                created_ids.append(self.create(vals))
                self._cr.commit()
            return created_ids[0].id
        return None
