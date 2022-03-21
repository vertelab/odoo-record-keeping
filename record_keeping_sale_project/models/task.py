# -*- coding: utf-8 -*-

from datetime import date, timedelta
from xml.dom import ValidationErr 
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def create_sale(self):
        self.ensure_one()
        if not self.partner_id:
            raise ValidationError(_('Please assign a customer to this task'))
        else:
            self.create_matter()
            if not self.sale_order_id:
                SaleOrder= self.env['sale.order']
                vals = {
                    'is_official': True,
                    'matter_id': self.matter_id.id,
                    'partner_id': self.partner_id.id,
                    'project_id': False,
                }
                if SaleOrder.fields_get().get('name_description'):
                    vals['name_description'] = self.name
                self.sale_order_id = SaleOrder.create(vals)
            stage_xmlid = 'record_keeping_sale_project.project_stage_quote_created'
            if (stage:= self.env.ref(stage_xmlid)):
                self.stage_id= stage.id

    def create_matter(self):
        self.ensure_one()
        if self.sale_order_id and self.sale_order_id.matter_id:
            self.matter_id = self.sale_order_id.matter_id
        else:
            super().create_matter()
            if self.sale_order_id and not self.sale_order_id.matter_id:
                self.sale_order_id.matter_id = self.matter_id
