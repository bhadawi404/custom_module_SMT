# -*- coding: utf-8 -*-
from odoo import api, models, fields

class SMTSalesOrder(models.Model):
    _name = 'smt.sales.order'
    _description = 'Sales Order Sukses Mandiri Teknindo'
    
    name = fields.Char('Sales Order', default="/")
    customer_id = fields.Many2one('smt.master.data.customer', string='Customer Name')
    customer_email = fields.Char('Customer Email', related='customer_id.customer_email')
    customer_phone = fields.Char('Customer Phone', related='customer_id.customer_phone')
    customer_address = fields.Text('Customer_addres', related='customer_id.customer_address')
    customer_attn = fields.Char('Customer Attn', related='customer_id.customer_attn')
    source_document = fields.Char('PO. Number')
    view_sales_line_ids = fields.One2many('smt.sales.order.line', 'sales_order_id', string='Sales Order Line')
    date = fields.Date('Date')
    subtotal = fields.Float('Total')
    discount = fields.Float('Discount')
    net = fields.Float('Net', compute='_compute_net', store=True)
    tax = fields.Float('Tax', compute='_compute_tax', readonly=True, store=True)
    pph23 = fields.Float('Pph23')
    gross = fields.Float('Gross', readonly=True, compute='_compute_gross', store=True)
    user_id = fields.Many2one('res.users', string='Sales Name', default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('request_to_admin','Requested'),
        ('confirm', 'Confirm'),
        ('delivery', 'Delivery'),
        ('done', 'Done')
    ], string='State')
    notes = fields.Text('Notes')
    payment_method = fields.Selection([
        ('cod', 'Cash On Delivery'),
        ('30_days', '30 Day After Invoice Receipt'),
    ], string='Payment Method')
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('smt.sales.order') or '/'
        res = super(SMTSalesOrder, self).create(vals)
        return res
    
    @api.depends('view_sales_line_ids.total_price','discount')
    def _compute_net(self):
        for rec in self:
            total_all_price = 0
            for line in rec.view_sales_line_ids:
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
        
SMTSalesOrder()

class SMTSalesOrderLine(models.Model):
    _name = 'smt.sales.order.line'
    _description = 'Sales Order Line Customer Sukses Mandiri Teknindo'
    
    sales_order_id = fields.Many2one('smt.sales.order', string='SO')
    product_name = fields.Many2one('smt.master.data.product', string='Product Name', domain=[('sale_ok','=', True)])
    quantity = fields.Float('Qty')
    unit_price = fields.Float('Unit Price', related='product_name.item_price')
    total_price = fields.Float('Total Price',compute='_compute_total_price')
    
    @api.depends('quantity','unit_price')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.quantity * rec.unit_price
            
SMTSalesOrderLine()