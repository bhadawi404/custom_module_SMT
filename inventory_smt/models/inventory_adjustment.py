# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class SMTQuants(models.Model):
    _name = 'smt.inventory.stock.quants'
    _description = 'Stock Quant Sukses Mandiri Teknindo'
    
    
    location_id = fields.Many2one('smt.inventory.stock.location', string='Location')
    product_id = fields.Many2one('smt.master.data.product', string='Item')
    material_id = fields.Many2one('smt.master.data.material', string='Material')
    quantity = fields.Float('Quantity')
    quantity_reserved = fields.Float('Qty Akan dikeluarkan')
    inventory_quantity = fields.Float('Qty Actual')
    diference_qty = fields.Float('Selisih')
    user_id = fields.Many2one('res.users', string='User')

SMTQuants()