# -*- coding: utf-8 -*-
from odoo import models, fields

class SMTCRMContact(models.Model):
    _name = 'smt.crm.lead.contact'
    _description = 'CRM Contact Sukses Mandiri Teknindo'
    _rec_name = 'name'
    
    name = fields.Char('Contact Name')
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    address = fields.Char('Address')
    attn = fields.Char('Attn')
    user_id = fields.Many2one('res.users', string='user',default=lambda self: self.env.user)
    is_customer = fields.Boolean('is_customer')
    
SMTCRMContact()