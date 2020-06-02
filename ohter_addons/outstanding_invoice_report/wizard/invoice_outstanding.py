from datetime import datetime
from odoo import api, fields, models


class InvoiceOutstanding(models.TransientModel):
    _name = "invoice.outstanding"
    
    start_date = fields.Date(string='From Date', required=True,
                             default=datetime.today().replace(day=1).date())
    end_date = fields.Date(string='To Date', required=True,
                           default=datetime.now().date())
    partner_ids = fields.Many2many('res.partner', string="Partners")
    invoice_type = fields.Selection([('customer', 'Customer'),
                                     ('vendor', 'Vendor')],
                                    string="Invoice Type",
                                    default="customer")
    order_by = fields.Selection([('date_due', 'Due Date'),
                                 ('date_invoice', 'Invoice Date')],
                                string="Order By",
                                default="date_due")
    sort_by = fields.Selection([('asc', 'Ascending'),
                                ('desc', 'Descending')],
                               default="asc")
    
    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['start_date', 'end_date', 'partner_ids',
                                  'invoice_type', 'order_by', 'sort_by'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        return self.env.ref('outstanding_invoice_report.action_customer_invoice_outstanding').report_action(
            self, data=data)