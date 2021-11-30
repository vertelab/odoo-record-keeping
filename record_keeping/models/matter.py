# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Matter(models.Model):
    _name = 'rk.matter'
    _description = 'Matter'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'rk.mixin']
    _order = 'name desc'

    description = fields.Char(
        help='The description of this matter',
        string='Description',
        tracking=True,
    )
    name = fields.Char(
        compute='_compute_name',
        help=('The format is [current year]/[sequence] and is set when '
              'the matter is created'),
        string='Matter Number',
        store=True,
    )
    document_ids = fields.One2many(
        comodel_name='rk.document',
        inverse_name='matter_id',
        string='Documents',
        tracking=True,
    )
    document_no_next = fields.Integer(
        copy=False,
        default=1,
        help='Counter used to assign to the next document',
        string='The next document number',
    )
    matter_name = fields.Char(
        help='The name of this matter',
        string='Matter Name',
        tracking=True,
    )
    reg_no = fields.Char(
        readonly=True,
        help='The format is [current year]/[sequence]',
        string='Registration number',
        store=True,
    )

    @api.depends('matter_name', 'reg_no')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.reg_no or ""} {record.matter_name or ""}'

    @api.model
    def create(self, vals):
        vals.update(
            {'reg_no': self.env['ir.sequence'].next_by_code('rk.matter')})
        return super(Matter, self).create(vals)
