# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'rk.document.mixin']


    @api.model
    def create(self, vals):
        res = super(Task,self).create(vals)
        if not res.matter_id and res.project_id.automatic_matter_connection_task and res.sale_line_id.order_id and res.sale_line_id.order_id.matter_id:
            res.matter_id = res.sale_line_id.order_id.matter_id
        return res

