from odoo.tests import common
 
 
class TestExecuteQuery(common.TransactionCase):
    
    def test_execute_query(self):
        
        data = {}
        data['name']        = 'query select company'
        data['type']        = 'select'
        data['query']       = 'select * from res_company'
        data['repetition']  = '6hours'
        data['automate']    = True
        
        record1 = self.env['execute.query'].create(data)
        self.assertEqual(record1.name, 'query select company')
        self.env['execute.query'].execute_by_cron(record1)
        print("+++++++++")
        print(record1.result)
        
        
        data['name']        = 'query select company2'
        data['repetition']  = 'daily'
        record2 = self.env['execute.query'].create(data)
        self.assertEqual(record2.name, 'query select company2')
        self.env['execute.query'].execute_by_cron(record2)
        print("+++++++++")
        print(record2.result)
        
        
        data['name']        = 'query select company3'
        data['repetition']  = 'weekly'
        record3 = self.env['execute.query'].create(data)
        self.assertEqual(record3.name, 'query select company3')
        self.env['execute.query'].execute_by_cron(record3)
        print("+++++++++")
        print(record3.result)
        
        
        data['name']        = 'query select company4'
        data['repetition']  = 'monthly'
        record4 = self.env['execute.query'].create(data)
        self.assertEqual(record4.name, 'query select company4')
        self.env['execute.query'].execute_by_cron(record4)
        print("+++++++++")
        print(record4.result)
        
        
        self.env['execute.query'].scheduler_monthly()
        self.env['execute.query'].shceduler_weekly()
        self.env['execute.query'].scheduler_daily()
        self.env['execute.query'].shceduler_6hours()
        
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Test Was Successfull")
        
        
        
        