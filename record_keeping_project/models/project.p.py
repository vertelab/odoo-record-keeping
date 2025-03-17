# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'rk.document.mixin']

    def attachment_tree_view(self):
        action = super().attachment_tree_view()
        if (ctx := action['context']) and (matter_id := self.matter_id):
            new_ctx = [
                x.replace('{', '').replace('}', '')
                for x in ctx.split(',')
            ]
            new_ctx.append(f"'active_matter': {matter_id.id}")
            action['context'] = f"{{{', '.join(new_ctx)}}}"
        return action

    @api.model
    def create(self, vals):
        if not 'matter_id' in vals and (sale_order_id := vals.get('sale_order_id')):
            if (matter_id := self.env['sale.order'].browse(sale_order_id).matter_id):
                vals['matter_id'] = matter_id.id
        return super().create(vals)
