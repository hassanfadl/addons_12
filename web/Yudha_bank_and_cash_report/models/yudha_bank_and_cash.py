# -*- coding : utf-8 -*-
# Author   => Albertus Restiyanto Pramayudha
# email    => xabre0010@gmail.com
# linkedin => https://www.linkedin.com/in/albertus-restiyanto-pramayudha-470261a8/

from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import datetime, timedelta
from odoo.addons.web.controllers.main import clean_action
from odoo.tools import float_is_zero
import time
from odoo.addons import decimal_precision as dp

class yudhabankdankas(models.Model):
    _name = "yudha.bank.kas"
    _description = "Bank Cash Register"

    @api.depends('bankcash_ids.deposit')
    def _amount_depo(self):
        for order in self:
            amount_depo = 0.0
            for line in order.bankcash_ids:
                amount_depo += line.deposit
            order.update({
                'totaldepo': amount_depo,
            })

    @api.depends('bankcash_ids.wd')
    def _amount_wd(self):
        for order in self:
            amount_wd = 0.0
            for line in order.bankcash_ids:
                amount_wd += line.wd
            order.update({
                'totalwd': amount_wd,
            })

    ed_fromdate = fields.Date('From Date', default=lambda self: time.strftime("%Y-%m-%d"))
    ed_todate = fields.Date('To Date', default=lambda self: time.strftime("%Y-%m-%d"))
    akunnya = fields.Many2one(comodel_name='account.account',inverse_name='id', string='Account' ,domain=[('user_type_id', '=', 3)])
    bankcash_ids = fields.One2many(comodel_name="yudha.bank.kas.details", inverse_name="bankcash_id", string="Bank And Cash Register ", required=False )
    totaldepo = fields.Float(string='Total Deposit', digits=dp.get_precision('Product Price'), readonly=True, compute='_amount_depo', track_visibility='onchange')
    totalwd = fields.Float(string='Total Withdrawal', digits=dp.get_precision('Product Price'), store=True, readonly=True, compute='_amount_wd', track_visibility='onchange')
    initbal = fields.Float(string='Initial Balance', digits=dp.get_precision('Product Price'), store=True, track_visibility='onchange')
    endingbal = fields.Float(string='Ending Balance', digits=dp.get_precision('Product Price'), store=True,track_visibility='onchange')
    balusd = fields.Float(string='Initial Balance(USD)', digits=dp.get_precision('Product Price'), store=True, track_visibility='onchange')
    endusd = fields.Float(string='Ending Balance(USD)', digits=dp.get_precision('Product Price'), store=True,track_visibility='onchange')

    @api.onchange('akunnya','ed_fromdate','ed_todate')
    def onchange_akunnya(self):
        if not self.akunnya:
            return
        if not self.ed_todate or not self.ed_fromdate:
            self.bankcash_ids = self.tampilakun(self.akunnya.id)
        else:
            DATETIME_FORMAT = "%Y-%m-%d"
            timbang_date1 = datetime.strptime(self.ed_fromdate, DATETIME_FORMAT)
            timbang_date2 = datetime.strptime(self.ed_todate, DATETIME_FORMAT)

            # bulanan = timbang_date.strftime('%m')
            tgldari = timbang_date1.strftime('%Y-%m-%d')
            tglsampai = timbang_date2.strftime('%Y-%m-%d')
            self.bankcash_ids = self.tampildata(tgldari,tglsampai,self.akunnya.id)

    def tampilakun(self,idakun):
       # myquery = """select a.move_id,a.date,a.name,a.account_id,a.debit,a.credit,b.currency_id,b.partner_id from account_move_line a INNER JOIN account_move b ON a.move_id=b.id INNER JOIN res_partner c ON b.partner_id=c.id where a.account_id=%s"""
        myquery = """select a.move_id,a.date,a.name,a.account_id,a.debit,a.credit from account_move_line a  where a.account_id=%s ORDER BY a.date asc"""

        self.env.cr.execute(myquery, (idakun,))
        result = self.env.cr.dictfetchall()
        hasil = {}
        semua_hasil = []
        if not result:
            return
        else:
            #inbal = self.getbalanceawal(tgldari, idakun)
            totakhir = 0.0
            for res in result:
                tgl = res['date']
                nama = res['name']
                accid = res['account_id']
                curid = self.env['account.move'].search([('id','=', res['move_id'])]).currency_id.id #res['currency_id']
                partid = self.env['account.move'].search([('id','=', res['move_id'])]).partner_id.id #res['partner_id']
                deb = res['debit']
                cred = res['credit']
                totakhir += deb -cred
                hasil = {'tglakun': tgl,
                         'namaakun': accid,
                         'memo': nama,
                         'partner': partid,
                         'currency': curid,
                         'deposit': deb,
                         'wd': cred}
                semua_hasil += [hasil]
            self.update({'endingbal': self.initbal - totakhir})
            return semua_hasil

    def getbalanceawal(self,tgl,accid):
        myquery = """select sum(debit - credit) as balance_awal from account_move_line where date < %s and account_id = %s """
        self.env.cr.execute(myquery, (tgl,accid,))
        res = self.env.cr.fetchone()[0]
        if res:
            return res
        else:
            return 0

    def gettotusd(self,tgl1,tgl2,accid):
        myquery = """select sum(amount_currency) as balance_awal from account_move_line where date BETWEEN %s and %s and account_id = %s """
        self.env.cr.execute(myquery, (tgl1,tgl2,accid,))
        res = self.env.cr.fetchone()[0]
        if res:
            return res
        else:
            return 0

    def getbalanceawalusd(self, tgl, accid):
        myquery = """select sum(amount_currency) as balance_awal from account_move_line where date < %s and account_id = %s """
        self.env.cr.execute(myquery, (tgl, accid,))
        res = self.env.cr.fetchone()[0]
        if res:
            return res
        else:
            return 0

    def tampildata(self,dari,sampai, idakun):
        # print('tgl dari',dari)
        # print('tgl sampai',sampai)
        # print('idakun', idakun)
        # where_params = self.env['account.move.line']._query_get(
        #     domain=[('user_type_id.include_initial_balance', '=', True)])
        # if where_params:
        #     print
        #myquery = """select a.move_id,a.date,a.name,a.account_id,a.debit,a.credit,b.currency_id,b.partner_id from account_move_line a INNER JOIN account_move b ON a.move_id=b.id INNER JOIN res_partner c ON b.partner_id=c.id where a.date between %s and %s and account_id=%s"""
        #myquery = """select a.move_id,a.date,a.name,a.account_id,a.debit,a.credit, a.balance from account_move_line a  where a.date BETWEEN %s AND %s AND a.account_id=%s ORDER BY a.date asc"""
        myquery  = """select a.move_id,a.date,a.name,a.account_id,a.journal_id,a.debit,a.credit, a.balance, a.currency_id, a.amount_currency,a.ref, b.partner_id from account_move_line a INNER JOIN account_move b ON a.move_id=b.id left JOIN res_partner c ON b.partner_id=c.id where a.date between %s and %s and account_id=%s ORDER BY a.date asc"""
        self.env.cr.execute(myquery, (dari,sampai,idakun,))
        result = self.env.cr.dictfetchall()
        hasil = {}
        semua_hasil = []
        if not result:
            return
        else:
            inbal = self.getbalanceawal(dari, idakun)
            usdbal = self.getbalanceawalusd(dari,idakun)
            #totusd = self.gettotusd(dari,sampai,idakun)
            totakhir = 0.0
            totusd = 0.0
            totdepo = 0.0
            totwd = 0.0
            bal = 0
            balakir = inbal
            for res in result:
                tgl = res['date']
                nama = []
                nama = res['name'] and res['name'] or ''
                if res['ref']:
                    nama = nama and nama + ' - ' + res['ref'] or res['ref']
                if len(nama) > 35:
                    nama = nama[:32] + "..."
                # if res['name'] =='' or res['name']=='/':
                #     nama = res['ref']
                # else:
                #     nama= res['name']

                accid = res['account_id']
                curid = res['currency_id'] #self.env['account.move'].search([('id','=', res['move_id'])]).currency_id.id #res['currency_id']
                partid = res['partner_id'] #self.env['account.move'].search([('id','=', res['move_id'])]).partner_id.id #res['partner_id']
                jurid = res['journal_id']
                # inusd = 0.0
                # myaccount = self.env['account.move'].search([('id','=', res['move_id'])]) #res['currency_id']
                # if myaccount:
                #     if myaccount.currency_id ==13:
                #         inusd = 0.0
                #     else:
                #         inusd = myaccount.amount_currency
                inusd=res['amount_currency']
                if inusd == 0:
                    curid= 13
                deb = res['debit']
                cred = res['credit']
                if deb >0 and cred ==0:
                    bal = balakir + deb
                elif deb==0 and cred >0:
                    bal = balakir -cred
                elif deb>0 and cred >0:
                    bal = (balakir +deb) - cred
                balakir = bal
                #totakhir += deb - cred
                totdepo +=deb
                totwd +=cred
                totusd +=  inusd
                hasil = {'tglakun':tgl,
                         'namaakun': accid,
                         'memo': nama,
                         'notrans': res['move_id'],
                         'partner': partid,
                         'currency': curid,
                         'foreign_cur': inusd,
                         'deposit': deb,
                         'wd': cred,
                         'balance': balakir}
                semua_hasil += [hasil]
            totakhir = (inbal + totdepo) - totwd
            totusdakhir = usdbal+totusd
            self.update({'initbal': inbal,
                         'endingbal': totakhir,
                         'balusd': usdbal,
                         'endusd': totusdakhir})
            return semua_hasil



class yudhabankdankasdetails(models.Model):
    _name = "yudha.bank.kas.details"

    bankcash_id = fields.Many2one(comodel_name='yudha.bank.kas', inverse_name='id', string="BANK AND CASH REGISTER DETAILS",required=False, store=True, index=True)
    tglakun = fields.Date('Date')
    namaakun = fields.Many2one(comodel_name='account.account',inverse_name='id',string='Acccount Name')
    notrans = fields.Many2one(comodel_name='account.move',inverse_name='id', string='Nomor Transaction')
    memo = fields.Char('Memo')
    partner = fields.Many2one(comodel_name='res.partner',inverse_name='id',string='Partner')
    currency = fields.Many2one('res.currency',string='Currency')
    foreign_cur = fields.Float('Foreign Currency', digits=dp.get_precision('Product Price'))
    deposit = fields.Float('Deposit', digits=dp.get_precision('Product Price'))
    balance = fields.Float('Balance',digits=dp.get_precision('Product Price'))
    wd = fields.Float('Withdrawal', digits=dp.get_precision('Product Price'))




