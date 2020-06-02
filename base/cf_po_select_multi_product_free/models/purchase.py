from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def action_select_products(self):
        dummy, view_id = self.env['ir.model.data'].get_object_reference('cf_po_select_multi_product_free',
                                                                        'view_po_select_product_wiz_cf')
        wiz = self.env['po.select.product.wiz'].create({'purchase_order_id': self.id})
        return {
            'name': _("Select Products"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_id': wiz.id,
            'res_model': 'po.select.product.wiz',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }

