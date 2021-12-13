# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools


class Matter(models.Model):
    _name = 'rk.matter'
    _description = 'Matter'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'rk.mixin']
    _order = 'id'

    administrator_id = fields.Many2one(
        comodel_name='res.users',
        string='Administrator',
        tracking=True,
    )
    description = fields.Char(
        help='The description of this matter',
        string='Description',
        tracking=True,
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
    latest_change = fields.Char(
        compute='_compute_latest_change',
        string='Latest change',
    )
    matter_name = fields.Char(
        help='The name of this matter',
        string='Matter Name',
        tracking=True,
    )
    name = fields.Char(
        compute='_compute_name',
        help=('The format is [current year]/[sequence] and is set when '
              'the matter is created'),
        string='Matter Number',
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        tracking=True,
    )
    partner_name = fields.Char(
        compute='_compute_partner_name',
        help='Name of partner ',
        string='Partner Name',
    )
    reg_no = fields.Char(
        readonly=True,
        help='The format is [current year]/[sequence]',
        string='Registration number',
        store=True,
    )

    @api.depends('message_ids')
    def _compute_latest_change(self):
        for record in self:
            if record.message_ids:
                description = record.message_ids[0].description
                tracking_values = record.message_ids[0].tracking_value_ids
                if description:
                    record.latest_change = description
                elif tracking_values:
                    record.latest_change = (
                        f"{tracking_values[0].field_desc} -> {tracking_values[0].get_new_display_value()[0]}")
            else:
                record.latest_change = ''

    @api.depends('matter_name', 'reg_no')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.reg_no or ""} {record.matter_name or ""}'

    @api.depends('is_secret', 'partner_id')
    def _compute_partner_name(self):
        for record in self:
            if record.is_secret:
                record.partner_name = _('Confidential')
            elif record.partner_id:
                record.partner_name = record.partner_id.name
            else:
                record.partner_name = ''

    @api.model
    def create(self, vals):
        vals.update(
            {'reg_no': self.env['ir.sequence'].next_by_code('rk.matter')})
        return super(Matter, self).create(vals)
