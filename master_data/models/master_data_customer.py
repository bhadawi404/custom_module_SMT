# -*- coding: utf-8 -*-
from odoo import models, fields

class SMTCustomer(models.Model):
    _name = 'smt.master.data.customer'
    _description = 'Master Data Customer Sukses Mandiri Teknindo'
    _rec_name = 'customer_name'
    
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorite'),
    ], default='0', string="Favorite")
     
    customer_name = fields.Char('Customer Name', required=True)
    customer_code = fields.Char('Customer Code')
    customer_email = fields.Char('Customer Email',required=True)
    customer_phone = fields.Char('Customer Phone')
    customer_tax = fields.Char('Customer NPWP')
    customer_address = fields.Text('Customer Address', required=True)
    customer_attn = fields.Char('Customer Attn')
    sales_id = fields.Many2one('res.users', string='Sales Name')
    
    
SMTCustomer()