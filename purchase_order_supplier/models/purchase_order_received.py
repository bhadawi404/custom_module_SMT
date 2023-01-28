# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError

class SMTPurchaseOrderSupplierReceived(models.Model):
    _name = 'smt.purchase.order.supplier.received'
    _description = 'Purchase Order Supplier Received Sukses Mandiri Teknindo'
    _rec_name = 'name'
    
    name = fields.Char('No. Received', default="/")
    purchase_order_id = fields.Many2one('smt.purchase.order.supplier', string='PO Number', required=True)
    supplier_id = fields.Many2one('smt.master.data.supplier', related='purchase_order_id.supplier_id',string='Supplier Name')
    received_date = fields.Date('Received Date', readonly=True)
    delivery_order = fields.Char('Delivery Order')
    view_received_purchase_order_ids = fields.One2many('smt.purchase.order.supplier.received.line', 'received_po_id', string='Product',ondelete='cascade')
    state = fields.Selection([
        ('waiting', 'Waiting Product'),
        ('done', 'Done'),
    ], default='waiting', string="State")
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_done_or_cancel(self):
        for rec in self:
            if rec.state!='waiting':
                raise UserError(_("Sorry, You can't delete Received Product(s) that has already been processed"))
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('smt.purchase.order.supplier.received') or '/'
        res = super(SMTPurchaseOrderSupplierReceived, self).create(vals)
        return res
    
    def set_quantity(self):
        for rec in self.view_received_purchase_order_ids:
            self.env['smt.purchase.order.supplier.received.line'].browse(rec.id).write({'quantity_done': rec.quantity_request})
    
    def button_received(self):
        now = datetime.now()
        invoice = self.env['smt.purchase.order.invoice']
        for rec in self.view_received_purchase_order_ids:
            if rec.quantity_done:
                self.env['smt.purchase.order.supplier.line'].browse(rec.purchase_order_line.id).write({'quantity_received': rec.quantity_done})
                self.write({'received_date': now, 'state': 'done'})
                invoice.create(
                    {'purchase_order_id':self.purchase_order_id.id, 
                     'state':'draft'
                    })
            else:
                raise UserError(_("Sorry, You can't Received Product(s), Click set quantity first to received the product"))
SMTPurchaseOrderSupplierReceived()


class SMTPurchaseOrderSupplierReceivedLine(models.Model):
    _name = 'smt.purchase.order.supplier.received.line'
    _description = 'Purchase Order Supplier Received Line Sukses Mandiri Teknindo'
    
    received_po_id = fields.Many2one('smt.purchase.order.supplier.received', ondelete='cascade',string='Received Number')
    purchase_order_line = fields.Many2one('smt.purchase.order.supplier.line', string='Line ID')
    product_id = fields.Many2one('smt.master.data.product', string='Product Name')
    description = fields.Char('Description', readonly=True)
    quantity_request = fields.Float('Quantity Request')
    quantity_done = fields.Float('Quantity Done')
    
    
SMTPurchaseOrderSupplierReceivedLine()

