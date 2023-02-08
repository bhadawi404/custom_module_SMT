# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.exceptions import UserError

class SMTQuotationCustomer(models.Model):
    _name = 'smt.quotation.customer'
    _description = 'QuotationCustomer Sukses Mandiri Teknindo'
    
    name = fields.Char('Quotation No.', default="/")
    inquiry_id = fields.Many2one('smt.crm.lead.inquiry', string='Inquiry')
    date_quote = fields.Date('Date')
    due_date_quote = fields.Date('Expired Quote')
    contact_id = fields.Many2one('smt.crm.lead.contact', string='Customer Name')
    customer_email = fields.Char('Customer Email', related='contact_id.email', store=True)
    customer_phone = fields.Char('Customer Phone', related='contact_id.phone',store=True)
    customer_address = fields.Char('Customer Address', related='contact_id.address',store=True)
    customer_attn = fields.Char('Customer Attn', related='contact_id.attn',store=True)
    payment_method = fields.Selection([
        ('cod', 'Cash On Delivery'),
        ('30_days', '30 Day After Invoice Receipt'),
    ], string='Payment Method')
    quote_line_ids = fields.One2many('smt.quotation.line.customer', 'quote_id', string='Detail Quote',ondelete='cascade')
    subtotal = fields.Float('Total')
    discount = fields.Float('Discount')
    net = fields.Float('Net', compute='_compute_net', store=True)
    tax = fields.Float('Tax', compute='_compute_tax', readonly=True, store=True)
    pph23 = fields.Float('Pph23')
    gross = fields.Float('Gross', readonly=True, compute='_compute_gross', store=True)
    user_id = fields.Many2one('res.users', string='Sales Name')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('win', 'Win'),
        ('lose', 'Lose'),
        ('negotiation', 'Negotiation'),
        ('request_to_sales_order', 'Request To Sales Order'),
    ], string='State')
    notes = fields.Text('Notes')
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('smt.quotation.customer') or '/'
        res = super(SMTQuotationCustomer, self).create(vals)
        return res
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_done_or_cancel(self):
        for rec in self:
            if rec.state!='draft':
                raise UserError(("Sorry, You can't delete Quotation(s) that has already been processed"))
            
    @api.depends('quote_line_ids.total_price','discount')
    def _compute_net(self):
        for rec in self:
            total_all_price = 0
            for line in rec.quote_line_ids:
                total_all_price += line.total_price
            net = total_all_price - rec.discount
            rec.update({
                'net': net,
            })
        return

    @api.depends('net')
    def _compute_tax(self):
        for rec in self:
            rec.tax = rec.net * 11 / 100
            
    @api.depends('net','tax','pph23')
    def _compute_gross(self):
        for rec in self:
            rec.gross = rec.net + rec.tax - rec.pph23
    
    def button_confirm(self):
        self.write({'state': 'confirm'})
    
    def button_set_to_draft(self):
        self.write({'state': 'draft'})
    
    def button_win(self):
        pass
    
    def button_lose(self):
        pass
    
    def button_nego(self):
        pass
    
    def button_convert_so(self):
        pass
          
SMTQuotationCustomer()

class SMTQuotationLineCustomer(models.Model):
    _name = 'smt.quotation.line.customer'
    _description = 'Quotation Line Customer Sukses Mandiri Teknindo'
    
    quote_id = fields.Many2one('smt.quotation.customer', string='Quote ID')
    product_name = fields.Char('Item Name')
    quantity = fields.Float('Qty', default=1)
    unit_price = fields.Float('Unit Price')
    total_price = fields.Float('Total Price',compute='_compute_total_price')
    
    @api.depends('quantity','unit_price')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.quantity * rec.unit_price
            
SMTQuotationLineCustomer()