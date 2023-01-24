# -*- coding: utf-8 -*-
from odoo import models, fields

class SMTMaterial(models.Model):
    _name = 'smt.master.data.material'
    _description = 'Master Data Material Sukses Mandiri Teknindo'

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorite'),
    ], default='0', string="Favorite")

    item_code = fields.Char('Item Code')
    name = fields.Char('Material Name', required=True)
    type_material = fields.Selection([
        ('ground', 'Ground'),
        ('unground', 'Unground'),
        ('hss', 'HSS'),
        ('carbide_tip', 'Carbide TIP'),
        ('oil_hole', 'Oil Hole'),
    ], string="Jenis material", required=True)
    # uom_id = fields.Many2one('uom.uom', string='Satuan Material')


SMTMaterial()