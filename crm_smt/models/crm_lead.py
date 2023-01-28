# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class SMTCRMLeadInquiry(models.Model):
    _name = 'smt.crm.lead.inquiry'
    _description = 'CRM Inquiry Sukses Mandiri Teknindo'
    _rec_name = 'name'
    
    name = fields.Char('Inquiry No', default="/")
    contact_id = fields.Many2one('smt.crm.lead.contact', string='contact')
    email = fields.Char('Email', related='contact_id.email')
    phone = fields.Char('Phone', related='contact_id.phone')
    address = fields.Char('Address', related='contact_id.address')
    attn = fields.Char('Attn', related='contact_id.attn')
    view_line_inquiry_ids = fields.One2many('smt.crm.lead.inquiry.line', 'inquiry_id', string='Item Spesification',ondelete='cascade')
    date = fields.Date('Date')
    qty_all_request = fields.Float('Total Qty', compute='_get_qty_all')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('checking_ts', 'Checking Technical Support'),
        ('approved_ts', 'Approved Technical Support'),
        ('approved_spv', 'Approved Spv Sales'),
        ('approved_spv_produksi', 'Approved Spv Produksi'),
        ('waiting_quote', 'Waiting Quote'),
    ], string='state', default='draft')
    show_material_required = fields.Boolean('show_materal_required')
    show_pricing_required = fields.Boolean('show_pricing_required')
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('smt.crm.lead.inquiry') or '/'
        res = super(SMTCRMLeadInquiry, self).create(vals)
        return res
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_done_or_cancel(self):
        for rec in self:
            if rec.state!='draft':
                raise UserError(_("Sorry, You can't delete Inquiry(s) that has already been processed"))
            
    @api.depends('view_line_inquiry_ids.quantity')
    def _get_qty_all(self):
        for rec in self:
            qty = 0
            for line in rec.view_line_inquiry_ids:
                qty += line.quantity
            rec.update({
                'qty_all_request': qty,
            })
            return
    
    def button_confirm(self):
        self.write({'state': 'confirm'})
    
    def button_set_to_draft(self):
        self.write({'state': 'draft'})
SMTCRMLeadInquiry()

class SMTCRMLeadInquiryLine(models.Model):
    _name = 'smt.crm.lead.inquiry.line'
    _description = 'CRM Inquiry Line Sukses Mandiri Teknindo'
    
    inquiry_id = fields.Many2one('smt.crm.lead.inquiry', string='Inquiry ID')
    description_product = fields.Selection([
        ('new', 'New'),
        ('regrinding', 'Regrinding'),
        ('modify', 'Modify'),
        ('retyping', 'Retyping'),
        ('brazing_carbide_tip', 'Brazing Carbide Tip'),
        ('brazing_v_cut', 'Brazing V-Cut'),
    ], string='Item Description')
    treatment_product = fields.Selection([
        ('coating', 'Coating'),
        ('non_coating', 'Non Coating')
    ], string='Item Treatment')
    product_name = fields.Char('Item Name')
    quantity = fields.Float('Qty')
    customer_product = fields.Char('Customer Product')
    grade = fields.Char('Grade')
    hardness = fields.Char('Hardness')
    machine_merk = fields.Char('Machine Merk')
    machine_type = fields.Char('Machine Type')
    remarks = fields.Char('Remarks')
    
    
SMTCRMLeadInquiry()

