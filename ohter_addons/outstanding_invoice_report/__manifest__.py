{
    'name': "Outstanding Invoice Report",
    'website': 'http://www.aktivsoftware.com',
    'author': 'Aktiv Software',
    'category': 'Accounting',
    'summary': """Generate report for customer/vendor outstanding Invoice.""",
    'license': 'AGPL-3',
    'description': """
		Generate report for customer/vendor outstanding Invoice. User can also
		generate report for specific customers/vendors.
	""",
    'version': '12.0.1.0.0',
    'depends': ['account'],
    'data': [
        'wizard/invoice_outstanding.xml',
        'views/invoice_outstanding_report_view.xml',
        'report/invoice_outstanding_template.xml',
        'report/invoice_outstanding_report.xml'
    ],
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'installable': True,
    'application': False
}
