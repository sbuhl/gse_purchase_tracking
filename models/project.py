# -*- coding: utf-8 -*-

from odoo import api, fields, models

INVOICE_STATUS = [
    ('upselling', 'Upselling Opportunity'),
    ('invoiced', 'Fully Invoiced'),
    ('to invoice', 'To Invoice'),
    ('no', 'Nothing to Invoice')
]


class Tasks(models.Model):
    _inherit = "project.task"

    sale_order = fields.Many2one("sale.order", string="Final Customer SO")
    direct_purchase = fields.Many2one("purchase.order", string="Ref Final Supplier")
    indirect_purchase = fields.Many2one("purchase.order", string="Ref Atimex")

    purchase = fields.Many2one('purchase.order', compute='_compute_purchase', store=True)
    purchase_picking_id = fields.Many2many('stock.picking', compute='_compute_purchase_picking_id', store=True)
    
    inspection_status = fields.Selection([
        ('1', '1. License opening requested'),
        ('2', '2. RFI received'),
        ('3', '3. RFI sent'),
        ('4', '4. FDR received'),
        ('5', '5. FDR sent'),
        ('6', '6. ARA received - action to be taken'),
        ('7', '7. AV received - fisnish')
    ], string="Status inspection BIVAC")

    delivery_step = fields.Selection([
        ('1', '1. PO Accepted'),
        ('2', '2. in Manufacturing'),
        ('3', '3. ready for Shipping'),
        ('4', '4. at the Port/Airport'),
        ('5', '5. on the Water/in the Air'),
        ('6', '6. waiting to Dock'),
        ('7', '7. at Customs'),
        ('8', '8. in Drayage'),
        ('9', '9. at Distribution Center'),
        ('10', '10. Receipt Scheduled'),
        ('11', '11. Received')
    ], string="Delivery Step")

    final_supplier = fields.Char(related="direct_purchase.partner_id.name", string="Final Supplier", store=True)
    dp_name = fields.Char(related="direct_purchase.name", string="PO Ref", store=True)
    dp_po_state = fields.Selection(related="direct_purchase.state", string="PO Status")
    dp_receipt_status = fields.Selection(related="direct_purchase.receipt_status", string="Dir. Recept. Status")
    dp_date_approve = fields.Datetime(related="direct_purchase.date_approve", string="Conf. Final Sup. Date", store=True)
    dp_date_done = fields.Datetime(related="direct_purchase.picking_ids.date_done", string="Effective Date")
    dp_billing_status = fields.Selection(related="direct_purchase.invoice_status", string="Billing Status")

    indirect_supplier = fields.Char(related="indirect_purchase.partner_id.name", string="Indirect Supplier - Atimex")
    ip_name = fields.Char(related="indirect_purchase.name", string="PO Atimex", store=True)
    ip_po_state = fields.Selection(related="indirect_purchase.state", string="PO Atimex Status")
    ip_receipt_status = fields.Selection(related="indirect_purchase.receipt_status", string="Rec. Status Atimex")
    ip_date_approve = fields.Datetime(related="indirect_purchase.date_approve", string="Conf. Date Atimex")
    ip_date_scheduled = fields.Datetime(related="indirect_purchase.picking_ids.scheduled_date", string="Scheduled Date")
    ip_date_done = fields.Datetime(related="indirect_purchase.picking_ids.date_done", string="Effective Date in Atimex")
    ip_billing_status = fields.Selection(related="indirect_purchase.invoice_status", string="Atimex Billing Status", store=True)

    fd_location_dest = fields.Char(related="purchase_picking_id.location_dest_id.warehouse_id.name", string="Destination", store=True)
    fd_scheduled_date = fields.Datetime(related="purchase_picking_id.scheduled_date", string="Final Dest. Scheduled Date")
    fd_forwarder = fields.Char(related="purchase_picking_id.carrier_id.name", string="Forwarder", store=True)
    fd_date_done = fields.Datetime(related="purchase_picking_id.date_done", string="Final Effective Date")
    fd_forwarder_ref = fields.Char(related="purchase_picking_id.carrier_tracking_ref", string="Forwarder Ref", store=True)
    fd_forwarder_method = fields.Selection(related="purchase_picking_id.carrier_method", string="Forwarder Method", store=True)
    fd_departure_date = fields.Datetime(related="purchase_picking_id.departure_date", string="Departure Date")
    fd_receipt_status = fields.Selection(related="purchase.receipt_status", string="Final Destination Status", store=True)
    at_receipt_status = fields.Selection([
        ('empty', ''),
        ('pending', 'Not Received'),
        ('partial', 'Partially Received'),
        ('full', 'Fully Received'),
    ], compute="_compute_at_receipt_status", string="Atimex Reception Status", store=True)

    @api.depends('indirect_purchase', 'direct_purchase')
    def _compute_purchase(self):
        for record in self:
            record.purchase = record.indirect_purchase or record.direct_purchase

    @api.depends('purchase', 'purchase.picking_ids')
    def _compute_purchase_picking_id(self):
        for record in self:
            if record.purchase.picking_ids:
                record.purchase_picking_id = record.purchase.picking_ids.sorted('create_date', reverse=True)[0]
            else:
                record.purchase_picking_id = self.env['stock.picking']

    @api.depends("indirect_purchase", "direct_purchase.receipt_status", "indirect_purchase.receipt_status")
    def _compute_at_receipt_status(self):
        for record in self:
            if record.indirect_purchase:
                record.at_receipt_status = record.indirect_purchase.receipt_status
            else:
                record.at_receipt_status == 'empty'
