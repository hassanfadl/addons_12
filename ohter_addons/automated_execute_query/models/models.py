# -*- coding: utf-8 -*-

from odoo import models, fields, api

class automated_execute_query(models.Model):
    _name = "execute.query"
    
    name        = fields.Char(string ="Name")
    query       = fields.Text(string = "Query")
    automate    = fields.Boolean(string = "Automate")
    result      = fields.Text(string="Result")    
    repetition  = fields.Selection([('6hours', '6 Hours'), ('daily','Daily'),('weekly', 'Weekly'),('monthly','Monthly')])
    type        = fields.Selection([('select','Select Data'),('update','Update Data'),('delete','Delete Data')])
    
    
    @api.multi
    def execute_manually(self):
        
        try : 
            query = self.env.cr.execute(self.query)
        
            if self.type == "select" :
                 self.result = str(self.env.cr.dictfetchall())
            elif self.type == "update" :
                self.result = "Update success"
            elif self.type == "delete" :
                self.result = "Delete success"
        
                    
        except Exception as e:
            self.result = "error : " + str(e)
            
            


    
    def execute_by_cron(self,id):
        
                       
        try : 
            query = self.env.cr.execute(id.query)
        
            if id.type == "select" :
                 id.result = str(self.env.cr.dictfetchall())
            elif id.type == "update" :
                id.result = "Update success"
            elif id.type == "delete" :
                id.result = "Delete success"
        
                    
        except Exception as e:
            id.result = "" + str(e)
            
            
    @api.multi
    def shceduler_6hours(self):   
        ids = self.env['execute.query'].search([])
        
        for id in ids :
            
            if id.repetition == '6hours' :        
                self.execute_by_cron(id)             
    
        
    @api.multi
    def scheduler_daily(self):
        
        ids = self.env['execute.query'].search([])
        
        for id in ids :
            
            if id.repetition == 'daily' :        
                self.execute_by_cron(id)
                
    @api.multi
    def shceduler_weekly(self):
        
        ids = self.env['execute.query'].search([])
        
        for id in ids :
            
            if id.repetition == 'weekly' :        
                self.execute_by_cron(id)
                
                
    @api.multi                
    def scheduler_monthly(self):
        
        ids = self.env['execute.query'].search([])
        
        for id in ids :
            
            if id.repetition == 'monthly' :        
                self.execute_by_cron(id)
        
                
             
    
    
    