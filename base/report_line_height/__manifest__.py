{
	'name'      : 'Report Line Height',
	'version'   : '1.0.0',
	'category'  : 'Report',
	'summary'   : 'Reduce Report Line height and margin',
	'description': """
		This module reduce the qweb report line height (line spacing) for Table Listing report and html type report.

	""",
	'author'    : 'Qten Computer',
	'website'   :'http://www.qtencomputer.com',
	'license'   : "LGPL-3",
	'images': ['static/src/img/ReportLineHeight-banner.jpg'],
	'depends'   : ['base'],
	'data'      : [
		'views/report_format.xml',  
		],
	'demo'      : [],
	'test'      : [],
	'installable'   : True,
	'auto_install'  : False,
	'application'   : False,
}
