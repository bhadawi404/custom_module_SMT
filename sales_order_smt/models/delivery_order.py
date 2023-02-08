# -*- coding: utf-8 -*-
from odoo import api, models, fields

class SMTDeliveryOrder(models.Model):
    _name = 'smt.delivery.order'
    _description = 'Delivery Order Sukses Mandiri Teknindo'
    
    name = fields.Char('No. Delivery', default="/")
    sales_order_id = fields.Many2one('smt.sales.order', string='SO')
    source_document = fields.Char('PO. Number', related='sales_order_id.source_document')
    customer_id = fields.Many2one('smt.master.data.customer', string='Customer Name', related='sales_order_id.customer_id')
    customer_email = fields.Char('Customer Email', related='customer_id.customer_email')
    customer_phone = fields.Char('Customer Phone', related='customer_id.customer_phone')
    customer_address = fields.Text('Customer_addres', related='customer_id.customer_address')
    customer_attn = fields.Char('Customer Attn', related='customer_id.customer_attn')
    receipt_date = fields.Date('Tanggal Pengiriman')
    view_delivery_line_ids = fields.One2many('smt.delivery.order.line', 'delivery_id', string='Delivery ID')
    state = fields.Selection([
        ('draft','Draft'),
        ('assigned', 'Waiting Delivery'),
        ('done', 'Done')
    ], string='State', default='draft')
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('smt.delivery.order') or '/'
        res = super(SMTDeliveryOrder, self).create(vals)
        return res
SMTDeliveryOrder()

class SMTDeliveryOrderLine(models.Model):
    _name = 'smt.delivery.order.line'
    _description = 'Delivery Order Line Sukses Mandiri Teknindo'
    
    delivery_id = fields.Many2one('smt.delivery.order', string='Delivery ID')
    product_id = fields.Many2one('smt.master.data.product', string='Product Name')
    qty_request = fields.Float('Qty Request')
    qty_send = fields.Float('Qty Kirim')

SMTDeliveryOrderLine()
    