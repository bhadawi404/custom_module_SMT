from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class SMTPurchaseOrderInvoice(models.Model):
    _name = 'smt.purchase.order.invoice'
    _description = 'Invoice Sukses Mandiri Teknindo'
    _rec_name = 'purchase_order_id'
    
    
     
    name = fields.Char('No. Invoice',default='Draft')
    faktur_no = fields.Char('No Faktur')
    purchase_order_id = fields.Many2one('smt.purchase.order.supplier', string='No. Purchase Order')
    supplier_id = fields.Many2one('smt.master.data.supplier', string='Supplier Name', related='purchase_order_id.supplier_id')
    email_supplier = fields.Char('Supplier Email', related='supplier_id.supplier_email')
    phone_supplier = fields.Char('Supplier Phone', related='supplier_id.supplier_phone')
    address_supplier = fields.Text('Supplier Address', related='supplier_id.supplier_address')
    attn_supplier = fields.Char('Supplier Phone', related='supplier_id.supplier_attn')
    ref_code = fields.Char('Code', related='purchase_order_id.ref_code')
    due_date_invoice = fields.Date('Tanggal Jatuh Tempo', compute='_get_due_date')
    date_terima_invoice = fields.Date('Tanggal Terima Invoice')
    state = fields.Selection([
        ('draft', 'Waiting Approved'),
        ('approved', 'Waiting Payment'),
        ('done', 'Lunas'),
    ], default='draft', string="State")
    line_purchase_ids = fields.One2many('smt.purchase.order.supplier.line','purchase_order_id', string='Product', compute='_get_line_purchase')
    discount = fields.Float('Discount')
    net = fields.Float('Net', related='purchase_order_id.net')
    tax = fields.Float('Tax',related='purchase_order_id.tax')
    pph23 = fields.Float('Pph23',related='purchase_order_id.pph23')
    gross = fields.Float('Gross',related='purchase_order_id.gross')
    notes = fields.Text('Notes',related='purchase_order_id.notes')
    
    
    
    
    @api.onchange('purchase_order_id')
    def _get_line_purchase(self):
        line = []
        for rec in self:
            for rec in self.purchase_order_id.view_purchase_line_ids:
                line.append(rec.id)
            
        self.line_purchase_ids = line
    
    @api.onchange('date_terima_invoice') 
    def _get_due_date(self):
        self.due_date_invoice = False
        for rec in self:
            if rec.date_terima_invoice:
                rec.due_date_invoice = rec.date_terima_invoice + relativedelta(days=30)
                
    def button_approved(self):
        payment = self.env['smt.payment']
        self.write({'state':'approved'})
        payment.create({
            'invoice_supplier_id': self.id,
            'payment_type': 'send'
        })
SMTPurchaseOrderInvoice() 