# -*- coding: utf-8 -*-
from odoo import models, fields

class SMTPayment(models.Model):
    _name = 'smt.payment'
    _description = 'Payment Sukses Mandiri Teknindo'
    _rec_name = 'payment_number'
    
    
    payment_number = fields.Char('No. Payment')
    payment_type = fields.Selection([
        ('send', 'Kirim Pembayaran'),
        ('received','Terima Pembayaran')
    ], string='Type Pembayaran')
    invoice_supplier_id = fields.Many2one('smt.purchase.order.invoice', string='Invoice Supplier')
    supplier_id = fields.Many2one('smt.master.data.supplier', string='Supplier Name', related='invoice_supplier_id.supplier_id')
    total_invoice = fields.Float('Total Invoice', related='invoice_supplier_id.gross')
    amount = fields.Float('Amount')
    date = fields.Date('Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='state', default='draft')
    
    