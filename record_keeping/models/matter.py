# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Matter(models.Model):
    _name = 'rk.matter'
    _description = 'Matter'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'rk.mixin']

    description = fields.Char(
        help="The description of this matter",
        string='Description',
    )
    name = fields.Char(
        compute='_compute_name',
        help="The format is [current year]/[sequence] and is set when the matter is created",
        string="Display name",
        store=True,
    )
    document_ids = fields.One2many(
        comodel_name='rk.document',
        inverse_name='matter_id',
        string='Documents'
    )
    document_no_next = fields.Integer(
        copy=False,
        default=1,
        help="Counter used to assign to the next document",
        string="The next document number",
    )
    matter_name = fields.Char(
        help="The name of this matter",
        string='Matter Name',
    )
    registration_no = fields.Char(
        readonly=True,
        help="The format is [current year]/[sequence] and is set when the matter is created",
        string="Registration number",
        store=True,
    )

    @api.depends('matter_name', 'registration_no')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.registration_no or ''} {rec.matter_name or ''}"

    @api.model
    def create(self, vals):
        vals.update(
            {'registration_no': self.env['ir.sequence'].next_by_code('rk.matter')})
        return super(Matter, self).create(vals)
