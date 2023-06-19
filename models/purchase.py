# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    task_count = fields.Integer(compute='_compute_task_count', string="Task Count")
    task_ids = fields.One2many('project.task', 'purchase', string="Tasks")
    
    @api.depends('task_ids')
    def _compute_task_count(self):
        for record in self:
            record.task_count = len(record.task_ids)


    def action_view_tasks(self):
        return {
            'name': _('Tasks'),
            'res_model': 'project.task',
            'view_mode': 'list,form',
            'context': {},
            'domain': ['|',('direct_purchase', '=', self.id),('indirect_purchase', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
            