# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'rk.document.mixin']

    automatic_matter_connection_task = fields.Boolean(string="Automatic Matter Connection on Tasks")

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
        paramsudo =  self.env['ir.config_parameter'].sudo().get_param('record_keeping.project_task_default_automatic_matter_connection')

        _logger.error(f"{paramsudo=}"*100)

        if not 'matter_id' in vals and (sale_order_id := vals.get('sale_order_id')):
            if (matter_id := self.env['sale.order'].browse(sale_order_id).matter_id) and paramsudo:
                vals['matter_id'] = matter_id.id
        return super().create(vals)
