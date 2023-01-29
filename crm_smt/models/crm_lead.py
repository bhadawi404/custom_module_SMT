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
    show_material_required = fields.Boolean('show_materal_required', compute='_show_material')
    show_pricing_required = fields.Boolean('show_pricing_required', compute='_show_pricing')
    count_material = fields.Integer('count_material', compute='_count_material')
    
    def _count_material(self):
        for rec in self:
            rec.count_material = self.env['smt.crm.lead.inquiry.material'].search_count([('inquiry_id','=', rec.id)])
    
    def action_view_material(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Material Required',
            'res_model': 'smt.crm.lead.inquiry.material',
            'view_mode': 'tree,form',
            'view_id': False,
            'views': [(self.env.ref('crm_smt.smt_crm_lead_inquiry_material_views_tree').id, 'tree'), (self.env.ref('crm_smt.smt_crm_lead_inquiry_material_views_form').id, 'form')],
            'domain': [('inquiry_id','=',self.id)],
            'target': 'current',
        }
        return action
            
    def _show_material(self):
        for rec in self:
            rec.show_material_required = False
            if rec.state == 'approved_ts':
                rec.show_material_required = True
    
    def _show_pricing(self):
        for rec in self:
            if rec.state == 'approved_spv_produksi':
                rec.show_pricing_required = True
                
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
        
        material_obj = self.env['smt.crm.lead.inquiry.material']
        material_line_obj = self.env['smt.crm.lead.inquiry.material.line']
        action_data = {}
        for rec in self:
            vals = {
                'inquiry_id': rec.id,
            }
            material_ids = material_obj.create(vals)
            action_data['material'] = [material_ids]
            material = material_ids
            if material:
                for line in rec.view_line_inquiry_ids:
                    material_line = material_line_obj.create({
                    'inquiry_material_id': material_ids.id,
                    'line_inquiry_item_id': line.id
                })
            rec.write({'state': 'confirm'})    
    
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

class SMTCRMLeadInquiryLineMaterial(models.Model):
    _name = 'smt.crm.lead.inquiry.material'
    _description = 'CRM Inquiry Material Sukses Mandiri Teknindo'
    
    name = fields.Char('Request Material Inquiry', default="/")
    inquiry_id = fields.Many2one('smt.crm.lead.inquiry', string='Inquiry ID')
    view_inquiry_material_ids = fields.One2many('smt.crm.lead.inquiry.material.line', 'inquiry_material_id', string='view_inquiry_material')
    view_line_inquiry_ids = fields.One2many('smt.crm.lead.inquiry.line', 'inquiry_id', related='inquiry_id.view_line_inquiry_ids', string='Item Spesification',ondelete='cascade')
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('smt.crm.lead.inquiry.material') or '/'
        res = super(SMTCRMLeadInquiryLineMaterial, self).create(vals)
        return res
    
SMTCRMLeadInquiryLineMaterial()

class SMTCRMLeadInquiryMaterialLine(models.Model):
    _name = 'smt.crm.lead.inquiry.material.line'
    _description = 'CRM Inquiry Material Line Sukses Mandiri Teknindo'
    
    inquiry_material_id = fields.Many2one('smt.crm.lead.inquiry.material', string='inquiry_material_id')
    line_inquiry_item_id = fields.Many2one('smt.crm.lead.inquiry.line', string='line_item')
    inquiry_id = fields.Many2one('smt.crm.lead.inquiry', string='Inquiry', related='inquiry_material_id.inquiry_id')
    product_name = fields.Char('Item name', related='line_inquiry_item_id.product_name', store=True)
    description_product = fields.Selection([
        ('new', 'New'),
        ('regrinding', 'Regrinding'),
        ('modify', 'Modify'),
        ('retyping', 'Retyping'),
        ('brazing_carbide_tip', 'Brazing Carbide Tip'),
        ('brazing_v_cut', 'Brazing V-Cut'),
    ], string='Item Description', related='line_inquiry_item_id.description_product')
    treatment_product = fields.Selection([
        ('coating', 'Coating'),
        ('non_coating', 'Non Coating')
    ], string='Item Treatment', related='line_inquiry_item_id.treatment_product')
    quantity = fields.Float('Qty', related='line_inquiry_item_id.quantity')
    customer_product = fields.Char('Customer Product',related='line_inquiry_item_id.customer_product')
    grade = fields.Char('Grade', related='line_inquiry_item_id.grade')
    hardness = fields.Char('Hardness', related='line_inquiry_item_id.hardness')
    machine_merk = fields.Char('Machine Merk', related='line_inquiry_item_id.machine_merk')
    machine_type = fields.Char('Machine Type', related='line_inquiry_item_id.machine_type')
    remarks = fields.Char('Remarks', related='line_inquiry_item_id.remarks')
    ground_unground = fields.Selection([
        ('ground', 'Ground'),
        ('unground', 'Unground'),
    ], string='Ground / Unground')
    solid_hole_hss = fields.Selection([
        ('solid', 'Solid'),
        ('oil_hole', 'Oil Hole'),
        ('hss', 'HSS'),
    ], string='Solid / Oil Hole / HSS')
    dc = fields.Char('DC')
    sd = fields.Char('SD')
    helix_straight = fields.Selection([
        ('helix', 'Helix'),
        ('straight', 'Straight'),
    ], string='Helix / Straight')
    length = fields.Integer('Length')
    grade = fields.Char('Grade')
    
SMTCRMLeadInquiryMaterialLine()