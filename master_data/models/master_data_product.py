# -*- coding: utf-8 -*-
from odoo import models, fields


class SMTProduct(models.Model):
    _name = 'smt.master.data.product'
    _description = 'Master Data Product Sukses Mandiri Teknindo'

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorite'),
    ], default='0', string="Favorite")

    item_code = fields.Char('Item Code')
    name = fields.Char('Item Name', required=True)
    item_description = fields.Char('Item Description')
    item_price = fields.Float('Item Price', required=True)
    state = fields.Boolean('State', default=True)
    sale_ok = fields.Boolean('Penjualan')
    purchase_ok = fields.Boolean('Pembelian')
    customer_id = fields.Many2one(
        'smt.master.data.customer', string='Customer Name')
    supplier_id = fields.Many2one(
        'smt.master.data.supplier', string='Supplier Name')


SMTProduct()
