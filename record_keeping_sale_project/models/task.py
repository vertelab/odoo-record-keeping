# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    allow_create_sale = fields.Boolean(
        compute='_compute_allow_create_sale',
        help='Allow Sale Order creation',
        string='Allow Create Sale',
    )

    @api.depends('project_id.allow_create_sale')
    def _compute_allow_create_sale(self):
        for task in self:
            task.allow_create_sale = task.project_id.allow_create_sale

    def create_sale(self):
        self.ensure_one()
        if not self.allow_create_sale:
            raise UserError(
                _('Allow sale order creation on the project first'))
        if not self.partner_id:
            raise ValidationError(_('Please assign a customer to this task'))
        else:
            self.create_matter()
            if not self.sale_order_id:
                SaleOrder = self.env['sale.order']
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
            if (stage := self.env.ref(stage_xmlid)):
                self.stage_id = stage.id

    def create_matter(self):
        self.ensure_one()
        if self.sale_order_id and self.sale_order_id.matter_id:
            self.matter_id = self.sale_order_id.matter_id
        else:
            super().create_matter()
            if self.sale_order_id and not self.sale_order_id.matter_id:
                self.sale_order_id.matter_id = self.matter_id
        self.matter_id.partner_id = self.partner_id.id
        self.matter_id.name = self.display_name
