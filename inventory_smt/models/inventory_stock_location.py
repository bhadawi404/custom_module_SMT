# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class SMTStockLocation(models.Model):
    _name = 'smt.inventory.stock.location'
    _description = 'Location Sukses Mandiri Teknindo'
    
    
    warehouse_id = fields.Many2one('smt.inventory.warehouse', string='Warehouse')
    name = fields.Char('Location Name')
    capacity = fields.Float('Capacity Location')
    parent_id = fields.Many2one('smt.inventory.stock.location', string='Parent Location')
    type_id = fields.Many2one('smt.inventory.operation.type', string='Operation type')
SMTStockLocation()