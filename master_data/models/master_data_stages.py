# -*- coding: utf-8 -*-
from odoo import models, fields

class SMTStages(models.Model):
    _name = 'smt.master.data.stages'
    _description = 'Master Data Stages Sukses Mandiri Teknindo'

    machine_id = fields.Many2one('smt.master.data.machine', string='Machine Name')
    name = fields.Char('Stages Name', required=True)

SMTStages()