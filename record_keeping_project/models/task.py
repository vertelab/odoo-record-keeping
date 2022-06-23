# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'rk.document.mixin']

    @api.model
    def create(self, vals):
        if not 'matter_id' in vals and (sale_order_id := vals.get('sale_order_id')):
            if (matter_id := self.env['sale.order'].browse(sale_order_id).matter_id):
                vals['matter_id'] = matter_id.id
        return super().create(vals)
        


