# -*- coding: utf-8 -*-
from odoo import models, fields

class SMTMachine(models.Model):
    _name = 'smt.master.data.machine'
    _description = 'Master Data Machine Sukses Mandiri Teknindo'

    
    name = fields.Char('Machine Name', required=True)

SMTMachine()