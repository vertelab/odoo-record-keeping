# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
class Task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'rk.document.mixin']
    
    @api.model
    def create(self, vals):
      connect_task_to_matter = self.env['ir.config_parameter'].sudo().get_param('record_keeping.project_task_default_automatic_matter_connection')
      if connect_task_to_matter:
         for val in vals:
            if not 'matter_id' in vals and (sale_order_id := val.get('sale_order_id')):
               if matter_id := self.env['sale.order'].browse(sale_order_id).matter_id:
                  val['matter_id'] = matter_id.id
      return super().create(vals)
