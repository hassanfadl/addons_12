from odoo import api, models


class ReportInvoices(models.AbstractModel):
    _name = 'report.outstanding_invoice_report.report_invoice_outstanding'

    '''Find Outstanding invoices between the date and find total outstanding amount'''
    @api.model
    def _get_report_values(self, docids, data=None):
        type = "out_invoice"
        if data['form']['invoice_type'] == 'vendor':
            type = "in_invoice"

        order_by = "partner_id, date_due"
        if data['form']['order_by'] == 'date_invoice':
            order_by = "partner_id, date_invoice"

        if data['form']['sort_by'] == 'desc':
            order_by += " desc"

        # prepare domain for invoice.
        domain = [('date_due', '>=', data['form']['start_date']),
                  ('date_due', '<=', data['form']['end_date']),
                  ('type', '=', type), ('state', '=', 'open')]
        # Apply domain to filter invoices by partners.
        if data['form']['partner_ids']:
            domain += [('partner_id', 'in', data['form']['partner_ids'])]
        invoices = self.env['account.invoice'].search(domain, order=order_by)

        # Calculate total pending amount from all invoices.
        amount_total = sum([inv.residual for inv in invoices])
        data.update({'amount_total': amount_total, 'invoices': invoices})
        return {
            'doc_ids': docids,
            'doc_model': 'invoice.outstanding',
            'docs': self.env['invoice.outstanding'].browse(docids),
            'data': data
        }
