# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class SMTWarehouse(models.Model):
    _name = 'smt.inventory.warehouse'
    _description = 'Warehouse Sukses Mandiri Teknindo'
    
    
    name = fields.Char('Warehouse Name')
    code = fields.Char('Warehouse Code')

SMTWarehouse()