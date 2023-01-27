# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class SMTPayment(models.Model):
    _name = 'smt.payment'
    _description = 'Payment Sukses Mandiri Teknindo'
    _rec_name = 'payment_number'
    
    
    payment_number = fields.Char('No. Payment', default="/")
    payment_type = fields.Selection([
        ('send', 'Kirim Pembayaran'),
        ('received','Terima Pembayaran')
    ], string='Type Pembayaran', required=True)
    invoice_supplier_id = fields.Many2one('smt.purchase.order.invoice', string='Invoice Supplier')
    supplier_id = fields.Many2one('smt.master.data.supplier', string='Supplier Name', related='invoice_supplier_id.supplier_id')
    total_invoice = fields.Float('Total Invoice', related='invoice_supplier_id.gross')
    due_date_invoice = fields.Date('Tanggal Jatoh Tempo', related='invoice_supplier_id.due_date_invoice')
    amount = fields.Float('Amount')
    date = fields.Date('Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='state', default='draft')
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_done_or_cancel(self):
        for rec in self:
            if rec.state!='draft':
                raise UserError(_("Sorry, You can't delete Payment(s) that has already been processed"))
            
    @api.model
    def create(self, vals):
        if vals.get('payment_number', '/') == '/':
            vals['payment_number'] = self.env['ir.sequence'].next_by_code('smt.payment') or '/'
        res = super(SMTPayment, self).create(vals)
        return res
        
    def button_approved(self):
        for rec in self:
            rec.write({'state': 'posted'})
            rec.env['smt.purchase.order.invoice'].browse(rec.invoice_supplier_id.id).write({'state': 'done'})
            rec.env['smt.purchase.order.supplier'].browse(rec.invoice_supplier_id.purchase_order_id.id).write({'state': 'done'})

SMTPayment()
    