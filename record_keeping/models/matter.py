# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class Matter(models.Model):
    _name = 'rk.matter'
    _description = 'Matter'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'rk.mixin']
    _order = 'id'

    administrator_id = fields.Many2one(
        comodel_name='res.users',
        copy=False,
        string='Administrator',
        tracking=True,
        index=True
    )
    classification_id = fields.Many2one(
        comodel_name='rk.classification',
        copy=False,
        string='Classification',
        default=lambda self: int(self._get_default_param('classification_id')) or 0,
        tracking=True,
        index=True
    )
    department_id = fields.Many2one(
        copy=False,
        related='administrator_id.department_id',
        store=True,
        string='Department',
        tracking=True,
        index=True
    )
    description = fields.Char(
        copy=False,
        help='The description of this matter',
        string='Description',
        tracking=True,
    )
    document_count = fields.Integer(
        compute='_compute_document_count',
        string='Number of documents in this matter',
    )
    document_ids = fields.One2many(
        comodel_name='rk.document',
        copy=False,
        inverse_name='matter_id',
        string='Documents',
        tracking=True,
    )
    document_no_next = fields.Integer(
        copy=False,
        default=1,
        help='Counter used to assign to the next document',
        readonly=True,
        string='The next document number',
    )
    close_date = fields.Date(
        copy=False,
        help='Date when matter is closed',
        readonly=1,
        string='Closed',
        tracking=True,
    )
    latest_change = fields.Char(
        compute='_compute_latest_change',
        string='Latest change',
        tracking=True,
    )
    legacy_reg_no = fields.Char(
        copy=False,
        help='From other sources',
        string='Legacy registration number',
        tracking=True,
    )
    matter_name = fields.Char(
        copy=False,
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
        tracking=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        tracking=True,
        index=True
    )
    partner_name = fields.Char(
        compute='_compute_partner_name',
        help='Name of partner',
        string='Partner Name',
        tracking=True,
    )
    reg_no = fields.Char(
        copy=False,
        help='The format is [current year]/[sequence]',
        readonly=True,
        string='Registration number',
        tracking=True,
    )
    sorting_out_date = fields.Date(
        help='The date this matter should be archived or moved out',
        index=True,
        tracking=True,
    )

    def _get_rk_matter_states(self):
        return [('draft', 'Draft'), ('pending', 'Pending'), ('done', 'Done'), ('cancel', 'Cancelled')]

    state = fields.Selection(
        selection=_get_rk_matter_states,
        copy=False,
        default='draft',
        group_expand='_expand_states',
        string='Status',
        tracking=True,
    )

    def _compute_document_count(self):
        for matter in self:
            matter.document_count = self.env['rk.document'].search_count([
                ('matter_id', '=', matter.id),
            ])

    @api.depends('message_ids')
    def _compute_latest_change(self):
        self = self.sudo()
        for record in self:
            if record.message_ids:
                description = record.message_ids[-1].description
                tracking_values = record.message_ids[-1].tracking_value_ids
                if description:
                    record.latest_change = description
                elif tracking_values:
                    record.latest_change = (
                        f"{tracking_values[-1].field_desc} -> "
                        f"{tracking_values[-1].get_new_display_value()[-1]}")
            else:
                record.latest_change = ''

    @api.depends('matter_name', 'reg_no')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.reg_no or ''} {record.matter_name or ''}"

    @api.depends('is_secret', 'partner_id')
    def _compute_partner_name(self):
        for record in self:
            if record.is_secret:
                record.partner_name = _('Confidential')
            else:
                record.partner_name = record.partner_id.name or ''

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def _get_default_param(self, field):
        param = f"record_keeping.{self._name.replace('.', '_')}_default_{field}"
        return self.env['ir.config_parameter'].sudo().get_param(param)

    def action_archive_after_sorting_date(self):
        if self.state in ['done']:
            if self.sorting_out_date < fields.Date.today():
                self.write(dict(active=False))

    def action_archive_documents(self):
        for document in self.document_ids:
            document.write(dict(active=False))

    def action_done(self):
        self.write(dict(state='done'))

    @api.model
    def create(self, vals):
        if 'description' not in vals:
            vals['description'] = vals.get('name')
        vals['reg_no'] = self.env['ir.sequence'].next_by_code('rk.matter')
        if 'is_official' not in vals.keys():
            vals['is_official'] = True
        _logger.info(f"{vals=}")
        return super(Matter, self).create(vals)

    def document_tree_view(self):
        # shows the tree view of the documents linked to rk.matter
        action_xmlid = 'record_keeping.action_document_view'
        action = self.env['ir.actions.act_window']._for_xml_id(action_xmlid)
        action['domain'] = str([('matter_id', 'in', self.ids)])
        action['context'] = "{'matter_id': '%d'}" % self.id
        return action

    def write(self, vals):
        if vals.get('state') == 'done':
            vals['close_date'] = fields.Date.today()
            if days := int(self._get_default_param('sorting_out_days')) or 0:
                vals['sorting_out_date'] = fields.Date.today() + timedelta(days=days)
        if not vals.get('active', True):
            if self.state not in ['done']:
                vals.pop('active')
            else:
                self.action_archive_documents()
        return super().write(vals)
