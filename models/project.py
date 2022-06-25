# -*- coding: utf-8 -*-

from odoo import api, fields, models

from odoo.addons.gse_purchase_tracking.models.stock_picking import CARRIER_METHOD

INVOICE_STATUS = [('upselling', 'Upselling Opportunity'),
                    ('invoiced', 'Fully Invoiced'),
                    ('to invoice', 'To Invoice'),
                    ('no', 'Nothing to Invoice')]


class Tasks(models.Model):
    _inherit = "project.task"

    sale_order = fields.Many2one("sale.order", string="Final Customer SO")
    direct_purchase = fields.Many2one("purchase.order", string="Ref Final Supplier")
    indirect_purchase = fields.Many2one("purchase.order", string="Ref Atimex") 
    delivery_step = fields.Selection([('1', '1. PO Accepted'),
                                        ('2', '2. in Manufacturing'),
                                        ('3', '3. ready for Shipping'),
                                        ('4', '4. at the Port/Airport'),
                                        ('5', '5. on the Water/in the Air'),
                                        ('6', '6. waiting to Dock'),
                                        ('7', '7. at Customs'),
                                        ('8', '8. in Drayage'),
                                        ('9', '9. at Distribution Center'),
                                        ('10', '10. Receipt Scheduled'), 
                                        ('11', '11. Received')], 
                                        string="Delivery Step")
    
    final_supplier = fields.Char(related="direct_purchase.partner_id.name", string="Final Supplier")
    dp_name = fields.Char(related="direct_purchase.name", string="PO Ref")
    dp_po_state = fields.Selection(related="direct_purchase.state", string="PO Status")
    dp_receipt_status = fields.Selection(related="direct_purchase.receipt_status", string="Dir. Recept. Status")
    dp_date_approve = fields.Datetime(related="direct_purchase.date_approve", string="Conf. Final Sup. Date")
    dp_date_done = fields.Datetime(related="direct_purchase.picking_ids.date_done", string="Effective Date")
    dp_billing_status = fields.Selection(related="direct_purchase.invoice_status", string="Billing Status")
    
    indirect_supplier = fields.Char(related="indirect_purchase.partner_id.name", string="Indirect Supplier - Atimex")
    ip_name = fields.Char(related="indirect_purchase.name", string="PO Atimex")
    ip_po_state = fields.Selection(related="indirect_purchase.state", string="PO Atimex Status")
    ip_receipt_status = fields.Selection(related="indirect_purchase.receipt_status", string="Rec. Status Atimex")
    ip_date_approve = fields.Datetime(related="indirect_purchase.date_approve", string="Conf. Date Atimex")
    ip_date_scheduled = fields.Datetime(related="indirect_purchase.picking_ids.scheduled_date", string="Scheduled Date")
    ip_date_done = fields.Datetime(related="indirect_purchase.picking_ids.date_done", string="Effective Date in Atimex")
    ip_billing_status = fields.Selection(related="indirect_purchase.invoice_status", string="Atimex Billing Status")

    fd_location_dest = fields.Char(compute="_compute_final_location_dest", string="Destination")
    fd_scheduled_date = fields.Datetime(compute="_compute_final_dest_date", string="Final Dest. Scheduled Date")
    fd_forwarder = fields.Char(compute="_compute_final_forwarder", string="Forwarder")
    fd_date_done = fields.Datetime(compute="_compute_final_effective_date", string="Final Effective Date")
    fd_forwarder_ref = fields.Char(compute="_compute_final_forwarder_ref", string="Forwarder Ref")
    fd_forwarder_method = fields.Selection(CARRIER_METHOD, compute="_compute_forwarder_method", string="Forwarder Method")
    fd_departure_date = fields.Date(compute="_compute_departure_date", string="Departure Date")
    fd_receipt_status = fields.Selection([
         ('pending', 'Not Received'),
         ('partial', 'Partially Received'),
         ('full', 'Fully Received'),
     ], compute="_compute_receipt_status", string="Final Destination Status")
    at_receipt_status = fields.Selection([
         ('empty', ''),
         ('pending', 'Not Received'),
         ('partial', 'Partially Received'),
         ('full', 'Fully Received'),
     ], compute="_compute_at_receipt_status", string="Atimex Reception Status")

    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.location_dest_id", "indirect_purchase.picking_ids.location_dest_id")
    def _compute_final_location_dest(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_location_dest = record.indirect_purchase.picking_ids.location_dest_id.warehouse_id.name
            else:
                record.fd_location_dest = record.direct_purchase.picking_ids.location_dest_id.warehouse_id.name
    
    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.date_done", "indirect_purchase.picking_ids.date_done")
    def _compute_final_effective_date(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_date_done = record.indirect_purchase.picking_ids.date_done
            else:
                record.fd_date_done = record.direct_purchase.picking_ids.date_done
    
    @api.depends("indirect_purchase.name", "direct_purchase.receipt_status", "indirect_purchase.receipt_status")
    def _compute_receipt_status(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_receipt_status = record.indirect_purchase.receipt_status
            else:
                record.fd_receipt_status = record.direct_purchase.receipt_status

    @api.depends("indirect_purchase.name", "direct_purchase.receipt_status", "indirect_purchase.receipt_status")
    def _compute_at_receipt_status(self):
        for record in self:
            if record.indirect_purchase.name:
                record.at_receipt_status = record.direct_purchase.receipt_status
            else:
                record.at_receipt_status == 'empty'
    
    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.scheduled_date", "indirect_purchase.picking_ids.scheduled_date")
    def _compute_final_dest_date(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_scheduled_date = record.indirect_purchase.picking_ids.scheduled_date
            else:
                record.fd_scheduled_date = record.direct_purchase.picking_ids.scheduled_date
                
    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.carrier_id.name", "indirect_purchase.picking_ids.carrier_id.name")
    def _compute_final_forwarder(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_forwarder = record.indirect_purchase.picking_ids.carrier_id.name
            else:
                record.fd_forwarder = record.direct_purchase.picking_ids.carrier_id.name

    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.carrier_tracking_ref", "indirect_purchase.picking_ids.carrier_tracking_ref")
    def _compute_final_forwarder_ref(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_forwarder_ref = record.indirect_purchase.picking_ids.carrier_tracking_ref
            else:
                record.fd_forwarder_ref = record.direct_purchase.picking_ids.carrier_tracking_ref
    
    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.carrier_method", "indirect_purchase.picking_ids.carrier_method")
    def _compute_forwarder_method(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_forwarder_method = record.indirect_purchase.picking_ids.carrier_method
            else:
                record.fd_forwarder_method = record.direct_purchase.picking_ids.carrier_method

    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.departure_date", "indirect_purchase.picking_ids.departure_date")
    def _compute_departure_date(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_departure_date = record.indirect_purchase.picking_ids.departure_date
            else:
                record.fd_departure_date = record.direct_purchase.picking_ids.departure_date
