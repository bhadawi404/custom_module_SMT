# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class SMTOperationtype(models.Model):
    _name = 'smt.inventory.operation.type'
    _description = 'Operation Sukses Mandiri Teknindo'
    
    
    name = fields.Char('Operation Name')
    code = fields.Char('Operation Code')
    description = fields.Char('Description')
    source_location_id = fields.Many2one('smt.inventory.stock.location', string='Source Location')
    destination_location_id = fields.Many2one('smt.inventory.stock.location', string='Destination Location')

SMTOperationtype()