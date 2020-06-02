##############################################################################
#
# Odoo Proprietary License v1.0
#
# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, or if you have received a written
# agreement from the authors of the Software (see the COPYRIGHT file).
#
# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
###############################################################################
{
    'name': 'Manifest JSON for odoo application',
    'author': 'Disaster',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'sequence': 10,
    'summary': 'Add a programmable manifest.json file to you odoo applications.',
    'description': 'manifest.json'
                   'progressive web app'
                   'pwa'
                   'manifest',
    'license': 'OPL-1',
    'website': 'http://www.disastersoftware.net/',
    'images': ['static/description/cover.png'],
    'depends': [
        'base',
        'web',
    ],

    'data': [
        'data/ir_web_manifest.xml',
        'security/ir.model.access.csv',

        'views/assets_backend.xml',
        'views/ir_web_manifest.xml'
    ],
    'demo': [],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
