# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError

class SMTPurchaseOrderSupplier(models.Model):
    _name = 'smt.purchase.order.supplier'
    _description = 'Purchase Order Supplier Sukses Mandiri Teknindo'
    _rec_name = 'purchase_order_number'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('approved', 'Approved'),
        ('done', 'Done'),
    ], default='draft', string="State")

    purchase_order_number = fields.Char('PO. Number',  default='/')
    supplier_id = fields.Many2one('smt.master.data.supplier', string='Supplier Name', required=True)
    email_supplier = fields.Char('Supplier Email', related='supplier_id.supplier_email')
    phone_supplier = fields.Char('Supplier Phone', related='supplier_id.supplier_phone')
    address_supplier = fields.Text('Supplier Address', related='supplier_id.supplier_address')
    attn_supplier = fields.Char('Supplier Phone', related='supplier_id.supplier_attn')
    ref_code = fields.Char('Code')
    date_order = fields.Date('Date Order', required=True)
    view_purchase_line_ids = fields.One2many('smt.purchase.order.supplier.line', 'purchase_order_id', string='Item Description',ondelete='cascade')
    discount = fields.Float('Discount')
    net = fields.Float('Net', compute='_compute_net', store=True)
    tax = fields.Float('Tax', compute='_compute_tax', readonly=True, store=True)
    pph23 = fields.Float('Pph23')
    gross = fields.Float('Gross', readonly=True, compute='_compute_gross', store=True)
    notes = fields.Text('Notes')
    count_delivery = fields.Integer('count_delivery', compute='_count_picking')
    count_invoice = fields.Integer('count_invoice', compute='_count_invoice')
    
    def _count_picking(self):
        for rec in self:
            rec.count_delivery = self.env['smt.purchase.order.supplier.received'].search_count([('purchase_order_id','=', rec.id)])
    
    def action_view_picking(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Delivery Order',
            'res_model': 'smt.purchase.order.supplier.received',
            'view_mode': 'tree,form',
            'view_id': False,
            'views': [(self.env.ref('purchase_order_supplier.smt_purchase_order_supplier_received_tree').id, 'tree'), (self.env.ref('purchase_order_supplier.smt_purchase_order_supplier_received_form').id, 'form')],
            'domain': [('purchase_order_id','=',self.id)],
            'target': 'current',
        }
        return action
    
    def _count_invoice(self):
        for invoice in self:
            inv = self.env['smt.purchase.order.invoice'].search([('purchase_order_id','=', invoice.id)])
            if inv:
                invoice.count_invoice = inv.gross
            else:
                invoice.count_invoice = 0
    def action_view_invoice(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'smt.purchase.order.invoice',
            'view_mode': 'tree,form',
            'view_id': False,
            'views': [(self.env.ref('purchase_order_supplier.smt_purchase_order_supplier_invoice_views_tree').id, 'tree'), (self.env.ref('purchase_order_supplier.smt_purchase_order_supplier_invoice_views_form').id, 'form')],
            'domain': [('purchase_order_id','=',self.id)],
            'target': 'current',
        }
        return action
    @api.model
    def create(self, vals):
        if vals.get('purchase_order_number', '/') == '/':
            vals['purchase_order_number'] = self.env['ir.sequence'].next_by_code('smt.purchase.order.supplier') or '/'
        res = super(SMTPurchaseOrderSupplier, self).create(vals)
        return res
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_done_or_cancel(self):
        for rec in self:
            if rec.state!='draft':
                raise UserError(_("Sorry, You can't delete Purchase Order(s) that has already been processed"))

    #button approved groups admin sales 1
    def button_confirm(self):
        self.write({'state': 'confirm'})
        
    #button approved groups finance    
    def button_approved(self):
        received_obj = self.env['smt.purchase.order.supplier.received']
        received_line_obj = self.env['smt.purchase.order.supplier.received.line']
        action_data = {}
        for rec in self:
            received_ids = received_obj.create({
                'purchase_order_id': rec.id,
                'supplier_id': rec.supplier_id.id,
                'state': 'waiting'
            })
            action_data['purchase'] = [received_ids]
            received = received_ids
            if received:
                for line in rec.view_purchase_line_ids:
                    received_line = received_line_obj.create({
                    'purchase_order_line': line.id,
                    'product_id': line.product_id.id,
                    'received_po_id':received.id,
                    'description': line.description,
                    'quantity_request': line.quantity
                })
            rec.write({'state': 'approved'})
                 
            
                 

    def button_set_to_draft(self):
        self.write({'state': 'draft'})
    
    def print_purchase_order(self):
        pass
    
    def action_po_send(self):
        pass
    
    @api.depends('view_purchase_line_ids.total_price','discount')
    def _compute_net(self):
        for rec in self:
            total_all_price = 0
            for line in rec.view_purchase_line_ids:
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
        
    
SMTPurchaseOrderSupplier()

class SMTPurchaseOrderSupplierLine(models.Model):
    _name = 'smt.purchase.order.supplier.line'
    _description = 'Purchase Order Supplier Line Sukses Mandiri Teknindo'

    purchase_order_id = fields.Many2one('smt.purchase.order.supplier', string='purchase')
    product_id = fields.Many2one('smt.master.data.product', string='Product', required=True, domain=[('purchase_ok','=', True)])
    description = fields.Char('Description', related='product_id.item_description', readonly=True)
    quantity = fields.Float('Quantity', required=True)
    quantity_received = fields.Float('Quantity Received', readonly=True)
    price = fields.Float('Unit Price', required=True)
    total_price = fields.Float('Total Price', compute='_compute_subtotal_price')
    
    
    @api.depends('quantity','price')
    def _compute_subtotal_price(self):
        for rec in self:
            rec.total_price = rec.price * rec.quantity

SMTPurchaseOrderSupplierLine()