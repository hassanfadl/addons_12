# Part of web_manifest module. See LICENSE file for full copyright and licensing details.

import json
from odoo import http


class Main(http.Controller):
    def _get_manifest(self):
        return http.request.env.ref('web_manifest.default_manifest').get_manifest_data()

    @http.route('/manifest.json', type='json', auth="none")
    def manifest_json(self):
        return self._get_manifest()

    @http.route('/manifest.json', type='http', auth="none")
    def manifest_http(self):
        return json.dumps(self._get_manifest())
