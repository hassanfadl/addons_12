# -*- coding: utf-8 -*-
# © 2018 Hideki Yamamoto
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
	

from odoo import api, fields, models
from datetime import datetime

class ees_group_tagging_multi_action(models.TransientModel):
	_name = 'ees_group_tagging.multi_tag_action'
	categories = fields.Many2many('res.partner.category',string="Tags")
	partners = fields.Many2many('res.partner', string="Partners")
	@api.depends('categories','partners')
	def do_tag_all(self):
		if self.partners:
			if self.categories:
				for c in self.categories:
					for p in self.partners:
						p.update({'category_id': [[4,c.id]]})
				
	@api.depends('categories','partners')
	def do_untag_all(self):
		if self.partners:
			if self.categories:
				for c in self.categories:
					for p in self.partners:
						p.update({'category_id': [[3,c.id]]})
	
	@api.multi 
	def create_wizard(self): 
		wizard_id = self.create({})
		wizard_id.partners = self.env.context.get('active_ids', []) or []
		return { 
			'name': 'Multi Tag Action', 
			'view_type': 'form',
			'view_mode': 'form', 
			'res_model': 'ees_group_tagging.multi_tag_action', 
			'res_id': wizard_id.id, 
			'type': 'ir.actions.act_window', 
			'target': 'new', 
			'context': self.env.context 
		}