# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class DiscussExtendMailComposer(models.TransientModel):
   
    _name = 'discuss.extend'
    _description = 'Discuss Extend'
    _log_access = True
    _batch_size = 500


    body = fields.Html('Contents', default='', sanitize_style=True)
    
    @api.multi
    def action_send_mail(self):
        self.send_mail()
        return {'type': 'ir.actions.act_window_close', 'infos': 'mail_sent'}


    @api.multi
    def send_mail(self, auto_commit=False):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed. """
        notif_layout = self._context.get('custom_layout')
        # Several custom layouts make use of the model description at rendering, e.g. in the
        # 'View <document>' button. Some models are used for different business concepts, such as
        # 'purchase.order' which is used for a RFQ and and PO. To avoid confusion, we must use a
        # different wording depending on the state of the object.
        # Therefore, we can set the description in the context from the beginning to avoid falling
        # back on the regular display_name retrieved in '_notify_prepare_template_context'.
        model_description = self._context.get('model_description')
        for wizard in self:
            
            wizard.model =  self._context.get('default_model')
            wizard.res_id =  self._context.get('default_res_id')

            ActiveModel = self.env[wizard.model] if wizard.model and hasattr(self.env[wizard.model], 'message_post') else self.env['mail.thread']
            
            
            res_ids = [wizard.res_id]

            batch_size = int(self.env['ir.config_parameter'].sudo().get_param('mail.batch_size')) or self._batch_size
            sliced_res_ids = [res_ids[i:i + batch_size] for i in range(0, len(res_ids), batch_size)]

            subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment')

            for res_ids in sliced_res_ids:
                all_mail_values = wizard.get_mail_values(res_ids)
                for res_id, mail_values in all_mail_values.items():
                    post_params = dict(
                        message_type= 'comment',
                        subtype_id=subtype_id,
                        notif_layout=notif_layout,
                        model_description=model_description,
                        **mail_values)
                    if ActiveModel._name == 'mail.thread' and wizard.model:
                        post_params['model'] = wizard.model
                    ActiveModel.browse(res_id).message_post(**post_params)

    @api.multi
    def get_mail_values(self, res_ids):
        """Generate the values that will be used by send_mail to create mail_messages
        or mail_mails. """
        self.ensure_one()
        results = dict.fromkeys(res_ids, False)
       
        for res_id in res_ids:
            # static wizard (mail.message) values
            mail_values = {
                'body': self.body or '',
            }

            results[res_id] = mail_values
        return results
              

   