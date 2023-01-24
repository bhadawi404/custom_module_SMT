# -*- coding: utf-8 -*-
from odoo import models, fields

class SMTSupplier(models.Model):
    _name = 'smt.master.data.supplier'
    _description = 'Master Data Supplier Sukses Mandiri Teknindo'
    _rec_name = 'supplier_name'
    
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorite'),
    ], default='0', string="Favorite")
     
    supplier_name = fields.Char('Supplier Name', required=True)
    supplier_code = fields.Char('Supplier Code')
    supplier_email = fields.Char('Supplier Email', required=True)
    supplier_phone = fields.Char('Supplier Phone', required=True)
    supplier_tax = fields.Char('Supplier NPWP')
    supplier_address = fields.Text('Supplier Address', required=True)
    supplier_attn = fields.Char('Supplier Attn')
    
    
SMTSupplier()