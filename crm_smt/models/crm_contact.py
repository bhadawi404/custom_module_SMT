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
    is_customer = fields.Boolean('is_customer', default=False)
    
    
    def created_customer(self):
        customer_obj = self.env['smt.master.data.customer']
        for rec in self:
            rec.write({'is_customer': True})
            vals = {
                'customer_name': rec.name,
                'customer_email':rec.email,
                'customer_phone':rec.phone,
                'customer_address':rec.address,
                'customer_attn':rec.attn,
                'sales_id':rec.user_id.id,
                
            }
            customer_obj.create(vals)
SMTCRMContact()

class SMTCRMCalender(models.Model):
    _inherit = 'calendar.event'
    
    contact_id = fields.Many2one('smt.crm.lead.contact', string='contact')
    
SMTCRMCalender()