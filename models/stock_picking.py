# -*- coding: utf-8 -*-

from odoo import fields, models

CARRIER_METHOD = [('seafreight', 'Seafreight'), ('airfreight', 'Airfreight')]


class Transferts(models.Model):
    _inherit = "stock.picking"
    
    carrier_method = fields.Selection(CARRIER_METHOD, string="Carrier Method")
    departure_date = fields.Datetime(string="Departure Date")
